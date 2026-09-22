# Home page — Elementor structure

The ChatGPT mockup rebuilt as a real, editable, full-width Elementor page for
**futuronazionalealbignasego.it** (Astra + Elementor 4.2.4).

Every heading, paragraph, icon, colour and button is a live Elementor widget —
nothing is baked into an image except the two photographs. 100% native widgets:
container, heading, text editor, button, icon box, spacer, HTML, shortcode.
**No Pro controls, no add-on plugins.**

---

## 1. Import

1. **Templates → Saved Templates → Import Templates** → `fna-home-page.json`
2. Open your page with Elementor → folder icon → **My Templates** →
   *"Home Page — Futuro Nazionale Albignasego (struttura)"* → **Insert**
3. Asked whether to import document settings → **No**
4. Set the page template to **Elementor Full Width** or **Elementor Canvas**
   (Page Settings → Layout), otherwise Astra adds its own container and the
   full-bleed strips stop reaching the window edge.

## 2. The five sections

| # | Section | Notes |
|---|---|---|
| 1 | Hero | `COVER-ok.png` as the background, anchored right. Copy on the left. |
| 2 | Quali valori | 55 / 45 split, 4 icon rows on the right |
| 3 | I quattro pilastri | blue strip, 4 columns, ringed icons |
| 4 | Il cambiamento | photo strip + quote card |
| 5 | Partecipa / modulo | white + navy split, bleeds to the window edge |

Grid behaviour: desktop as shown → tablet the splits stack and the 4 pillars go
2×2 → mobile everything is one column. Elementor's own breakpoints (1024 / 767).

## 3. Two things you need to swap

**a) The park photo.** The "IL CAMBIAMENTO INIZIA DA QUI" strip currently uses
`cov-Villa_Obizzi_municipio_Albignasego.jpg` as a stand-in, because the park
picture from the mockup is not in your media library. Upload it, then: select
that strip → Style → Background → Image → choose the new file. Nothing else
changes.

**b) The form.** The navy panel has a dashed placeholder where the form goes.
You already have Contact Form 7 installed. Create a form with the markup below,
then replace the placeholder with a **Shortcode** widget containing
`[contact-form-7 id="…"]`. The page CSS dresses the fields automatically — white
rounded inputs, email and phone side by side, yellow pill submit.

```
<span class="fna-1col">[text* nome placeholder "Nome e cognome"]</span>
<span class="fna-2col">[email* email placeholder "Email"][tel telefono placeholder "Telefono"]</span>
<span class="fna-1col">[textarea messaggio placeholder "Messaggio (opzionale)"]</span>
[submit "Voglio unirmi"]
```

The `fna-2col` span is what puts Email and Telefono on one line — keep it.

## 4. Where the styling lives

One HTML widget sits at the very top of the page and carries the whole
stylesheet, scoped to `.fna-home`. It holds only the five things Elementor's
controls can't do natively:

- the **tricolour rules** (green/white/red, drawn in CSS, not images) — class `fna-tricolore`, smaller variant `fna-tricolore-sm`, centred variant `fna-tricolore-c`
- the **icon rings** in the blue strip — class `fna-ring`, and the filled blue circles in section 2 — class `fna-dot`
- the **hero scrim** and the **photo-strip scrim** — classes `fna-hero`, `fna-scrim`
- the **edge-bleeding split panel** — classes `fna-split`, `fna-split-l`, `fna-split-r`
- the **Contact Form 7 styling** — class `fna-form`

Everything else — colours, sizes, spacing, responsive values — is set on the
widgets themselves, so you edit it in the normal Elementor panels.

## 5. Palette and type

Sampled from the mockup:

| | |
|---|---|
| Navy (headings) | `#0A2472` |
| Blue (strips, icons) | `#003E7F` |
| Deep navy (hero scrim, form panel) | `#00295D` |
| Yellow (CTA) | `#FDE01A` |
| Body text | `#173A79` |
| Tricolour | `#009246` / `#FFFFFF` / `#CE2B37` |

Type is **Roboto** throughout (900 for the display headings), which your
Elementor kit already loads — the page adds no extra font request.

## 6. Not included

The blue nav bar at the top of the mockup and the footer strip at the bottom are
**header and footer templates**, not page content — you already have a header
live on the site. Say the word and I'll rebuild both to match the mockup.
