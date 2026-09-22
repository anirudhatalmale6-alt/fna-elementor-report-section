#!/usr/bin/env python3
"""Rebuilds the Futuro Nazionale Albignasego home-page mockup as a real,
editable, full-width Elementor page.

Native Elementor widgets only: container, heading, text-editor, button,
icon-box, image, spacer, html, shortcode. No Pro controls, no add-ons.
"""
import json, sys, hashlib

SITE = sys.argv[1] if len(sys.argv) > 1 else "https://futuronazionalealbignasego.it"
OUT  = sys.argv[2] if len(sys.argv) > 2 else "fna-home-page.json"
CF7  = sys.argv[3] if len(sys.argv) > 3 else ""      # optional CF7 form id

UP = SITE + "/wp-content/uploads/2026/09/"
IMG_HERO   = UP + "COVER-ok.png"
IMG_BAND   = UP + "cov-Villa_Obizzi_municipio_Albignasego.jpg"   # stand-in for the park shot

_n = [0]
def eid(tag=""):
    _n[0] += 1
    return hashlib.md5(f"fnah{tag}{_n[0]}".encode()).hexdigest()[:7]

# ------------------------------------------------------------------ palette
NAVY   = "#0A2472"   # headings on white
BLUE   = "#003E7F"   # bands, icon circles, labels
DEEP   = "#00295D"   # hero / form panel
YELLOW = "#FDE01A"
INK    = "#173A79"   # body copy (the mockup's body text is navy, not grey)
WHITE  = "#FFFFFF"
GREEN  = "#009246"
RED    = "#CE2B37"

SANS = "Roboto"      # already enqueued by his Elementor kit


def dim(t=0, r=0, b=0, l=0, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def typo(size=17, weight="400", lh=1.6, ls=None, transform=None, style=None,
         size_t=None, size_m=None, family=SANS):
    s = {"typography_typography": "custom",
         "typography_font_family": family,
         "typography_font_size": {"unit": "px", "size": size, "sizes": []},
         "typography_font_weight": weight,
         "typography_line_height": {"unit": "em", "size": lh, "sizes": []}}
    if size_t is not None:
        s["typography_font_size_tablet"] = {"unit": "px", "size": size_t, "sizes": []}
    if size_m is not None:
        s["typography_font_size_mobile"] = {"unit": "px", "size": size_m, "sizes": []}
    if ls is not None:
        s["typography_letter_spacing"] = {"unit": "px", "size": ls, "sizes": []}
    if transform:
        s["typography_text_transform"] = transform
    if style:
        s["typography_font_style"] = style
    return s


def widget(wtype, settings, classes=None):
    if classes:
        settings = dict(settings, _css_classes=classes)
    return {"id": eid(wtype), "elType": "widget", "widgetType": wtype,
            "settings": settings, "elements": [], "isInner": False}


def container(children, settings=None, classes=None, inner=True):
    s = dict(settings or {})
    s.setdefault("container_type", "flex")
    s.setdefault("content_width", "full")
    if classes:
        s["css_classes"] = classes
    return {"id": eid("con"), "elType": "container", "settings": s,
            "elements": children, "isInner": inner}


def band(children, bg=None, bg_img=None, padding=(72, 24, 72, 24),
         padding_m=(44, 18, 44, 18), classes=None, extra=None, boxed=1200):
    """A full-bleed strip whose inner content is boxed to `boxed` px."""
    inner = container(children, {
        "content_width": "boxed",
        "boxed_width": {"unit": "px", "size": boxed, "sizes": []},
        "flex_direction": "column",
        "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0", "isLinked": True},
        "padding": dim(0, 0, 0, 0),
    })
    s = {
        "content_width": "full",
        "flex_direction": "column",
        "padding": dim(*padding),
        "padding_mobile": dim(*padding_m),
        "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0", "isLinked": True},
    }
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    if bg_img:
        s.update({
            "background_background": "classic",
            "background_image": {"url": bg_img, "id": "", "source": "library"},
            "background_position": "center center",
            "background_repeat": "no-repeat",
            "background_size": "cover",
        })
    s.update(extra or {})
    return container([inner], s, classes)


