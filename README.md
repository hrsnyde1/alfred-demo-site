# Harbor & Pine Studio (demo site)

A small website that Alfred's development team builds on, so the whole flow can
be tested for real: owner text → Alfred → CTO plan → frontend and backend agents
→ QA, Reviewer and Security → GitHub → live on Vercel.

## What's here
- `index.html`, `styles.css`, `app.js`: the frontend. Plain HTML, CSS and JS with
  no build step. Every colour comes from a design token in `:root`.
- `api/tip.py`: the backend. A Vercel Python function serving `GET /api/tip`.
- `tests/`: standard-library `unittest` tests for the page and the API.

## Run the tests

```bash
python3 -m unittest discover -v
```

## Preview locally
For now the site runs on this machine only (no Vercel yet):

```bash
python3 serve.py
```

Then open http://127.0.0.1:8080. `serve.py` serves the pages and runs
`api/*.py` the way Vercel would.

## Deploy (later)
Import this repository in Vercel with the default settings (framework preset
"Other", no build command). Every push to `main` deploys.
