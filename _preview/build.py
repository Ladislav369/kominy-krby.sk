# -*- coding: utf-8 -*-
"""
Generátor okresných lokálnych podstránok pre kominy-krby.sk.
Výstup: _preview/kominar/<slug>/index.html  +  _preview/kominar/index.html (rozcestník)
        + _preview/sitemap.xml
Drží dizajn pôvodného index.html (rovnaké CSS premenné, header, footer).
Každá stránka UNIKÁTNA: rotujúce intro/služby/FAQ podľa hash(slug) + regiónu.
"""
import os, html, hashlib, shutil
from cities import CITIES, REGIONS

SRC = os.path.expanduser("~/Documents/AresLab/aresLab-tools/ecokom/kominy-krby.sk")
OUT = os.path.join(SRC, "_preview")
BASE = "https://kominy-krby.sk"

def esc(s): return html.escape(s, quote=True)

def h(slug, n):
    """deterministický index 0..n-1 z slugu (+soľ pre rôzne bloky)."""
    return int(hashlib.md5(slug.encode("utf-8")).hexdigest(), 16) % n

def hs(slug, salt, n):
    return int(hashlib.md5((slug+salt).encode("utf-8")).hexdigest(), 16) % n

# ---------- ROTUJÚCE TEXTOVÉ BLOKY (unikátnosť) ----------
INTRO = [
    "Hľadáte spoľahlivého kominára v meste {mesto}? Postavíme nový komín, vyvložkujeme starý murovaný prieduch, vyfrézujeme zanesený komín alebo namontujeme krb — odborne, v súlade s STN a so zárukou na materiál aj prácu.",
    "Komín v {lokativ} potrebuje revíziu, čistenie alebo opravu? Zabezpečíme kompletné kominárske služby — od montáže nerezových a keramických komínov cez vložkovanie až po krby a pravidelné revízie podľa platnej legislatívy.",
    "Pôsobíme ako kominári v {lokativ} a okolí. Riešime montáž komínov, sanáciu starých prieduchov vložkovaním, frézovanie dechtu a sadze, montáž krbov aj východiskové a pravidelné revízie s vystavením revíznej správy.",
    "Potrebujete v {lokativ} odborníka na komíny a krby? Sme kominárska firma s 15+ rokmi praxe — staviame, vložkujeme, čistíme a revidujeme komíny a navrhujeme krby, ktoré kúria efektívne a vydržia desaťročia.",
]
LOCAL_CTX = [
    "Mesto {mesto} ({kraj}) má svoje špecifiká — {region}. Tomu prispôsobujeme návrh prierezu komína aj voľbu materiálu.",
    "V {lokativ} a okolitých obciach ({kraj}) sa stretávame najmä s touto situáciou: {region}. Pri obhliadke s tým vždy počítame.",
    "Pri zákazkách v {lokativ} berieme do úvahy miestne podmienky: {region}. Práve preto navrhujeme riešenie na mieru, nie šablónovito.",
]
CITY_NOTE_TPL = "Konkrétne v {lokativ} ide často o {note}."

SERVICES_ALL = [
    ("i-chimney","Montáž komínov v {lokativ}","Trojvrstvové nerezové, keramické a šamotové komíny. Návrh prierezu podľa spotrebiča a paliva, statika, prestup strechou a oplechovanie."),
    ("i-lining","Vložkovanie komínov","Sanácia starých murovaných komínov nerezovou vložkou bez búrania. Riešime kondenzát, decht aj praskanie prieduchu."),
    ("i-brush","Čistenie a frézovanie komína","Mechanické čistenie sadze a dechtu, frézovanie zaneseného prierezu, odstránenie hniezd a prekážok."),
    ("i-clipboard","Revízie a kontroly","Východisková revízia po montáži aj pravidelná kontrola podľa vyhlášky MV SR č. 401/2007. Vystavíme revíznu správu pre poisťovňu."),
    ("i-fireplace","Montáž krbov a krbových vložiek","Teplovzdušné a teplovodné krby, akumulačné krby a kachľové pece. Pripojenie na komín, obstavba a dizajn na mieru."),
    ("i-wrench","Servis a poradenstvo","Diagnostika slabého ťahu, oprava netesností, výmena tesnení a sklíčok aj poradenstvo pri kúpe spotrebiča."),
]

