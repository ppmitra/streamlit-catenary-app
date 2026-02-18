# Deploy to Streamlit Cloud

This guide shows the minimal steps to deploy the `catenary_app.py` Streamlit app to Streamlit Cloud (share.streamlit.io).

Prerequisites:
- A GitHub account
- Your repository committed and pushed to GitHub
- `requirements.txt` present (includes `streamlit`, `numpy`, `scipy`, `matplotlib`)

1) Quick local test

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run catenary_app.py
```

2) Push to GitHub

```bash
git add .
git commit -m "Add catenary Streamlit app"
git push origin main
```

3) Deploy on Streamlit Cloud

- Visit https://share.streamlit.io and sign in with GitHub.
- Click "New app" → select the repo, branch (e.g., `main`) and the main file `catenary_app.py`.
- Click `Deploy` — Streamlit Cloud will install from `requirements.txt` and launch the app.

4) Post-deploy notes

- App auto-redeploys on pushes to the selected branch.
- If your app needs secrets or private tokens, add them in the app settings under "Secrets" on Streamlit Cloud.
- If you want to enforce a specific Python version, add a `runtime.txt` (optional).

Troubleshooting

- If deployment fails, open the app logs from the Streamlit Cloud dashboard to see pip install or runtime errors.
- Common fixes: pin package versions in `requirements.txt`, ensure `streamlit` is listed, remove unsupported system packages.

If you want, I can:
- Run the app locally here to confirm it starts (I can attempt to install requirements), or
- Create a small `.github/workflows` CI file to auto-run a smoke test on push.
