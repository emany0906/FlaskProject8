from flask import Flask, render_template, jsonify, request
import psycopg

app = Flask(__name__)

# 🔹 Your PostgreSQL connection (replace if needed)
conn = psycopg2.connect(
    host="aws-1-eu-west-1.pooler.supabase.com",
    database="postgres",
    user="postgres.eockpjperqujlokwapdb",
    password="2odqA6x55vUTjDI2",
    port="5432"
)

flags = ["BE", "FR", "DE", "ES", "IT", "IE", "US", "JP"]

def get_flag_url(code):
    return f"https://flagcdn.com/w320/{code.lower()}.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_flag/<int:index>")
def get_flag(index):
    index = index % len(flags)
    code = flags[index]
    url = get_flag_url(code)
    return jsonify({"url": url, "index": index, "code": code})

# ✅ Save flag to DB
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

# ✅ Get all saved flags
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