FAQ_POOL = [
    ("Koľko stojí vyvložkovanie komína v {lokativ}?",
     "Cena závisí od priemeru vložky, výšky komína, materiálu (nerez, šamot) a prístupu. Orientačne 60 až 130 € za bežný meter vrátane montáže. Presnú cenu pre vašu adresu v {lokativ} uvedieme v písomnej ponuke po bezplatnej obhliadke."),
    ("Ako často treba robiť revíziu komína?",
     "Intervaly upravuje vyhláška MV SR č. 401/2007. Pre spotrebič na pevné palivo do 50 kW je kontrola raz za 4 mesiace pri celoročnej a raz za 6 mesiacov pri sezónnej prevádzke. Pre plyn platia dlhšie intervaly."),
    ("Prídete aj do okrajových obcí pri meste {mesto}?",
     "Áno. Pôsobíme v {lokativ} aj v okolitých obciach v rámci okresu a susedných okresov. Dopravu kalkulujeme vopred a transparentne v cenovej ponuke."),
    ("Dá sa starý komín zachrániť bez búrania?",
     "Vo väčšine prípadov áno — vložkovaním nerezovou alebo keramickou vložkou. Je to rýchlejšie a lacnejšie ako stavba nového komína. Pri obhliadke v {lokativ} posúdime stav prieduchu a odporučíme najvhodnejšie riešenie."),
    ("Vystavíte revíznu správu potrebnú pre poisťovňu?",
     "Áno. Po každej montáži a revízii vystavujeme revíznu správu. Bez nej môže poisťovňa pri škode z komína plnenie krátiť alebo zamietnuť."),
    ("Ako dlho trvá montáž komína alebo krbu?",
     "Montáž alebo vložkovanie komína zvládneme zvyčajne za 1–3 dni. Montáž krbovej vložky a pripojenie na komín trvá 1 deň, obstavba ďalších 3–7 dní podľa zložitosti."),
    ("Aký krb je vhodný pre dom v {lokativ}?",
     "Pre rodinný dom s ústredným kúrením zvyčajne odporúčame teplovodný krb s akumulačnou nádržou — vykuruje celý dom aj ohrieva vodu. Pre vykúrenie jednej miestnosti postačí teplovzdušný krb. Konkrétne riešenie navrhneme podľa dispozície domu."),
    ("Čo spôsobuje slabý ťah komína?",
     "Najčastejšie zanesený prierez sadzou a dechtom, nevhodná výška alebo priemer komína, zatekanie či netesnosti. Diagnostiku urobíme priamo na mieste v {lokativ} a navrhneme opravu — čistenie, frézovanie alebo úpravu komína."),
]

IMG_POOL = [
    ("montaz-nerezoveho-komina-rodinny-dom.jpg","Montáž nerezového komína na rodinnom dome"),
    ("nerezovy-komin-na-keramickej-streche.jpg","Nerezový komín na keramickej streche"),
    ("poskodeny-murovany-komin-pred-vlozkovanim.jpg","Murovaný komín pred vložkovaním"),
    ("vyfrezovany-komin-pohlad-zhora.jpg","Vyfrézovaný komín — pohľad zhora"),
    ("moderna-krbova-pec-v-obyvacke.jpg","Moderná krbová pec v obývačke"),
    ("krbova-vlozka-s-keramickymi-kachlickami.jpg","Krbová vložka s keramickými kachličkami"),
    ("obhliadka-komina-na-streche.jpg","Obhliadka komína na streche"),
    ("nerezovy-komin-na-fasade-poschodoveho-domu.jpg","Komín na fasáde poschodového domu"),
]

