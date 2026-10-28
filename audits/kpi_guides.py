"""Explicaciones de los indicadores del dashboard."""

KPI_GUIDES = [
    {
        'id': 'kpi-1', 'title': 'Total de auditorías',
        'meaning': 'Cantidad de auditorías de la importación activa que coinciden con la semana y los demás filtros seleccionados.',
        'calculation': 'Se cuenta una auditoría por cada registro del Excel dentro de los filtros. Por ejemplo, 49 significa que se están consultando 49 auditorías.',
        'interpretation': 'Es la base para los porcentajes de auditorías con incumplimientos y con defectos visuales. No representa piezas producidas ni la cantidad de controles evaluados.',
    },
    {
        'id': 'kpi-2', 'title': 'Auditorías con incumplimientos',
        'meaning': 'Auditorías que tienen al menos un NO CUMPLE en cualquiera de los once controles.',
        'calculation': 'Porcentaje = auditorías con al menos un NO CUMPLE / total de auditorías filtradas × 100. Por ejemplo: 40 / 49 × 100 = 81.63 %. Cada auditoría se cuenta una sola vez.',
        'interpretation': 'Una misma auditoría puede tener varios incumplimientos. Por eso este indicador puede ser menor que el total de incumplimientos. N/A cuenta como cumplido; los defectos visuales se cuentan por separado.',
    },
    {
        'id': 'kpi-3', 'title': 'Total de incumplimientos',
        'meaning': 'Suma de todas las respuestas NO CUMPLE en los once controles de las auditorías filtradas.',
        'calculation': 'Se suman los NO CUMPLE de cada auditoría. Si una auditoría tiene tres controles NO CUMPLE, aporta tres al total, aunque solo sea una auditoría con incumplimientos.',
        'interpretation': 'Por ejemplo, 40 auditorías pueden acumular 56 incumplimientos. No incluye N/A, vacíos ni detecciones visuales. No es un porcentaje.',
    },
    {
        'id': 'kpi-4', 'title': 'Cumplimiento de evaluaciones aplicables',
        'meaning': 'Porcentaje de evaluaciones cumplidas en los once controles. Los N/A se consideran cumplidos y los campos vacíos se excluyen.',
        'calculation': 'Cumplimiento = (CUMPLE + N/A) / (CUMPLE + N/A + NO CUMPLE) × 100. Por ejemplo: 483 / 539 × 100 = 89.61 %. Primero se suman las evaluaciones y después se divide.',
        'interpretation': 'Mide controles, no auditorías completas. Puede existir un porcentaje alto de cumplimiento aunque muchas auditorías tengan al menos un incumplimiento. Si no hay evaluaciones aplicables se muestra Sin datos aplicables.',
    },
    {
        'id': 'kpi-5', 'title': 'Auditorías con defectos visuales',
        'meaning': 'Auditorías que tienen al menos una respuesta DETECTADO en los siete campos de inspección visual.',
        'calculation': 'Porcentaje = auditorías con al menos un defecto visual / total de auditorías filtradas × 100. Por ejemplo: 15 / 49 × 100 = 30.61 %. Una auditoría se cuenta una sola vez aunque tenga varios tipos de defecto.',
        'interpretation': 'Una auditoría puede tener tanto defectos visuales como incumplimientos de controles. Estos grupos pueden coincidir y sus porcentajes no deben sumarse como si fueran excluyentes.',
    },
    {
        'id': 'kpi-6', 'title': 'Evaluaciones sin dato',
        'meaning': 'Cantidad de campos vacíos en los once controles de las auditorías filtradas.',
        'calculation': 'Se suman los controles sin respuesta. Los N/A no son vacíos: se muestran aparte y cuentan como cumplidos. Por eso puede haber 0 evaluaciones sin dato y 104 N/A.',
        'interpretation': 'Un vacío no se interpreta como cumplimiento ni entra en el denominador del porcentaje de cumplimiento. Este indicador cuenta celdas de controles, no auditorías completas ni campos de inspección visual.',
    },
]
