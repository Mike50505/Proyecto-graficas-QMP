# Dashboard de Auditorías FCD

Aplicación local en español con Django Templates, ORM, SQLite, importación Excel validada, historial independiente, filtros, CSV seguro y permisos. Los archivos de auditoría no se envían a servicios externos.

## Iniciar en Windows PowerShell

```powershell
Set-Location 'C:\Users\miguel.arroyo\Desktop\Proyectos\proyecto graficas QMP'
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edite .env y cambie SECRET_KEY por una clave aleatoria.
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py createsuperuser
.\.venv\Scripts\python manage.py runserver 127.0.0.1:8000
```

Abra http://127.0.0.1:8000 e inicie sesión con el usuario creado. Pulse **Importar Excel**, seleccione el archivo, revise hoja, fechas, filas, errores y advertencias y confirme. El archivo nuevo queda activo. El selector superior recupera cualquier importación anterior; al cambiar de archivo se reinician los filtros. El archivo original permanece intacto. La base normal entregada está migrada y vacía, sin usuarios ni contraseñas precargados.

Se eligió Django 5.2 LTS, con soporte extendido hasta abril de 2028, según https://www.djangoproject.com/download/. Instale la última revisión de seguridad de esa rama mediante requirements.txt.

## Bibliotecas visuales y funcionamiento sin conexión

La red de este entorno impidió descargar Chart.js y Bootstrap 5. Se incluye CSS Bootstrap 3.4.1 (MIT) disponible localmente y una vista alternativa con barras HTML y evolución SVG. Las gráficas ya funcionan sin red. El código de integración de Chart.js está implementado en static/dashboard.js, pero **su biblioteca y su ejecución visual no pudieron verificarse aquí**.

Con conexión, ejecute una sola vez antes de iniciar:

```powershell
.\preparar_assets.ps1
```

Este script descarga únicamente las bibliotecas públicas Chart.js 4.4.8 y Bootstrap 5.3.3 a static/vendor. No lee ni transmite archivos Excel. Al recargar se utiliza automáticamente Chart.js; después no se requiere red. Si la política de PowerShell impide ejecutar scripts, abra preparar_assets.ps1 y ejecute manualmente sus comandos Invoke-WebRequest. No hay CDN ni fuentes externas en las páginas.

## Usuarios y permisos

El superusuario tiene acceso completo. Cree usuarios desde /admin/. Para consulta asigne **audits | auditoría | Can view auditoría** (`audits.view_audit`). Para importar asigne además **audits | importación | Can add importación** (`audits.add_importation`). Las vistas, JSON, detalle y CSV están protegidos. Los permisos se aplican a todas las importaciones; no se implementa aislamiento por propietario porque el tablero es compartido de planta. No habilite permisos administrativos de edición de auditorías para usuarios de consulta.

## Pruebas

```powershell
.\.venv\Scripts\python manage.py check
.\.venv\Scripts\python manage.py test --verbosity 2
.\.venv\Scripts\python generar_sinteticos.py
```

`datos_sinteticos/` contiene exclusivamente ejemplos artificiales. A tiene 2 auditorías con 2 incumplimientos; B tiene 3 auditorías sin incumplimientos y una detección visual. Comparten IDs y pueden importarse A → B → A usando el historial. Las pruebas generan sus propios Excel en memoria y una base temporal. No escriben sobre el archivo original ni la base de desarrollo.

Se ejecutaron 36 pruebas: encabezados normalizados y reordenados, faltantes y duplicados, fechas, ceros iniciales, N/A/vacíos/desconocidos, archivo vacío o repetido, IDs duplicados, transacción y rollback, permisos, vista previa y confirmación, límites de archivo/filas/descompresión, filtros combinados, fórmulas, CSV, denominadores cero, ponderación, unión de hallazgos, semanas y huecos diarios, aislamiento completo A → B → A y referencia real.

## Resultado del Excel de referencia

`Reporte_Auditorias_FCD_2026_10 (2).xlsx`, hoja `Auditorías FCD`:

