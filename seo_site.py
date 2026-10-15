"""TrialTally SEO build (hand-authored HTML, edited in place, idempotent).
INDEXABLE gates robots meta and sitemap for the whole site. Run: python3 seo_site.py"""
import os, re, shutil, sys, copy
from bs4 import BeautifulSoup
INDEXABLE = True
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT); import seo
LOGOS = "/workspace/atulit-logos/trialtally"

def hook(ctx):
    p, s, paths, soups = ctx["path"], ctx["soup"], ctx["paths"], ctx["soups"]
    seg = p.strip("/").split("/") if p else []
    h1 = ctx["h1"]
    if p == "": return dict(titles=["Free Trials and Deals, Checked by Hand", "Free Trials and Deals, Checked"])
    if seg[0] == "trials" and len(seg) == 2:
        k = seg[1]
        name = re.split(r" Free Trial", h1)[0]
        t = f"{name} Free Trial: Length, Cost After & How to Cancel"
        # price after trial row
        tbl = s.find("table", class_="facts")
        if tbl and not tbl.find("th", string="Price after trial"):
            for th in tbl.find_all("th"):
                if th.get_text() == "Auto-renews": th.string = "Price after trial"
        # cancel steps pulled from the cancel guide
        for old in s.find_all(attrs={"data-seo": "cancel"}): old.decompose()
        cs = soups.get(f"cancel/{k}/")
        if cs:
            parts = []
            for h2 in cs.find("main").find_all("h2"):
                ol = h2.find_next_sibling("ol")
                if ol: parts.append(f"<h3>{h2.get_text()}</h3>{ol}")
            if parts:
                sec = BeautifulSoup(f'<section data-seo="cancel"><h2>How to cancel {name}</h2>{"".join(parts)}<p><a href="../../cancel/{k}/">Full {name} cancel guide</a></p></section>', "html.parser")
                anchor = s.find(class_="ctabox") or tbl or s.find(class_="phero")
                anchor.insert_after(sec)
        rel = [q for q in [f"cancel/{k}/", f"student-discounts/{k}/", f"deals/{k}/"] if q in paths] + [q for q in paths if q.startswith("trials/") and q != p]
        return dict(h1=t, titles=[t, f"{name} Free Trial: Length, Cost & How to Cancel", f"{name} Free Trial: Length, Cost After, Cancel", f"{name} Free Trial: Length & How to Cancel"], related=rel[:8])
    if seg[0] in ("cancel", "student-discounts", "deals") and len(seg) == 2:
        k = seg[1]
        rel = [f"trials/{k}/"] + [f"{x}/{k}/" for x in ("cancel", "student-discounts", "deals") if x != seg[0]] + [q for q in paths if q.startswith(seg[0] + "/") and q != p]
        return dict(titles=[h1, re.sub(r" \(.*\)", "", h1)], related=rel[:8])
    if seg[0] == "newsletter":   # lead / signup page
        if not s.find("h1"): s.find("h2").name = "h1"
        return dict(index=False, canonical="", titles=["Free Trial Ending Alerts Newsletter"])
    return dict(titles=[h1])

def guides():
    names = {}
    for k in sorted(os.listdir(f"{ROOT}/cancel")):
        h = BeautifulSoup(open(f"{ROOT}/trials/{k}/index.html").read(), "html.parser").find("h1").get_text()
        names[k] = re.split(r" Free Trial", h)[0]
    li = lambda pre, lab: "".join(f'<li><a href="../{pre}/{k}/">{lab.format(n=n)}</a></li>' for k, n in names.items())
    return {"guides/": ("Guides", f'<h1>Free Trial Guides: Cancel, Students and Deals</h1><p>Step by step guides for every service we track, from canceling before you are charged to finding student pricing. Updated Oct 13, 2026.</p><h2>How to cancel</h2><ul>{li("cancel", "How to cancel {n}")}</ul><h2>Free trials</h2><ul>{li("trials", "{n} free trial")}</ul><p><a href="../how-we-verify/">How we verify</a></p>')}

def build():
    for a, b in [("option-b-icon.svg", "favicon.svg")]:
        shutil.copy(f"{LOGOS}/{a}", f"{ROOT}/img/brand/{b}")
    shutil.copy(f"{ROOT}/img/brand/option-b-icon-32.png", f"{ROOT}/img/brand/favicon-32.png")
    shutil.copy(f"{ROOT}/img/brand/option-b-icon-180.png", f"{ROOT}/img/brand/apple-touch-icon.png")
    site = seo.Site(ROOT, "TrialTally", "trialtally.com", "deals-tracker-prototype", INDEXABLE, "Oct 13, 2026", "2026-10-13",
        "Free trials and deals, checked by humans. Funded by affiliate links.",
        f"{LOGOS}/option-b-wordmark-1200.png", "img/brand/option-b-icon-512.png",
        ["Last checked Oct 13, 2026.", "From official pages.", "From TrialTally.", "Source linked.", "US prices.", "Not affiliated.", "Checked Oct 13, 2026."], hook, extra_pages=guides())
    return seo.run(site)
if __name__ == "__main__": build()
