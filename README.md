# artwork-web
Artwork- and Layout generator provided as static frontend module .

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
```
Edits show up on reload; the server sends `Cache-Control: no-cache`.


## API Credit
This tool stands on other people's work, and the table below is meant as more
than a dependency list. Entries are grouped by layer: **Build** covers what
produces the README assets, **Utility** the Python and JavaScript toolchain —
including d3-random, whose seedable generators are what makes reproducible
artwork possible in the first place. **Framework** is the TUI foundation,
while **Conversion** and **Processing** form the rendering heart: Playwright
drives the browser, Chromium's HTML-in-Canvas API rasterizes the composed
layout, and the PixiJS filter collection provides the WebGL effects layered on
top. The layout engine itself is homegrown, but it would have nothing to run on
without these.

The **Inspiration** entries are of a different kind than in filterx-tui: no
code, not even patterns — purely visual debts. The linked Pinterest board is
the moodboard this tool was built to chase, and print-artwork.com is the
commercial ancestor both sibling projects were carved out of. If you want to
understand what the random generator is aiming at aesthetically, those two
links say more than any parameter documentation could.

<table width="100%">
    <tr>
        <th align="left">Layer</th>
        <th align="left">Name</th>
        <th align="left"><img src="artwork/Frontend/model.png" width="9999" height="0" align="right" alt="">Link</th>
    </tr>
    <tr>
        <td><kbd>
        Build</kbd></td>
        <td>Apng</td><td>
        <a href="//github.com/apngasm/apngasm">
        https://github.com/apngasm/apng</a></td>
    </tr>
    </tr>
        <tr><td><kbd>
        Build</kbd></td>
        <td>Grim</td><td>
        <a href="//github.com/emersion/grim">
        https://github.com/emersion/grim</a></td>
    </tr>
    <tr>
        <td><kbd>
        Utilities</kbd></td>
        <td>Random</td><td>
        <a href="https://github.com/d3/d3-random">
        https://github.com/d3/d3-random</a></td>
    </tr>
    <tr>
        <td><kbd>
        Conversion</kbd></td>
        <td>Canvas Img</td><td>
        <a href="https://github.com/WICG/html-in-canvas">
        https://github.com/html-in-canvas</a></td>
    </tr>
    <tr>
        <td><kbd>
        Processing</kbd></td>
        <td>Pixi Filter</td><td>
        <a href="//github.com/pixijs/filters">
        https://github.com/pixijs/filters</a></td>
    </tr>
    <tr>
        <td><kbd>
        Inspiration</kbd></td>
        <td>Pinterest</td><td>
        <a href="//de.pinterest.com/andriberger/_saved">
        https://de.pinterest.com/andri</a></td>
    </tr>
    <tr>
        <td><kbd>
        Inspiration</kbd></td>
        <td>Artwork</td><td>
        <a href="//print-artwork.com">
        https://print-artwork.com</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; </td> 
    </tr>
</table>

## PI Gallery
Thirty layouts straight from the random generator — where the filterx gallery
shows one image transformed many ways, this one shows the opposite: many
compositions from one machine. Each piece below was generated with Create,
rendered through the Playwright/PixiJS pipeline, and exported untouched; the
differences between them are nothing but different values in the six-tab
spreadsheet.

None of these are dead ends, either. Every png in the grid has a json sibling
carrying its complete parameter set — reopen it, change a seed or a single
cell, and you get a variation instead of starting over. Filenames are the
Unix timestamps of their render runs, left as-is: batch outputs, not a
curated portfolio. Click any thumbnail for full resolution.

<table>
  <tr>
    <td><a href="artwork/Backend/module/17000000000.png">
    <img src="artwork/Backend/module/17000000000.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000001.png">
    <img src="artwork/Backend/module/17000000001.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000002.png">
    <img src="artwork/Backend/module/17000000002.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000003.png">
    <img src="artwork/Backend/module/17000000003.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000004.png">
    <img src="artwork/Backend/module/17000000004.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000005.png">
    <img src="artwork/Backend/module/17000000005.png">
    </a></td>
  </tr>
  <tr>
    <td><a href="artwork/Backend/module/17000000006.png">
    <img src="artwork/Backend/module/17000000006.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000007.png">
    <img src="artwork/Backend/module/17000000007.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000008.png">
    <img src="artwork/Backend/module/17000000008.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000009.png">
    <img src="artwork/Backend/module/17000000009.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000010.png">
    <img src="artwork/Backend/module/17000000010.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000011.png">
    <img src="artwork/Backend/module/17000000011.png">
    </a></td>
  </tr>
  <tr>
    <td><a href="artwork/Backend/module/17000000012.png">
    <img src="artwork/Backend/module/17000000012.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000013.png">
    <img src="artwork/Backend/module/17000000013.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000014.png">
    <img src="artwork/Backend/module/17000000014.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000015.png">
    <img src="artwork/Backend/module/17000000015.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000016.png">
    <img src="artwork/Backend/module/17000000016.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000017.png">
    <img src="artwork/Backend/module/17000000017.png">
    </a></td>
  </tr>
  <tr>
    <td><a href="artwork/Backend/module/17000000018.png">
    <img src="artwork/Backend/module/17000000018.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000019.png">
    <img src="artwork/Backend/module/17000000019.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000020.png">
    <img src="artwork/Backend/module/17000000020.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000021.png">
    <img src="artwork/Backend/module/17000000021.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000022.png">
    <img src="artwork/Backend/module/17000000022.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000023.png">
    <img src="artwork/Backend/module/17000000023.png">
    </a></td>
  </tr>
  <tr>
    <td><a href="artwork/Backend/module/17000000024.png">
    <img src="artwork/Backend/module/17000000024.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000025.png">
    <img src="artwork/Backend/module/17000000025.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000026.png">
    <img src="artwork/Backend/module/17000000026.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000027.png">
    <img src="artwork/Backend/module/17000000027.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000028.png">
    <img src="artwork/Backend/module/17000000028.png">
    </a></td>
    <td><a href="artwork/Backend/module/17000000029.png">
    <img src="artwork/Backend/module/17000000029.png">
    </a></td>
  </tr>
</table>
