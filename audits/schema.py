import unicodedata, re
HEADERS = ['ID','Fecha Registro','Turno','Proceso','No. Parte','Líneas Auditadas','Estatus','Folio RDM','Nómina Operador','Cat. Operador','Shop Order','Lote Tubería','Máquinas','Series Equipos','Validación Mtto','1ra Pieza','SPC','Formato 30x30','Auditorías Cruzadas','Material Identificado','Equipo Identificado','Equipo Calibrado','IT Proceso','Tipo Aceite','Hora Liberación','Marcas','Golpes','Contaminación','Ovalamiento','Rebaba','Pandeado','Exceso Aceite','Mediciones Dimensionales / Checklist Visual','Nomina Inspector','Adecuado Para La Medición','Corresponde Al Operador Auditado']
CONTROLS = HEADERS[14:23] + HEADERS[34:36]
DEFECTS = HEADERS[25:32]
DIMENSIONS = {'turno':'Turno','proceso':'Proceso','linea':'Líneas Auditadas','maquina':'Máquinas','inspector':'Nomina Inspector','parte':'No. Parte'}
IDENTIFIERS = [HEADERS[i] for i in [0,4,7,8,10,11,13,33]]
def norm(value):
    return ' '.join(str('' if value is None else value).split()).upper()
def header(value):
    return ''.join(c for c in unicodedata.normalize('NFKD',norm(value)) if not unicodedata.combining(c))
