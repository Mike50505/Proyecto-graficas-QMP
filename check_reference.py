import os,json
os.environ['DJANGO_SETTINGS_MODULE']='config.settings'
import django; django.setup()
from audits.importer import preview
from pathlib import Path
r=preview(Path('Reporte_Auditorias_FCD_2026_10 (2).xlsx').read_bytes(),'referencia.xlsx')
print('errores',r['errors'][:10],'advertencias',len(r['warnings']),'filas',len(r['rows']),r['start'],r['end'])
print('incumplimientos',sum(x['failures'] for x in r['rows']),'auditorias',sum(x['failures']>0 for x in r['rows']),'visuales',sum(x['detections']>0 for x in r['rows']))
print('controles', {h:sum(x['values'][h]=='NO CUMPLE' for x in r['rows']) for h in ['Validación Mtto','Material Identificado']})
Path('docs/referencia.json').write_text(json.dumps({k:v for k,v in r.items() if k!='rows'},ensure_ascii=False,indent=2),encoding='utf-8')
