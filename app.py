from flask import Flask, render_template, jsonify, request
import psycopg
import os
import random
import requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def load_all_flags():
    response = requests.get("https://flagcdn.com/en/codes.json")
    response.raise_for_status()
    return list(response.json().keys())

flags = load_all_flags()

def get_flag_url(code):
    return f"https://flagcdn.com/w320/{code.lower()}.png"

def get_conn():
    return psycopg.connect("host=aws-1-eu-west-1.pooler.supabase.com port=5432 dbname=postgres user=postgres.eockpjperqujlokwapdb password=twigisanidiot sslmode=require")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test_db")
def test_db():
    try:
        conn = get_conn()
        conn.close()
        return jsonify({"status": "connected"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_flag/<int:index>")
def get_flag(index):
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
    try:
        data = request.json
        code = data["code"]
        url = data["url"]
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT code FROM flags WHERE code = %s", (code,))
        existing = cur.fetchone()
        if existing:
            cur.close()
            conn.close()
            return jsonify({"message": "already_saved"}), 200
        cur.execute("INSERT INTO flags (code, url) VALUES (%s, %s)", (code, url))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "saved"})
    except Exception as e:
        print("SAVE ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/get_saved_flags")
def get_saved_flags():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT code, url FROM flags ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"code": r[0], "url": r[1]} for r in rows])
    except Exception as e:
        print("LOAD ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/delete_flag", methods=["DELETE"])
def delete_flag():
    try:
        data = request.json
        code = data["code"]
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM flags WHERE code = %s", (code,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "deleted"})
    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)