def row(children, gap=32, gap_t=26, gap_m=20, settings=None, classes=None):
    s = {
        "flex_direction": "row",
        "flex_wrap_tablet": "wrap",
        "flex_align_items": "stretch",
        "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap), "isLinked": True},
        "flex_gap_tablet": {"unit": "px", "size": gap_t, "column": str(gap_t), "row": str(gap_t), "isLinked": True},
        "flex_gap_mobile": {"unit": "px", "size": gap_m, "column": str(gap_m), "row": str(gap_m), "isLinked": True},
        "flex_direction_mobile": "column",
        "padding": dim(0, 0, 0, 0),
    }
    s.update(settings or {})
    return container(children, s, classes)


def cell(children, w=50, w_t=100, w_m=100, classes=None, extra=None):
    s = {
        "content_width": "full",
        "width": {"unit": "%", "size": w, "sizes": []},
        "width_tablet": {"unit": "%", "size": w_t, "sizes": []},
        "width_mobile": {"unit": "%", "size": w_m, "sizes": []},
        "flex_direction": "column",
        "flex_gap": {"unit": "px", "size": 10, "column": "10", "row": "10", "isLinked": True},
        "padding": dim(0, 0, 0, 0),
    }
    s.update(extra or {})
    return container(children, s, classes)


def heading(text, tag="h2", color=NAVY, t=None, classes=None, extra=None, align=None):
    s = {"title": text, "header_size": tag, "title_color": color}
    s.update(t or typo(34, "900", 1.15))
    if align:
        s["align"] = align
    s.update(extra or {})
    return widget("heading", s, classes)


def text(html, color=INK, t=None, classes=None, extra=None, align=None):
    s = {"editor": html, "text_color": color}
    s.update(t or typo(17, "400", 1.6))
    if align:
        s["align"] = align
    s.update(extra or {})
    return widget("text-editor", s, classes)


def button(label, url="#", classes=None, extra=None):
    s = {
        "text": label,
        "link": {"url": url, "is_external": "", "nofollow": ""},
        "align": "left",
        "size": "md",
        "background_color": YELLOW,
        "button_text_color": DEEP,
        "border_radius": dim(40, 40, 40, 40),
        "text_padding": dim(20, 38, 20, 38),
        "text_padding_mobile": dim(16, 24, 16, 24),
        "selected_icon": {"value": "fas fa-arrow-right", "library": "fa-solid"},
        "icon_align": "right",
        "icon_indent": {"unit": "px", "size": 12, "sizes": []},
        "hover_color": DEEP,
        "button_background_hover_color": "#FFE94D",
    }
    s.update(typo(20, "900", 1, ls=0.4, transform="uppercase", size_m=17))
    s.update(extra or {})
    return widget("button", s, classes)


def spacer(px=16, px_m=None):
    s = {"space": {"unit": "px", "size": px, "sizes": []}}
    if px_m:
        s["space_mobile"] = {"unit": "px", "size": px_m, "sizes": []}
    return widget("spacer", s)


def icon_box(icon, title, desc, position="left", title_color=BLUE,
             desc_color=INK, icon_color=WHITE, classes=None, extra=None,
             title_size=17, desc_size=15, align="left"):
    s = {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "view": "default",
        "title_text": title,
        "description_text": desc,
        "position": position,
        "text_align": align,
        "primary_color": icon_color,
        "icon_primary_color": icon_color,
        "icon_size": {"unit": "px", "size": 26, "sizes": []},
        "icon_space": {"unit": "px", "size": 16, "sizes": []},
        "title_color": title_color,
        "description_color": desc_color,
        "title_typography_typography": "custom",
        "title_typography_font_family": SANS,
        "title_typography_font_size": {"unit": "px", "size": title_size, "sizes": []},
        "title_typography_font_weight": "900",
        "title_typography_text_transform": "uppercase",
        "title_typography_letter_spacing": {"unit": "px", "size": 0.4, "sizes": []},
        "description_typography_typography": "custom",
        "description_typography_font_family": SANS,
        "description_typography_font_size": {"unit": "px", "size": desc_size, "sizes": []},
        "description_typography_line_height": {"unit": "em", "size": 1.5, "sizes": []},
    }
    s.update(extra or {})
    return widget("icon-box", s, classes)


