/* Gráficas HTML/SVG locales accesibles cuando Chart.js aún no está instalado. */
window.renderLocalCharts=function(m){
 const ns='http://www.w3.org/2000/svg';
 
 function chart(id,rows,mode){
  const canvas=document.getElementById(id),box=canvas.parentElement;canvas.remove();box.style.height='330px';box.classList.add('local-bars');
  const total=rows.reduce((a,r)=>a+(r.count||0),0);
  if(!rows.length){box.textContent='Sin datos para graficar';return;}
  const max=Math.max(1,...rows.map(r=>mode==='pareto'?r.count:mode==='process'?r.total:mode==='machine'?r.bad:100));
  for(const r of rows){
   const group=document.createElement('div');group.className='local-chart-row';
   const title=document.createElement('span');title.textContent=r.label;group.append(title);
   const track=document.createElement('div');track.className='local-track';
   let value=mode==='pareto'?r.count:mode==='process'?r.total:mode==='machine'?r.bad:mode==='line'?r.compliance:r.pct;
   const parts=[{value,label:mode==='line'?'CUMPLE':'Cantidad',color:mode==='line'?'#44baa3':'#439bfa'}];
   if(mode==='line'&&value!==null)parts.push({value:100-value,label:'NO CUMPLE',color:'#ee9a79'});
   window.FCDBarTrack(track,parts,max,r.label);
   group.append(track);
   const info=document.createElement('span');
   info.textContent=mode==='pareto'?`${r.count} · Acum. ${r.cumulative===null?'Sin datos aplicables':r.cumulative+' %'}`:mode==='line'?`${value===null?'Sin datos aplicables':value+' % CUMPLE'} · ${r.total} auditorías · ${r.applicable} aplicables · ${r.na} N/A`:mode==='process'?`${r.total} auditorías`:`${r.bad} / ${r.total} auditorías · ${r.pct} %`;
   group.title=info.textContent;group.append(info);box.append(group);
  }
 }
 chart('controls',m.controls,'pareto');chart('defects',m.defects,'pareto');chart('lines',m.lines,'line');chart('shifts',m.shifts,'shift');chart('processes',m.processes,'process');chart('machines',m.machines,'machine');
 const box=document.getElementById('timeline').parentElement;box.replaceChildren();
 const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 860 300');svg.setAttribute('role','img');svg.setAttribute('aria-label','Evolución del porcentaje de auditorías con incumplimientos y volumen de auditorías');svg.classList.add('timeline-svg');svg.style.width='100%';
 const dark=document.body.classList.contains('presentation-mode'),textColor=dark?'#898b9a':'#86868b',gridColor=dark?'#ffffff10':'#e9e9ed',volumeColor=dark?'#2e4562':'#d8e9fc',lineColor='#65adff';
 function node(tag,attrs,text){const e=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;svg.append(e);return e;}
 const left=48,right=808,top=24,bottom=238,plotHeight=bottom-top,step=(right-left)/Math.max(1,m.timeline.length-1),maxVolume=Math.max(1,...m.timeline.map(r=>r.total));
 [0,25,50,75,100].forEach(tick=>{const y=bottom-tick/100*plotHeight;node('line',{x1:left,x2:right,y1:y,y2:y,stroke:gridColor});node('text',{x:32,y:y+4,fill:textColor,'font-size':10,'text-anchor':'end'},tick+' %');});
 node('text',{x:right,y:12,fill:textColor,'font-size':9,'text-anchor':'end'},'VOLUMEN · MÁX. '+maxVolume+' AUDITORÍAS');
 let previous=null;
 m.timeline.forEach((r,i)=>{const x=left+i*step,y=bottom-(r.pct||0)/100*plotHeight,bh=r.total/maxVolume*plotHeight*.45;
 const bar=node('rect',{x:x-Math.min(step*.28,10),y:bottom-bh,width:Math.min(step*.56,20),height:bh,rx:3,fill:volumeColor});const bt=document.createElementNS(ns,'title');bt.textContent=r.label+': '+r.total+' auditorías';bar.append(bt);
 if(i===0||i===m.timeline.length-1||i%Math.max(1,Math.ceil(m.timeline.length/6))===0)node('text',{x,y:bottom+23,fill:textColor,'font-size':9,'text-anchor':'middle'},r.label.slice(8,10)+'/'+r.label.slice(5,7));
 if(r.pct===null){previous=null;return;}if(previous)node('line',{x1:previous.x,y1:previous.y,x2:x,y2:y,stroke:lineColor,'stroke-width':2.5,'stroke-linecap':'round'});
 const dot=node('circle',{cx:x,cy:y,r:3.5,fill:lineColor,stroke:dark?'#101114':'white','stroke-width':2});const title=document.createElementNS(ns,'title');title.textContent=`${r.label}: ${r.pct} % · ${r.bad} / ${r.total} auditorías`;dot.append(title);previous={x,y};});
 node('circle',{cx:315,cy:288,r:3,fill:lineColor});node('text',{x:325,y:291,fill:textColor,'font-size':10},'Con incumplimientos %');node('rect',{x:495,y:284,width:8,height:8,rx:2,fill:volumeColor});node('text',{x:510,y:291,fill:textColor,'font-size':10},'Total de auditorías');box.append(svg);
 const details=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Consultar fechas y cantidades';details.append(summary);for(const r of m.timeline){const p=document.createElement('p');p.textContent=`${r.label}: ${r.pct===null?'Sin registros':r.pct+' %'} · ${r.total} auditorías`;details.append(p);}box.append(details);
};
