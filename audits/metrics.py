from datetime import timedelta
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncDay, TruncWeek
from .schema import CONTROLS, DEFECTS, DIMENSIONS

def pct(n,d): return round(n/d*100,2) if d else None

def filtered(imp,params):
    qs=imp.audits.all()
    for key in DIMENSIONS:
        if params.get(key): qs=qs.filter(**{key:params[key]})
    from .importer import parse_date
    for key,lookup in [('desde','date__gte'),('hasta','date__lte')]:
        if params.get(key):
            try: qs=qs.filter(**{lookup:parse_date(params[key])})
            except ValueError: qs=qs.none()
    finding=params.get('hallazgos')
    if finding=='controles': qs=qs.filter(failures__gt=0)
    elif finding=='visuales': qs=qs.filter(detections__gt=0)
    elif finding=='cualquiera': qs=qs.filter(Q(failures__gt=0)|Q(detections__gt=0))
    elif finding=='inconsistentes': qs=qs.filter(inconsistent=True)
    elif finding=='sin': qs=qs.filter(failures=0,detections=0)
    if params.get('q'):
        query=Q()
        for key in ['source_id',*DIMENSIONS]: query |= Q(**{key+'__icontains':params['q']})
        qs=qs.filter(query)
    return qs

def aggregate(qs):
    a=qs.aggregate(total=Count('pk'),with_failures=Count('pk',filter=Q(failures__gt=0)),with_defects=Count('pk',filter=Q(detections__gt=0)),union=Count('pk',filter=Q(failures__gt=0)|Q(detections__gt=0)),failures=Sum('failures'),detections=Sum('detections'),passes=Sum('passes'),missing=Sum('missing'),na=Sum('na'),inconsistent=Count('pk',filter=Q(inconsistent=True)))
    for k in a: a[k]=a[k] or 0
    a['applicable']=a['passes']+a['failures']; a['compliance']=pct(a['passes'],a['applicable']); a['failure_pct']=pct(a['with_failures'],a['total']); a['defect_pct']=pct(a['with_defects'],a['total'])
    return a

def pareto(qs,fields,state):
    counts=qs.aggregate(**{'v'+str(i):Count('pk',filter=Q(**{'values__'+h:state})) for i,h in enumerate(fields)})
    rows=sorted([{'label':h,'count':counts['v'+str(i)]} for i,h in enumerate(fields)],key=lambda x:(-x['count'],x['label']))
    total=sum(r['count'] for r in rows); acc=0
    for r in rows: acc+=r['count']; r['cumulative']=pct(acc,total)
    return rows

def grouped(qs,field):
    rows=list(qs.values(field).annotate(total=Count('pk'),bad=Count('pk',filter=Q(failures__gt=0)),passes=Sum('passes'),failures=Sum('failures'),na=Sum('na'),missing=Sum('missing'),with_defects=Count('pk',filter=Q(detections__gt=0))).order_by(field))
    for r in rows:
        r['label']=r[field] or 'Sin dato'; r['applicable']=r['passes']+r['failures']; r['pct']=pct(r['bad'],r['total']); r['compliance']=pct(r['passes'],r['applicable'])
    return rows

def evaluation_profile(qs):
    counts=qs.aggregate(**{prefix+str(i):Count('pk',filter=Q(**{'values__'+h:state})) for i,h in enumerate(CONTROLS) for prefix,state in [('p','CUMPLE'),('f','NO CUMPLE'),('n','N/A'),('m','')]})
    result=[]
    for i,h in enumerate(CONTROLS):
        passes=counts['p'+str(i)]; failures=counts['f'+str(i)]
        result.append({'label':h,'passes':passes,'failures':failures,'na':counts['n'+str(i)],'missing':counts['m'+str(i)],'applicable':passes+failures,'compliance':pct(passes,passes+failures)})
    return result

def heatmap(qs,dimension):
    result=[]
    for group in qs.values(dimension).annotate(total=Count('pk')).order_by(dimension):
        rows=evaluation_profile(qs.filter(**{dimension:group[dimension]}))
        result.append({'label':group[dimension] or 'Sin dato','cells':[{'label':r['label'],'bad':r['failures'],'den':r['applicable'],'pct':pct(r['failures'],r['applicable']),'color':round(95-35*r['failures']/r['applicable']) if r['applicable'] else 95} for r in rows]})
    return result

