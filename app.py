import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from db import get_conn, init_db
from ai_service import analyze_text_with_groq

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = {"txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ Initialize the database when app starts (Flask 3.x compatible)
with app.app_context():
    init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/upload", methods=["POST"])
def upload_contract():
    f = request.files.get("file")
    if not f or not allowed_file(f.filename):
        return jsonify({"error": "Please upload a .txt file"}), 400

    filename = secure_filename(f.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(filepath)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO contracts (filename, filepath) VALUES (?, ?)", (filename, filepath))
    conn.commit()
    contract_id = cur.lastrowid
    conn.close()
    return jsonify({"contract_id": contract_id, "filename": filename}), 201

@app.route("/analyze/<int:contract_id>", methods=["POST"])
def analyze(contract_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Contract not found"}), 404

    with open(row["filepath"], "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    result = analyze_text_with_groq(text)
    cur.execute("INSERT INTO analyses (contract_id, result, model) VALUES (?, ?, ?)", 
                (contract_id, result, "llama-3.1-8b-instant"))
    conn.commit()
    conn.close()

    return jsonify({"contract_id": contract_id, "analysis_result": result}), 200

@app.route("/results/<int:contract_id>")
def results(contract_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses WHERE contract_id = ?", (contract_id,))
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(debug=True, port=5000)