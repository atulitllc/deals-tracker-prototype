"""Builds TrialTally pages from trials_data.py (real data), then runs seo_site.py. Run: python3 build_trials.py"""
import os,json,html,shutil
from trials_data import T,CHECKED,CATS
from atulit_gfx import icon,flogo,hero,THEME_HEAD,toggle,CREDIT,install_css
CATICON={"streaming":"tv","music":"music","productivity":"briefcase","shopping":"shopping-bag"}
CATCOL={"streaming":"#FF5A36","music":"#8b5cf6","productivity":"#0ea5e9","shopping":"#10b981"}
E=html.escape; SITE="https://trialtally.com/"
def page(path,title,desc,crumbs,body):
    r="../"*path.count("/")
    nav="".join(f'<a href="{r}category/{k}/">{icon(CATICON[k],16)}{v.split(" ")[0]}</a>' for k,v in CATS.items())
    bl={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate([("Home","")]+crumbs)]}
    org={"@context":"https://schema.org","@type":"Organization","name":"TrialTally by Atulit","url":SITE,"logo":SITE+"img/brand/option-b-icon-512.png"}
    cr=" <span>/</span> ".join([f'<a href="{r}">Home</a>']+[f'<a href="{r}{u}">{E(n)}</a>' for n,u in crumbs[:-1]]+[f'<span aria-current="page">{E(crumbs[-1][0])}</span>']) if crumbs else '<span aria-current="page">Home</span>'
    o=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex, nofollow">{THEME_HEAD}<link rel="canonical" href="{SITE}{path}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="{r}img/brand/option-b-icon.svg" type="image/svg+xml"><link rel="stylesheet" href="{r}assets/style.css?v=20261013logos">
<script type="application/ld+json">{json.dumps(org)}</script><script type="application/ld+json">{json.dumps(bl)}</script>
</head><body>
<div class="sample">Prototype · Real trial facts from official pages, checked {CHECKED} · Not indexed</div>
<header class="top"><div class="wrap nav"><a class="brand" href="{r}"><img src="{r}img/brand/option-b-wordmark.svg" alt="TrialTally" height="34"></a>
<nav>{nav}<a href="{r}trials/">{icon("list-checks",16)}All trials</a></nav>{toggle()}</div></header>
<main class="wrap"><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>
{body}
<p class="checked">Last checked {CHECKED} · <a href="{r}how-we-verify/">How we verify</a></p></main>
<footer class="foot"><div class="wrap fgrid"><div><a class="brand" href="{r}"><img src="{r}img/brand/option-b-wordmark.svg" alt="TrialTally" height="34"></a><p>Free trial facts taken from official service pages, with a source link on every page.</p></div>
<div><a href="{r}about/">About</a><a href="{r}how-we-verify/">How we verify</a><a href="{r}disclosure/">Affiliate disclosure</a></div>
<div>{"".join(f'<a href="{r}category/{k}/">{v}</a>' for k,v in CATS.items())}</div></div>
<p class="wrap fine">© 2026 Atulit LLC · Not affiliated with any service listed. Prices are US prices as shown on official pages and can change.</p><p class="wrap fine">{CREDIT}</p></footer>
<script src="{r}assets/app.js"></script></body></html>'''
    os.makedirs(path or ".",exist_ok=True); open((path or "")+"index.html","w").write(o)
mono=lambda t,big=False:f'<span class="mono{" big" if big else ""}" style="--c:{t["color"]}" aria-hidden="true">{E(t["name"][:2])}</span>'
def table(ts,r):
    rows="".join(f'<tr><td><a class="svc" href="{r}trials/{t["slug"]}/">{flogo(t["url"],t["name"],28)}<b>{E(t["name"])}</b></a></td><td><span class="gchip">{icon("clock",16,"ic ok")}{E(t["trial"])}</span></td><td><span class="gchip">{icon("tag",16,"ic pr")}{E(t["after"] or "Not shown")}</span></td><td><a class="gchip" href="{t["url"]}" rel="nofollow">{icon("badge-check",16,"ic ok")}Source</a></td></tr>' for t in ts)
    return f'<div style="overflow-x:auto"><table class="facts"><thead><tr><th>Service</th><th>Free trial</th><th>Price after</th><th>Official page</th></tr></thead><tbody>{rows}</tbody></table></div>'
def steps(c): return "".join(f'<h3>{E(h)}</h3><ol>'+"".join(f"<li>{E(x)}</li>" for x in l)+"</ol>" for h,l in c[1])
for d in ("trials","cancel","deals","student-discounts","ending-soon","no-credit-card","category"):
    shutil.rmtree(d,ignore_errors=True)
for t in T:
    r="../../"; c=t.get("cancel")
    canc=(f'<section><h2>How to cancel {E(t["name"])}</h2>{steps(c)}'+(f'<p>{E(t["cnote"])}</p>' if t.get("cnote") else "")+f'<p class="disc">Source: <a href="{c[0]}" rel="nofollow">official cancel instructions</a>, checked {CHECKED}. <a href="{r}cancel/{t["slug"]}/">Full cancel guide</a></p></section>') if c else f'<section><h2>How to cancel</h2><p>We have not verified cancel steps for {E(t["name"])} yet. Use the official help center for {E(t["name"])}.</p></section>'
    alts="".join(f'<a class="alt" href="{r}trials/{a["slug"]}/">{mono(a)}<span>{E(a["name"])}<small>{E(a["trial"][:40])}</small></span></a>' for a in T if a["cat"]==t["cat"] and a is not t)
    body=f'''<section class="phero" style="--c:{t["color"]}"><span class="mono big lg">{flogo(t["url"],t["name"],56,False)}</span><div><span class="kick">Free trial · {CATS[t["cat"]]}</span><h1>{E(t["name"])} Free Trial</h1><p class="lede">{E(t["trial"])}.</p></div></section><div class="layout"><div><table class="facts"><caption>Trial facts</caption><tr><th>Free trial</th><td>{E(t["trial"])}</td></tr><tr><th>Price after trial</th><td>{E(t["after"] or "Not shown on the page we checked")}</td></tr>{f'<tr><th>Notes</th><td>{E(t["extra"])}</td></tr>' if t.get("extra") else ""}<tr><th>Official page</th><td><a href="{t["url"]}" rel="nofollow">{E(t["url"].split("//")[1].rstrip("/"))}</a></td></tr><tr><th>Last checked</th><td>{CHECKED}</td></tr></table>
