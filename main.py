from flask import Flask, request, render_template, redirect, url_for
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False  # aceita /login e /login/

# --- Carrega os dados dos usuários: por env JSON OU por arquivo secreto ---
user_data_path = os.getenv('USER_DATA_PATH')            # ex.: /etc/secrets/user_data.json
user_data_json = os.getenv('USER_DATA_JSON')            # opcional, JSON direto na env

if user_data_json:
    users = json.loads(user_data_json)
elif user_data_path and os.path.exists(user_data_path):
    with open(user_data_path, 'r', encoding='utf-8') as file:
        users = json.load(file)
else:
    users = {}  # evita crash se faltar dado

@app.route('/', methods=['GET', 'HEAD'])
def home():
    # sempre manda pra /login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST', 'HEAD', 'OPTIONS'])
def login():
    if request.method != 'POST':
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if username in users and users[username].get('password') == password:
        dashboard_html = users[username].get('dashboard', '')
        return render_template('dashboard.html', dashboard_html=dashboard_html)

    return render_template('login.html', error="Credenciais inválidas!")

@app.errorhandler(405)
def method_not_allowed(_e):
    # se baterem com método estranho, redireciona pro login (resolve Safari/preview)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
