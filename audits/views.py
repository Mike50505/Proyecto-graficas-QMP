import csv, io, json, secrets
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .models import Importation, Audit
from .schema import HEADERS, DIMENSIONS
from .importer import preview, confirm, InvalidExcel
from .metrics import filtered, metrics, week_options
from .chart_catalog import CHARTS
from .kpi_guides import KPI_GUIDES

def active(request):
    if request.GET.get('importacion'):
        try: import_id=int(request.GET['importacion'])
        except (ValueError,TypeError): raise Http404
        imp=get_object_or_404(Importation,pk=import_id)
    else:
        imp=Importation.objects.filter(pk=request.session.get('active_import')).first() or Importation.objects.first()
    if imp:
        previous=request.session.get('active_import'); request.session['active_import']=imp.pk
        if previous and previous!=imp.pk:
            return imp,True
    return imp,False

@login_required
def dashboard(request, presentation=False):
    imp,changed=active(request)
    if changed: return redirect(reverse('presentation' if presentation else 'dashboard')+'?importacion='+str(imp.pk))
    context={'imports':Importation.objects.all(),'imp':imp,'charts':CHARTS,'kpi_guides':KPI_GUIDES}
    if imp:
        context['weeks']=week_options(imp)
        context['selected_week']=next((week['label'] for week in context['weeks'] if week['value']==request.GET.get('semana')), '')
        qs=filtered(imp,request.GET); context['metrics']=metrics(qs,request.GET.get('periodo')=='semanal')
        context['cards']=[('Total de auditorías',context['metrics']['summary']['total']),('Auditorías con incumplimientos',context['metrics']['summary']['with_failures']),('Total de incumplimientos',context['metrics']['summary']['failures']),('Cumplimiento de evaluaciones aplicables',str(context['metrics']['summary']['compliance'])+' %' if context['metrics']['summary']['compliance'] is not None else 'Sin datos aplicables'),('Auditorías con defectos visuales',context['metrics']['summary']['with_defects']),('Evaluaciones sin dato',context['metrics']['summary']['missing'])]
        context['filters']=[{'key':k,'label':v,'selected':request.GET.get(k,''),'options':imp.audits.order_by(k).values_list(k,flat=True).distinct()} for k,v in DIMENSIONS.items()]
        order=request.GET.get('orden','-date'); allowed=['date','-date','source_id','-source_id','linea','-linea','failures','-failures','operador','-operador']
        context['page']=Paginator(qs.order_by(order if order in allowed else '-date','pk'),25).get_page(request.GET.get('pagina'))
        params=request.GET.copy(); params.pop('pagina',None); context['query']=params.urlencode()
    return render(request,'presentation.html' if presentation else 'dashboard.html',context)

@login_required
def data(request):
    imp,changed=active(request)
    return JsonResponse(metrics(filtered(imp,{} if changed else request.GET),request.GET.get('periodo')=='semanal') if imp else {})

@login_required
@require_http_methods(['GET','POST'])
def upload(request):
    context={}
    # Pending bytes are private, token stored only in this user's session; expire after one day.
    private=Path(settings.PRIVATE_DIR or settings.BASE_DIR/'private'); private.mkdir(exist_ok=True)
    import time
    for old in private.glob('*.xlsx'):
        if old.stat().st_mtime<time.time()-86400: old.unlink(missing_ok=True)
    token=request.session.get('pending_token'); pending=private/(token+'.xlsx') if token and token.isalnum() else None
    if request.method=='POST':
        try:
            if request.FILES.get('archivo'):
                file=request.FILES['archivo']
                if file.size>settings.MAX_EXCEL_BYTES: raise InvalidExcel('El archivo excede el límite de tamaño.')
                content=file.read(settings.MAX_EXCEL_BYTES+1); filename=Path(file.name).name
            elif pending and pending.exists(): content=pending.read_bytes(); filename=request.session['pending_name']
            else: raise InvalidExcel('Seleccione un archivo Excel para generar la vista previa.')
            result=preview(content,filename,request.POST.get('hoja') or None)
            context['result']=result
            duplicate=Importation.objects.filter(sha256=result['hash']).first(); context['duplicate']=duplicate
            if request.POST.get('confirmar') and not duplicate:
                if request.POST.get('hash')!=result['hash']: raise InvalidExcel('La vista previa cambió. Revise el archivo nuevamente.')
                imp,_=confirm(result,request.user)
                request.session['active_import']=imp.pk
                if pending: pending.unlink(missing_ok=True)
                request.session.pop('pending_token',None)
                messages.success(request,'Importación confirmada correctamente.')
                return redirect('dashboard')
            if request.FILES.get('archivo'):
                if pending: pending.unlink(missing_ok=True)
                token=secrets.token_hex(24); (private/(token+'.xlsx')).write_bytes(content)
                request.session['pending_token']=token; request.session['pending_name']=filename
        except (InvalidExcel,ValueError) as exc: context['error']=str(exc)
    return render(request,'upload.html',context)

@login_required
def detail(request,pk):
    imp,_=active(request)
    audit=get_object_or_404(Audit,pk=pk,importation=imp)
    return render(request,'detail.html',{'audit':audit,'fields':[(h,audit.values.get(h) or 'Sin dato',audit.original.get(h,{})) for h in HEADERS]})

def csv_safe(value):
    value=str(value)
    if value.lstrip().startswith(('=','+','-','@')) or value.startswith(('\t','\r','\n')): return "'"+value
    # Excel text wrapper is not used: no executable formulas in exported content.
    if value.isdigit() and value.startswith('0'): return "'"+value
    return value


@login_required
@require_http_methods(['GET', 'POST'])
def delete_importation(request, pk):
    imp = get_object_or_404(Importation, pk=pk)
    if request.method == 'POST':
        if request.POST.get('confirmar') != 'eliminar':
            return HttpResponse('Confirma la eliminación de la importación.', status=400)
        with transaction.atomic():
            imp = get_object_or_404(Importation.objects.select_for_update(), pk=pk)
            filename = imp.filename
            count = imp.audits.count()
            imp.delete()
        if request.session.get('active_import') == pk:
            request.session.pop('active_import', None)
        messages.success(request, f'Se eliminó la importación «{filename}» y sus {count} auditorías.')
        return redirect('dashboard')
    return render(request, 'delete_importation.html', {'imp': imp, 'audit_count': imp.audits.count()})

@login_required
def export(request):
    imp,changed=active(request)
    if not imp: raise Http404
    response=HttpResponse(content_type='text/csv; charset=utf-8'); response['Content-Disposition']='attachment; filename="auditorias_filtradas.csv"'
    response.write('\ufeff'); writer=csv.writer(response); writer.writerow(HEADERS)
    for a in filtered(imp,{} if changed else request.GET).iterator(): writer.writerow([csv_safe(a.values.get(h,'')) for h in HEADERS])
    return response
