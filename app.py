from flask import Flask, render_template, jsonify, request
import psycopg
import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = psycopg.connect(os.getenv("DATABASE_URL"))



# Fetch all flag codes from flagcdn on startup
def load_all_flags():
    response = requests.get("https://flagcdn.com/en/codes.json")
    response.raise_for_status()
    return list(response.json().keys())  # e.g. ["af", "ax", "al", ...]

flags = load_all_flags()

def get_flag_url(code):
    return f"https://flagcdn.com/w320/{code.lower()}.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_flag/<int:index>")
def get_flag(index):
    # Use index to seed so the same index always returns the same flag,
    # but spread across all available flags randomly
    code = flags[index % len(flags)]
    url = get_flag_url(code)
    return jsonify({"url": url, "index": index, "code": code})

@app.route("/get_random_flag")
def get_random_flag():
    code = random.choice(flags)
    url = get_flag_url(code)
    index = flags.index(code)
    return jsonify({"url": url, "index": index, "code": code})

@app.route("/save_flag", methods=["POST"])
def save_flag():
    data = request.json
    code = data["code"]
    url = data["url"]

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO flags (code, url) VALUES (%s, %s)",
        (code, url)
    )
    conn.commit()
    cur.close()

    return jsonify({"message": "saved"})

@app.route("/get_saved_flags")
def get_saved_flags():
    cur = conn.cursor()
    cur.execute("SELECT code, url FROM flags ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()

    flags_list = [{"code": r[0], "url": r[1]} for r in rows]
    return jsonify(flags_list)

if __name__ == "__main__":
    app.run(debug=True)