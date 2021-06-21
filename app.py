import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://microblog:ana@microblogapplication.cljcf.mongodb.net/test")
    app.db = client.microblog
    #entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
    #        entries.append((entry_content, formatted_date))   # add tuple
            app.db.entries.insert({"content": entry_content, "date": formatted_date})  # add to MongoDB base

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.today().strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})  # get content from the MongoDB base
        ]

        return render_template("home.html", entries=entries_with_date)

    return app