# ---------- ZDIEĽANÉ CSS (z originálu, zjednodušené pre podstránku) ----------
CSS = """:root{--c-bg:#fffaf3;--c-fg:#1c1410;--c-muted:#5a4a40;--c-accent:#7a2e0c;--c-accent-2:#b8541f;--c-line:#e8dccd;--c-card:#fff;--r:10px;--maxw:1080px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--c-fg);background:var(--c-bg);line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:var(--c-accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 1.25rem}
header{border-bottom:1px solid var(--c-line);background:#fff}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:1rem 0;flex-wrap:wrap;gap:.75rem}
.brand{font-weight:800;font-size:1.15rem;letter-spacing:-.01em;color:var(--c-fg)}.brand span{color:var(--c-accent)}
nav ul{display:flex;gap:1.25rem;list-style:none;margin:0;padding:0;flex-wrap:wrap}
nav a{color:var(--c-fg);font-weight:500;font-size:.95rem}nav a:hover{color:var(--c-accent)}
.cta-btn{display:inline-block;background:var(--c-accent);color:#fff;padding:.7rem 1.1rem;border-radius:var(--r);font-weight:600;font-size:.95rem;line-height:1}
.cta-btn:hover{background:var(--c-accent-2);text-decoration:none}
.crumbs{font-size:.85rem;color:var(--c-muted);padding:.9rem 0 0}.crumbs a{color:var(--c-muted)}.crumbs a:hover{color:var(--c-accent)}
.hero{padding:2.5rem 0 2rem;background:linear-gradient(180deg,#fff 0,var(--c-bg) 100%)}
.hero h1{font-size:clamp(1.6rem,4vw,2.4rem);margin:.4rem 0 1rem;line-height:1.15;letter-spacing:-.02em}
.hero .lead{font-size:clamp(1.02rem,1.8vw,1.15rem);color:var(--c-muted);max-width:44em;margin:0 0 1.3rem}
.hero .cta-row{display:flex;gap:.75rem;flex-wrap:wrap;align-items:center}
.hero .meta{margin-top:1.5rem;display:flex;gap:1.4rem;flex-wrap:wrap;color:var(--c-muted);font-size:.9rem}.hero .meta b{color:var(--c-fg)}
section{padding:2.5rem 0;border-top:1px solid var(--c-line)}
section h2{font-size:clamp(1.3rem,2.5vw,1.7rem);margin:0 0 .35rem;letter-spacing:-.01em}
section .sub{color:var(--c-muted);margin:0 0 1.6rem;max-width:44em}
.prose p{color:var(--c-muted);max-width:44em}
.grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.card{background:var(--c-card);border:1px solid var(--c-line);border-radius:var(--r);padding:1.25rem}
.card h3{margin:0 0 .4rem;font-size:1.05rem}.card p{margin:0;color:var(--c-muted);font-size:.95rem}
.card-icon{width:2rem;height:2rem;color:var(--c-accent);display:block;margin:0 0 .75rem}
details{background:#fff;border:1px solid var(--c-line);border-radius:var(--r);padding:.85rem 1.1rem;margin:.5rem 0}
details summary{font-weight:600;cursor:pointer;list-style:none}
details summary::after{content:"+";float:right;font-size:1.2rem;color:var(--c-accent);font-weight:400}
details[open] summary::after{content:"−"}details p{color:var(--c-muted);margin:.6rem 0 0}
.gallery{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.gallery figure{margin:0;background:#fff;border:1px solid var(--c-line);border-radius:var(--r);overflow:hidden}
.gallery img{width:100%;height:200px;object-fit:cover;display:block;background:#eee}
.gallery figcaption{padding:.55rem .8rem;font-size:.86rem;color:var(--c-muted)}
.nearby{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.4rem}
.nearby a{display:inline-block;background:#fff;border:1px solid var(--c-line);border-radius:99px;padding:.4rem .9rem;font-size:.9rem;font-weight:500}
.nearby a:hover{border-color:var(--c-accent);text-decoration:none}
.ccards{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin:0 0 1rem}
.ccard{background:var(--c-card);border:1px solid var(--c-line);border-left:3px solid var(--c-accent);border-radius:var(--r);padding:1.1rem 1.2rem}
.ccard h3{margin:0 0 .5rem;font-size:1rem}.ccard a{font-weight:600}.ccard .lbl{color:var(--c-muted);font-size:.84rem;text-transform:uppercase;letter-spacing:.04em;display:block}
footer{background:#1c1410;color:#d8c8b8;padding:2rem 0;margin-top:1rem;font-size:.9rem}
footer a{color:#fff}.footer-sister{display:flex;gap:.6rem;flex-wrap:wrap;padding:0 0 1rem;border-bottom:1px solid #2a1f18;margin-bottom:1rem}
.footer-sister .lbl{color:#a89684;font-weight:600}.footer-sister .sep{color:#5a4a40}
.frow{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.75rem}
.skip{position:absolute;left:-9999px}.skip:focus{position:static;display:inline-block;background:var(--c-accent);color:#fff;padding:.5rem 1rem}
.citylist{display:grid;gap:.4rem .9rem;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));margin:1rem 0 0;padding:0;list-style:none}
.citylist a{display:block;padding:.35rem 0}
.kraj-h{margin:1.6rem 0 .3rem;font-size:1.05rem;color:var(--c-accent)}"""