# ------------------------------------------------------------------ the CSS
CSS = ("""<style id="fna-home-style">
/* =========================================================================
   Home page — Futuro Nazionale Albignasego
   Everything below is scoped to .fna-home. It carries the four things
   Elementor's own controls can't do natively: the tricolour rules, the icon
   rings, the hero/photo overlays and the edge-bleeding split panel.
   ========================================================================= */
.fna-home{ --fna-green:%(GREEN)s; --fna-red:%(RED)s; --fna-yellow:%(YELLOW)s;
           --fna-blue:%(BLUE)s; --fna-deep:%(DEEP)s; }

/* ---- tricolour rule (green | white | red) -------------------------------- */
.fna-home .fna-tricolore::after{
  content:""; display:block; position:relative; inset:auto;
  width:340px; max-width:100%%; height:7px; margin:16px 0 0; border-radius:2px;
  background:linear-gradient(90deg,
    var(--fna-green) 0 33.33%%, #FFFFFF 33.33%% 66.66%%, var(--fna-red) 66.66%% 100%%);
}
.fna-home .fna-tricolore-sm::after{ width:190px; height:6px; margin-top:12px; }
.fna-home .fna-tricolore-c::after{ margin-left:auto; margin-right:auto; }

/* ---- HERO ---------------------------------------------------------------- */
/* COVER-ok.png (1942x810) is anchored right so the badge and the script line
   stay in frame at every height; the blue column on the left is rebuilt here
   as a scrim, so the copy stays legible whatever the crop does. */
.fna-home .fna-hero::before{
  content:""; position:absolute; inset:0; width:auto; height:auto; border:0; z-index:0;
  background:linear-gradient(90deg,
    rgba(0,41,93,.94) 0%%, rgba(0,41,93,.86) 26%%, rgba(0,41,93,.55) 46%%,
    rgba(0,41,93,.12) 62%%, rgba(0,41,93,0) 74%%);
  pointer-events:none;
}
.fna-home .fna-hero > .e-con-inner{ position:relative; z-index:1; }
.fna-home .fna-hero-copy .elementor-heading-title{ text-shadow:0 2px 18px rgba(0,20,50,.35); }
@media (max-width:1024px){
  .fna-home .fna-hero::before{
    background:linear-gradient(90deg, rgba(0,41,93,.94) 0%%, rgba(0,41,93,.80) 55%%, rgba(0,41,93,.35) 100%%);
  }
}
@media (max-width:767px){
  .fna-home .fna-hero::before{ background:rgba(0,41,93,.86); }
}

/* ---- icon rings (pillars band) ------------------------------------------- */
.fna-home .fna-ring .elementor-icon{
  width:92px; height:92px; border:3px solid rgba(255,255,255,.9);
  border-radius:50%%; display:inline-flex; align-items:center; justify-content:center;
}
.fna-home .fna-ring .elementor-icon-box-icon{ margin-bottom:18px; }
/* thin separators between the four pillars, desktop only */
@media (min-width:1025px){
  .fna-home .fna-pillar + .fna-pillar{ border-left:1px solid rgba(255,255,255,.28); }
  .fna-home .fna-pillar{ padding-left:26px; padding-right:26px; }
}

/* ---- filled circular icons (valori list) --------------------------------- */
.fna-home .fna-dot .elementor-icon{
  width:62px; height:62px; background:var(--fna-blue); color:#fff;
  border-radius:50%%; display:inline-flex; align-items:center; justify-content:center;
}
@media (min-width:1025px){
  .fna-home .fna-valori-list{ border-left:1px solid rgba(10,36,114,.18); padding-left:44px; }
}

/* ---- photo band with a left-to-right scrim ------------------------------- */
.fna-home .fna-scrim::before{
  content:""; position:absolute; inset:0; width:auto; height:auto; border:0;
  background:linear-gradient(90deg,
    rgba(0,41,93,.90) 0%%, rgba(0,41,93,.72) 38%%, rgba(0,41,93,.10) 72%%, rgba(0,41,93,0) 100%%);
  z-index:0; pointer-events:none;
}
.fna-home .fna-scrim > .e-con-inner{ position:relative; z-index:1; }
@media (max-width:767px){
  .fna-home .fna-scrim::before{ background:rgba(0,41,93,.82); }
}

/* ---- quote card ---------------------------------------------------------- */
.fna-home .fna-quote-card{ box-shadow:0 14px 34px rgba(0,20,50,.28); }

/* ---- split panel that bleeds to the window edge -------------------------- */
.fna-home .fna-split{ align-items:stretch; }
.fna-home .fna-split-l{ padding:64px 40px 64px max(24px, calc((100%% - 1200px) / 2 + 12px)); }
.fna-home .fna-split-r{ padding:56px max(24px, calc((100%% - 1200px) / 2 + 12px)) 56px 44px; }
@media (max-width:1024px){
  .fna-home .fna-split-l{ padding:48px 24px; }
  .fna-home .fna-split-r{ padding:44px 24px; }
}

/* ---- Contact Form 7, dressed to match the mockup ------------------------- */
.fna-home .fna-form .wpcf7 input[type=text],
.fna-home .fna-form .wpcf7 input[type=email],
.fna-home .fna-form .wpcf7 input[type=tel],
.fna-home .fna-form .wpcf7 textarea{
  width:100%%; box-sizing:border-box; background:#fff; border:0; border-radius:8px;
  padding:15px 18px; font:400 16px/1.4 Roboto,sans-serif; color:%(DEEP)s;
  margin:0 0 12px; box-shadow:0 1px 0 rgba(0,0,0,.05);
}
.fna-home .fna-form .wpcf7 textarea{ height:104px; min-height:104px; resize:vertical; }
.fna-home .fna-form .wpcf7 ::placeholder{ color:#8FA2BF; opacity:1; }
.fna-home .fna-form .wpcf7 .fna-2col{ display:flex; gap:12px; }
.fna-home .fna-form .wpcf7 .fna-2col > span{ flex:1; }
.fna-home .fna-form .wpcf7 input[type=submit]{
  width:100%%; border:0; border-radius:40px; cursor:pointer;
  background:var(--fna-yellow); color:%(DEEP)s;
  font:900 19px/1 Roboto,sans-serif; letter-spacing:.4px; text-transform:uppercase;
  padding:19px 26px; margin-top:4px;
}
.fna-home .fna-form .wpcf7 input[type=submit]:hover{ background:#FFE94D; }
.fna-home .fna-form .wpcf7-not-valid-tip{ color:#FFD9D9; font-size:13px; margin:-8px 0 10px; }
.fna-home .fna-form .wpcf7-response-output{
  border-color:rgba(255,255,255,.5); color:#fff; border-radius:8px; font-size:14px;
}
/* placeholder shown until the real form is dropped in */
.fna-home .fna-form-placeholder{
  border:2px dashed rgba(255,255,255,.45); border-radius:10px; padding:22px;
  color:#CFE0F5; font:400 15px/1.6 Roboto,sans-serif;
}
.fna-home .fna-form-placeholder b{ color:#fff; }

/* ---- privacy line -------------------------------------------------------- */
.fna-home .fna-privacy{ display:flex; align-items:center; gap:9px; }
</style>""") % {"GREEN": GREEN, "RED": RED, "YELLOW": YELLOW, "BLUE": BLUE, "DEEP": DEEP}


