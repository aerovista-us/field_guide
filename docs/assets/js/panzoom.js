/* Minimal pan/zoom for index map SVG */
(function(){
  const svg=document.getElementById('bg');
  const stage=document.getElementById('stage');
  if(!svg||!stage) return;

  let vb={x:0,y:0,w:1400,h:900}, vb0={...vb};
  function setVB(){ svg.setAttribute('viewBox', `${vb.x} ${vb.y} ${vb.w} ${vb.h}`); }
  function clamp(){
    const minW=850,maxW=2800;
    vb.w=Math.max(minW,Math.min(maxW,vb.w));
    vb.h=vb.w*(900/1400);
    vb.x=Math.max(-320,Math.min(1400 - vb.w + 320, vb.x));
    vb.y=Math.max(-320,Math.min(900 - vb.h + 320, vb.y));
  }
  let dragging=false,last={x:0,y:0};
  stage.addEventListener('pointerdown',e=>{dragging=true;stage.setPointerCapture(e.pointerId);last={x:e.clientX,y:e.clientY};});
  stage.addEventListener('pointermove',e=>{
    if(!dragging) return;
    const dx=e.clientX-last.x, dy=e.clientY-last.y; last={x:e.clientX,y:e.clientY};
    const r=stage.getBoundingClientRect(); const sx=vb.w/r.width, sy=vb.h/r.height;
    vb.x -= dx*sx; vb.y -= dy*sy; clamp(); setVB();
  });
  stage.addEventListener('pointerup',e=>{dragging=false; try{stage.releasePointerCapture(e.pointerId);}catch{};});
  stage.addEventListener('wheel',e=>{
    e.preventDefault();
    const r=stage.getBoundingClientRect();
    const mx=(e.clientX-r.left)/r.width, my=(e.clientY-r.top)/r.height;
    const zoom=Math.exp((e.deltaY>0?1:-1)*0.08);
    const newW=vb.w*zoom, newH=vb.h*zoom;
    vb.x = vb.x + (vb.w-newW)*mx;
    vb.y = vb.y + (vb.h-newH)*my;
    vb.w=newW; vb.h=newH;
    clamp(); setVB();
  }, {passive:false});
  window.addEventListener('keydown',e=>{ if(e.key.toLowerCase()==='r'){ vb={...vb0}; setVB(); }});
  setVB();
})();
