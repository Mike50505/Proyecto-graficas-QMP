(() => {
const el=document.getElementById('dashboard-data');if(!el)return;
const m=JSON.parse(el.textContent);
if(typeof Chart==='undefined'){window.renderLocalCharts(m);return;}
const presenting=document.body.classList.contains('presentation-mode');
Chart.defaults.color=presenting?'#a5a5b1':'#6e6e73';Chart.defaults.borderColor=presenting?'#ffffff0d':'#eeeeF2';Chart.defaults.font.family='-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif';Chart.defaults.animation=false;
Chart.defaults.plugins.legend.labels.usePointStyle=true;Chart.defaults.plugins.legend.labels.boxWidth=7;
const blue='#439bfa',red='#ee9a79',green='#44baa3';
function draw(id,labels,datasets,opts={}){const canvas=document.getElementById(id);if(!canvas)return;new Chart(canvas,{type:'bar',data:{labels,datasets},options:{maintainAspectRatio:false,responsive:true,plugins:{legend:{position:'bottom'}},...opts}});}
function pareto(id,rows){draw(id,rows.map(r=>r.label),[{label:'Cantidad',data:rows.map(r=>r.count),backgroundColor:blue,yAxisID:'y'},{type:'line',label:'Acumulado %',data:rows.map(r=>r.cumulative),borderColor:red,backgroundColor:red,yAxisID:'percent'}],{scales:{y:{beginAtZero:true,title:{display:true,text:'Cantidad'},ticks:{precision:0}},percent:{position:'right',min:0,max:100,grid:{drawOnChartArea:false},ticks:{callback:v=>v+' %'}}}});}
pareto('controls',m.controls);pareto('defects',m.defects);
function horizontal(id,rows,datasets,opts={}){document.getElementById(id).parentElement.style.height=Math.max(330,rows.length*32)+'px';draw(id,rows.map(r=>r.label),datasets,{indexAxis:'y',...opts});}
horizontal('lines',m.lines,[{label:'CUMPLE %',data:m.lines.map(r=>r.compliance),backgroundColor:green},{label:'NO CUMPLE %',data:m.lines.map(r=>r.applicable?100-r.compliance:null),backgroundColor:red}],{scales:{x:{stacked:true,min:0,max:100},y:{stacked:true}},plugins:{legend:{position:'bottom'},tooltip:{callbacks:{afterBody:ctx=>{const r=m.lines[ctx[0].dataIndex];return [`${r.total} auditorías`,`${r.applicable} evaluaciones aplicables`,`${r.na} N/A`];}}}}});
function failures(id,rows){horizontal(id,rows,[{label:id==='shifts'?'Auditorías con incumplimientos %':'Auditorías con incumplimientos',data:rows.map(r=>id==='shifts'?r.pct:r.bad),backgroundColor:blue}],{scales:{x:{beginAtZero:true,...(id==='shifts'?{max:100}:{ticks:{precision:0}})}},plugins:{legend:{position:'bottom'},tooltip:{callbacks:{afterBody:ctx=>{const r=rows[ctx[0].dataIndex];return `${r.bad} / ${r.total} auditorías · ${r.pct} %`;}}}}});}
failures('shifts',m.shifts);failures('machines',m.machines);
horizontal('processes',m.processes,[{label:'Auditorías',data:m.processes.map(r=>r.total),backgroundColor:blue}],{scales:{x:{beginAtZero:true,ticks:{precision:0}}}});
draw('timeline',m.timeline.map(r=>r.label),[{label:'Auditorías',data:m.timeline.map(r=>r.total),backgroundColor:'#bfd7f2',yAxisID:'y'},{type:'line',label:'Con incumplimientos %',data:m.timeline.map(r=>r.pct),borderColor:red,spanGaps:false,yAxisID:'percent'}],{scales:{y:{beginAtZero:true,ticks:{precision:0}},percent:{position:'right',min:0,max:100,grid:{drawOnChartArea:false}}}});
})();