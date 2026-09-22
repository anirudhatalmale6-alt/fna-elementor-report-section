# Report / white-paper section — Elementor template

Built for **futuronazionalealbignasego.it** (Astra 4.13 + Elementor 4.2.4).
100% native Elementor widgets — container, heading, text editor, image, icon box,
spacer, HTML. **No Pro controls, no add-on plugins, no extra font requests.**

---

## 1. Files

| File | What it is |
|---|---|
| `fna-report-section.json` | The template. Import this. |
| `chart-1-adesioni.png` | Sample chart for the side slot (1600 × 612) |
| `chart-2-andamento.png` | Sample chart for the wide slot (1600 × 572) |
| `anteprima-desktop.png` / `-tablet` / `-mobile` | Preview renders |

## 2. Import (2 minutes)

1. WordPress admin → **Templates → Saved Templates**
2. **Import Templates** (top of the page) → choose `fna-report-section.json` → **Import Now**
3. Open the page you want it on with Elementor
4. In the canvas, click the **folder icon** → **My Templates** → find
   *"Relazione / Report — Futuro Nazionale Albignasego"* → **Insert**
5. When asked *"Import the document settings too?"* → **No** (keeps your page settings)

It drops in as one outer container with the CSS class `fna-report`. Everything
inside is a normal Elementor container, so right-click → Duplicate / Delete works
on every block.

## 3. What's inside

```
fna-report                       ← outer container, max 1200px
├── HTML widget                  ← the section's CSS lives here (see §4)
├── Header       eyebrow + H2 + tricolour rule
├── Standfirst   lead paragraph, capped at 760px for readability
├── 3 stat cells                 desktop 3 / tablet 3 / mobile 1
├── Analysis (58%) + side chart (42%)   → stacks on tablet
├── 4 pillar cells (icon box)    desktop 4 / tablet 2 / mobile 1
├── Wide chart cell              full width
├── Pull quote                   navy block
└── Methodology note
```

Breakpoints used are Elementor's own: desktop / tablet ≤1024 / mobile ≤767.

## 4. The background words & pattern

They are **CSS pseudo-elements**, not images or extra widgets — so they cost
nothing to load, never get in the way of the text (they sit at z-index 0 behind
it) and disappear when printing.

All of it lives in the **HTML widget at the very top of the section**. Open it and
you'll find one line per cell:

```css
.fna-report .fna-w-identita::before { content:"IDENTITÀ"; }
.fna-report .fna-w-difesa::before   { content:"DIFESA"; }
```

**To change a word:** edit the text inside `content:"…"`.
**To put a word behind a new cell:** give the container two classes in
*Advanced → CSS Classes* — `fna-cell` plus your own `fna-w-yourword` — then add
one line to the stylesheet.

Size presets (add to the cell alongside `fna-cell`):

| Class | Ghost size | Use for |
|---|---|---|
| *(none)* | 42–80px | full-width cells |
| `fna-ghost-m` | 34–58px | 3-across cells |
| `fna-ghost-s` | 26–38px | 4-across cells |

**Dot pattern instead of a word:** class `fna-pattern` (used on the side chart cell).

**Turn every ghost off at once:** add `fna-ghost-off` to the outer `fna-report`
container. Nothing else changes.

Opacity is 6% of the navy — it sits well under the WCAG contrast of the body text,
which stays #334155 on #F4F7FB.

## 5. Charts

Two image widgets are marked `fna-chart-slot`. Click one → **Choose Image** →
upload your PNG. Nothing else to adjust.

- Side slot — recommended **840 × 640 px**
- Wide slot — recommended **1600 × 600 px**

Images are capped at 520px tall (`object-fit: contain`) so an oversized upload
can't blow the layout apart. The two sample PNGs in this package are real,
brand-coloured examples if you want a starting point.

If you'd rather generate a chart inside Elementor, delete the image widget and
drop any chart widget in its place — the cell styling stays.

## 6. Colours & type used

Taken from your live header/footer and the design on the home page:

| Token | Value | Where |
|---|---|---|
| Navy | `#051632` | headings, quote background — identical to your live header |
| Blue | `#003F84` | eyebrows, stat numbers, icons, keylines |
| Yellow | `#FDD91C` | quote mark, accent |
| Body ink | `#334155` | paragraphs (= Astra global colour 3) |
| Muted | `#64748B` | labels, captions, sources |
| Cell background | `#F4F7FB` | grid cells |
| Cell border | `#E2E8F2` | grid cells |
| Tricolour | `#009246` / `#FFFFFF` / `#CE2B37` | the rule under the H2 |

Type: **Roboto Slab 700** for headings, **Roboto** for body — both already
enqueued by your Elementor kit, so the section adds **zero** extra font requests.

## 7. One thing worth fixing on the site itself

Your Astra palette and your Elementor kit are both still on **stock defaults**
(Astra `#046bd2` blue; Elementor kit primary `#051632`, accent `#61CE70` green).
Nothing on the site actually uses that green, so "inherit the global styles"
currently inherits factory settings rather than your brand.

Recommended (**Elementor → Site Settings → Global Colors**):

```
Primary    #051632     Secondary  #003F84
Text       #334155     Accent     #FDD91C
```

and **Global Fonts**: Primary → Roboto Slab 700, Text → Roboto 400.

Once those are set the section can be switched from fixed hex values to global
references, so a future palette change updates it everywhere at once. Say the
word and I'll ship that variant.
