(()=>{
const d=document,root=d.documentElement;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
const $=(s,c=d)=>c.querySelector(s),$$=(s,c=d)=>[...c.querySelectorAll(s)];

/* header, burning-fuse progress, mobile bar */
const hdr=$('.hdr'),prog=$('.progress'),mbar=$('.mbar');
function onScroll(){const y=scrollY,h=root.scrollHeight-innerHeight;hdr&&hdr.classList.toggle('scrolled',y>30);if(prog)prog.style.transform=`scaleX(${h>0?y/h:0})`;if(mbar)mbar.classList.toggle('show',y>260)}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* mobile nav */
const bg=$('.burger'),mn=$('.mnav');
if(bg&&mn){const set=o=>{bg.setAttribute('aria-expanded',o);bg.setAttribute('aria-label',o?'Close menu':'Open menu');mn.classList.toggle('open',o);mn.setAttribute('aria-hidden',!o);mn.inert=!o;d.body.style.overflow=o?'hidden':''};
 mn.inert=true;
 bg.addEventListener('click',()=>set(bg.getAttribute('aria-expanded')!=='true'));
 $$('a',mn).forEach(a=>a.addEventListener('click',()=>set(false)));
 addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('open')){set(false);bg.focus()}})}

/* split headings into characters */
$$('.split-h').forEach(h=>{if(RM)return;const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3){const f=d.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(w=>{if(!w)return;if(/^\s+$/.test(w)){f.appendChild(d.createTextNode(w));return}const ws=d.createElement('span');ws.style.whiteSpace='nowrap';ws.style.display='inline-block';[...w].forEach(ch=>{const s=d.createElement('span');s.className='ch1';s.textContent=ch;ws.appendChild(s)});f.appendChild(ws)});c.replaceWith(f)}else if(c.nodeType===1)walk(c)})};
 h.setAttribute('aria-label',h.textContent.replace(/\s+/g,' ').trim());walk(h);[...h.children].forEach(s=>s.setAttribute('aria-hidden','true'));$$('.ch1',h).forEach((c,i)=>c.style.transitionDelay=(i*22)+'ms')});

/* reveals */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -5% 0px'});
$$('[data-r],.stagger,.split-h,.flow,.big-ic').forEach(el=>{if(RM)el.classList.add('in');else io.observe(el)});
$$('.stagger').forEach(g=>[...g.children].forEach((c,i)=>c.style.transitionDelay=(i*90)+'ms'));

/* phoenix-rise intro (home only, once per session; click to skip) */
const hero=$('.hero'),rise=$('.rise');
const goHero=()=>hero&&hero.classList.add('go');
if(rise){let seen=false;try{seen=sessionStorage.getItem('pd-rise')==='1';sessionStorage.setItem('pd-rise','1')}catch(e){}
 if(RM||seen){rise.classList.add('gone');goHero()}
 else{const st=$('.stage',rise);for(let i=0;i<18;i++){const s=d.createElement('i');s.className='sp';s.style.left=(8+Math.random()*84)+'%';s.style.setProperty('--dx',(Math.random()*80-40).toFixed(0)+'px');s.style.animationDelay=(Math.random()*1.6).toFixed(2)+'s';rise.appendChild(s)}
  d.body.style.overflow='hidden';
  const finish=()=>{if(rise.classList.contains('out'))return;rise.classList.add('out');d.body.style.overflow='';setTimeout(goHero,250);setTimeout(()=>rise.classList.add('gone'),950)};
  const tm=setTimeout(finish,2300);rise.addEventListener('click',()=>{clearTimeout(tm);finish()});addEventListener('keydown',e=>{if(e.key==='Escape'){clearTimeout(tm);finish()}},{once:true})}}
else goHero();