| Comprobación | Resultado real |
| --- | ---: |
| Auditorías | 149 |
| Período | 05/10/2026–26/10/2026 |
| Auditorías con incumplimientos | 95 |
| Celdas NO CUMPLE en los once controles | 126 |
| Auditorías con defectos visuales | 38 |
| Estatus original CONFORME | 149 |
| NO CUMPLE en Validación Mtto | 85 |
| NO CUMPLE en Material Identificado | 31 |
| Detecciones visuales | 69 |
| Unión de auditorías con hallazgos | 103 |
| Cumplimiento aplicable | 90.49 % (1199 / 1325) |
| Evaluaciones N/A en once controles | 314 |

No hubo errores ni advertencias en el archivo de referencia. Todas las cifras esperadas coinciden. Los valores de verificación aparecen en pruebas/documentación, nunca como constantes del dashboard.

## Reglas y supuestos

- La primera fila de cada hoja contiene los encabezados. Se detectan por los 36 nombres, normalizando mayúsculas, acentos y espacios. Los puntos y signos de los nombres se conservan. No hay comparación aproximada. Si varias hojas coinciden, se selecciona una antes de confirmar. Se admiten columnas extra, pero no forman parte de los 36 campos de auditoría.
- Cada fila es una auditoría. Solo se ignoran filas completamente vacías. Los encabezados duplicados normalizados bloquean esa hoja; una hoja inválida no impide usar otra válida.
- Los estados de control admitidos son CUMPLE, NO CUMPLE y N/A. Los visuales admiten LIMPIO, DETECTADO y N/A. Vacíos generan advertencia y se preservan; desconocidos bloquean la confirmación y no se convierten. Los estatus de auditoría admitidos son CONFORME y NO CONFORME. Cambie explícitamente esta lista si la planta usa otros estados válidos.
- Se suman las evaluaciones aplicables antes de dividir. Los once controles están separados de los siete defectos y del texto dimensional. N/A y vacíos se excluyen del denominador. Sin denominador se muestra Sin datos aplicables. Sin hallazgos registrados no implica completamente conforme cuando faltan evaluaciones.
- La zona de planta asumida es America/Mexico_City, configurable. Las fechas Excel sin zona se interpretan como hora local y se guarda su fecha de calendario sin convertirla a UTC. La hora y el valor original permanecen en el detalle. Se aceptan fechas nativas y texto AAAA-MM-DD, DD/MM/AAAA, con hora opcional HH:MM:SS; también AAAA-MM-DDTHH:MM:SS. No se adivinan fechas ambiguas, números seriales sin formato fecha ni formatos estadounidenses.
- Las semanas empiezan el lunes. Los períodos intermedios sin registros tienen cantidad cero y porcentaje nulo, y la evolución muestra huecos. El intervalo visual va de la primera a la última auditoría filtrada.
- Categorías se normalizan en espacios/mayúsculas sin fusionar nombres por similitud. Cada celda de línea/máquina se trata como categoría literal; no se divide una cadena que pueda contener múltiples nombres porque no se conoce un separador fiable.
- Los identificadores mantienen texto y ceros. Se recuperan ceros de formatos numéricos simples como 000000; un código que Excel ya truncó, redondeó o guardó como número sin formato no permite recuperar ceros ni precisión perdida. Se conservan los valores, tipo, formato Excel y fila para trazabilidad.
- No se ejecutan fórmulas. Se acepta su valor en caché únicamente si está presente y supera las mismas validaciones. Una fórmula sin caché bloquea la importación. El CSV neutraliza texto que pudiera iniciar fórmulas y antepone apóstrofo a identificadores con ceros iniciales; algunos lectores muestran ese apóstrofo. CSV no tiene tipos de datos: para reabrir identificadores en Excel use Importar texto/CSV con columnas de tipo Texto.
- SHA-256 identifica un archivo idéntico: se ofrece consultar el existente, sin duplicarlo. La unicidad de ID es por importación. No se usa caché de indicadores.
- La vista previa guarda temporalmente el Excel en private/ con un nombre aleatorio ligado a la sesión. Se elimina al confirmar o tras 24 horas cuando se abre la pantalla de importación. Los originales completos no se conservan tras confirmar: los 36 campos y su trazabilidad se guardan en la base. No sirva private/ públicamente. Los archivos pendientes no deben compartirse ni subirse a Git.
- Las cargas y cálculos son síncronos con límites configurables. Con archivos cercanos a 50 000 filas y miles de categorías, ajuste límites o añada procesamiento en segundo plano y tablas de agregación. Un fallo de validación bloquea todo el archivo; un error de base de datos revierte la transacción.

## Configuración y PostgreSQL

