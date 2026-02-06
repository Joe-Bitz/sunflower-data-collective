# Sunflower Data Collective

Marketing site + interactive demo for Sunflower Data Collective.

## Structure
- `site/` Flask app, templates, and static assets
- `demo/` Streamlit demo app

## Quick Start (Local)
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r site/requirements.txt`
3. Run the Flask site:
   - `python site/app.py`
4. (Optional) Run the Streamlit demo in a separate terminal:
   - `pip install -r demo/requirements.txt`
   - `streamlit run demo/demo_app.py`

The site runs at `http://localhost:5000`. The demo (Streamlit) runs at `http://localhost:8501`.

## Configuration
For email on the contact form, create `site/.env` with:
- `SENDGRID_API_KEY`
- `MAIL_FROM` (must be a verified sender in SendGrid)
- `MAIL_TO`

Optional:
- `DEMO_URL` to point the site demo page to a hosted Streamlit app.
- `SECRET_KEY` to keep contact form CSRF tokens stable across restarts.

## Notes
- `.env` is ignored in git.
- The demo link points to `http://localhost:8501` by default unless `DEMO_URL` is set.
- The root `requirements.txt` is for the Streamlit demo deployment only.
