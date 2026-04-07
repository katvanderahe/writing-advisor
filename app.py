from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, WritingSample
import requests
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Secret key & DB config
    app.config["SECRET_KEY"] = "change-this-in-production"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///writing.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            user_text = request.form.get("text", "").strip()
            if not user_text:
                return render_template("index.html", error="Please paste some text.", text=user_text)

            # Call external API (mocked here)
            advice = get_writing_advice(user_text)

            sample = WritingSample(text=user_text, advice=advice)
            db.session.add(sample)
            db.session.commit()

            return render_template("index.html", text=user_text, advice=advice)

        return render_template("index.html")

    @app.route("/history")
    def history():
        samples = WritingSample.query.order_by(WritingSample.created_at.desc()).all()
        return render_template("history.html", samples=samples)

    return app


def get_writing_advice(text: str) -> str:
    """
    Replace this with a real writing-improvement API call.
    For now, we simulate an API response.
    """
    # Example of how a real call might look:
    # api_url = "https://api.example.com/v1/writing/advice"
    # api_key = os.environ.get("WRITING_API_KEY")
    # response = requests.post(
    #     api_url,
    #     headers={"Authorization": f"Bearer {api_key}"},
    #     json={"text": text}
    # )
    # response.raise_for_status()
    # data = response.json()
    # return data["advice"]

    # Mocked advice logic
    advice_lines = []
    if len(text.split()) < 50:
        advice_lines.append("Try expanding your ideas with more detail and examples.")
    if any(len(word) > 15 for word in text.split()):
        advice_lines.append("Some words are very long—consider simpler alternatives for clarity.")
    if text.endswith("!"):
        advice_lines.append("Too many exclamation marks can weaken your tone; use them sparingly.")

    if not advice_lines:
        advice_lines.append("Your writing is clear. You could refine rhythm by varying sentence length.")

    return "\n".join(advice_lines)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