def status_findings(qs):
    rows=qs.values('values__Estatus').annotate(total=Count('pk'),both=Count('pk',filter=Q(failures__gt=0,detections__gt=0)),controls_only=Count('pk',filter=Q(failures__gt=0,detections=0)),visual_only=Count('pk',filter=Q(failures=0,detections__gt=0)),neither=Count('pk',filter=Q(failures=0,detections=0)),missing=Count('pk',filter=Q(missing__gt=0))).order_by('values__Estatus')
    return [{'label':r.pop('values__Estatus') or 'Sin dato',**r} for r in rows]

def line_shifts(qs):
    shifts=list(qs.order_by('turno').values_list('turno',flat=True).distinct())
    counts=list(qs.values('linea','turno').annotate(total=Count('pk')).order_by('linea','turno'))
    lines=sorted({r['linea'] for r in counts}); lookup={(r['linea'],r['turno']):r['total'] for r in counts}
    return {'shifts':[s or 'Sin dato' for s in shifts],'rows':[{'label':line or 'Sin dato','counts':[lookup.get((line,s),0) for s in shifts],'total':sum(lookup.get((line,s),0) for s in shifts)} for line in lines]}

def visual_processes(qs):
    counts=qs.values('proceso').annotate(total=Count('pk'),with_defects=Count('pk',filter=Q(detections__gt=0)),**{'d'+str(i):Count('pk',filter=Q(**{'values__'+h:'DETECTADO'})) for i,h in enumerate(DEFECTS)}).order_by('proceso')
    return [{'label':r['proceso'] or 'Sin dato','total':r['total'],'with_defects':r['with_defects'],'pct':pct(r['with_defects'],r['total']),'counts':[r['d'+str(i)] for i in range(len(DEFECTS))],'detections':sum(r['d'+str(i)] for i in range(len(DEFECTS)))} for r in counts]

def operator_compliance(qs):
    rows=grouped(qs,'operador')
    for row in rows:
        row['label']='Nómina '+row['operador'] if row['operador'] else 'Sin nómina de operador'
    return rows

def metrics(qs,weekly=False):
    a=aggregate(qs)
    fn=TruncWeek if weekly else TruncDay
    evolution=list(qs.annotate(period=fn('date')).values('period').annotate(total=Count('pk'),bad=Count('pk',filter=Q(failures__gt=0)),passes=Sum('passes'),failures=Sum('failures')).order_by('period'))
    periods={r['period'].date() if hasattr(r['period'],'date') else r['period']:r for r in evolution}; timeline=[]
    if periods:
        current=min(periods); end=max(periods)
        while current<=end:
            r=periods.get(current,{'total':0,'bad':0,'passes':0,'failures':0}); den=r['passes']+r['failures']
            timeline.append({'label':current.isoformat(),'total':r['total'],'bad':r['bad'],'pct':pct(r['bad'],r['total']),'passes':r['passes'],'failures':r['failures'],'applicable':den,'compliance':pct(r['passes'],den)})
            current+=timedelta(days=7 if weekly else 1)
    distribution=[{'number':r['failures'],'label':str(r['failures'])+' incumplimientos','count':r['count'],'pct':pct(r['count'],a['total']),'with_missing':r['with_missing']} for r in qs.values('failures').annotate(count=Count('pk'),with_missing=Count('pk',filter=Q(missing__gt=0))).order_by('failures')]
    return {'summary':a,'controls':pareto(qs,CONTROLS,'NO CUMPLE'),'defects':pareto(qs,DEFECTS,'DETECTADO'),'lines':grouped(qs,'linea'),'shifts':grouped(qs,'turno'),'processes':grouped(qs,'proceso'),'machines':sorted(grouped(qs,'maquina'),key=lambda r:-r['bad']),'timeline':timeline,'heat':heatmap(qs,'linea'),'requirements':CONTROLS,'requirement_profile':evaluation_profile(qs),'failure_distribution':distribution,'status_findings':status_findings(qs),'line_shifts':line_shifts(qs),'process_heat':heatmap(qs,'proceso'),'visual_processes':visual_processes(qs),'defect_types':DEFECTS,'operators':operator_compliance(qs)}