ICONS_SVG = """<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false"><defs>
<symbol id="i-chimney" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 21V9h10v12"/><path d="M5 9h14V6H5z"/><path d="M9 4c.5-.6.5-1.4 0-2"/><path d="M12 4c.5-.6.5-1.4 0-2"/><path d="M15 4c.5-.6.5-1.4 0-2"/></symbol>
<symbol id="i-lining" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="15"/><rect x="7" y="10" width="10" height="11"/><path d="M12 2v6"/><path d="m9 4 3-2 3 2"/></symbol>
<symbol id="i-clipboard" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></symbol>
<symbol id="i-brush" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m13 13 7 7"/><circle cx="8" cy="8" r="4.5"/><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2"/></symbol>
<symbol id="i-fireplace" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21V8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v13"/><path d="M8 21V12h8v9"/><path d="M12 19c-1.4-.5-2.3-1.9-1.9-3.3.3-1 1-1.6 1.4-2.2.4.6.5 1.1.5 1.7.6-.4 1-.9 1-1.7 1 1 1.5 2 1.5 3 0 1.4-1.1 2.5-2.5 2.5z" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-wrench" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></symbol>
<symbol id="i-youtube" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z" fill="currentColor"/></symbol>
<symbol id="i-facebook" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></symbol>
</defs></svg>"""

HEADER = """<a href="#main" class="skip">Preskočiť na obsah</a>
<header><div class="wrap topbar">
<a class="brand" href="/" aria-label="Kominy-Krby.sk — domov">Kominy<span>-</span>Krby<span>.sk</span></a>
<nav aria-label="Hlavná navigácia"><ul>
<li><a href="/#sluzby">Služby</a></li>
<li><a href="/kominar/">Mestá</a></li>
<li><a href="/#realizacie">Realizácie</a></li>
<li><a href="/#faq">FAQ</a></li>
<li><a href="/#kontakt">Kontakt</a></li>
</ul></nav>
<a class="cta-btn" href="#kontakt">Cenová ponuka</a>
</div></header>"""

def footer():
    return """<footer><div class="wrap">
<div class="footer-sister" aria-label="Sesterské weby">
<span class="lbl">Sesterské weby:</span>
<a href="https://www.kominy-frezovanie.sk" rel="noopener">Frézovanie komínov</a>
<span class="sep" aria-hidden="true">·</span>
<a href="http://eshop.toup.sk" rel="noopener">E-shop TOUP</a></div>
<div class="frow">
<div>© <span id="y">2026</span> Kominy-Krby.sk — komíny a krby na celom Slovensku · <a href="/kominar/">Mestá a okresy</a></div>
<div class="footer-social">
<a href="https://www.youtube.com/@ToupSk" rel="noopener" aria-label="YouTube"><svg style="width:1.4rem;height:1.4rem;color:#d8c8b8" aria-hidden="true"><use href="#i-youtube"/></svg></a>
<a href="https://www.facebook.com/TOUP.sk" rel="noopener" aria-label="Facebook"><svg style="width:1.4rem;height:1.4rem;color:#d8c8b8" aria-hidden="true"><use href="#i-facebook"/></svg></a>
<a href="#main">Hore ↑</a></div></div></div></footer>
<script>document.getElementById('y').textContent=new Date().getFullYear()</script>"""

CONTACT = """<section id="kontakt" aria-labelledby="kontakt-h2"><div class="wrap">
<h2 id="kontakt-h2">Kontakt — {mesto}</h2>
<p class="sub">Napíšte alebo zavolajte. Odpovedáme zvyčajne v ten istý pracovný deň. Obhliadka a cenová ponuka sú nezáväzné.</p>
<div class="ccards">
<div class="ccard"><h3>Oprava a montáž komínov</h3>
<span class="lbl">Telefón</span><a href="tel:+421902223355">0902 22 33 55</a><br><br>
<span class="lbl">E-mail</span><a href="mailto:info@toup.sk">info@toup.sk</a></div>
<div class="ccard"><h3>Revízie, čistenie a kontrola</h3>
<span class="lbl">Telefón</span><a href="tel:+421911896989">0911 896 989</a><br><br>
<span class="lbl">E-mail</span><a href="mailto:kominarstvo@toup.sk">kominarstvo@toup.sk</a></div>
</div>
<p class="prose"><a class="cta-btn" href="mailto:info@toup.sk?subject=Cenova%20ponuka%20{mesto_url}">Napísať e-mail</a></p>
</div></section>"""