# ------------------------------------------------------------------ sections
def sec_hero():
    copy = cell([
        heading("COMITATO COSTITUENTE", "h6", WHITE,
                t=typo(21, "700", 1.2, ls=2.6, transform="uppercase", size_t=18, size_m=15)),
        heading("FUTURO<br>NAZIONALE", "h1", WHITE,
                t=typo(78, "900", 0.94, ls=-1.5, transform="uppercase", size_t=58, size_m=40),
                extra={"_margin": dim(8, 0, 0, 0)}),
        heading("ALBIGNASEGO 1866", "h2", YELLOW,
                t=typo(52, "900", 1.0, ls=-0.6, transform="uppercase", size_t=38, size_m=27),
                classes="fna-tricolore", extra={"_margin": dim(2, 0, 0, 0)}),
        text("<p>Persone, idee, azione per un’Italia più forte,<br>"
             "a partire dal nostro territorio.</p>", WHITE,
             t=typo(23, "500", 1.45, size_t=20, size_m=17),
             extra={"_margin": dim(20, 0, 0, 0)}),
        button("Entra nel comitato", "#partecipa",
               extra={"_margin": dim(22, 0, 0, 0)}),
        text("<p>Insieme possiamo fare la differenza</p>", WHITE,
             t=typo(15, "700", 1.4, ls=1.6, transform="uppercase"),
             extra={"_margin": dim(16, 0, 0, 0)}),
    ], 50, 74, 100, classes="fna-hero-copy")

    return band([row([copy], gap=0)],
                bg_img=IMG_HERO,
                padding=(76, 24, 76, 24), padding_m=(48, 18, 48, 18),
                classes="fna-hero",
                extra={"min_height": {"unit": "px", "size": 620, "sizes": []},
                       "min_height_tablet": {"unit": "px", "size": 520, "sizes": []},
                       "background_position": "center right",
                       "flex_justify_content": "center"})


