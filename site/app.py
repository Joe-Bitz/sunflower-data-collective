import os
import secrets

from flask import Flask, render_template, request, session
from dotenv import load_dotenv

from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)
load_dotenv()


def _get_secret_key() -> str:
    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        return secret_key

    flask_env = (os.getenv("FLASK_ENV") or "").lower()
    flask_debug = (os.getenv("FLASK_DEBUG") or "").strip() == "1"
    is_local_run = __name__ == "__main__"
    if flask_env in {"development", "dev", "local"} or flask_debug or is_local_run:
        return secrets.token_hex(32)

    raise RuntimeError("SECRET_KEY must be set outside local development")


app.secret_key = _get_secret_key()
DEMO_URL = os.getenv("DEMO_URL", "")


def _ensure_csrf_token() -> str:
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

    if not all((api_key, mail_to, mail_from)):
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
        to_emails=mail_to,
        subject=subject,
        plain_text_content=body,
    )
    # So you can hit "Reply" and respond to the person who filled out the form
    mail.reply_to = email

    sg = SendGridAPIClient(api_key)
    resp = sg.send(mail)
    if not 200 <= resp.status_code < 300:
        raise RuntimeError(f"SendGrid returned non-success status: {resp.status_code}")
    return resp.status_code


def _get_contact_form_data() -> tuple[dict[str, str], str | None]:
    form_data = {
        "name": (request.form.get("name") or "").strip(),
        "email": (request.form.get("email") or "").strip(),
        "company": (request.form.get("company") or "").strip(),
        "message": (request.form.get("message") or "").strip(),
    }
    csrf_token = request.form.get("csrf_token")
    return form_data, csrf_token


def _validate_contact_form(form_data: dict[str, str], csrf_token: str | None) -> str | None:
    if not csrf_token or csrf_token != session.get("csrf_token"):
        return "Your session expired. Please refresh and try again."

    if not form_data["name"] or not form_data["email"] or not form_data["message"]:
        return "Please fill out name, email, and message."

    return None


def _render_contact(*, error: str | None = None, success: bool = False, form_data: dict[str, str] | None = None):
    return render_template(
        "contact.html",
        error=error,
        success=success,
        form_data=form_data,
        csrf_token=_ensure_csrf_token(),
    )


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
        return _render_contact()

    form_data, csrf_token = _get_contact_form_data()
    validation_error = _validate_contact_form(form_data, csrf_token)
    if validation_error:
        return _render_contact(error=validation_error, form_data=form_data)

    try:
        _send_contact_email_sendgrid(
            form_data["name"],
            form_data["email"],
            form_data["company"],
            form_data["message"],
        )

        session.pop("csrf_token", None)
        return _render_contact(success=True)

    except (RuntimeError, HTTPError):
        app.logger.exception("Contact form error")
        return _render_contact(
            error="Could not send your message right now. Please try again.",
            form_data=form_data,
        )


if __name__ == "__main__":
    # For local dev; Render will run via gunicorn typically
    app.run(debug=True, use_reloader=False)
