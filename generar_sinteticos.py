"""Archivos A y B artificiales; no contienen datos del Excel real."""
from pathlib import Path
from datetime import datetime
from openpyxl import Workbook
from audits.schema import HEADERS, CONTROLS, DEFECTS
output=Path(__file__).resolve().parent/'datos_sinteticos';output.mkdir(exist_ok=True)
for name,count in [('A',2),('B',3)]:
    wb=Workbook();ws=wb.active;ws.title='Ejemplo sintético';ws.append(HEADERS)
    for i in range(count):
        r={h:'' for h in HEADERS};r.update({h:'CUMPLE' for h in CONTROLS});r.update({h:'LIMPIO' for h in DEFECTS})
        r.update({'ID':str(i+1).zfill(3),'Fecha Registro':datetime(2026,10,5+i*2),'Estatus':'CONFORME','Turno':'DÍA','Líneas Auditadas':'LÍNEA SINTÉTICA','Máquinas':'MÁQUINA DEMO','Proceso':'PROCESO DEMO','No. Parte':'000012','Nomina Inspector':'000007'})
        if name=='A':r[CONTROLS[0]]='NO CUMPLE'
        if name=='B' and i==0:r[DEFECTS[0]]='DETECTADO'
        ws.append([r[h] for h in HEADERS])
    wb.save(output/f'SINTETICO_{name}.xlsx')
print('Creados datos_sinteticos/SINTETICO_A.xlsx y SINTETICO_B.xlsx')