def sec_valori():
    left = cell([
        heading("Quali valori vorresti vedere maggiormente rappresentati "
                "nella vita pubblica di Albignasego?", "h2", NAVY,
                t=typo(40, "900", 1.18, ls=-0.6, size_t=33, size_m=27)),
        text("<p>Il nostro comitato è uno spazio aperto a tutti coloro che credono "
             "in un’Italia più consapevole, sicura e unita. Unisciti a noi per "
             "portare idee, proposte e soluzioni concrete dal territorio.</p>",
             INK, t=typo(18, "400", 1.65, size_m=16.5),
             extra={"_margin": dim(16, 0, 0, 0)}),
    ], 55, 100, 100)

    items = [
        ("fas fa-users", "CITTADINI", "Persone comuni, unite da valori comuni."),
        ("fas fa-lightbulb", "IDEE", "Proposte concrete per il nostro territorio."),
        ("fas fa-cog", "AZIONE", "Dalle idee ai fatti, insieme."),
        ("fas fa-heart", "UN FUTURO MIGLIORE",
         "Per Albignasego, per l’Italia, per le prossime generazioni."),
    ]
    right = cell([icon_box(i, t, d, classes="fna-dot") for i, t, d in items],
                 45, 100, 100, classes="fna-valori-list",
                 extra={"flex_gap": {"unit": "px", "size": 22, "column": "22",
                                     "row": "22", "isLinked": True},
                        "flex_justify_content": "center"})

    return band([row([left, right], gap=48, gap_t=32)],
                bg=WHITE, padding=(74, 24, 74, 24), padding_m=(46, 18, 46, 18))


