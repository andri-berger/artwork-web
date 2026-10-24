# artwork-web
Artwork- and Layout generator provided as static frontend module.

artwork-web is the browser version of
[artwork-tui](https://github.com/andri-berger/artwork-tui). It generates
abstract artwork out of plain HTML and CSS: hundreds of boxes, lines and
shapes, filled with colors, gradients or classic paintings, then run through
WebGL filters. Every single value behind the picture lives in a spreadsheet,
so you can start with one click on **GENERATE ART** and then change anything
down to a single pixel.

- **No backend.** It's static files plus a few frontend libraries. Nothing is
  uploaded and nothing is fetched from the internet; the local setup never
  talks to print-artwork.com.
- **Your work is kept.** Sliders, tables, chosen painting and uploaded images
  are saved in your browser (`localStorage` and IndexedDB) and come back after
  a refresh.
- **Print-ready output.** DOWNLOAD renders the artwork again at 5× screen
  resolution and saves it as a PNG.

## Installation
artwork-web is a static frontend, but it still needs a web server: every asset
path starts with `/` and the page uses `fetch`, a Web Worker and an iframe, so
opening `index.html` as a file does not work. `serve.py` is a small server
built on the Python standard library. It serves everything from the local
files with no outside connection, and maps `/cd/…` to the local `cdn/` folder.

Always open the page via **http://localhost:8000**, not `127.0.0.1`: the page
only accepts messages from its iframe on the `localhost` hostname.

#### Generic Install (curl)
Downloads the full repo (~1.4 GB, the images are part of it) to
`~/.local/share/artwork-web` and adds an `artwork-web` launcher to
`~/.local/bin`. Requires `python3` (3.7+), `curl` and `tar`. As always with
curl-into-sh: the script is short and readable — take a look before you run it.

```bash
curl -fsSL https://raw.githubusercontent.com/\
andri-berger/artwork-web/main/install.sh | sh
artwork-web --open
```

Run the same command again to update. Options: `--port 9000`, `--open`, `--quiet`.

#### From a clone (for working on it)
```bash
git clone https://github.com/andri-berger/artwork-web
cd artwork-web
python3 serve.py --open

# for experimental html-to-canvas flag
python3 serve.py &
google-chrome --user-data-dir="$HOME/.cache/artwork-web-chrome" \
  --enable-features=CanvasDrawElement http://localhost:8000/
```
Edits show up on reload; the server sends `Cache-Control: no-cache`.

## How it works in one minute
The screen has two halves. The **dashboard** (buttons, sliders and, in Expert
Mode, a spreadsheet) is where you change things. The **canvas** shows the
result.

The artwork itself is a small web page that runs inside an iframe: three
families of elements called **L00**, **K00** and **T00** (up to 100 L00, 100
K00 and 1,000 T00 elements), laid out and styled with CSS. The spreadsheet
holds every one of their properties: size, position, order, margins, rotation,
blur, colors, gradients, blend modes, the painting they are filled with, and
so on. The sliders and GENERATE ART are shortcuts that fill this spreadsheet
for you with seeded random values.

When something changes, the iframe rebuilds the HTML, takes a picture of it,
runs the picture through the filters you picked, and shows that picture on the
canvas. [The full trace](#the-full-trace) below follows one edit through every
step.

## What you can do
Hover over any dashboard button or slider while the info screen (**i**) is on
and the app shows a short help text for it.

### Top buttons
| Button | What it does |
|---|---|
| **GENERATE ART** | Creates a new random artwork in one click. It reads the slider settings, rolls new seeds (unless a seed is locked) and refills the tables. |
| **SHOT** | Shot Mode. Shows the artwork as a rendered picture in a mockup room, with a wall behind it. Padding X/Y and canvas zoom only apply here. |
| **BLEND** | Blends the artwork into the wall (CSS `multiply`), as if it were printed on it. |
| **WALL** | Picks another room. There are 676 walls; the app prefers ones whose shape matches your window. |
| **SLOT** | Slot Mode. Shows the rendered picture full size, without the room. The best view for working on the FX filters. |
| **L00 / K00 / T00** (checkboxes) | Lock the random seed of that element family, so GENERATE ART keeps it and only changes the rest. |
| **F00** | Circle Mode: the Granular filter draws circles instead of blocks (needs SLOT on). |
| **F01** | Stroke Mode: the Granular filter draws strokes instead of filled blocks (needs SLOT on). |
| **F02** | Vector Mode (PNG to SVG). Currently inert: it needed the removed API. |

With both SHOT and SLOT off you get the **HTML view**: the live artwork page
itself, not a picture of it. This is the fastest view while editing, but the
FX filters don't show here.

### Slider panels
The two radio rows pick which slider panel you see. In every panel the first
slider scrolls through the panel's other sliders, two at a time. Drag a slider's
handle to change its value.

| Panel | What it controls |
|---|---|
| **SLOT** (first row) | Global settings: dashboard colors, padding, label size, stacking order, rotations, container width and height, morph and wave (SVG displacement) for everything, and two color palettes (dual colors per family, plus a 6-slot global palette). |
| **L00 / K00 / T00** | The randomizer for one element family: how many elements, how chaotic, average position and spread, how much of the painting fills them (Image A/B), rotation, shift, size, morph, wave and color intensity. |
| **SLOT** (second row) | Creative filter (PixiJS). The first slider picks one of 13 effects: Ascii, Noise, Dot, CRT, Simplex Noise, Glow, Kawase Blur, Advanced Bloom, Zoom Blur, Twist, Bulge/Pinch, Glitch, Reflection. The others tune it. |
| **F00** | Granular filter: block size, spacing, random offsets and stroke thickness. It redraws the picture as many small blocks, circles or strokes. |
| **F01** | Granular shapes for Circle and Stroke Mode: start, end, angle, curves and randomness of each shape. |
| **F02** | Glamour filter (oil painting, sketch, cartoon) and Vector Mode settings. Inert, like the F02 button. |

### Expert Mode: the spreadsheet
The last radio row opens the tables (Handsontable). The label shows where you
are: **Hidden**, **Format** or **Styling**.

| Tab | Rows × columns | What's in it |
|---|---|---|
| **1 · Format** | 245 × 103 | The foundation. One column per element and 18 layout rows each: width, height, alignment, order, offset, margin, padding and which frame an element sits in. |
| **2 · Styling** | 1,304 × 43 | One row per element: position, blur, 3D axes, outline, corner angles, slide, scale, rotation, origin and more. |
| **3 · Styling & Colors** | 1,304 × 42 | One row per element: shape, shade, border and outline fills, gradients, display, blend, drop shadow, brightness, opacity, grayscale, saturation, contrast and image shift. |

Cells outside an element's range are read-only, dropdown cells only accept their listed values, and
the placeholder in an empty cell tells you the expected unit (`px`, `%`,
`deg`, `#hex`, ...). Selecting a cell shows a short explanation with a link to
the MDN docs for that CSS property. Undo, redo, copy, paste and cut work as
usual, and every edit redraws the artwork right away.

### Bottom buttons
| Button | What it does |
|---|---|
| **DOWNLOAD** | Renders the artwork again at 5× screen resolution and saves it as `<timestamp>.png`. Ctrl+Alt+Meta inside the canvas does the same. |
| **Painting browser** (frame icon) | Browse 3,236 paintings by 100 artists (the `cdn/` folder). The painting you pick becomes the texture inside the elements. Use ↑/↓ for the artist and the arrow pair for the painting; the painting's title links to the full image. |
| **?** | Use your own images. **LOAD** picks up to 100 image files; they are kept in IndexedDB and replace the paintings in the browser. Cancel the picker to go back to the paintings. |
| **i** | Info screen with a short tour of the app, and hover help for every control. |
| Last two buttons | Move the dashboard up/down and left/right. |
| **X / GO!** | In the browser: close it, or jump to the next artist. |

### Where your work is saved
Everything stays in your browser, for this site only:

- `localStorage` key `IC` holds the UI: slider values, toggles, the open
  panel, the wall and the painting position.
- `localStorage` key `ID` holds seeds and palette colors, and `IB` remembers
  which painting you last used per artist.
- IndexedDB database `IB` holds the spreadsheet edits and your uploaded
  images.

On load the app reads all of this back and redraws the same artwork. A
damaged `localStorage` entry is dropped instead of breaking the app. To start
fresh, clear the site data for `localhost` in your browser.

## The full trace
What happens between typing a value into a cell and seeing it on the canvas:

```mermaid
flowchart TD
    A["Spreadsheet edit or slider<br/>(main page, =/model-0.2.js)"] -->|"save"| S[("localStorage + IndexedDB")]
    A -->|"postMessage: only the changed cells"| B["iframe (iframe.html, =/script-0.0.js)<br/>merges the change"]
    B --> C["Artwork generator (=/script-0.1.js)<br/>rebuilds the SVG filters, the element HTML and 2 style sheets"]
    C --> D{"Capture the HTML as a picture"}
    D -->|"Chrome with HTML-in-Canvas"| E["native drawElementImage"]
    D -->|"otherwise"| F["html-to-image (loaded on demand)"]
    E --> G["PixiJS + pixi-filters<br/>Creative filter (WebGL)"]
    F --> G
    G --> H["Web Worker (=/script-0.2.js)<br/>Granular filter: blocks, circles, strokes"]
    H --> I["Canvas on screen (3×)"]
    H --> J["DOWNLOAD: same steps at 5× → PNG"]
```

Step by step, in plain words:

1. **You change something.** A cell edit, a slider or GENERATE ART on the main
   page turns into a small list of changed values. The main page saves it
   (`localStorage` and IndexedDB) and sends only that change to the iframe with
   `postMessage`. The iframe only listens on `localhost`, which is why
   `127.0.0.1` doesn't work.
2. **The iframe rebuilds the artwork page.** It merges the change into its
   copy of the tables, and the generator writes new HTML: an `<svg>` with
   morph and wave filters, the `<div>` tree of L00/K00/T00 elements and two
   `<style>` sheets. Depending on which table changed, only the affected parts
   are rewritten. The artwork is then centered.
3. **It takes a picture of that page.** Where the browser supports
   HTML-in-Canvas (`drawElementImage`), the page is drawn natively into a
   canvas, after waiting for images and fonts. Otherwise, or if that fails,
   times out or comes out blank, it loads `html-to-image` and uses that
   instead. Both give the same result (they differ in under 0.15% of pixels).
   The picture is taken at 3× for the screen and 5× for DOWNLOAD, then cropped
   to the artwork plus padding.
4. **WebGL filters.** If a Creative filter is chosen, PixiJS puts the picture
   on a sprite, applies the filter and reads the result back.
5. **Pixel filter.** If Granular settings are on, a Web Worker repaints the
   picture as blocks, circles or strokes on an OffscreenCanvas, sampling the
   color underneath each one.
6. **Show or save.** The final picture goes onto the canvas you see (SHOT or
   SLOT), or into a PNG file (DOWNLOAD).

Each stage keeps its result. If you only move a filter slider, the app reruns
the stages from that filter on and reuses the earlier picture, which keeps
dragging smooth. Captures that pile up while you drag are merged, so only the
latest one is drawn.

## File layout
Everything is plain static files. Paths are absolute from the site root
(`/=/`, `/@/`, ...), which is why it needs `serve.py`. The original
unminified sources are lost, so the files in `=/` are minified and are the
source.

| Path | What's in it |
|---|---|
| `index.html` | The main page: dashboard, tables and the iframe. |
| `iframe.html` | The artwork page that gets rendered. |
| `serve.py`, `install.sh` | Local server and the curl installer (see Installation). |
| `frame.js` | Service worker stub; only registers on print-artwork.com. |
| `=/model-0.2.js` | Main page logic: buttons, sliders, tables, saving and the messages to the iframe. |
| `=/model-0.0.js`, `=/model-0.1.js` | Data: help texts, table layouts and dropdown values, the painting catalog, the wall list. |
| `=/script-0.0.js` | iframe renderer: capture, PixiJS filters, worker, display and download. |
| `=/script-0.1.js` | Artwork generator: turns the tables into SVG, HTML and CSS. |
| `=/script-0.2.js` | Web Worker for the Granular filter. |
| `=/style-0.1.css`, `=/style-0.0.css` | Styles for the main page and the iframe. |
| `=/bundle/` | Blank placeholder images. |
| `@/` | Third-party libraries (see below). `@/bundle/` holds the Montserrat font, `@/bundles/` the app icons. |
| `cdn/` | 3,236 paintings by 100 artists (AVIF), one folder per artist. Served as `/cd/` too. |
| `fonts/` | Full-size wall photos for SHOT/WALL. Despite the name, there are no fonts in here. |
| `frame/` | Small previews of the same walls, shown while the full one loads. |
| `cdns/` | Product mockup photos from the former print shop. |

## Built with
These libraries ship in `@/`, unchanged:

| Library | Version | Used for | License |
|---|---|---|---|
| [Handsontable](https://github.com/handsontable/handsontable) | 12.0.0 | The spreadsheet in Expert Mode | Proprietary, used under its free non-commercial license |
| [PixiJS](https://github.com/pixijs/pixijs) | 8.10.1 | WebGL rendering (`@/pixi-filter-8.10.1.js`) | MIT |
| [pixi-filters](https://github.com/pixijs/filters) | 6.1.3 | The 13 Creative filters | MIT |
| [html-to-image](https://github.com/bubkoo/html-to-image) | 1.11.13 | Capture fallback when HTML-in-Canvas isn't available | MIT |
| [d3-random](https://github.com/d3/d3-random) | 3.0.1 | Seeded random numbers, so a seed always gives the same artwork | ISC |
| [Montserrat](https://github.com/JulietaUla/Montserrat) | 9.000 | Dashboard font | SIL OFL 1.1 |
| [HTML-in-Canvas](https://github.com/WICG/html-in-canvas) | (browser API) | Native capture of the artwork page | — |

**Third-party note.** The license in `LICENSE` covers this project's own code.
It does not cover the libraries above, which keep their own licenses.
Handsontable in particular is not open source: it is free for non-commercial
use only, and commercial use needs a license from Handsoncode. The paintings in
`cdn/` are reproductions of artworks that are mostly in the public domain. The
wall and mockup photos have their own terms, separate from the code license.

## Inspiration
No code, purely visual debts. The Pinterest board is the moodboard this tool
was built to chase, and print-artwork.com is the commercial ancestor that
artwork-web and its sibling projects were carved out of.

- Pinterest: https://de.pinterest.com/andriberger/_saved
- Artwork: https://print-artwork.com
