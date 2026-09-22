#!/usr/bin/env python3
"""Builds the Elementor 'Relazione / Report' section template JSON.

Native Elementor widgets only (container, heading, text-editor, image,
icon-box, html). No add-ons, no Pro-only controls.
"""
import json, sys, hashlib

SITE = sys.argv[1] if len(sys.argv) > 1 else "https://futuronazionalealbignasego.it"
OUT = sys.argv[2] if len(sys.argv) > 2 else "fna-report-section.json"

_n = [0]
def eid(tag=""):
    _n[0] += 1
    return hashlib.md5(f"fna{tag}{_n[0]}".encode()).hexdigest()[:7]

# ---------------------------------------------------------------- palette
NAVY      = "#051632"   # live header/footer navy
BLUE      = "#003F84"   # brand blue from the design
BLUE_DK   = "#00285A"
YELLOW    = "#FDD91C"
INK       = "#334155"   # = Astra global color 3
MUTED     = "#64748B"
CELL_BG   = "#F4F7FB"
CELL_BD   = "#E2E8F2"
WHITE     = "#FFFFFF"

SLAB = "Roboto Slab"    # = Elementor kit "Secondary" font (already loaded)
SANS = "Roboto"         # = Elementor kit "Primary/Text" font (already loaded)

PLACEHOLDER = SITE + "/wp-content/plugins/elementor/assets/images/placeholder.png"
CHART1 = sys.argv[3] if len(sys.argv) > 3 else PLACEHOLDER
CHART2 = sys.argv[4] if len(sys.argv) > 4 else PLACEHOLDER