def sec_pilastri():
    items = [
        ("fas fa-flag", "IDENTITÀ",
         "Valorizziamo la nostra storia, la cultura e le tradizioni. "
         "Un popolo consapevole costruisce il futuro."),
        ("fas fa-shield-alt", "DIFESA DELLA PATRIA",
         "Sicurezza, sovranità e interesse nazionale al centro. "
         "Un’Italia forte tutela i suoi cittadini."),
        ("fas fa-users", "FAMIGLIA",
         "Sostegno alle famiglie, protezione dei più giovani e "
         "valorizzazione dei valori che ci uniscono."),
        ("fas fa-landmark", "TERRITORIO",
         "Albignasego al centro: ascolto, iniziative locali e "
         "soluzioni concrete per una comunità più viva."),
    ]
    cells = [
        cell([icon_box(i, t, d, position="top", title_color=WHITE,
                       desc_color="#D6E4F7", icon_color=WHITE, align="center",
                       title_size=21, desc_size=15,
                       classes="fna-ring",
                       extra={"icon_size": {"unit": "px", "size": 38, "sizes": []}})],
             25, 50, 100, classes="fna-pillar")
        for i, t, d in items
    ]
    return band([row(cells, gap=0, gap_t=30, gap_m=26)],
                bg=BLUE, padding=(64, 24, 64, 24), padding_m=(44, 18, 44, 18))


def sec_cambiamento():
    left = cell([
        heading("IL CAMBIAMENTO<br>INIZIA DA QUI", "h2", WHITE,
                t=typo(52, "900", 1.02, ls=-0.8, transform="uppercase",
                       size_t=40, size_m=30)),
        text("<p>Un territorio più forte,<br>un’Italia più grande.</p>", WHITE,
             t=typo(25, "700", 1.35, size_t=21, size_m=18),
             classes="fna-tricolore fna-tricolore-sm",
             extra={"_margin": dim(14, 0, 0, 0)}),
    ], 58, 100, 100)

    card = cell([
        text("<p>“Se ognuno fa qualcosa, allora insieme possiamo fare molto.”</p>",
             NAVY, t=typo(23, "500", 1.4, style="italic", size_m=19), align="center"),
        text("<p>Roberto Vannacci</p>", NAVY,
             t=typo(16, "900", 1.3, ls=1.2, transform="uppercase"), align="center",
             classes="fna-tricolore fna-tricolore-sm fna-tricolore-c",
             extra={"_margin": dim(10, 0, 0, 0)}),
    ], 38, 100, 100, classes="fna-quote-card", extra={
        "background_background": "classic",
        "background_color": WHITE,
        "border_radius": dim(12, 12, 12, 12),
        "padding": dim(30, 32, 34, 32),
        "padding_mobile": dim(24, 20, 26, 20),
        "flex_justify_content": "center",
    })

    return band([row([left, card], gap=40, gap_t=30,
                     settings={"flex_align_items": "center"})],
                bg_img=IMG_BAND,
                padding=(78, 24, 78, 24), padding_m=(48, 18, 48, 18),
                classes="fna-scrim",
                extra={"min_height": {"unit": "px", "size": 380, "sizes": []},
                       "flex_justify_content": "center"})


