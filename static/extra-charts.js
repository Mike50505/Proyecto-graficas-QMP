/* Additional charts share the exact metrics payload of the dashboard. */
(() => {
const source=document.getElementById('dashboard-data');if(!source)return;const m=JSON.parse(source.textContent);
const colors=['#44baa3','#ee9a79','#a5a6b4','#d8b968','#439bfa','#bd99df','#e489b3'];
const fmt=n=>n===null?'Sin datos aplicables':new Intl.NumberFormat('es-MX',{maximumFractionDigits:2}).format(n);
function stacked(id,labels,series,details){
 const canvas=document.getElementById(id);if(!canvas)return;const box=canvas.parentElement;
 if(typeof Chart!=='undefined'){
  box.style.height=Math.max(330,labels.length*38)+'px';new Chart(canvas,{type:'bar',data:{labels,datasets:series.map(s=>({label:s.label,data:s.data,backgroundColor:s.color,borderRadius:3}))},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,scales:{x:{stacked:true,beginAtZero:true,ticks:{precision:0},title:{display:true,text:'Cantidad'}},y:{stacked:true}},plugins:{legend:{position:'bottom'},tooltip:{callbacks:{afterBody:ctx=>details[ctx[0].dataIndex]}}}}});return;
 }
 canvas.remove();box.classList.add('additional-bars');const legend=document.createElement('div');legend.className='chart-legend';
 series.forEach(s=>{const item=document.createElement('span'),dot=document.createElement('i');dot.style.background=s.color;item.append(dot,document.createTextNode(s.label));legend.append(item);});box.append(legend);
 if(!labels.length){const p=document.createElement('p');p.className='chart-empty';p.textContent='Sin auditorías para los filtros seleccionados.';box.append(p);return;}
 const totals=labels.map((_,i)=>series.reduce((n,s)=>n+s.data[i],0)),max=Math.max(1,...totals),rows=document.createElement('div');rows.className='stack-rows';box.append(rows);
 labels.forEach((label,i)=>{const row=document.createElement('div');row.className='local-chart-row';const name=document.createElement('span');name.textContent=label;const track=document.createElement('div');track.className='local-track';track.style.background='transparent';const group=document.createElement('div');group.className='stack-group';group.style.width=totals[i]/max*100+'%';const counts=[];
 series.forEach(s=>{const n=s.data[i];counts.push(s.label+': '+n);const segment=document.createElement('span');segment.className='stack-segment';segment.style.width=(totals[i]?n/totals[i]*100:0)+'%';segment.style.background=s.color;segment.title=s.label+': '+n;group.append(segment);});track.append(group);track.setAttribute('role','img');track.setAttribute('aria-label',counts.join('; '));const info=document.createElement('span');info.textContent=details[i];row.title=counts.join(' · ')+' · '+details[i];row.append(name,track,info);rows.append(row);});
}
const profiles=m.requirement_profile;
stacked('requirement_profile',profiles.map(r=>r.label),[['CUMPLE','passes'],['NO CUMPLE','failures'],['N/A','na'],['Sin dato','missing']].map(([label,key],i)=>({label,data:profiles.map(r=>r[key]),color:colors[i]})),profiles.map(r=>`${fmt(r.compliance)}${r.compliance===null?'':' %'} · ${r.passes}/${r.applicable} aplicables · N/A ${r.na} · Sin dato ${r.missing}`));
const distribution=m.failure_distribution;
stacked('failure_distribution',distribution.map(r=>r.label),[{label:'Auditorías',data:distribution.map(r=>r.count),color:colors[4]}],distribution.map(r=>`${r.count} auditorías · ${fmt(r.pct)} % · ${r.with_missing} con datos faltantes`));
const statuses=m.status_findings;
stacked('status_findings',statuses.map(r=>r.label),[['Solo incumplimientos','controls_only'],['Solo visuales','visual_only'],['Ambos','both'],['Sin hallazgos registrados','neither']].map(([label,key],i)=>({label,data:statuses.map(r=>r[key]),color:[colors[1],colors[4],colors[5],colors[2]][i]})),statuses.map(r=>`${r.total} auditorías · ${r.missing} con datos faltantes`));
const shifts=m.line_shifts;
stacked('line_shifts',shifts.rows.map(r=>r.label),shifts.shifts.map((label,i)=>({label,data:shifts.rows.map(r=>r.counts[i]),color:colors[i%colors.length]})),shifts.rows.map(r=>`${r.total} auditorías · `+shifts.shifts.map((s,i)=>`${s}: ${r.counts[i]}`).join(' · ')));
stacked('visual_processes',m.visual_processes.map(r=>r.label),m.defect_types.map((label,i)=>({label,data:m.visual_processes.map(r=>r.counts[i]),color:colors[i%colors.length]})),m.visual_processes.map(r=>`${r.detections} detecciones · ${r.with_defects}/${r.total} auditorías con defectos (${fmt(r.pct)} %)`));
const canvas=document.getElementById('compliance_timeline');if(!canvas)return;
if(typeof Chart!=='undefined'){
 new Chart(canvas,{type:'line',data:{labels:m.timeline.map(r=>r.label),datasets:[{label:'Cumplimiento aplicable %',data:m.timeline.map(r=>r.compliance),borderColor:colors[0],pointBackgroundColor:colors[0],spanGaps:false}]},options:{responsive:true,maintainAspectRatio:false,scales:{y:{min:0,max:100,ticks:{callback:v=>v+' %'}}},plugins:{legend:{position:'bottom'},tooltip:{callbacks:{afterBody:ctx=>{const r=m.timeline[ctx[0].dataIndex];return `${r.passes}/${r.applicable} evaluaciones aplicables · ${r.total} auditorías`;}}}}}});return;
}
const ns='http://www.w3.org/2000/svg',box=canvas.parentElement;canvas.remove();box.classList.add('compliance-trend');const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 860 300');svg.setAttribute('role','img');svg.setAttribute('aria-label','Cumplimiento de evaluaciones aplicables por período; huecos sin aplicables');svg.classList.add('timeline-svg');const dark=document.body.classList.contains('presentation-mode'),text=dark?'#a5a5b1':'#6e6e73';
function node(tag,attrs,value){const e=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(value!==undefined)e.textContent=value;svg.append(e);return e;}
const left=50,right=810,top=25,bottom=245,step=(right-left)/Math.max(1,m.timeline.length-1);
[0,25,50,75,100].forEach(t=>{const y=bottom-t/100*(bottom-top);node('line',{x1:left,x2:right,y1:y,y2:y,stroke:dark?'#ffffff10':'#e9e9ed'});node('text',{x:37,y:y+4,fill:text,'font-size':10,'text-anchor':'end'},t+' %');});let previous=null;
m.timeline.forEach((r,i)=>{const x=left+i*step;if(i===0||i===m.timeline.length-1||i%Math.max(1,Math.ceil(m.timeline.length/6))===0)node('text',{x,y:bottom+24,fill:text,'font-size':10,'text-anchor':'middle'},r.label.slice(8,10)+'/'+r.label.slice(5,7));if(r.compliance===null){previous=null;return;}const y=bottom-r.compliance/100*(bottom-top);if(previous)node('line',{x1:previous.x,y1:previous.y,x2:x,y2:y,stroke:colors[0],'stroke-width':3,'stroke-linecap':'round'});const point=node('circle',{cx:x,cy:y,r:4,fill:colors[0]});const title=document.createElementNS(ns,'title');title.textContent=`${r.label}: ${fmt(r.compliance)} % · ${r.passes}/${r.applicable} aplicables · ${r.total} auditorías`;point.append(title);previous={x,y};});box.append(svg);
const details=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Consultar fechas y denominadores';details.append(summary);for(const r of m.timeline){const p=document.createElement('p');p.textContent=`${r.label}: ${fmt(r.compliance)}${r.compliance===null?'':' %'} · ${r.passes}/${r.applicable} aplicables · ${r.total} auditorías`;details.append(p);}box.append(details);
})();