def page(c, by_slug):
    mesto, lok, kraj = c["mesto"], c["lokativ"], c["kraj"]
    region_txt = REGIONS[c["region"]]
    title = f"Kominár {mesto} — komíny, vložkovanie, revízie a krby | Kominy-Krby.sk"
    desc = (f"Kominárske služby v {lok}: montáž a vložkovanie komínov, čistenie a frézovanie, "
            f"revízie podľa vyhlášky 401/2007 a montáž krbov. 15+ rokov praxe, záruka. "
            f"Cenová ponuka zdarma.")
    url = f"{BASE}/kominar/{c['slug']}/"
    intro = INTRO[h(c["slug"],len(INTRO))].format(mesto=esc(mesto), lokativ=esc(lok))
    ctx = LOCAL_CTX[hs(c["slug"],"ctx",len(LOCAL_CTX))].format(
        mesto=esc(mesto), lokativ=esc(lok), kraj=esc(kraj), region=esc(region_txt))
    citynote = CITY_NOTE_TPL.format(lokativ=esc(lok), note=esc(c["note"]))

    # služby — rotujúce poradie (všetkých 6, ale poradie sa líši)
    off = h(c["slug"],len(SERVICES_ALL))
    svc = SERVICES_ALL[off:]+SERVICES_ALL[:off]
    svc_html = "".join(
        f'<article class="card"><svg class="card-icon" aria-hidden="true"><use href="#{i}"/></svg>'
        f'<h3>{esc(t.format(lokativ=lok))}</h3><p>{esc(d)}</p></article>'
        for (i,t,d) in svc)

    # FAQ — vyber 5 z poolu rotujúco
    fo = hs(c["slug"],"faq",len(FAQ_POOL))
    faq_sel = (FAQ_POOL[fo:]+FAQ_POOL[:fo])[:5]
    faq_html = "".join(
        f'<details><summary>{esc(q.format(mesto=mesto,lokativ=lok))}</summary>'
        f'<p>{esc(a.format(mesto=mesto,lokativ=lok))}</p></details>'
        for (q,a) in faq_sel)
    faq_schema = [{"@type":"Question","name":q.format(mesto=mesto,lokativ=lok),
                   "acceptedAnswer":{"@type":"Answer","text":a.format(mesto=mesto,lokativ=lok)}}
                  for (q,a) in faq_sel]

    # galéria — 3 obrázky rotujúco
    go = hs(c["slug"],"img",len(IMG_POOL))
    imgs = (IMG_POOL[go:]+IMG_POOL[:go])[:3]
    gal = "".join(
        f'<figure><img src="/img/{fn}" alt="{esc(alt)} — realizácia v okolí mesta {esc(mesto)}" '
        f'width="1200" height="1600" loading="lazy" decoding="async"><figcaption>{esc(alt)}</figcaption></figure>'
        for (fn,alt) in imgs)

    # susedné mestá
    nb = [by_slug[n] for n in c["neighbors"] if n in by_slug]
    nearby = "".join(f'<a href="/kominar/{n["slug"]}/">Kominár {esc(n["mesto"])}</a>' for n in nb)

    # schema.org graf
    import json
    graph = {
      "@context":"https://schema.org",
      "@graph":[
        {"@type":["LocalBusiness","HomeAndConstructionBusiness"],
         "@id":url+"#business",
         "name":f"Kominy-Krby.sk — kominár {mesto}",
         "url":url,
         "image":f"{BASE}/img/{imgs[0][0]}",
         "telephone":["+421902223355","+421911896989"],
         "email":"info@toup.sk",
         "priceRange":"€€",
         "areaServed":[{"@type":"City","name":mesto},{"@type":"AdministrativeArea","name":kraj}],
         "address":{"@type":"PostalAddress","streetAddress":"Liptovská Porúbka 321",
                    "postalCode":"033 01","addressLocality":"Liptovský Mikuláš","addressCountry":"SK"},
         "parentOrganization":{"@type":"Organization","name":"ECOKOM s.r.o.","url":BASE+"/"},
         "openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
            "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"17:00"}],
         "sameAs":["https://www.youtube.com/@ToupSk","https://www.facebook.com/TOUP.sk"]},
        {"@type":"Service","name":f"Kominárske služby {mesto}",
         "serviceType":"Montáž a vložkovanie komínov, čistenie, revízie a montáž krbov",
         "areaServed":{"@type":"City","name":mesto},
         "provider":{"@id":url+"#business"}},
        {"@type":"FAQPage","mainEntity":faq_schema},
        {"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Domov","item":BASE+"/"},
          {"@type":"ListItem","position":2,"name":"Kominár podľa mesta","item":BASE+"/kominar/"},
          {"@type":"ListItem","position":3,"name":mesto,"item":url}]}
      ]}
    schema = json.dumps(graph, ensure_ascii=False, indent=1)

    return f"""<!doctype html>
<html lang="sk"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#7a2e0c">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc('Kominár '+mesto+' — komíny, vložkovanie, revízie a krby')}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="sk_SK">
<meta property="og:image" content="{BASE}/img/{imgs[0][0]}">
<style>{CSS}</style>
</head><body>
{ICONS_SVG}
{HEADER}
<div class="wrap"><nav class="crumbs" aria-label="Omrvinková navigácia">
<a href="/">Domov</a> › <a href="/kominar/">Kominár podľa mesta</a> › <span>{esc(mesto)}</span>
</nav></div>
<main id="main">
<section class="hero" aria-labelledby="h1"><div class="wrap">
<h1 id="h1">Kominár {esc(mesto)} — komíny, vložkovanie, revízie a krby</h1>
<p class="lead">{intro}</p>
<div class="cta-row"><a class="cta-btn" href="#kontakt">Žiadosť o cenovú ponuku</a>
<a href="#sluzby-mesto">Pozrieť služby →</a></div>
<p class="meta"><span>✓ <b>{esc(kraj)}</b></span><span>✓ <b>15+ rokov</b> praxe</span>
<span>✓ <b>Záruka</b> na materiál aj prácu</span><span>✓ Revízie podľa <b>vyhl. 401/2007</b></span></p>
</div></section>

<section aria-labelledby="ctx-h"><div class="wrap prose">
<h2 id="ctx-h">Kominárske služby v {esc(lok)}</h2>
<p>{ctx} {citynote}</p>
<p>Sme kominárska firma ECOKOM (značka TOUP.sk) so sídlom v Liptovskom Mikuláši a pôsobíme po celom Slovensku vrátane okresu {esc(mesto)}. Špecializujeme sa na frézovanie a vložkovanie starých murovaných komínov bez búrania — to nerobí každý kominár. Okrem toho staviame nové nerezové a keramické komíny, čistíme a revidujeme prieduchy a montujeme krby a krbové vložky.</p>
</div></section>

<section id="sluzby-mesto" aria-labelledby="svc-h"><div class="wrap">
<h2 id="svc-h">Čo pre vás v {esc(lok)} zabezpečíme</h2>
<p class="sub">Komplexná starostlivosť o komín a krb — od návrhu cez montáž až po revíziu.</p>
<div class="grid">{svc_html}</div>
</div></section>

<section aria-labelledby="gal-h"><div class="wrap">
<h2 id="gal-h">Ukážky našich realizácií</h2>
<p class="sub">Skutočné práce — montáž komínov, vložkovanie, frézovanie a krby na rodinných domoch.</p>
<div class="gallery">{gal}</div>
</div></section>

<section aria-labelledby="faq-h"><div class="wrap">
<h2 id="faq-h">Časté otázky — komíny a krby {esc(mesto)}</h2>
<p class="sub">Najčastejšie otázky zákazníkov v {esc(lok)} a okolí.</p>
{faq_html}
</div></section>

<section aria-labelledby="nb-h"><div class="wrap">
<h2 id="nb-h">Kominár v okolitých mestách</h2>
<p class="sub">Pôsobíme aj v susedných okresoch. Vyberte si svoje mesto:</p>
<div class="nearby">{nearby}<a href="/kominar/">Všetky mestá →</a></div>
</div></section>

{CONTACT.format(mesto=esc(mesto), mesto_url=esc(mesto.replace(' ','%20')))}
</main>
{footer()}
<script type="application/ld+json">
{schema}
</script>
</body></html>"""

