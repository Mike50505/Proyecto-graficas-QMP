"""Catálogo compartido de títulos y explicaciones para ambas vistas."""
CHARTS = [{'id': 'controls',
  'title': 'Pareto de incumplimientos',
  'subtitle': 'Celdas NO CUMPLE por requisito y porcentaje acumulado',
  'meaning': 'Cuenta cada NO CUMPLE en los once controles y ordena los requisitos de mayor a menor. Una '
             'auditoría puede aportar varios incumplimientos.',
  'calculation': 'Acumulado = suma de los incumplimientos hasta ese requisito / total de incumplimientos × '
                 '100.',
  'interpretation': 'Las barras señalan los requisitos que concentran más hallazgos. El acumulado se refiere '
                    'a incumplimientos, no a auditorías ni piezas.'},
 {'id': 'defects',
  'title': 'Pareto de detecciones visuales',
  'subtitle': 'Detecciones por defecto y porcentaje acumulado',
  'meaning': 'Cuenta las celdas DETECTADO de los siete defectos visuales. Una auditoría puede tener varios '
             'tipos de defecto.',
  'calculation': 'Acumulado = detecciones acumuladas / total de detecciones × 100.',
  'interpretation': 'Sirve para reconocer qué defectos concentran más detecciones. No representa piezas '
                    'defectuosas ni una tasa de rechazo.'},
 {'id': 'lines',
  'title': 'Cumplimiento por línea',
  'subtitle': 'CUMPLE y NO CUMPLE entre evaluaciones aplicables',
  'meaning': 'Compara las evaluaciones de los once controles agrupadas por línea. Se suman primero todas las '
             'evaluaciones aplicables.',
  'calculation': 'Cumplimiento = CUMPLE / (CUMPLE + NO CUMPLE) × 100. N/A y vacíos se excluyen.',
  'interpretation': 'Una línea con más auditorías tiene mayor peso según sus evaluaciones. Consulta los '
                    'denominadores y los N/A; sin aplicables se muestra Sin datos aplicables.'},
 {'id': 'shifts',
  'title': 'Auditorías con incumplimientos por turno',
  'subtitle': 'Porcentaje y total de auditorías de cada turno',
  'meaning': 'Cuenta auditorías que contienen al menos un NO CUMPLE en los once controles, agrupadas por '
             'turno.',
  'calculation': 'Porcentaje = auditorías con incumplimientos del turno / total de auditorías del turno × '
                 '100.',
  'interpretation': 'Una auditoría se cuenta una sola vez, aunque tenga varios incumplimientos. Las '
                    'diferencias entre turnos no demuestran una causa.'},
 {'id': 'timeline',
  'title': 'Evolución de incumplimientos',
  'subtitle': 'Porcentaje de auditorías con incumplimientos y volumen',
  'meaning': 'Muestra cómo cambia la proporción de auditorías con al menos un NO CUMPLE por día o semana, '
             'según el filtro de evolución.',
  'calculation': 'Porcentaje del período = auditorías con incumplimientos / auditorías del período × 100. '
                 'Las semanas van de lunes a domingo.',
  'interpretation': 'Lee el porcentaje junto con el volumen: pocas auditorías pueden producir cambios '
                    'grandes. Los períodos sin registros son huecos, no 0 %.'},
 {'id': 'processes',
  'title': 'Auditorías por proceso',
  'subtitle': 'Cantidad de auditorías registradas',
  'meaning': 'Agrupa y cuenta los registros de auditoría por proceso. Cada fila del Excel representa una '
             'auditoría.',
  'calculation': 'Cantidad = número de auditorías del proceso dentro de los filtros activos.',
  'interpretation': 'Describe cobertura de auditoría. Más registros no significan más producción, más piezas '
                    'ni peor calidad.'},
 {'id': 'machines',
  'title': 'Máquinas con más auditorías con incumplimientos',
  'subtitle': 'Cantidad, porcentaje y total por máquina',
  'meaning': 'Ordena las máquinas por auditorías que contienen al menos un NO CUMPLE en los once controles.',
  'calculation': 'Porcentaje = auditorías con incumplimientos de la máquina / auditorías de esa máquina × '
                 '100.',
  'interpretation': 'Revisa cantidad y porcentaje juntos: las máquinas más auditadas tienen más '
                    'oportunidades de registrar hallazgos. No demuestra que la máquina sea la causa.'},
 {'id': 'heat',
  'title': 'Mapa de calor · Línea × requisito',
  'subtitle': 'Porcentaje de NO CUMPLE y denominador aplicable',
  'meaning': 'Cruza cada línea con cada uno de los once requisitos. Una celda resume sus evaluaciones '
             'aplicables.',
  'calculation': 'Celda = NO CUMPLE / (CUMPLE + NO CUMPLE) × 100. Debajo se muestra NO CUMPLE / aplicables.',
  'interpretation': 'Un color más intenso indica mayor porcentaje. N/A y vacíos no entran al denominador. '
                    'Sin aplicables no equivale a 0 %.'},
 {'id': 'requirement_profile',
  'title': 'Cumplimiento por requisito',
  'subtitle': 'CUMPLE, NO CUMPLE, N/A y Sin dato',
  'meaning': 'Muestra los cuatro estados por cada uno de los once controles. Las barras apiladas cuentan '
             'evaluaciones; la leyenda separa los estados.',
  'calculation': 'Para cada requisito: CUMPLE + NO CUMPLE + N/A + Sin dato = total de auditorías filtradas. '
                 'Cumplimiento = CUMPLE / (CUMPLE + NO CUMPLE) × 100.',
  'interpretation': 'Permite distinguir incumplimiento de falta de evaluación. N/A y Sin dato no se '
                    'interpretan como cumplimiento. El número de auditorías es el mismo para cada '
                    'requisito.'},
 {'id': 'failure_distribution',
  'title': 'Incumplimientos por auditoría',
  'subtitle': 'Auditorías con 0, 1, 2 o más incumplimientos',
  'meaning': 'Agrupa las auditorías según cuántos NO CUMPLE contienen en los once controles. Cada auditoría '
             'pertenece a una sola barra.',
  'calculation': 'Cantidad por grupo = auditorías con ese número de incumplimientos. Porcentaje = cantidad '
                 'del grupo / total de auditorías × 100.',
  'interpretation': 'Distingue hallazgos aislados de múltiples incumplimientos en una misma auditoría. Tener '
                    'cero NO CUMPLE no descarta defectos visuales, N/A o datos faltantes.'},
 {'id': 'status_findings',
  'title': 'Estatus del Excel frente a hallazgos',
  'subtitle': 'Estatus original y cuatro grupos de hallazgos',
  'meaning': 'Conserva el Estatus del Excel y divide sus auditorías en: solo incumplimientos, solo defectos '
             'visuales, ambos y sin hallazgos registrados.',
  'calculation': 'Cada auditoría se asigna exactamente a uno de los cuatro grupos. La suma de los grupos '
                 'equivale al total de auditorías de ese estatus.',
  'interpretation': 'Explica por qué un registro CONFORME puede tener hallazgos calculados. No cambia el '
                    'estatus. Sin hallazgos registrados no significa evaluación completa si faltan datos.'},
 {'id': 'line_shifts',
  'title': 'Auditorías por línea y turno',
  'subtitle': 'Cobertura de auditoría por línea, separada por turno',
  'meaning': 'Cada barra representa una línea y sus segmentos representan los turnos presentes en el archivo '
             'seleccionado.',
  'calculation': 'Cada segmento cuenta auditorías de una combinación línea-turno. La suma de segmentos es el '
                 'total de esa línea.',
  'interpretation': 'Muestra dónde y cuándo se ha auditado más o menos. Es cobertura de auditoría, no '
                    'cantidad de piezas ni tasa de incumplimiento.'},
 {'id': 'compliance_timeline',
  'title': 'Evolución del cumplimiento aplicable',
  'subtitle': 'Cumplimiento ponderado por día o semana',
  'meaning': 'Muestra la evolución del cumplimiento de los once controles entre las evaluaciones aplicables '
             'de cada período.',
  'calculation': 'CUMPLE del período / (CUMPLE + NO CUMPLE del período) × 100. No se promedian los '
                 'porcentajes de auditorías o líneas.',
  'interpretation': 'Es diferente del porcentaje de auditorías con hallazgos: una auditoría puede cumplir '
                    'unos controles e incumplir otros. Los períodos sin aplicables son huecos, no '
                    'cumplimiento total.'},
 {'id': 'process_heat',
  'title': 'Mapa de calor · Proceso × requisito',
  'subtitle': 'Requisitos con incumplimientos por proceso',
  'meaning': 'Cruza los procesos presentes en los datos con los once controles, mostrando el porcentaje de '
             'NO CUMPLE y su denominador.',
  'calculation': 'Celda = NO CUMPLE del proceso y requisito / evaluaciones aplicables de esa combinación × '
                 '100.',
  'interpretation': 'Ayuda a ubicar concentraciones de hallazgos. Revisa el denominador: una sola evaluación '
                    'puede dar 100 %. No demuestra causas y excluye N/A y vacíos.'},
 {'id': 'visual_processes',
  'title': 'Defectos visuales por proceso',
  'subtitle': 'Detecciones por proceso, separadas por tipo de defecto',
  'meaning': 'Cuenta cada DETECTADO en los siete campos visuales y lo agrupa por proceso. Los colores '
             'separan los tipos de defecto.',
  'calculation': 'Cada segmento cuenta detecciones de un tipo en un proceso. Una auditoría puede aportar '
                 'varias detecciones.',
  'interpretation': 'El total apilado son detecciones, no auditorías únicas. Consulta también auditorías con '
                    'defectos / auditorías del proceso para considerar la cobertura. N/A y vacíos no se '
                    'convierten en defectos ni en LIMPIO.'}]

CHARTS.append({
 'id':'operators','title':'Cumplimiento por nómina de operador',
 'subtitle':'Evaluaciones aplicables asociadas al empleado auditado',
 'meaning':'Agrupa las auditorías por Nómina Operador, el identificador del empleado auditado. Nomina Inspector corresponde a quien realizó la auditoría y no se usa para identificar al operador.',
 'calculation':'Para cada nómina: CUMPLE / (CUMPLE + NO CUMPLE) × 100 en los once controles. Se suman las evaluaciones antes de dividir. N/A y vacíos se excluyen y se muestran aparte. También se indican las auditorías con incumplimientos y con defectos visuales.',
 'interpretation':'Compara los porcentajes junto con la cantidad de auditorías y el denominador aplicable. Resume condiciones de las auditorías asociadas al operador, incluidos mantenimiento y equipo; no demuestra que el empleado sea la causa de los hallazgos ni mide su productividad. Sin evaluaciones aplicables no equivale a 100 %. Los registros sin nómina se agrupan aparte.'
})