Copie .env.example a .env. Se carga sin sobrescribir variables del entorno. Configure zona, hosts y límites allí. Para PostgreSQL instale requirements.txt y configure DB_ENGINE=postgresql, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST y DB_PORT; ejecute migrate contra esa base. SQLite usa db.sqlite3; SQLITE_PATH permite otra ruta para revisión/pruebas. PostgreSQL no estuvo disponible para comprobarse aquí.

El modo de desarrollo usa DEBUG=1 y una clave local de respaldo si falta SECRET_KEY; configure una clave secreta real en .env. La aplicación se entrega para uso local, sin publicación. Mantiene CSRF, escape de plantillas y JSON seguro. El servidor de desarrollo sirve static/ únicamente con DEBUG=1.

## Dónde modificar

| Necesidad | Archivo |
| --- | --- |
| Columnas, controles, defectos, dimensiones, normalización | audits/schema.py |
| Fechas, estados permitidos, lectura, validación, identificadores | audits/importer.py |
| Persistencia, restricciones | audits/models.py y migraciones |
| Indicadores, agrupaciones, Pareto, filtros | audits/metrics.py |
| Permisos, importación activa, CSV, paginación | audits/views.py |
| Interfaz, formularios, detalle de 36 campos | templates/ |
| Gráficas Chart.js | static/dashboard.js |
| Gráficas locales sin biblioteca | static/fallback-charts.js |
| Estilos y adaptación móvil | static/app.css |
| Zona, base de datos, límites | config/settings.py y .env |

## Evidencia y límites de la revisión

Las migraciones y `manage.py check` se ejecutaron correctamente. Las 36 pruebas pasaron con Django 5.2.17 y openpyxl 3.1.5 copiados de dependencias ya disponibles, debido al bloqueo de red. `requirements.txt` solicita Django >=5.2.18 para incorporar la revisión de seguridad vigente al instalar con conexión.

Se renderizaron mediante el cliente Django dashboard, filtros, importación, vista previa y detalle, todos con HTTP 200. Se revisaron en Chrome headless las páginas renderizadas y las gráficas HTML/SVG, en 1440 px y 390 px, sin errores JavaScript ni desbordamiento horizontal. Las capturas están en docs/. No fue posible abrir un puerto local: runserver fue rechazado por las restricciones del entorno. Por ello no se comprobó la navegación mediante servidor vivo, ni Chart.js, ni PostgreSQL. No se desplegó ni se transmitió el Excel a ningún servicio.

## Diseño y presentaciones

La interfaz usa un diseño inspirado en la claridad de macOS: tipografía del sistema, fondos neutros, tarjetas redondeadas, controles discretos y una jerarquía visual amplia. Los filtros combinables se despliegan desde **Filtrar auditorías**. Los cálculos, importaciones y permisos conservan su comportamiento.

Desde **Modo presentación** se abre un estudio para preparar las diapositivas. La selección lateral permite elegir entre las quince gráficas y definir una, dos o cuatro por diapositiva. El modo **Una · Enfoque** es el predeterminado del nuevo diseño. Las preferencias y la selección se recuerdan en ese navegador. Los títulos y cifras destacadas de cada diapositiva se obtienen de los indicadores filtrados.

**Iniciar presentación** muestra exclusivamente el escenario oscuro a pantalla completa. La vista del editor desaparece. Use las flechas, Page Up/Page Down, la barra espaciadora para avanzar, o Home/End para ir al principio/final. **Esc** y **Finalizar** regresan al estudio. No hay avance automático. Los controles se ocultan tras unos segundos sin actividad y reaparecen con el puntero o el teclado; permanecen disponibles al tener el foco. Las transiciones respetan la preferencia de movimiento reducido y la navegación por teclado es inmediata. Si el navegador rechaza la API de pantalla completa, el escenario ocupa la ventana y se puede usar F11.

La ruta /presentacion/ mantiene la importación, los filtros y los permisos del dashboard. **Dashboard** vuelve a la misma consulta. Las gráficas compartidas están en templates/charts.html, el estudio en templates/presentation.html y su comportamiento en static/presentation.js. Los estilos visuales nuevos están en static/apple.css, cargado después de static/app.css.