def sec_partecipa():
    items = [
        ("fas fa-calendar-alt", "EVENTI", "Incontri, dibattiti, iniziative sul territorio."),
        ("fas fa-users", "RETE", "Entra in una comunità di persone motivate."),
        ("fas fa-leaf", "PROGETTI", "Diamo voce alle tue idee per Albignasego."),
    ]
    icons = row([
        cell([icon_box(i, t, d, position="top", title_color=NAVY, desc_color=INK,
                       icon_color=BLUE, align="left", title_size=18, desc_size=15,
                       extra={"icon_size": {"unit": "px", "size": 34, "sizes": []}})],
             33.33, 33.33, 100)
        for i, t, d in items
    ], gap=26, gap_t=20)

    left = cell([
        heading("PARTECIPA ANCHE TU", "h2", NAVY,
                t=typo(46, "900", 1.08, ls=-0.8, transform="uppercase",
                       size_t=36, size_m=28)),
        text("<p>Porta le tue idee. Costruiamo insieme il futuro.</p>", INK,
             t=typo(22, "400", 1.4, size_t=19, size_m=17),
             extra={"_margin": dim(8, 0, 0, 0)}),
        spacer(26, 18),
        icons,
    ], 55, 100, 100, classes="fna-split-l", extra={
        "background_background": "classic",
        "background_color": WHITE,
        "flex_justify_content": "flex-start",
        "padding": dim(0, 0, 0, 0),
    })

    if CF7:
        form = widget("shortcode",
                      {"shortcode": '[contact-form-7 id="%s" title="Richiedi informazioni"]' % CF7},
                      classes="fna-form")
    else:
        form = widget("html", {"html":
            '<div class="fna-form-placeholder">'
            '<b>Modulo Contact Form 7.</b><br>'
            'Sostituisci questo blocco con il widget <i>Shortcode</i> e incolla '
            '<code>[contact-form-7 id="…"]</code>. Il CSS della pagina veste '
            'automaticamente i campi come nel mockup.'
            '</div>'}, classes="fna-form")

    right = cell([
        heading("RICHIEDI INFORMAZIONI", "h3", WHITE,
                t=typo(28, "900", 1.15, ls=-0.2, transform="uppercase",
                       size_t=24, size_m=21)),
        text("<p>Compila il modulo per entrare nel comitato.</p>", "#CFE0F5",
             t=typo(17, "400", 1.45),
             extra={"_margin": dim(6, 0, 18, 0)}),
        form,
        widget("icon-box", {
            "selected_icon": {"value": "fas fa-lock", "library": "fa-solid"},
            "view": "default", "position": "left", "text_align": "left",
            "title_text": "", "description_text":
                "I tuoi dati sono trattati nel rispetto della privacy.",
            "primary_color": "#9FC0E8", "icon_primary_color": "#9FC0E8",
            "icon_size": {"unit": "px", "size": 14, "sizes": []},
            "icon_space": {"unit": "px", "size": 9, "sizes": []},
            "description_color": "#9FC0E8",
            "description_typography_typography": "custom",
            "description_typography_font_family": SANS,
            "description_typography_font_size": {"unit": "px", "size": 13.5, "sizes": []},
            "description_typography_line_height": {"unit": "em", "size": 1.4, "sizes": []},
            "_margin": dim(14, 0, 0, 0),
        }, classes="fna-privacy"),
    ], 45, 100, 100, classes="fna-split-r", extra={
        "background_background": "classic",
        "background_color": DEEP,
        "flex_justify_content": "center",
        "padding": dim(0, 0, 0, 0),
    })

    outer = row([left, right], gap=0, gap_t=0, gap_m=0,
                settings={"padding": dim(0, 0, 0, 0)},
                classes="fna-split")
    outer["settings"]["_element_id"] = "partecipa"
    return container([outer], {
        "content_width": "full",
        "flex_direction": "column",
        "padding": dim(0, 0, 0, 0),
        "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0", "isLinked": True},
    })


# ------------------------------------------------------------------ assemble
def build():
    kids = [widget("html", {"html": CSS})]
    kids += [sec_hero(), sec_valori(), sec_pilastri(), sec_cambiamento(), sec_partecipa()]
    return {
        "id": eid("root"),
        "elType": "container",
        "isInner": False,
        "settings": {
            "container_type": "flex",
            "content_width": "full",
            "flex_direction": "column",
            "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0", "isLinked": True},
            "padding": dim(0, 0, 0, 0),
            "css_classes": "fna-home",
        },
        "elements": kids,
    }


doc = {
    "version": "0.4",
    "title": "Home Page — Futuro Nazionale Albignasego (struttura)",
    "type": "container",
    "content": [build()],
    "page_settings": [],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("wrote", OUT)