/* ember particles on <canvas class="embers"> (paused off-screen, static when reduced motion) */
function embers(cv){const ctx=cv.getContext('2d');if(!ctx)return;let W=0,H=0,P=[],run=false,raf;const dpr=Math.min(devicePixelRatio||1,2);
 const sprite=d.createElement('canvas');sprite.width=sprite.height=32;{const g=sprite.getContext('2d'),r=g.createRadialGradient(16,16,0,16,16,16);r.addColorStop(0,'rgba(255,236,190,1)');r.addColorStop(.25,'rgba(246,181,68,.9)');r.addColorStop(.55,'rgba(240,138,44,.35)');r.addColorStop(1,'rgba(194,65,12,0)');g.fillStyle=r;g.fillRect(0,0,32,32)}
 const dens=+(cv.dataset.n||1);
 function mk(init){return{x:Math.random()*W,y:init?Math.random()*H:H+10,r:.6+Math.random()*2.3,vy:.25+Math.random()*1.1,ph:Math.random()*6.28,w:.3+Math.random()*.9,life:1,fade:.0015+Math.random()*.004}}
 function size(){const r=cv.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);const n=Math.min(150,Math.round(W*H/9000*dens));P=Array.from({length:n},()=>mk(true));if(RM)draw(false)}
 function draw(move){ctx.clearRect(0,0,W,H);ctx.globalCompositeOperation='lighter';
  for(const p of P){if(move){p.y-=p.vy;p.ph+=.02;p.x+=Math.sin(p.ph)*p.w*.6;p.life-=p.fade;if(p.y<-10||p.life<=0)Object.assign(p,mk(false))}
   const k=Math.max(0,Math.min(1,p.life))*Math.min(1,p.y/(H*.25+1)+.15);const s=p.r*6;ctx.globalAlpha=k;ctx.drawImage(sprite,p.x-s/2,p.y-s/2,s,s)}
  ctx.globalAlpha=1}
 function loop(){draw(true);raf=requestAnimationFrame(loop)}
 size();addEventListener('resize',()=>{clearTimeout(cv._t);cv._t=setTimeout(size,150)});
 if(RM)return;
 new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting&&!run){run=true;loop()}else if(!e.isIntersecting&&run){run=false;cancelAnimationFrame(raf)}})).observe(cv)}
$$('canvas.embers').forEach(embers);

/* orbit: trades light up in turn around the phoenix; hover/focus takes over */
$$('.orbit').forEach(o=>{const bs=$$('.ob',o),now=$('.now b',o);if(!bs.length)return;let i=0,tm;
 const lite=k=>{bs.forEach((b,j)=>b.classList.toggle('lit',j===k));if(now)now.textContent=bs[k].dataset.name;i=k};
 const auto=()=>{clearInterval(tm);if(!RM)tm=setInterval(()=>lite((i+1)%bs.length),1700)};
 bs.forEach((b,k)=>{b.addEventListener('mouseenter',()=>{clearInterval(tm);lite(k)});b.addEventListener('focus',()=>{clearInterval(tm);lite(k)});b.addEventListener('mouseleave',auto);b.addEventListener('blur',auto)});
 lite(0);auto()});

/* tilt cards + magnetic buttons */
if(FINE&&!RM)$$('.gcard').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.setProperty('--ry',(x*7).toFixed(2)+'deg');c.style.setProperty('--rx',(-y*7).toFixed(2)+'deg')});c.addEventListener('pointerleave',()=>{c.style.setProperty('--ry','0deg');c.style.setProperty('--rx','0deg')})});
if(FINE&&!RM)$$('.btn.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;b.style.transform=`translate(${(x*.16).toFixed(1)}px,${(y*.26).toFixed(1)}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});

/* services jump bar: highlight the group in view */
const jl=$$('.jump a');
if(jl.length){const map=new Map(jl.map(a=>[a.getAttribute('href').slice(1),a]));
 const jo=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){jl.forEach(a=>a.classList.remove('on'));const a=map.get(e.target.id);if(a){a.classList.add('on');a.scrollIntoView({block:'nearest',inline:'center',behavior:RM?'auto':'smooth'})}}}),{rootMargin:'-45% 0px -50% 0px'});
 map.forEach((a,id)=>{const s=d.getElementById(id);s&&jo.observe(s)})}

/* estimate form: builds a text message to the business phone; nothing is submitted anywhere */
const f=$('#estimate-form');
if(f){const v=n=>(f.elements[n]&&f.elements[n].value||'').trim();
 const msg=()=>`Estimate request from the Phoenix Delta website\nName: ${v('name')}\nPhone: ${v('phone')}\nArea: ${v('area')}\nService: ${v('service')}\nDetails: ${v('details')}`;
 f.addEventListener('submit',e=>{e.preventDefault();if(!f.reportValidity())return;const ios=/iP(hone|ad|od)/.test(navigator.userAgent);location.href=f.dataset.sms+(ios?'&':'?')+'body='+encodeURIComponent(msg())});
 const em=$('[data-mail]',f);if(em)em.addEventListener('click',()=>{if(!f.reportValidity())return;location.href='mailto:'+f.dataset.email+'?subject='+encodeURIComponent('Estimate request')+'&body='+encodeURIComponent(msg())})}

/* demo pill */
const dm=$('.demo');if(dm){try{if(sessionStorage.getItem('pd-demo')==='x')dm.remove()}catch(e){};const x=$('button',dm);x&&x.addEventListener('click',()=>{dm.remove();try{sessionStorage.setItem('pd-demo','x')}catch(e){}})}
})();
