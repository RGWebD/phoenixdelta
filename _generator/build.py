#!/usr/bin/env python3
"""Generator for the Phoenix Delta LLC demo site (RGWebD). Writes ../site."""
import json, shutil, html, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from icons import I
from data import *
GEN=Path(__file__).parent; OUT=GEN.parent/'site'; BR=GEN.parent/'brand'
e=html.escape
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
    if p.name=='.git': continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
A=OUT/'assets'; shutil.copytree(GEN/'assets'/'img',A/'img'); shutil.copytree(GEN/'assets'/'fonts',A/'fonts')
for f in ['pd-wordmark-dark.svg','pd-wordmark-light.svg','pd-wordmark-white.svg','pd-wordmark-navy.svg','pd-wordmark-compact.svg','pd-wordmark-compact-light.svg']: shutil.copy(BR/f,A/f)
shutil.copy(BR/'png/favicon.ico',OUT/'favicon.ico'); shutil.copy(BR/'png/favicon-180.png',OUT/'apple-touch-icon.png')
for f in ['favicon-32.png','favicon-512.png','horizontal-dark-1400.png','horizontal-light-1400.png','stacked-dark-1000.png']: shutil.copy(BR/'png'/f,A/f)
shutil.copy(GEN/'src/styles.css',A/'styles.css'); shutil.copy(GEN/'src/script.js',A/'script.js')
# OG image: midnight plate, ember glow and sparks, emblem + wordmark
random.seed(7)
og=Image.new('RGB',(1200,630),(7,18,40)); gl=Image.new('RGB',(1200,630),(0,0,0)); g=ImageDraw.Draw(gl)
g.ellipse((300,380,900,900),fill=(150,50,10)); g.ellipse((700,40,1250,560),fill=(20,42,85)); gl=gl.filter(ImageFilter.GaussianBlur(120))
og=Image.blend(og,Image.composite(gl,og,Image.new('L',og.size,255)),.9)
from PIL import ImageChops
og=ImageChops.add(Image.new('RGB',og.size,(7,18,40)),gl.point(lambda v:int(v*.9)))
sp=Image.new('RGBA',og.size,(0,0,0,0)); s=ImageDraw.Draw(sp)
for _ in range(90):
    x=random.randint(0,1200); y=random.randint(200,630); r=random.choice([1,1,2,2,3]); c=random.choice([(246,181,68),(240,138,44),(255,226,166)])
    s.ellipse((x-r,y-r,x+r,y+r),fill=c+(random.randint(120,255),))
sp=Image.alpha_composite(sp.filter(ImageFilter.GaussianBlur(3)),sp)
og=og.convert('RGBA'); og.alpha_composite(sp)
em=Image.open(BR/'pd-emblem-cutout.png').convert('RGBA'); em=em.resize((560,round(em.height*560/em.width)),Image.LANCZOS); og.alpha_composite(em,(620,120))
lg=Image.open(BR/'png/stacked-dark-1000.png').convert('RGBA')
wm=Image.open(BR/'png/horizontal-dark-1400.png').convert('RGBA'); bb=wm.getbbox(); wm=wm.crop(bb)
# wordmark only = right part of horizontal lockup (after emblem); detect by taking right 58%
wcrop=wm.crop((int(wm.width*.36),0,wm.width,wm.height)); wcrop=wcrop.crop(wcrop.getbbox()); wcrop=wcrop.resize((560,round(wcrop.height*560/wcrop.width)),Image.LANCZOS)
og.alpha_composite(wcrop,(60,190)); og=og.convert('RGB'); d=ImageDraw.Draw(og)
try:
    fnt=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Jost/Jost-VariableFont_wght.ttf',30); fnt.set_variation_by_axes([500])
    d.text((62,215+wcrop.height),'Home installation & repair, many trades',font=fnt,fill=(255,248,240)); d.text((62,258+wcrop.height),f'Jacksonville, FL & surrounding areas · {PHONE}',font=fnt,fill=(246,181,68))
