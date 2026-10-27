(() => {
const source=document.getElementById('chart-catalog'),dialog=document.getElementById('chart-help');if(!source||!dialog)return;
const catalog=new Map(JSON.parse(source.textContent).map(c=>[c.id,c]));let opener;
document.addEventListener('click',event=>{const button=event.target.closest('[data-help]');if(!button)return;const c=catalog.get(button.dataset.help);if(!c)return;opener=button;document.getElementById('help-title').textContent=c.title;for(const [id,key] of [['help-meaning','meaning'],['help-calculation','calculation'],['help-interpretation','interpretation']])document.getElementById(id).textContent=c[key];dialog.showModal();});
document.getElementById('close-chart-help').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
dialog.addEventListener('close',()=>{if(opener?.isConnected&&!opener.closest('[hidden]'))opener.focus({preventScroll:true});});
})();