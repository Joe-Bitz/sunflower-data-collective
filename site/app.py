import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/thinking")
def thinking():
    return render_template("thinking.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")

    # --- Read form fields ---
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    company = (request.form.get("company") or "").strip()
    message = (request.form.get("message") or "").strip()
    form_data = {
        "name": name,
        "email": email,
        "company": company,
        "message": message,
    }

    # --- Basic validation ---
    if not name or not email or not message:
        return render_template(
            "contact.html",
            error="Please fill out name, email, and message.",
            form_data=form_data,
        )

    # --- Email config from .env ---
    mail_server = os.getenv("MAIL_SERVER")
    mail_port = int(os.getenv("MAIL_PORT", "587"))
    mail_use_tls = os.getenv("MAIL_USE_TLS", "true").lower() == "true"

    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_to = os.getenv("MAIL_TO")

    if not all([mail_server, mail_username, mail_password, mail_to]):
        return render_template(
            "contact.html",
            error="Email is not configured on the server yet.",
            form_data=form_data,
        )

    try:
        # --- Build email ---
        msg = EmailMessage()
        msg["Subject"] = f"New contact form: {name}"
        msg["From"] = mail_username
        msg["To"] = mail_to
        msg["Reply-To"] = email  # so you can reply directly to the sender

        body = f"""New message from Sunflower Data Collective site

Name: {name}
Email: {email}
Company: {company}

Message:
{message}
"""
        msg.set_content(body)

        # --- Send ---
        with smtplib.SMTP(mail_server, mail_port) as smtp:
            if mail_use_tls:
                smtp.starttls()
            smtp.login(mail_username, mail_password)
            smtp.send_message(msg)

        return render_template("contact.html", success=True)

    except Exception as e:
        print(f"Contact form error: {e}")
        return render_template(
            "contact.html",
            error="Could not send your message right now. Please try again.",
            form_data=form_data,
        )


@app.route("/demo")
def demo():
    return render_template("demo.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
