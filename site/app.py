import os
import secrets

from flask import Flask, render_template, request, session
from dotenv import load_dotenv

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
DEMO_URL = os.getenv("DEMO_URL", "")


def _ensure_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def _send_contact_email_sendgrid(name: str, email: str, company: str, message_text: str) -> int:
    """
    Sends contact form email via SendGrid HTTPS API (works on Render free tier).
    Env vars required:
      - SENDGRID_API_KEY
      - MAIL_TO (destination email)
      - MAIL_FROM (verified sender in SendGrid)
    """
    api_key = os.getenv("SENDGRID_API_KEY")
    mail_to = os.getenv("MAIL_TO")
    mail_from = os.getenv("MAIL_FROM")

    if not all([api_key, mail_to, mail_from]):
        raise RuntimeError("SendGrid email environment variables not configured")

    subject = f"New contact form: {name}"

    body = f"""New message from Sunflower Data Collective site

Name: {name}
Email: {email}
Company: {company}

Message:
{message_text}
"""

    mail = Mail(
        from_email=mail_from,          # must be verified in SendGrid
        to_emails=mail_to,             # where you receive it (josephbitz@gmail.com)
        subject=subject,
        plain_text_content=body,
    )
    # So you can hit "Reply" and respond to the person who filled out the form
    mail.reply_to = email

    sg = SendGridAPIClient(api_key)
    resp = sg.send(mail)
    return resp.status_code


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/thinking")
def thinking():
    return render_template("thinking.html", demo_url=DEMO_URL)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/demo")
def demo():
    return render_template("demo.html", demo_url=DEMO_URL)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", csrf_token=_ensure_csrf_token())

    # --- Read form fields ---
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    company = (request.form.get("company") or "").strip()
    message_text = (request.form.get("message") or "").strip()
    csrf_token = request.form.get("csrf_token")

    form_data = {
        "name": name,
        "email": email,
        "company": company,
        "message": message_text,
    }

    # --- Basic validation ---
    if not csrf_token or csrf_token != session.get("csrf_token"):
        return render_template(
            "contact.html",
            error="Your session expired. Please refresh and try again.",
            form_data=form_data,
            csrf_token=_ensure_csrf_token(),
        )

    if not name or not email or not message_text:
        return render_template(
            "contact.html",
            error="Please fill out name, email, and message.",
            form_data=form_data,
            csrf_token=_ensure_csrf_token(),
        )

    try:
        _send_contact_email_sendgrid(name, email, company, message_text)

        session.pop("csrf_token", None)
        return render_template("contact.html", success=True, csrf_token=_ensure_csrf_token())

    except Exception:
        app.logger.exception("Contact form error")
        return render_template(
            "contact.html",
            error="Could not send your message right now. Please try again.",
            form_data=form_data,
            csrf_token=_ensure_csrf_token(),
        )


if __name__ == "__main__":
    # For local dev; Render will run via gunicorn typically
    app.run(debug=True, use_reloader=False)
