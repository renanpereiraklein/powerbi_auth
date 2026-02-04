import os
import json
from dotenv import load_dotenv
from flask import (
    Flask, request, render_template, redirect, url_for,
    session, abort
)
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False  # aceita /login e /login/

# Secret key (OBRIGATÓRIO em produção)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

# --- Carrega os dados dos usuários: por env JSON OU por arquivo secreto ---
user_data_path = os.getenv("USER_DATA_PATH")  # ex.: /etc/secrets/user_data.json
user_data_json = os.getenv("USER_DATA_JSON")  # opcional, JSON direto na env

if user_data_json:
    users = json.loads(user_data_json)
elif user_data_path and os.path.exists(user_data_path):
    with open(user_data_path, "r", encoding="utf-8") as file:
        users = json.load(file)
else:
    users = {}  # evita crash se faltar dado


# ---------------------------
# Helpers
# ---------------------------
def _get_user(username: str):
    return users.get(username)


def _password_ok(stored: str, provided: str) -> bool:
    """
    Compatível com dois formatos:
    - texto puro (legado): "password": "1234"
    - hash (recomendado): "password": "pbkdf2:sha256:..."
    """
    if not stored:
        return False

    # Heurística simples: hashes do Werkzeug geralmente começam com "pbkdf2:" ou "scrypt:"
    if stored.startswith(("pbkdf2:", "scrypt:")):
        return check_password_hash(stored, provided)

    # fallback legado (texto puro)
    return stored == provided


def login_required():
    if not session.get("user"):
        return False
    return True


# ---------------------------
# Segurança básica / headers
# ---------------------------
@app.after_request
def set_security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["Referrer-Policy"] = "no-referrer"
    # evita cache do dashboard em browser compartilhado
    resp.headers["Cache-Control"] = "no-store"
    return resp


# ---------------------------
# Rotas
# ---------------------------
@app.route("/", methods=["GET", "HEAD"])
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST", "HEAD", "OPTIONS"])
def login():
    if request.method != "POST":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = _get_user(username)
    if user and _password_ok(user.get("password", ""), password):
        session["user"] = username
        return redirect(url_for("dashboard"))

    return render_template("login.html", error="Invalid credentials")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if not login_required():
        return redirect(url_for("login"))

    username = session.get("us
