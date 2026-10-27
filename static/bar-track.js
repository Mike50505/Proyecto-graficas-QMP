/* SVG tracks have intrinsic geometry and never depend on nested percentage heights. */
window.FCDBarTrack=function(track,parts,maximum,label){
 const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');
 svg.setAttribute('viewBox','0 0 1000 16');svg.setAttribute('preserveAspectRatio','none');svg.setAttribute('role','img');svg.classList.add('bar-svg');
 const available=parts.some(p=>p.value!==null&&p.value!==undefined&&Number.isFinite(Number(p.value))),total=parts.reduce((sum,p)=>sum+(Number(p.value)||0),0);
 track.dataset.state=!available?'unavailable':total===0?'zero':'value';
 const description=label+': '+parts.map(p=>p.label+' '+(p.value===null||p.value===undefined?'Sin datos aplicables':p.value)).join('; ');svg.setAttribute('aria-label',description);
 const title=document.createElementNS(ns,'title');title.textContent=description;svg.append(title);
 let offset=0;for(const part of parts){const value=Number(part.value);if(!Number.isFinite(value)||value<=0)continue;const width=value/Math.max(1,maximum)*1000,rect=document.createElementNS(ns,'rect');rect.setAttribute('x',offset);rect.setAttribute('y','0');rect.setAttribute('width',width);rect.setAttribute('height','16');rect.setAttribute('fill',part.color);rect.dataset.value=String(value);rect.dataset.series=part.label;svg.append(rect);offset+=width;}
 if(available&&total===0){const line=document.createElementNS(ns,'line');line.setAttribute('x1','0');line.setAttribute('x2','1000');line.setAttribute('y1','8');line.setAttribute('y2','8');line.setAttribute('stroke','currentColor');line.setAttribute('stroke-width','1');line.setAttribute('stroke-dasharray','8 8');svg.append(line);}
 track.replaceChildren(svg);track.title=description;
};
