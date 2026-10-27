(() => {
const grid=document.getElementById('presentation-grid');if(!grid)return;
const stage=document.getElementById('presentation-stage'),cards=[...grid.querySelectorAll('[data-chart]')];
cards.forEach(c=>grid.append(c));grid.querySelector('.charts')?.remove();
const m=JSON.parse(document.getElementById('dashboard-data').textContent),key='fcd-presentation-v2';
let saved={};try{saved=JSON.parse(localStorage.getItem(key)||localStorage.getItem('fcd-presentation-v1')||'{}')||{};}catch(_){}
const selected=new Set(Array.isArray(saved.selected)?saved.selected:cards.map(c=>c.dataset.chart));
if(Array.isArray(saved.known))cards.forEach(c=>{if(!saved.known.includes(c.dataset.chart))selected.add(c.dataset.chart);});
const perPage=document.getElementById('charts-per-page');if(saved.version===2&&[1,2,4].includes(Number(saved.perPage)))perPage.value=String(saved.perPage);
let page=0,exporting=false,presenting=false,hideTimer,transition;
const options=document.getElementById('chart-options'),dock=document.getElementById('presenter-dock'),number=new Intl.NumberFormat('es-MX',{maximumFractionDigits:2});
const fmt=v=>v===null?'—':number.format(v);
const titles={controls:['CUMPLIMIENTO','Dónde se concentran los incumplimientos.',m.summary.failures,'incumplimientos','Celdas NO CUMPLE por requisito · Porcentaje acumulado del total.'],defects:['INSPECCIÓN VISUAL','Cada detección cuenta.',m.summary.detections,'detecciones visuales','Celdas DETECTADO por tipo de defecto · Porcentaje acumulado.'],lines:['POR LÍNEA','Una visión de cada línea.',m.summary.compliance===null?null:fmt(m.summary.compliance)+' %','cumplimiento aplicable','CUMPLE y NO CUMPLE sobre evaluaciones aplicables. N/A incluido como cumplido; vacíos excluidos.'],shifts:['POR TURNO','El cumplimiento, turno a turno.',m.summary.with_failures,'auditorías con incumplimientos','Auditorías con incumplimientos sobre el total de auditorías de cada turno.'],timeline:['EVOLUCIÓN','La calidad a través del tiempo.',m.summary.failure_pct===null?null:fmt(m.summary.failure_pct)+' %','auditorías con incumplimientos','Porcentaje y volumen de auditorías. Los períodos sin registros se muestran como huecos.'],processes:['POR PROCESO','Cada proceso, en contexto.',m.summary.total,'auditorías','Cantidad de auditorías registradas por proceso.'],machines:['POR MÁQUINA','Los hallazgos, en perspectiva.',m.machines.filter(r=>r.bad>0).length,'máquinas con incumplimientos','Ranking por auditorías con incumplimientos. Las diferencias no demuestran causas.'],heat:['REQUISITO × LÍNEA','El detalle revela el panorama.',m.requirements.length,'requisitos de control','Porcentaje de NO CUMPLE sobre evaluaciones aplicables. Denominadores visibles.']};
Object.assign(titles,{
 operators:['POR NÓMINA','El cumplimiento por operador.',m.operators.filter(r=>r.operador).length,'nóminas auditadas','Evaluaciones asociadas a Nómina Operador. No corresponde a la nómina del inspector.'],
 requirement_profile:['POR REQUISITO','El cumplimiento, sin perder detalle.',m.requirements.length,'requisitos','CUMPLE, NO CUMPLE, N/A y Sin dato se muestran por separado.'],
 failure_distribution:['DISTRIBUCIÓN','Una auditoría. Varios posibles hallazgos.',m.summary.total,'auditorías','Número de NO CUMPLE en los once controles por cada auditoría.'],
 status_findings:['ESTATUS Y HALLAZGOS','El estatus y lo que muestran los datos.',m.summary.inconsistent,'CONFORME con hallazgos','Los hallazgos calculados no modifican el estatus original del Excel.'],
 line_shifts:['COBERTURA','Cada línea. Cada turno.',m.summary.total,'auditorías','Cobertura de auditoría por combinación de línea y turno.'],
 compliance_timeline:['CUMPLIMIENTO','El cumplimiento a través del tiempo.',m.summary.compliance===null?null:fmt(m.summary.compliance)+' %','cumplimiento aplicable','(CUMPLE + N/A) / (CUMPLE + N/A + NO CUMPLE), sumados antes de dividir.'],
 process_heat:['REQUISITO × PROCESO','Cada proceso, requisito a requisito.',m.requirements.length,'controles','NO CUMPLE sobre evaluaciones aplicables por proceso y requisito.'],
 visual_processes:['DEFECTOS POR PROCESO','Los defectos, en su contexto.',m.summary.detections,'detecciones visuales','Una auditoría puede aportar varios tipos de defecto.']
});
cards.forEach((card,i)=>{const label=document.createElement('label'),input=document.createElement('input'),index=document.createElement('span'),text=document.createElement('span'),check=document.createElement('span');input.type='checkbox';input.value=card.dataset.chart;input.checked=selected.has(input.value);index.className='option-index';index.textContent=String(i+1).padStart(2,'0');text.className='option-label';text.textContent=card.querySelector('h2').textContent;check.className='option-check';check.textContent='✓';input.addEventListener('change',()=>{input.checked?selected.add(input.value):selected.delete(input.value);page=0;update();});label.append(input,index,text,check);options.append(label);});
function resize(){requestAnimationFrame(()=>{if(typeof Chart!=='undefined')grid.querySelectorAll('canvas').forEach(c=>{const chart=Chart.getChart(c);if(chart&&!c.closest('[hidden]'))chart.resize();});});}
function update(animate=false){
 const visible=cards.filter(c=>selected.has(c.dataset.chart)),size=Number(perPage.value),pages=Math.ceil(visible.length/size);page=Math.max(0,Math.min(page,pages-1));const shown=visible.slice(page*size,(page+1)*size),current=new Set(shown);
 cards.forEach(card=>{card.hidden=!current.has(card);});grid.dataset.size=String(size);grid.hidden=!visible.length;document.getElementById('empty-selection').hidden=!!visible.length;
 document.getElementById('selection-count').textContent=String(visible.length);document.getElementById('slide-status').textContent=pages?`${page+1} de ${pages}`:'Sin selección';document.getElementById('presenter-status').textContent=pages?`${page+1} / ${pages}`:'0 / 0';document.getElementById('slide-number').textContent=`${String(pages?page+1:0).padStart(2,'0')} / ${String(pages).padStart(2,'0')}`;
 for(const id of ['previous-slide','presenter-previous'])document.getElementById(id).disabled=!pages||page===0;
 for(const id of ['next-slide','presenter-next'])document.getElementById(id).disabled=!pages||page>=pages-1;
 document.getElementById('fullscreen').disabled=!pages;
 for(const id of ['export-pdf','export-pptx'])document.getElementById(id).disabled=!pages||exporting;
 const meta=size===1&&shown.length?titles[shown[0].dataset.chart]:['PANORAMA DE CALIDAD','Una visión compartida.',m.summary.total,'auditorías filtradas','Indicadores de la misma importación y los mismos filtros.'];
 document.getElementById('slide-category').textContent=meta[0];document.getElementById('slide-title').textContent=meta[1];document.getElementById('slide-subtitle').textContent=meta[4];document.getElementById('slide-value').textContent=typeof meta[2]==='string'?meta[2]:fmt(meta[2]);document.getElementById('slide-value-label').textContent=meta[2]===null?'Sin datos aplicables':meta[3];stage.dataset.layout=String(size);
 const dots=document.getElementById('slide-dots');dots.replaceChildren();for(let i=0;i<pages;i++){const dot=document.createElement('button');dot.type='button';dot.setAttribute('aria-label',`Ir a diapositiva ${i+1}: ${visible[i*size].querySelector('h2').textContent}`);dot.setAttribute('aria-current',i===page?'step':'false');dot.addEventListener('click',()=>{page=i;update(true);});dots.append(dot);}
 try{localStorage.setItem(key,JSON.stringify({version:2,selected:[...selected],known:cards.map(c=>c.dataset.chart),perPage:size}));}catch(_){}
 if(transition)transition.cancel();if(animate&&!matchMedia('(prefers-reduced-motion: reduce)').matches)transition=grid.animate([{opacity:.15,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],{duration:240,easing:'cubic-bezier(.23,1,.32,1)'});
 resize();
}
function move(delta,animate=true){if(exporting)return;page+=delta;update(animate);showDock();}
perPage.addEventListener('change',()=>{page=0;update();});
for(const id of ['previous-slide','presenter-previous'])document.getElementById(id).addEventListener('click',()=>move(-1));
for(const id of ['next-slide','presenter-next'])document.getElementById(id).addEventListener('click',()=>move(1));
for(const [id,all] of [['select-all',true],['select-none',false]])document.getElementById(id).addEventListener('click',()=>{selected.clear();options.querySelectorAll('input').forEach(input=>{input.checked=all;if(all)selected.add(input.value);});page=0;update();});
function showDock(){if(!presenting)return;document.body.classList.remove('controls-idle');clearTimeout(hideTimer);hideTimer=setTimeout(()=>{if(!document.querySelector('#chart-help[open]')&&!dock.matches(':hover')&&!dock.contains(document.activeElement))document.body.classList.add('controls-idle');},2600);}
function stop(){presenting=false;clearTimeout(hideTimer);document.body.classList.remove('is-presenting','controls-idle');dock.hidden=true;resize();document.getElementById('fullscreen').focus();}
async function exit(){if(document.fullscreenElement){try{await document.exitFullscreen();}catch(_){}}stop();}
document.getElementById('fullscreen').addEventListener('click',async()=>{presenting=true;document.body.classList.add('is-presenting');dock.hidden=false;document.activeElement?.blur();resize();showDock();try{if(!document.fullscreenElement&&document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();}catch(_){document.getElementById('presentation-message').textContent='Presentación ampliada. El navegador no permitió ocultar su barra; puedes usar F11.';}});
document.getElementById('exit-presentation').addEventListener('click',exit);
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement&&presenting)stop();else resize();});
document.addEventListener('keydown',e=>{if(exporting)return;if(document.querySelector('#chart-help[open]'))return;if(e.target.closest('.chart-help-button')&&e.code==='Space')return;if(e.key==='Escape'&&presenting){exit();return;}if(e.target.closest('input,select,textarea')||e.altKey||e.ctrlKey||e.metaKey)return;if(e.key==='ArrowRight'||e.key==='PageDown'||(presenting&&e.code==='Space')){e.preventDefault();move(1,false);}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();move(-1,false);}else if(e.key==='Home'){e.preventDefault();page=0;update();}else if(e.key==='End'){e.preventDefault();page=cards.length;update();}});
for(const format of ['pdf','pptx'])document.getElementById('export-'+format).addEventListener('click',async()=>{
 if(exporting||!selected.size)return;
 const originalPage=page, scroll={x:scrollX,y:scrollY};
 const pages=Math.ceil(cards.filter(c=>selected.has(c.dataset.chart)).length/Number(perPage.value));
 const controls=[...document.querySelectorAll('.studio-sidebar input,.studio-sidebar select,.studio-sidebar button,.preview-navigation button')];
 const states=controls.map(control=>control.disabled);
 exporting=true;controls.forEach(control=>control.disabled=true);document.body.classList.add('presentation-exporting');
 stage.setAttribute('aria-busy','true');
 try{
  await window.FCDExportPresentation({format,stage,pages,render:async index=>{page=index;update();controls.forEach(control=>control.disabled=true);await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));grid.querySelectorAll('canvas').forEach(canvas=>{const chart=window.Chart?.getChart(canvas);if(chart&&!canvas.closest('[hidden]')){chart.resize();chart.update('none');}});}});
 }catch(error){console.error('Presentation export failed',error);document.getElementById('presentation-message').textContent='No se pudo exportar. Intenta de nuevo o reduce las gráficas por diapositiva.';}
 finally{exporting=false;stage.classList.remove('export-capture');stage.removeAttribute('aria-busy');document.body.classList.remove('presentation-exporting');controls.forEach((control,index)=>control.disabled=states[index]);page=originalPage;update();window.scrollTo(scroll.x,scroll.y);}
});
document.addEventListener('pointermove',showDock);document.addEventListener('focusin',showDock);window.addEventListener('resize',resize);update();
})();