Comprobación posterior del rediseño: 36 pruebas Django aprobadas; comprobación del sistema sin incidencias y sin migraciones pendientes. Chrome contra servidor local en 8765: selector de quince gráficas, selección vacía, persistencia, distribución de una/dos/cuatro, quince diapositivas, pantalla completa real, Esc, teclado, controles ocultables, filtros originales, escritorio, móvil de 390 px y proyector de 1366 × 768. Se verificó que los once requisitos completos caben en la diapositiva de Pareto del proyector. Sin errores JavaScript ni desbordamiento horizontal de la página. La revisión visual corresponde a las gráficas HTML/SVG locales; Chart.js continúa pendiente de descarga según el apartado de bibliotecas.

Capturas: docs/apple-dashboard.png, docs/apple-estudio.png, docs/apple-diapositiva.png, docs/apple-proyector-1366.png y versiones móviles. El servidor local quedó actualizado en http://127.0.0.1:8765/.

## Nuevas gráficas y explicación con «?»

El dashboard y el modo presentación comparten 15 gráficas. Se agregaron:

1. Cumplimiento por requisito, separando CUMPLE, NO CUMPLE, N/A y Sin dato.
2. Distribución de auditorías según su número de incumplimientos.
3. Estatus original frente a cuatro grupos excluyentes: solo incumplimientos, solo visuales, ambos y sin hallazgos registrados.
4. Cobertura de auditoría por línea y turno.
5. Evolución diaria/semanal del cumplimiento de evaluaciones aplicables, ponderado por su denominador.
6. Mapa de calor de proceso por requisito, con numerador y denominador visibles.
7. Detecciones visuales por proceso y tipo de defecto, distinguiendo detecciones de auditorías únicas.

Cada gráfica incluye un botón **?** en su esquina superior derecha. Abre una explicación de qué muestra, cómo se calcula y cómo interpretarla. La ayuda funciona en la vista normal, en la preparación de diapositivas y durante la presentación a pantalla completa. **Esc** cierra primero la explicación y mantiene la presentación. El botón de cierre y el clic fuera del cuadro también cierran la ayuda; el foco vuelve al botón original. Con una ayuda abierta, las flechas no cambian de diapositiva.

Los datos se calculan exclusivamente sobre los resultados filtrados de la importación activa. N/A y vacíos se mantienen separados; cero incumplimientos no se etiqueta como conformidad completa. Los estatus no se corrigen automáticamente. En la evolución del cumplimiento, los períodos sin evaluaciones aplicables tienen porcentaje nulo.

- Catálogo de títulos y explicaciones: `audits/chart_catalog.py`.
- Cálculos y agregaciones: `audits/metrics.py`.
- Paneles compartidos y mapas de calor: `templates/charts.html` y `templates/heatmap.html`.
- Gráficas adicionales: `static/extra-charts.js`, con integración Chart.js y alternativa local.
- Apertura y cierre accesible de las explicaciones: `static/chart-help.js`.
- Estilos de ayuda, leyendas y nuevas gráficas: `static/apple.css`.

Verificación de esta ampliación: **36 pruebas Django aprobadas**, incluyendo estados por requisito, distribución sin duplicados, estatus frente a hallazgos, cobertura línea-turno, detecciones por proceso, evolución ponderada, N/A/vacíos, filtros y aislamiento A → B → A de todo el conjunto de indicadores. Chrome contra el servidor local verificó las 15 ayudas en las dos vistas y en pantalla completa, restauración de foco, Esc sin abandonar la presentación, selección de las 15 gráficas y ancho móvil de 390 px. Sin errores JavaScript ni desbordamiento horizontal. Las gráficas revisadas visualmente usaron la alternativa local HTML/SVG; la biblioteca Chart.js sigue pendiente de descarga.

Capturas nuevas en `docs/`: `grafica-cumplimiento-requisito.png`, `grafica-estatus-hallazgos.png`, `grafica-proceso-requisito.png`, `explicacion-dashboard.png`, `explicacion-presentacion.png` y `explicacion-movil.png`.

## Contenido del repositorio

El repositorio incluye c?digo, migraciones, configuraci?n de ejemplo, documentaci?n y Excel sint?ticos. El Excel real, la base local con usuarios, las sesiones, las credenciales y las capturas con datos de planta se excluyen mediante .gitignore. Las capturas mencionadas en la documentaci?n pertenecen a la revisi?n local y no se publican. La prueba del Excel de referencia se omite autom?ticamente si ese archivo no est? disponible.
