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
