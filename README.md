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

## Deploy
Import this repository in Vercel with the default settings (framework preset
"Other", no build command). Every push to `main` deploys.