<div class="ctabox"><a class="btn" href="{t["url"]}" rel="nofollow" target="_blank">See the offer at {E(t["name"])}</a><p class="disc">Plain link to the official page. No affiliate link. Offers vary by region and account history.</p></div>
{canc}
<section><h2>Alternatives</h2><div class="alts">{alts}</div></section></div></div>'''
    page(f'trials/{t["slug"]}/',f'{t["name"]} Free Trial: Length, Price After, How to Cancel',f'{t["name"]}: {t["trial"]}. Price after: {t["after"] or "not shown"}. Checked {CHECKED}.',[(CATS[t["cat"]],f'category/{t["cat"]}/'),(t["name"],f'trials/{t["slug"]}/')],body)
    if c:
        page(f'cancel/{t["slug"]}/',f'How to Cancel {t["name"]}',f'Steps to cancel {t["name"]} from the official help page. Checked {CHECKED}.',[(t["name"],f'trials/{t["slug"]}/'),("How to cancel",f'cancel/{t["slug"]}/')],
             f'<article class="prose"><h1>How to cancel {E(t["name"])}</h1>{steps(c)}'+(f'<p>{E(t["cnote"])}</p>' if t.get("cnote") else "")+f'<p>Source: <a href="{c[0]}" rel="nofollow">official instructions</a>, checked {CHECKED}.</p><p><a href="../../trials/{t["slug"]}/">{E(t["name"])} free trial facts</a></p></article>')
for k,v in CATS.items():
    ts=[t for t in T if t["cat"]==k]
    page(f"category/{k}/",f"{v} Free Trials",f"{v} free trials with real lengths and prices from official pages. Checked {CHECKED}.",[(v,f"category/{k}/")],f'<h1 class="secdeco" style="--c:{CATCOL[k]}"><span class="ibadge">{icon(CATICON[k],22)}</span>{v} free trials</h1><p class="lede">{len(ts)} services. Every row comes from the official page, checked {CHECKED}.</p>{table(ts,"../../")}')
page("trials/","All Free Trials",f"All {len(T)} free trials we track, from official pages. Checked {CHECKED}.",[("All free trials","trials/")],f'<h1>All free trials</h1><p class="lede">{len(T)} services. Every row comes from the official page, checked {CHECKED}. US prices.</p>{table(T,"../")}')
page("",f"Free Trials Checked Against Official Pages",f"Real free trial lengths, prices after the trial and cancel steps for {len(T)} services. Checked {CHECKED}.",[],
     f'<section class="hsplit"><div><span class="kick">{icon("calendar-check",16)} Last checked {CHECKED}</span><h1>Free trials, checked against the official page</h1><p class="lede">Trial length, price after the trial and cancel steps for {len(T)} popular services. Every fact links to its source.</p><ul class="ticks"><li>{icon("circle-check",18)}Trial length from the official page</li><li>{icon("tag",18)}Price after the trial</li><li>{icon("calendar-x",18)}Cancel steps with a source</li></ul></div><div>{hero("trialtally")}</div></section><div class="cattiles">'+"".join(f'<a class="cattile" href="category/{k}/" style="--c:{CATCOL[k]}"><span class="ibadge">{icon(CATICON[k],22)}</span><b>{v}</b><small>{sum(1 for t in T if t["cat"]==k)} services</small><span class="logos">{"".join([flogo(t["url"],t["name"],22) for t in T if t["cat"]==k][:5])}</span></a>' for k,v in CATS.items())+'</div>'+"".join(f'<h2 class="secdeco" style="--c:{CATCOL[k]}"><span class="ibadge soft">{icon(CATICON[k],20)}</span><a href="category/{k}/">{v}</a></h2>{table([t for t in T if t["cat"]==k],"")}' for k,v in CATS.items()))
for p,tl,txt in [("about/","About TrialTally","<p>TrialTally lists free trial lengths, the price after the trial and cancel steps, taken from each service's official pages. It is built by Atulit LLC.</p><p>Every fact links to its source and shows the date we checked it. If a page did not state something, we say so instead of guessing.</p>"),
 ("how-we-verify/","How We Verify",f"<p>We open each service's official US plans or signup page and record only what it states: trial length, price after the trial and any conditions. Cancel steps come from the service's official help page. Each entry shows a source link and the date checked ({CHECKED}).</p><p>Where the official page does not state something, we write Not shown. We do not publish ways to get around trial limits.</p><h2>Not done yet</h2><p>We have not yet verified card requirements, regions, or cancel steps for every service. Those fields are left out until verified.</p>"),
 ("disclosure/","Affiliate Disclosure","<p>Right now no links on TrialTally are affiliate links. If we add any later, they will be marked rel=\"sponsored\" and will never change which trials we list. There are no ads.</p>")]:
    page(p,tl,tl,[(tl,p)],f'<article class="prose"><h1>{tl}</h1>{txt}</article>')
import glob,re
EXTRA=""".hsplit{display:grid;grid-template-columns:1.1fr 1fr;gap:28px;align-items:center;padding:6px 0 26px}.hsplit h1{font-size:clamp(34px,4.8vw,58px);margin:8px 0}
.kick .ic{color:var(--coral)}.ticks{list-style:none;padding:0;margin:18px 0 0;display:grid;gap:8px}.ticks li{display:flex;gap:9px;align-items:center;font-weight:500}.ticks .ic{color:var(--coral)}
.cattiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:8px 0 10px}.cattile{display:flex;flex-direction:column;gap:6px;padding:18px;border:1px solid var(--line);border-radius:var(--r);background:var(--paper);text-decoration:none;transition:transform .15s,box-shadow .15s}.cattile:hover{transform:translateY(-2px);box-shadow:0 10px 24px -14px rgba(0,0,0,.35)}
.cattile b{font:700 18px "Bricolage Grotesque";margin-top:6px}.cattile small{color:var(--mut)}.cattile .logos{display:flex;gap:6px;margin-top:6px}
.facts .svc{display:flex;align-items:center;gap:10px;text-decoration:none}.facts .gchip .ic.ok{color:#16a34a}.facts .gchip .ic.pr{color:var(--coral)}
.mono.lg{background:#fff;border:1px solid var(--line)}
@media(max-width:900px){.hsplit{grid-template-columns:1fr}.hsplit .hero-gfx{max-width:360px}.cattiles{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.facts:has(thead) thead{display:none}.facts:has(thead) tr{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid var(--line)}.facts:has(thead) td{border:0;padding:8px 14px;font-size:14px}.facts:has(thead) td:first-child{grid-column:1/-1;padding-top:14px}.facts:has(thead) td:last-child{grid-column:1/-1;padding-bottom:14px}.facts:has(thead) tr:last-child{border:0}.cattile{padding:14px}.cattile .logos{display:none}}
html[data-theme=dark] .sample{background:#1a1e26;color:#c8f560}
"""
for f in glob.glob("**/index.html",recursive=True)+["404.html"]:
    h=open(f).read(); h2=h.replace("Prototype · Sample data, not real offers · Not indexed",f"Prototype · Real trial facts from official pages, checked {CHECKED} · Not indexed")
    if h2!=h: open(f,"w").write(h2)
install_css("assets/style.css",EXTRA)
import seo_site; seo_site.build()
