# Deployment Guide

This project has two parts:
- `site/` Flask marketing site
- `demo/` Streamlit demo app

You can deploy them together behind a reverse proxy or separately on different services.

## Option A: Simple VPS (Nginx + systemd)
1. Copy the repo to your server.
2. Create a Python virtual environment and install dependencies:
   - `pip install -r site/requirements.txt`
   - `pip install -r demo/requirements.txt`
3. Run the Flask app with a production server (example using Gunicorn):
   - `pip install gunicorn`
   - `gunicorn -w 2 -b 127.0.0.1:5000 site.app:app`
4. Run the Streamlit demo on localhost:
   - `streamlit run demo/demo_app.py --server.port 8501 --server.address 127.0.0.1`
5. Use Nginx to proxy:
   - `/` -> `http://127.0.0.1:5000`
   - `/demo` or a subdomain -> `http://127.0.0.1:8501`

## Option B: Separate Hosts
- Deploy the Flask site on a platform like Render, Fly.io, or a VPS.
- Deploy the Streamlit demo on Streamlit Community Cloud or another host.
- Update `site/templates/demo.html` and `site/templates/thinking.html` to point to the public demo URL.

## Environment Variables
For contact form email, configure these on your host:
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_TO`

## Production Notes
- Set `debug=False` in production.
- Use HTTPS.
- Consider adding CSRF protection if the form is public.
