from flask import Flask, request, render_template
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Caminho do JSON vindo do .env
user_data_path = os.getenv('USER_DATA_PATH')

# Carrega os dados dos usuários
with open(user_data_path, 'r') as file:
    users = json.load(file)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username]['password'] == password:
        dashboard_html = users[username]['dashboard']
        return render_template('dashboard.html', dashboard_html=dashboard_html)
    else:
        return render_template('login.html', error="Credenciais inválidas!")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