# ---------- ROZCESTNÍK ----------
def hub(cities):
    by_kraj = {}
    for c in sorted(cities, key=lambda x:x["mesto"]):
        by_kraj.setdefault(c["kraj"],[]).append(c)
    kraj_order = ["Bratislavský kraj","Trnavský kraj","Trenčiansky kraj","Nitriansky kraj",
                  "Žilinský kraj","Banskobystrický kraj","Prešovský kraj","Košický kraj"]
    blocks=""
    for k in kraj_order:
        if k not in by_kraj: continue
        items="".join(f'<li><a href="/kominar/{c["slug"]}/">Kominár {esc(c["mesto"])}</a></li>' for c in by_kraj[k])
        blocks+=f'<h2 class="kraj-h">{esc(k)}</h2><ul class="citylist">{items}</ul>'
    url=f"{BASE}/kominar/"
    desc="Kominárske služby v mestách a okresoch po celom Slovensku — montáž a vložkovanie komínov, čistenie, frézovanie, revízie a krby. Vyberte si svoje mesto."
    schema = {
      "@context":"https://schema.org",
      "@graph":[
        {"@type":"CollectionPage","@id":url,"url":url,"name":"Kominár podľa mesta a okresu",
         "isPartOf":{"@type":"WebSite","url":BASE+"/"}},
        {"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Domov","item":BASE+"/"},
          {"@type":"ListItem","position":2,"name":"Kominár podľa mesta","item":url}]}
      ]}
    import json
    return f"""<!doctype html>
<html lang="sk"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kominár podľa mesta a okresu — komíny a krby na celom Slovensku | Kominy-Krby.sk</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#7a2e0c">
<style>{CSS}</style></head><body>
{ICONS_SVG}
{HEADER}
<div class="wrap"><nav class="crumbs" aria-label="Omrvinková navigácia">
<a href="/">Domov</a> › <span>Kominár podľa mesta</span></nav></div>
<main id="main">
<section class="hero"><div class="wrap">
<h1>Kominár podľa mesta a okresu</h1>
<p class="lead">Pôsobíme po celom Slovensku. Vyberte si svoje okresné mesto a pozrite si konkrétne kominárske služby — montáž a vložkovanie komínov, čistenie a frézovanie, revízie podľa vyhlášky 401/2007 a montáž krbov.</p>
<div class="cta-row"><a class="cta-btn" href="/#kontakt">Cenová ponuka zdarma</a></div>
</div></section>
<section><div class="wrap">
<h2 class="kraj-h" style="margin-top:0">Vyberte mesto ({len(cities)} okresných miest)</h2>
{blocks}
</div></section>
</main>
{footer()}
<script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=1)}
</script>
</body></html>"""