def dim(t=0, r=0, b=0, l=0, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def typo(family=SANS, size=17, weight="400", lh=1.7, ls=None, style=None,
         transform=None, size_t=None, size_m=None):
    s = {
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_size": {"unit": "px", "size": size, "sizes": []},
        "typography_font_weight": weight,
        "typography_line_height": {"unit": "em", "size": lh, "sizes": []},
    }
    if size_t is not None:
        s["typography_font_size_tablet"] = {"unit": "px", "size": size_t, "sizes": []}
    if size_m is not None:
        s["typography_font_size_mobile"] = {"unit": "px", "size": size_m, "sizes": []}
    if ls is not None:
        s["typography_letter_spacing"] = {"unit": "px", "size": ls, "sizes": []}
    if style:
        s["typography_font_style"] = style
    if transform:
        s["typography_text_transform"] = transform
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


def row(children, gap=24, gap_t=20, gap_m=16, settings=None, classes=None):
    s = {
        "flex_direction": "row",
        "flex_wrap_tablet": "wrap",
        "flex_align_items": "stretch",
        "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap), "isLinked": True},
        "flex_gap_tablet": {"unit": "px", "size": gap_t, "column": str(gap_t), "row": str(gap_t), "isLinked": True},
        "flex_gap_mobile": {"unit": "px", "size": gap_m, "column": str(gap_m), "row": str(gap_m), "isLinked": True},
        "flex_direction_mobile": "column",
    }
    s.update(settings or {})
    return container(children, s, classes)


def cell(children, w=33.33, w_t=50, w_m=100, classes="", extra=None):
    s = {
        "width": {"unit": "%", "size": w, "sizes": []},
        "width_tablet": {"unit": "%", "size": w_t, "sizes": []},
        "width_mobile": {"unit": "%", "size": w_m, "sizes": []},
        "flex_direction": "column",
        "content_width": "full",
    }
    s.update(extra or {})
    return container(children, s, classes)


def card_style():
    """Shared look for a report cell."""
    return {
        "background_background": "classic",
        "background_color": CELL_BG,
        "border_border": "solid",
        "border_width": dim(1, 1, 1, 1),
        "border_color": CELL_BD,
        "border_radius": dim(10, 10, 10, 10),
        "padding": dim(32, 28, 32, 28),
        "padding_tablet": dim(28, 24, 28, 24),
        "padding_mobile": dim(24, 20, 24, 20),
    }


def heading(text, tag="h3", color=NAVY, t=None, align=None, classes=None, extra=None):
    s = {"title": text, "header_size": tag, "title_color": color}
    s.update(t or typo(SLAB, 24, "700", 1.3))
    if align:
        s["align"] = align
    s.update(extra or {})
    return widget("heading", s, classes)


def text(html, color=INK, t=None, classes=None, extra=None):
    s = {"editor": html, "text_color": color}
    s.update(t or typo(SANS, 17, "400", 1.75, size_m=16))
    s.update(extra or {})
    return widget("text-editor", s, classes)


def spacer(px=16, px_m=None):
    s = {"space": {"unit": "px", "size": px, "sizes": []}}
    if px_m:
        s["space_mobile"] = {"unit": "px", "size": px_m, "sizes": []}
    return widget("spacer", s)


def image(caption=None, classes=None, extra=None, url=None):
    s = {
        "image": {"url": url or PLACEHOLDER, "id": "", "alt": "", "source": "library"},
        "image_size": "full",
        "align": "center",
        "width": {"unit": "%", "size": 100, "sizes": []},
        "image_border_radius": dim(6, 6, 6, 6),
    }
    if caption:
        s["caption_source"] = "custom"
        s["caption"] = caption
        s["text_color"] = MUTED
        s.update({
            "caption_typography_typography": "custom",
            "caption_typography_font_family": SANS,
            "caption_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
            "caption_typography_line_height": {"unit": "em", "size": 1.5, "sizes": []},
        })
    s.update(extra or {})
    return widget("image", s, classes)


def icon_box(icon, title, desc, classes=None):
    s = {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "view": "default",
        "title_text": title,
        "description_text": desc,
        "position": "top",
        "text_align": "left",
        "primary_color": BLUE,
        "icon_primary_color": BLUE,
        "icon_size": {"unit": "px", "size": 30, "sizes": []},
        "icon_space": {"unit": "px", "size": 14, "sizes": []},
        "title_color": NAVY,
        "description_color": INK,
        "title_typography_typography": "custom",
        "title_typography_font_family": SLAB,
        "title_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
        "title_typography_font_weight": "700",
        "title_typography_letter_spacing": {"unit": "px", "size": 0.2, "sizes": []},
        "description_typography_typography": "custom",
        "description_typography_font_family": SANS,
        "description_typography_font_size": {"unit": "px", "size": 15, "sizes": []},
        "description_typography_line_height": {"unit": "em", "size": 1.65, "sizes": []},
    }
    return widget("icon-box", s, classes)


# ---------------------------------------------------------------- the CSS
CSS = """<style id="fna-report-style">
/* ============================================================
   Relazione / report section  —  scoped to .fna-report
   Ghost words + pattern live here so the template is
   self-contained: no Customizer edits, no extra plugin.
   ============================================================ */
.fna-report{ --fna-navy:%(NAVY)s; --fna-blue:%(BLUE)s; --fna-yellow:%(YELLOW)s;
             --fna-ghost:rgba(5,22,50,.06); --fna-ghost-size:clamp(42px,5.4vw,80px); }

/* --- grid cells: the ghost word sits behind, never above, the copy --- */
.fna-report .fna-cell{ position:relative; overflow:hidden; isolation:isolate; }
.fna-report .fna-cell > *{ position:relative; z-index:1; }
.fna-report .fna-cell[class*="fna-w-"]::before{
  /* .e-con::before is Elementor's overlay box (inset:0) — reset it, then anchor */
  position:absolute; inset:auto .14em -.06em auto;
  width:auto; height:auto; border:0; background:none; transition:none;
  font-family:"Roboto Slab",Georgia,"Times New Roman",serif;
  font-weight:700; font-size:var(--fna-ghost-size); line-height:.78;
  letter-spacing:-.025em; color:var(--fna-ghost);
  white-space:nowrap; pointer-events:none; -webkit-user-select:none; user-select:none;
  z-index:0;
}
/* ghost scale per row — keeps long words inside narrow cells */
.fna-report .fna-ghost-s{ --fna-ghost-size:clamp(26px,3.0vw,38px); }
.fna-report .fna-ghost-m{ --fna-ghost-size:clamp(34px,4.2vw,58px); }

/* one line per cell — this is the only place the words are edited */
.fna-report .fna-w-1866::before     { content:"1866"; }
.fna-report .fna-w-aree::before     { content:"AREE"; }
.fna-report .fna-w-persone::before  { content:"PERSONE"; }
.fna-report .fna-w-identita::before { content:"IDENTITÀ"; }
.fna-report .fna-w-difesa::before   { content:"DIFESA"; }
.fna-report .fna-w-famiglia::before { content:"FAMIGLIA"; }
.fna-report .fna-w-territorio::before{ content:"TERRITORIO"; }
.fna-report .fna-w-dati::before     { content:"DATI"; }
.fna-report .fna-w-analisi::before  { content:"ANALISI"; }

/* --- alternative: dot pattern instead of a word (chart cells) --- */
.fna-report .fna-pattern{
  background-image:radial-gradient(rgba(5,22,50,.07) 1px, transparent 1.2px);
  background-size:15px 15px; background-position:-3px -3px;
}
.fna-report .fna-pattern > *{ position:relative; z-index:1; }
/* kill-switch: add fna-ghost-off to .fna-report to hide every ghost */
.fna-report.fna-ghost-off .fna-cell::before{ display:none; }
.fna-report.fna-ghost-off .fna-pattern{ background-image:none; }

/* --- headline rule: green / white / red, drawn, not an image --- */
.fna-report .fna-head::after{
  content:""; display:block; position:relative; inset:auto; width:132px; height:5px; margin:18px 0 0; border-radius:3px;
  background:linear-gradient(90deg,#009246 0 33.33%%,#FFFFFF 33.33%% 66.66%%,#CE2B37 66.66%% 100%%);
  box-shadow:0 0 0 1px rgba(5,22,50,.08);
}
.fna-report .fna-head.fna-center::after{ margin-left:auto; margin-right:auto; }

/* --- standfirst: keep the lead paragraph to a readable measure --- */
.fna-report .fna-lead{ max-width:760px; }

/* --- analysis block: thin blue keyline on the left --- */
.fna-report .fna-block{ padding-left:22px; border-left:3px solid rgba(0,63,132,.18); }
@media (max-width:767px){ .fna-report .fna-block{ padding-left:16px; } }

/* --- quote --- */
.fna-report .fna-quote::before{
  content:"\\201C"; display:block; margin:0 0 -12px;
  position:relative; inset:auto; width:auto; height:auto; border:0; background:none; font-family:"Roboto Slab",Georgia,serif;
  font-size:64px; line-height:.6; color:var(--fna-yellow);
}

/* --- tidy paragraph rhythm inside the section --- */
.fna-report .elementor-widget-text-editor p:last-child{ margin-bottom:0; }
.fna-report .fna-quote p{ margin:0; }

/* --- chart area keeps its shape before the PNG is dropped in --- */
.fna-report .fna-chart-slot img{ width:100%%; height:auto; display:block;
  max-height:520px; object-fit:contain; }
.fna-report .fna-chart-slot{ min-height:220px; }

/* --- print / reduced-motion friendliness --- */
@media print{ .fna-report .fna-cell::before,.fna-report .fna-pattern{ display:none; background-image:none; } }
</style>""" % {"NAVY": NAVY, "BLUE": BLUE, "YELLOW": YELLOW}


# ---------------------------------------------------------------- content
def build():
    kids = []

    # 0. self-contained CSS
    kids.append(widget("html", {"html": CSS}))

    # 1. section header ------------------------------------------------
    kids.append(container([
        heading("RELAZIONE DEL COMITATO · 2026", "h6", BLUE,
                t=typo(SANS, 13, "700", 1.4, ls=2.4, transform="uppercase")),
        heading("Albignasego in numeri:<br>analisi, idee e proposte", "h2", NAVY,
                t=typo(SLAB, 44, "700", 1.15, ls=-0.4, size_t=36, size_m=29),
                extra={"_margin": dim(6, 0, 0, 0)}),
    ], {
        "flex_direction": "column",
        "flex_gap": {"unit": "px", "size": 4, "column": "4", "row": "4", "isLinked": True},
        "padding": dim(0, 0, 0, 0),
    }, classes="fna-head"))

    kids.append(container([
        text("<p>Sintesi dell'attività del comitato e lettura dei dati del "
             "territorio. Ogni blocco è indipendente: sostituisci il testo, "
             "l'icona o il grafico senza toccare la griglia.</p>",
             t=typo(SANS, 19, "400", 1.7, size_t=18, size_m=17)),
    ], {
        "content_width": "full",
        "padding": dim(22, 0, 0, 0),
    }, classes="fna-lead"))

    # 2. key figures ---------------------------------------------------
    figures = [
        ("1.866", "ANNO DI FONDAZIONE", "fna-w-1866"),
        ("4", "AREE DI INTERVENTO", "fna-w-aree"),
        ("27.000", "CITTADINI DEL COMUNE", "fna-w-persone"),
    ]
    kids.append(spacer(46, 34))
    kids.append(row([
        cell([
            heading(num, "h3", BLUE,
                    t=typo(SLAB, 46, "700", 1.05, ls=-0.5, size_t=38, size_m=36)),
            text(f"<p>{label}</p>", MUTED,
                 t=typo(SANS, 12, "700", 1.5, ls=1.6, transform="uppercase"),
                 extra={"_margin": dim(4, 0, 0, 0)}),
        ], 33.33, 33.33, 100, f"fna-cell fna-ghost-m {ghost}", card_style())
        for num, label, ghost in figures
    ], gap=22))

    # 3. analysis + side chart ----------------------------------------
    kids.append(spacer(22, 16))
    kids.append(row([
        cell([
            container([
                heading("Il quadro attuale", "h3", BLUE),
                text("<p>Apri con il contesto: che cosa è stato osservato sul "
                     "territorio e in quale periodo. Due o tre frasi, non di più — "
                     "il dettaglio va nei grafici qui a fianco.</p>"),
            ], {"flex_direction": "column", "padding": dim(0, 0, 0, 0),
                "flex_gap": {"unit": "px", "size": 10, "column": "10", "row": "10", "isLinked": True}},
                classes="fna-block"),
            spacer(26, 20),
            container([
                heading("Le priorità per il territorio", "h3", BLUE),
                text("<p>Secondo blocco di analisi. Puoi duplicarlo (tasto destro "
                     "sul contenitore → Duplica) tutte le volte che serve: eredita "
                     "spaziatura, keyline e tipografia.</p>"),
            ], {"flex_direction": "column", "padding": dim(0, 0, 0, 0),
                "flex_gap": {"unit": "px", "size": 10, "column": "10", "row": "10", "isLinked": True}},
                classes="fna-block"),
        ], 58, 100, 100, "", {"padding": dim(6, 0, 0, 0)}),

        cell([
            heading("Adesioni per quartiere", "h4", NAVY,
                    t=typo(SLAB, 19, "700", 1.35)),
            spacer(14),
            image("Fig. 1 — Grafico laterale. PNG consigliato 840 × 640 px.",
                  classes="fna-chart-slot", url=CHART1),
        ], 42, 100, 100, "fna-cell fna-pattern", card_style()),
    ], gap=32, gap_t=26))

    # 4. pillars -------------------------------------------------------
    pillars = [
        ("fas fa-flag", "IDENTITÀ", "Valorizziamo la nostra storia, la cultura e le tradizioni.", "fna-w-identita"),
        ("fas fa-shield-alt", "DIFESA", "Sicurezza, sovranità e interesse nazionale al centro.", "fna-w-difesa"),
        ("fas fa-users", "FAMIGLIA", "Sostegno alle famiglie e ai più giovani.", "fna-w-famiglia"),
        ("fas fa-map-marker-alt", "TERRITORIO", "Ascolto, iniziative locali e soluzioni concrete.", "fna-w-territorio"),
    ]
    kids.append(spacer(34, 26))
    kids.append(row([
        cell([icon_box(ic, ti, de)], 25, 48, 100, f"fna-cell fna-ghost-s {gh}", card_style())
        for ic, ti, de, gh in pillars
    ], gap=20))

    # 5. wide chart ----------------------------------------------------
    kids.append(spacer(34, 26))
    kids.append(row([
        cell([
            heading("ANDAMENTO 2024 – 2026", "h6", BLUE,
                    t=typo(SANS, 12, "700", 1.4, ls=2.2, transform="uppercase")),
            heading("Il dato principale della relazione", "h3", NAVY,
                    t=typo(SLAB, 26, "700", 1.25, size_m=22),
                    extra={"_margin": dim(4, 0, 0, 0)}),
            spacer(18),
            image("Fig. 2 — Grafico a tutta larghezza. PNG consigliato 1600 × 600 px.",
                  classes="fna-chart-slot", url=CHART2),
            spacer(6),
            text("<p>Fonte: elaborazione del comitato su dati comunali.</p>", MUTED,
                 t=typo(SANS, 13, "400", 1.5, style="italic")),
        ], 100, 100, 100, "fna-cell fna-w-dati", card_style()),
    ], gap=20))

    # 6. quote ---------------------------------------------------------
    kids.append(spacer(34, 26))
    kids.append(row([
        cell([
            text("<p>Se ognuno fa qualcosa, allora insieme possiamo fare molto.</p>",
                 WHITE, t=typo(SLAB, 27, "400", 1.45, style="italic", size_t=24, size_m=21)),
            text("<p>— Inserisci qui l'attribuzione</p>", YELLOW,
                 t=typo(SANS, 13, "700", 1.5, ls=1.8, transform="uppercase"),
                 extra={"_margin": dim(16, 0, 0, 0)}),
        ], 100, 100, 100, "fna-cell fna-quote", {
            "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0", "isLinked": True},
            "background_background": "classic",
            "background_color": NAVY,
            "border_radius": dim(10, 10, 10, 10),
            "padding": dim(42, 46, 42, 46),
            "padding_tablet": dim(34, 32, 34, 32),
            "padding_mobile": dim(28, 22, 28, 22),
        }),
    ], gap=20))

    # 7. methodology note ---------------------------------------------
    kids.append(spacer(26, 20))
    kids.append(container([
        text("<p><strong>Nota metodologica.</strong> Periodo di riferimento, fonte "
             "dei dati ed eventuali limiti. Riga finale della relazione.</p>",
             MUTED, t=typo(SANS, 14, "400", 1.65)),
    ], {
        "border_border": "solid",
        "border_width": dim(1, 0, 0, 0),
        "border_color": CELL_BD,
        "padding": dim(20, 0, 0, 0),
    }))

    # ---------------- outer wrapper ----------------
    outer = {
        "id": eid("outer"),
        "elType": "container",
        "isInner": False,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
            "flex_direction": "column",
            "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0", "isLinked": True},
            "padding": dim(84, 24, 84, 24),
            "padding_tablet": dim(64, 24, 64, 24),
            "padding_mobile": dim(48, 18, 48, 18),
            "background_background": "classic",
            "background_color": WHITE,
            "css_classes": "fna-report",
        },
        "elements": kids,
    }
    return outer


doc = {
    "version": "0.4",
    "title": "Relazione / Report — Futuro Nazionale Albignasego",
    "type": "container",
    "content": [build()],
    "page_settings": [],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("wrote", OUT)