except Exception as ex: print('og font',ex)
og.save(A/'og-image.jpg',quality=86)

def dims(name,w=1600): return Image.open(A/'img'/f'{name}-{w}.webp').size
def pic(name,alt,sizes='(max-width:980px) 100vw, 33vw'):
    w,h=dims(name); w8,_=dims(name,800)
    return f'<img src="assets/img/{name}-1600.webp" srcset="assets/img/{name}-800.webp {w8}w, assets/img/{name}-1600.webp {w}w" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async">'
def slots(key,cls='slots'):
    out=''
    for sid,lab,img in SLOTS[key]:
        if img: out+=f'<figure class="slot has" data-slot="{sid}">{pic(img,lab)}<figcaption>{e(lab)}</figcaption></figure>'
        else: out+=f'<!-- PHOTO SLOT "{sid}": set SLOTS in data.py to swap in a real photo --><figure class="slot" data-slot="{sid}"><div class="ph">{I["camera"]}<b>{e(lab)}</b><span>Project photos coming soon</span></div></figure>'
    return f'<div class="{cls} stagger">{out}</div>' if cls else out
def btn_call(cls='',label=None): return f'<a class="btn mag {cls}" href="{TEL}">{I["phone"]}<span class="lbl">{label or "Call "+PHONE}</span></a>'
def btn_est(cls='ghost',label='Get an estimate'): return f'<a class="btn mag {cls}" href="contact.html#estimate">{I["msg"]}<span class="lbl">{label}</span></a>'
DEFS='<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs><linearGradient id="fireg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#C2410C"/><stop offset=".45" stop-color="#F08A2C"/><stop offset="1" stop-color="#F6B544"/></linearGradient></defs></svg>'
NAV=[('index.html','Home'),('services.html','Services'),('about.html','About'),('service-area.html','Service Area'),('contact.html','Contact')]
BRAND='<img class="em" src="assets/img/emblem-600.webp" width="600" height="387" alt=""><img class="wm" src="assets/pd-wordmark-compact.svg" width="216" height="90" alt="Phoenix Delta LLC, Installation and Repair">'
def header(cur):
    nav=''.join(f'<a href="{f}"{" aria-current=\"page\"" if f==cur else ""}>{t}</a>' for f,t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>{DEFS}
<header class="hdr"><div class="wrap"><a class="brand" href="index.html" aria-label="Phoenix Delta LLC home">{BRAND}</a>
<nav class="nav" aria-label="Main">{nav}</nav><div class="hdr-cta"><a class="btn sm mag" href="{TEL}" aria-label="Call {PHONE}">{I["phone"]}<span class="num">{PHONE}</span><span class="sr">Call</span></a></div>
<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><span></span><span></span><span></span></button></div></header>
<nav class="mnav" id="mnav" aria-label="Mobile" aria-hidden="true">{nav}<div class="ctas">{btn_call()}{btn_est()}</div></nav>'''
def footer():
    pages=''.join(f'<li><a href="{f}">{t}</a></li>' for f,t in NAV)
    sv=''.join(f'<li><a href="services.html#{g["id"]}">{g["t"]}</a></li>' for g in GROUPS)
    return f'''<footer class="ftr"><div class="wrap"><div class="fgrid">
<div><div class="flogo"><img src="assets/img/emblem-600.webp" width="600" height="387" alt="" loading="lazy"><img src="assets/pd-wordmark-compact.svg" width="216" height="90" alt="Phoenix Delta LLC" loading="lazy"></div><p>Home installation and repair across many trades, one call away. Serving {AREA}.</p></div>
<div><h4>Pages</h4><ul>{pages}</ul></div><div><h4>Services</h4><ul>{sv}</ul></div>
<div><h4>Get in touch</h4><ul><li><a href="{TEL}">{PHONE}</a></li><li><a href="contact.html#estimate">Estimate request</a></li><li><a href="service-area.html">Jacksonville &amp; surrounding areas</a></li></ul></div>
</div><div class="bigword" aria-hidden="true">PHOENIX</div><div class="legal"><span>© 2026 {NAME}. All rights reserved.</span><span>Design preview by RGWebD</span></div></div></footer>
<div class="mbar">{btn_call('', 'Call now')}<a class="btn mag ghost" href="contact.html#estimate">{I["msg"]}<span class="lbl">Estimate</span></a></div>
<div class="demo" role="note">Design preview by RGWebD<button type="button" aria-label="Dismiss preview note">×</button></div>'''
# ---------- JSON-LD ----------
AREA_LD=[{"@type":"City","name":"Jacksonville","containedInPlace":{"@type":"State","name":"Florida"}}]+[{"@type":"AdministrativeArea","name":f"{c} County, FL"} for c in COUNTIES]
def biz():
    return {"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","@id":BASE+"#business","name":NAME,"slogan":TAGLINE,
      "description":"Phoenix Delta LLC is a home installation and repair company serving Jacksonville, Florida and the surrounding areas: painting, plastering, caulking, interior remodeling (non-licensed work), cabinetry, handyman services, flooring, decorative stone, tile, marble, granite and terrazzo installation, stuccoing, pressure washing, driveway and tennis court installation, and canvas awning and ornamental iron installation.",
      "url":BASE,"telephone":"+1-904-562-9356","logo":BASE+"assets/favicon-512.png","image":[BASE+"assets/og-image.jpg",BASE+"assets/horizontal-dark-1400.png"],
      "address":{"@type":"PostalAddress","addressLocality":"Jacksonville","addressRegion":"FL","addressCountry":"US"},
      "areaServed":AREA_LD,"knowsAbout":[t for _,t,_,_ in ALL],
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Home installation and repair services","itemListElement":[{"@type":"OfferCatalog","name":g["t"],"itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":t,"description":dd,"areaServed":AREA_LD[0]["name"]+", FL","url":BASE+"services.html#"+g["id"]}} for _,t,dd in g["items"]]} for g in GROUPS]}}
def crumbs_ld(name,f): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":name,"item":BASE+f}]}
def faq_ld(items): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
def faq(items): return '<div class="faq" data-r>'+''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in items)+'</div>'
def crumbs(name): return f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span aria-current="page">{name}</span></nav>'
def phero(kick,h1,lead,name,word):
    return f'''<section class="phero"><canvas class="embers" data-n=".6" aria-hidden="true"></canvas><img class="wm-bg" src="assets/img/emblem-1200.webp" width="1200" height="774" alt=""><div class="gword" aria-hidden="true">{word}</div><div class="wrap">{crumbs(name)}<p class="kicker"><i></i>{kick}</p><h1 class="split-h">{h1}</h1><p class="lead" data-r>{lead}</p><div class="ctas" style="margin-top:28px" data-r>{btn_call()}{btn_est()}</div></div></section>'''
def cta(h,sub,kick='Call or request an estimate'):
    return f'''<section class="cta"><canvas class="embers" data-n="1.2" aria-hidden="true"></canvas><div class="flames" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div><div class="wrap"><p class="kicker both">{kick}</p><h2 class="split-h">{h}</h2><p class="lead">{sub}</p><a class="phone fire-t" href="{TEL}">{PHONE}</a><div class="ctas">{btn_call('xl')}{btn_est('ghost xl')}</div></div></section>'''
def page(fname,title,desc,body,ld):
    canon=BASE+('' if fname=='index.html' else fname)
    lds=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}"><meta name="robots" content="index,follow">
<meta name="theme-color" content="#071228"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.jpg">
<link rel="preload" href="assets/fonts/cinzel.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/jost.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css"><script>document.documentElement.classList.add('js')</script>{lds}</head>
<body>{header(fname)}<main id="main">{body}</main>{footer()}<script src="assets/script.js" defer></script></body></html>'''

# ---------- HOME ----------
ICON_OF={i:i for i,_,_,_ in ALL}
obs=''
for k,(i,t,_,gid) in enumerate(ALL):
    a=-math.pi/2+2*math.pi*k/len(ALL); x=50+44*math.cos(a); y=50+44*math.sin(a)
    obs+=f'<a class="ob" href="services.html#{gid}" style="left:{x:.2f}%;top:{y:.2f}%" data-name="{e(t)}" aria-label="{e(t)}">{I[i]}</a>'
orbit=f'''<div class="orbit" data-h="2"><svg class="ring" viewBox="0 0 100 100" aria-hidden="true"><circle class="r3" cx="50" cy="50" r="38"/><circle class="r1" cx="50" cy="50" r="50"/><circle class="r2" cx="50" cy="50" r="50" pathLength="282"/></svg>
<div class="core"><img src="assets/img/emblem-1200.webp" srcset="assets/img/emblem-600.webp 600w, assets/img/emblem-1200.webp 1200w" sizes="(max-width:980px) 60vw, 360px" width="1200" height="774" alt="Phoenix Delta emblem: a phoenix rising over the coast" fetchpriority="high"><p class="now" aria-live="off">Installation &amp; repair<b>{ALL[0][1]}</b></p></div>{obs}</div>'''
tick=''.join(f'<li>{I[i]}{e(t)}</li>' for i,t,_,_ in ALL)
gcards=''.join(f'''<a class="gcard" href="services.html#{g["id"]}"><span class="n">0{k+1}</span><span class="ic">{I[g["ic"]]}</span><p class="label" style="margin-bottom:10px">{g["k"]}</p><h3>{g["t"]}</h3><p>{g["s"]}</p><ul>{"".join(f"<li>{t}</li>" for _,t,_ in g["items"])}</ul><span class="go">See details {I["arrow"]}</span></a>''' for k,g in enumerate(GROUPS))
STEPS=[("phone","Call or text",f"Reach Phoenix Delta at {PHONE} and tell us what’s on your list."),("msg","Describe the job","Share the details, and photos if you have them. Big project or small fix."),("one","Get an estimate","We talk through the work and give you an estimate before anything starts."),("flame","Work gets done","One company, one point of contact, many trades.")]
flow=''.join(f'<div class="step"><div class="dot">{I[ic]}</div><h3>{t}</h3><p>{p}</p></div>' for ic,t,p in STEPS)
def radar(big=False):
    rings=''.join(f'<circle cx="50" cy="50" r="{r}"/>' for r in (12,24,36,48))+'<line x1="50" y1="0" x2="50" y2="100"/><line x1="0" y1="50" x2="100" y2="50"/>'
    pos={"Nassau":(47,17),"Duval":(64,38),"Clay":(28,70),"St. Johns":(66,77)}
    cty=''.join(f'<span class="cty" style="left:{x}%;top:{y}%">{c}</span>' for c,(x,y) in pos.items())
    return f'<div><div class="radar" data-r="zoom" role="img" aria-label="Stylized service-area graphic: Jacksonville at the center, with Nassau, Duval, Clay and St. Johns counties around it"><svg class="rings" viewBox="0 0 100 100" aria-hidden="true">{rings}</svg><div class="sweep"></div><span class="ctr"></span><span class="city">Jacksonville</span>{cty}<span class="sea">Atlantic</span></div><p class="radar-note">Stylized graphic, not to scale.</p></div>'
clist=''.join(f'<li>{I["pin"] if "pin" in I else I["map"]}<span>{c}<small>County</small></span></li>' for c in COUNTIES)
home=f'''<div class="rise" aria-hidden="true"><div class="stage"><div class="glow"></div><img class="bird" src="assets/img/emblem-1200.webp" width="1200" height="774" alt=""><img class="wm" src="assets/pd-wordmark-dark.svg" width="748" height="118" alt=""></div><span class="skipr">Tap to skip</span></div>
<section class="hero"><canvas class="embers" aria-hidden="true"></canvas><div class="flames" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
<div class="wrap"><div><p class="kicker" data-h="1"><i></i>Jacksonville &amp; surrounding areas</p>
<h1 data-h="2"><span class="l">One call.</span><span class="l fire-t">Many jobs.</span></h1>
<p class="lead" data-h="3">{NAME} handles home installation and repair across {len(ALL)} trades, from painting, flooring and cabinetry to stucco, tile and stone, pressure washing, driveways, awnings and ornamental iron.</p>
<div class="ctas" data-h="4">{btn_call('xl')}{btn_est('ghost xl')}</div>
<ul class="chips" data-h="5"><li>{I["flame"]}Brand-new company</li><li>{I["house"]}Installation &amp; repair</li><li>{I["compass"]}Duval · Clay · St. Johns · Nassau</li></ul></div>
{orbit}</div></section>
<div class="ticker" aria-hidden="true"><ul>{tick}{tick}</ul></div>
<section class="sec" id="services"><div class="wrap"><div class="shead c"><p class="kicker both">What we do</p><h2 class="split-h">Many trades, <span class="gold">one number</span></h2><p class="lead" data-r>Instead of lining up a different company for every job, call one. Here’s everything Phoenix Delta handles, grouped the way homeowners think about it.</p></div>
<div class="groups stagger">{gcards}</div></div></section>
<section class="sec alt"><div class="wrap"><div class="shead"><p class="kicker"><i></i>How it works</p><h2 class="split-h">From first call to finished work</h2></div><div class="flow">{flow}</div></div></section>
<section class="sec"><div class="wrap area"><div data-r="left"><p class="kicker"><i></i>Service area</p><h2 class="split-h">Serving Jacksonville &amp; the First Coast</h2><p class="lead">Phoenix Delta works across Jacksonville and the surrounding areas, including these Northeast Florida counties.</p><ul class="clist">{clist}</ul><a class="btn mag ghost" href="service-area.html">{I["compass"]}<span class="lbl">About our service area</span></a></div>{radar()}</div></section>
<section class="sec alt"><div class="wrap"><div class="shead"><p class="kicker"><i></i>Project gallery</p><h2 class="split-h">Our work, coming soon</h2><p class="lead" data-r>Phoenix Delta is just getting started. Photos of real finished projects will go here as the jobs are completed.</p></div>{slots("home")}<p class="slots-note">{I["camera"]}Every photo on this site will be our own work. No stock images.</p></div></section>
{cta("Got a list? <span class='gold'>Call one number.</span>","Tell us what needs installing, fixing or refreshing. Big project or a handful of small ones, start with a call.")}'''

# ---------- SERVICES ----------
jump=''.join(f'<a href="#{g["id"]}">{I[g["ic"]]}{g["t"]}</a>' for g in GROUPS)
grps=''
for k,g in enumerate(GROUPS):
    arts=''.join(f'<article id="{i}-svc"><span class="si">{I[i]}</span><div><h3>{t}</h3><p>{dd}</p></div></article>' for i,t,dd in g["items"])
    note=f'<div class="note">{I["info"] if "info" in I else I["flame"]}<span>Interior remodeling covers non-licensed work only. Work that requires a state-licensed trade isn’t part of this service.</span></div>' if g["id"]=="remodel" else ''
    grps+=f'''<section class="grp" id="{g["id"]}"><div class="side"><div class="big-ic">{I[g["ic"]]}</div><span class="gn">0{k+1} / 0{len(GROUPS)}</span><p class="label">{g["k"]}</p><h2 class="split-h">{g["t"]}</h2><p class="muted">{g["s"]}</p><a class="btn sm mag" href="contact.html#estimate" style="margin-top:8px">{I["msg"]}<span class="lbl">Ask about this</span></a></div>
<div><div class="svc stagger">{arts}</div>{note}{slots(g["id"],cls="")}</div></section>'''
services=f'''{phero("Installation &amp; repair","Every service, one call","{len(ALL)} home services from one company, serving Jacksonville and the surrounding areas. Not sure if your job fits? Call and ask.".replace("{len(ALL)}",str(len(ALL))),"Services","SERVICES")}
<nav class="jump" aria-label="Service groups"><div class="wrap">{jump}</div></nav><div class="wrap">{grps}</div>
<section class="sec alt"><div class="wrap"><div class="shead c"><p class="kicker both">Questions</p><h2 class="split-h">Good to know</h2></div>{faq(FAQ)}</div></section>
{cta("Don’t see your job? <span class='gold'>Ask.</span>","If it’s on your list, call and talk it through. We’ll tell you straight whether it’s work we do.")}'''

# ---------- ABOUT ----------
about=f'''{phero("About Phoenix Delta","A new local company, built to rise","Phoenix Delta LLC is a new home installation and repair company serving Jacksonville and the surrounding areas.","About","ABOUT")}
<section class="sec"><div class="wrap story"><div data-r="left"><p class="kicker"><i></i>Our story</p><h2 class="split-h">One company for the whole to-do list</h2>
<p>Most homes need more than one kind of work: a room to paint, a floor to replace, a driveway to pour, a railing to install, a wall that needs patching. Usually that means calling a different company for every job.</p>
<p>The idea behind Phoenix Delta is simple. It’s a new company that brings a wide range of installation and repair trades under one name and one phone number, so homeowners in the Jacksonville area can make one call and get many jobs handled.</p>
<p>Because the company is brand new, there’s no long list of past projects here yet. As the work gets done, real photos of it will fill this site.</p></div>
<img class="badge" data-r="right" src="assets/img/badge-400.webp" width="400" height="400" alt="Phoenix Delta LLC badge" loading="lazy"></div></section>
<section class="sec alt"><div class="wrap"><div class="shead c"><p class="kicker both">The name</p><h2 class="split-h">Why a phoenix?</h2><p class="lead" data-r>The phoenix is the bird that rises renewed. That’s the idea behind the work: taking worn, tired or unfinished parts of a home and bringing them back better.</p></div>
<div class="meaning stagger"><div class="mcard"><span class="big fire-t">Rise</span><p>A brand-new company starting out in the Jacksonville area, ready to earn its name one job at a time.</p></div><div class="mcard"><span class="big fire-t">Renew</span><p>Fresh paint, new floors, clean surfaces and solid finishes: the trades are all about making things new again.</p></div><div class="mcard"><span class="big fire-t">Repair</span><p>Installation and repair. When something needs fixing, it’s one call to the same number.</p></div></div></div></section>
<section class="sec"><div class="wrap"><div class="shead"><p class="kicker"><i></i>Project gallery</p><h2 class="split-h">Photos on the way</h2><p class="lead" data-r>These spaces are saved for photos of real Phoenix Delta projects.</p></div>{slots("about")}</div></section>
{cta("Be one of our <span class='gold'>first projects.</span>","Call to talk through what your home needs.")}'''

# ---------- SERVICE AREA ----------
AREA_FAQ=[FAQ[1],FAQ[2],FAQ[3]]
carea=''.join(f'<li>{I["map"]}<span>{c} County<small>Northeast Florida</small></span></li>' for c in COUNTIES)
svcarea=f'''{phero("Service area","Jacksonville &amp; surrounding areas","Phoenix Delta serves Jacksonville, Florida and the surrounding areas across Northeast Florida.","Service Area","FIRST COAST")}
<section class="sec"><div class="wrap area"><div data-r="left"><p class="kicker"><i></i>Where we work</p><h2 class="split-h">Based around Jacksonville</h2><p class="lead">Phoenix Delta is a service-area business: we come to you. Work is focused on Jacksonville and the surrounding areas, including:</p><ul class="clist">{carea}</ul><p class="muted">Just outside these areas? Call {PHONE} and ask. It depends on the job.</p><div class="ctas">{btn_call()}</div></div>{radar(True)}</div></section>
<section class="sec alt"><div class="wrap"><div class="shead c"><p class="kicker both">Available across the area</p><h2 class="split-h">Every service, wherever you are</h2></div><div class="groups stagger">{gcards}</div></div></section>
<section class="sec"><div class="wrap"><div class="shead c"><p class="kicker both">Questions</p><h2 class="split-h">Service area FAQ</h2></div>{faq(AREA_FAQ)}</div></section>
{cta("In the Jacksonville area? <span class='gold'>Let’s talk.</span>","Call or send an estimate request with your area and the job.")}'''

# ---------- CONTACT ----------
opts=''.join(f'<optgroup label="{e(g["t"])}">'+''.join(f'<option>{e(t)}</option>' for _,t,_ in g["items"])+'</optgroup>' for g in GROUPS)+'<option>Several jobs / not sure</option>'
mailbtn=f'<button class="btn ghost mag" type="button" data-mail>{I["mail"]}<span class="lbl">Email instead</span></button>' if EMAIL else ''
contact=f'''{phero("Contact","Let’s get it on the schedule","Call, or send an estimate request as a text. Tell us what needs doing and where.","Contact","CONTACT")}
<section class="sec" id="estimate"><div class="wrap cgrid"><div class="card callcard" data-r="left"><p class="label">Call or text</p><a class="phone fire-t" href="{TEL}">{PHONE}</a><div class="ctas">{btn_call('', 'Call now')}<a class="btn mag ghost" href="{SMS}">{I["msg"]}<span class="lbl">Send a text</span></a></div>
<ul class="tips"><li>{I["check"]}<span>Say what the job is, and list everything if there’s more than one.</span></li><li>{I["check"]}<span>Include your part of town or county.</span></li><li>{I["check"]}<span>Photos help. Text them over after your message.</span></li><li>{I["compass"]}<span>Serving {AREA}.</span></li></ul></div>
<form class="card" id="estimate-form" data-sms="{SMS}" data-email="{EMAIL}" data-r="right" novalidate><p class="label">Estimate request</p><h2 style="font-size:clamp(1.7rem,3vw,2.3rem)">Tell us about the job</h2>
<div class="row"><div class="fld"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div><div class="fld"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<div class="row"><div class="fld"><label for="f-area">Area / neighborhood</label><input id="f-area" name="area" placeholder="e.g. Jacksonville, Clay County"></div><div class="fld"><label for="f-service">Service</label><select id="f-service" name="service" required><option value="">Choose a service</option>{opts}</select></div></div>
<div class="fld"><label for="f-details">Details</label><textarea id="f-details" name="details" placeholder="What needs installing or repairing? Size, timing, anything useful." required></textarea></div>
<div class="ctas"><button class="btn mag" type="submit">{I["msg"]}<span class="lbl">Text my request</span></button>{mailbtn}</div>
<p class="fnote">This opens a pre-filled text message to {PHONE} on your phone. Nothing is sent until you press send. On a computer? Just call.</p></form></div></section>
<section class="sec alt"><div class="wrap"><div class="shead c"><p class="kicker both">Questions</p><h2 class="split-h">Before you call</h2></div>{faq(FAQ)}</div></section>'''

nf=f'''<section class="phero" style="min-height:80vh;display:flex;align-items:center"><canvas class="embers" aria-hidden="true"></canvas><div class="gword" aria-hidden="true">404</div><div class="wrap"><p class="kicker"><i></i>Page not found</p><h1>This page went up in smoke</h1><p class="lead">The page you’re looking for isn’t here. Head back home or give us a call.</p><div class="ctas" style="margin-top:28px"><a class="btn mag" href="/{REPO}/">{I["house"]}<span class="lbl">Back to home</span></a><a class="btn mag ghost" href="{TEL}">{I["phone"]}<span class="lbl">Call {PHONE}</span></a></div></div></section>'''

D_HOME=f"{NAME}: home installation and repair in Jacksonville, FL and surrounding areas. Painting, flooring, cabinetry, tile and stone, stucco, pressure washing, driveways, awnings, ornamental iron and more. Call {PHONE}."
PAGES=[
 ('index.html',f'{NAME} | Home Installation & Repair, Jacksonville FL',D_HOME,home,[biz()]),
 ('services.html',f'Services | {NAME}, Jacksonville FL',f'All {len(ALL)} home installation and repair services from {NAME}: painting, plastering, caulking, interior remodeling (non-licensed), cabinetry, handyman, flooring, decorative stone and tile, stucco, pressure washing, driveways, tennis courts, canvas awnings and ornamental iron.',services,[biz(),crumbs_ld('Services','services.html'),faq_ld(FAQ)]),
 ('about.html',f'About | {NAME}',f'{NAME} is a new local home installation and repair company serving Jacksonville, FL and the surrounding areas.',about,[biz(),crumbs_ld('About','about.html')]),
 ('service-area.html',f'Service Area: Jacksonville & Surrounding Areas | {NAME}',f'{NAME} serves Jacksonville, FL and the surrounding areas, including Duval, Clay, St. Johns and Nassau counties. Call {PHONE}.',svcarea,[biz(),crumbs_ld('Service Area','service-area.html'),faq_ld(AREA_FAQ)]),
 ('contact.html',f'Contact & Estimates | {NAME}',f'Call {PHONE} or send an estimate request to {NAME}, serving Jacksonville, FL and surrounding areas.',contact,[biz(),crumbs_ld('Contact','contact.html'),faq_ld(FAQ)]),
]
for f,t,dsc,b,ld in PAGES: (OUT/f).write_text(page(f,t,dsc,b,ld))
p404=page('404.html',f'Page not found | {NAME}','Page not found.',nf,[]).replace('href="assets/',f'href="/{REPO}/assets/').replace('src="assets/',f'src="/{REPO}/assets/').replace('href="favicon.ico"',f'href="/{REPO}/favicon.ico"').replace('href="apple-touch-icon.png"',f'href="/{REPO}/apple-touch-icon.png"')
for f,_ in NAV: p404=p404.replace(f'href="{f}',f'href="/{REPO}/{f}')
p404=p404.replace('<meta name="robots" content="index,follow">','<meta name="robots" content="noindex">')
(OUT/'404.html').write_text(p404)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{"" if f=="index.html" else f}</loc><lastmod>2026-11-25</lastmod></url>' for f,*_ in PAGES)+'</urlset>\n')
svc_lines='\n'.join(f'- {g["t"]}: '+'; '.join(t for _,t,_ in g["items"]) for g in GROUPS)
(OUT/'llms.txt').write_text(f'''# {NAME}

> {NAME} ("{TAGLINE}") is a new home installation and repair company serving Jacksonville, Florida and the surrounding areas. One call for many jobs. Phone: {PHONE}.

## Key facts
- Business type: home installation and repair, multi-service (HomeAndConstructionBusiness)
- Service area: Jacksonville, FL and surrounding areas, including {", ".join(COUNTIES[:-1])} and {COUNTIES[-1]} counties. Service-area business, no public storefront address.
- Phone: {PHONE} (estimate requests can be sent by text from the Contact page)
- Interior remodeling is non-licensed work only; work requiring a state-licensed trade is not offered.
- The company is new: no reviews, ratings, prices, hours or email are published yet.

## Services
{svc_lines}

## Pages
- [Home]({BASE}): overview, service groups, how it works, service area
- [Services]({BASE}services.html): all {len(ALL)} services in six groups, with FAQ
- [About]({BASE}about.html): the company and its name
- [Service Area]({BASE}service-area.html): Jacksonville and surrounding counties
- [Contact]({BASE}contact.html): phone and estimate request form
''')
(OUT/'.nojekyll').write_text('')
(OUT/'README.md').write_text(f'# {NAME} — website design preview\n\nStatic site generated by `_generator/build.py` (RGWebD). Live: {BASE}\n\nPhoto slots: see `SLOTS` in `_generator/data.py`.\n')
gd=OUT/'_generator'; gd.mkdir(exist_ok=True)
for f in ['build.py','data.py','icons.py']: shutil.copy(GEN/f,gd/f)
if (GEN/'qa.py').exists(): shutil.copy(GEN/'qa.py',gd/'qa.py')
shutil.copytree(GEN/'src',gd/'src')
print('built',[p[0] for p in PAGES])