def main():
    by_slug={c["slug"]:c for c in CITIES}
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT,"kominar"), exist_ok=True)
    # symlink img/favicon do preview pre lokálne overenie
    for asset in ["img","favicon.svg","favicon-32.png","apple-touch-icon.png","favicon-192.png","js"]:
        src=os.path.join(SRC,asset); dst=os.path.join(OUT,asset)
        if os.path.exists(src) and not os.path.exists(dst):
            try: os.symlink(src,dst)
            except OSError: pass
    n=0
    for c in CITIES:
        d=os.path.join(OUT,"kominar",c["slug"]); os.makedirs(d,exist_ok=True)
        with open(os.path.join(d,"index.html"),"w",encoding="utf-8") as f:
            f.write(page(c,by_slug))
        n+=1
    with open(os.path.join(OUT,"kominar","index.html"),"w",encoding="utf-8") as f:
        f.write(hub(CITIES))
    # sitemap len pre nové stránky (preview)
    urls=[f"{BASE}/kominar/"]+[f"{BASE}/kominar/{c['slug']}/" for c in CITIES]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm+=f'  <url><loc>{BASE}/</loc><priority>1.0</priority></url>\n'
    sm+=f'  <url><loc>{BASE}/kominar/</loc><priority>0.8</priority></url>\n'
    for c in CITIES:
        sm+=f'  <url><loc>{BASE}/kominar/{c["slug"]}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    sm+='</urlset>\n'
    with open(os.path.join(OUT,"sitemap-kominar.xml"),"w",encoding="utf-8") as f:
        f.write(sm)
    print(f"Vygenerovaných {n} mestských stránok + 1 rozcestník + sitemap-kominar.xml")
    print(f"Výstup: {OUT}")

if __name__=="__main__":
    main()
