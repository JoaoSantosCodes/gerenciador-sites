from flask import Flask, request, jsonify, session
from backend.auth.auth_service import create_user, authenticate_user
from backend.database.credential_service import add_credential, list_credentials, update_credential, delete_credential
from backend.database.models import SessionLocal, User
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:8080"])
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# Segurança do cookie de sessão
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'

load_dotenv()

# Helper para obter user_id da sessão

def get_user_id():
    return session.get("user_id")

def get_username():
    return session.get("username")

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    logger.info(f"[REGISTER] username={username}")
    if not username or not password:
        logger.warning("[REGISTER] Usuário e senha obrigatórios.")
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400
    if create_user(username, password):
        logger.info(f"[REGISTER] Usuário cadastrado: {username}")
        return jsonify({"message": "Usuário cadastrado com sucesso!"})
    logger.warning(f"[REGISTER] Usuário já existe: {username}")
    return jsonify({"error": "Usuário já existe."}), 409

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    logger.info(f"[LOGIN] username={username}")
    if not username or not password:
        logger.warning("[LOGIN] Usuário e senha obrigatórios.")
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400
    if authenticate_user(username, password):
        session["username"] = username
        db = SessionLocal()
        user = db.query(User).filter_by(username=username).first()
        session["user_id"] = user.id
        db.close()
        logger.info(f"[LOGIN] Sucesso: {username}")
        return jsonify({"message": "Login realizado com sucesso!"})
    logger.warning(f"[LOGIN] Falha: {username}")
    return jsonify({"error": "Usuário ou senha inválidos."}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout realizado."})

@app.route("/api/credentials", methods=["GET"])
def get_credentials():
    user_id = get_user_id()
    logger.info(f"[CREDENTIALS][GET] user_id={user_id}")
    if not user_id:
        logger.warning("[CREDENTIALS][GET] Não autenticado.")
        return jsonify({"error": "Não autenticado."}), 401
    creds = list_credentials(user_id)
    logger.info(f"[CREDENTIALS][GET] {len(creds)} credenciais retornadas.")
    return jsonify(creds)

@app.route("/api/credentials", methods=["POST"])
def add_cred():
    user_id = get_user_id()
    logger.info(f"[CREDENTIALS][ADD] user_id={user_id}")
    if not user_id:
        logger.warning("[CREDENTIALS][ADD] Não autenticado.")
        return jsonify({"error": "Não autenticado."}), 401
    data = request.json
    site = data.get("site_name")
    url = data.get("url")
    username = data.get("username")
    password = data.get("password")
    notes = data.get("notes", "")
    if not site or not username or not password:
        logger.warning("[CREDENTIALS][ADD] Campos obrigatórios ausentes.")
        return jsonify({"error": "Campos obrigatórios ausentes."}), 400
    if add_credential(user_id, site, url, username, password, notes):
        logger.info(f"[CREDENTIALS][ADD] Credencial adicionada para user_id={user_id}, site={site}")
        return jsonify({"message": "Credencial adicionada!"})
    logger.error(f"[CREDENTIALS][ADD] Erro ao adicionar credencial para user_id={user_id}, site={site}")
    return jsonify({"error": "Erro ao adicionar credencial."}), 500

@app.route("/api/credentials/<int:cred_id>", methods=["PUT"])
def edit_cred(cred_id):
    user_id = get_user_id()
    logger.info(f"[CREDENTIALS][EDIT] user_id={user_id}, cred_id={cred_id}")
    if not user_id:
        logger.warning("[CREDENTIALS][EDIT] Não autenticado.")
        return jsonify({"error": "Não autenticado."}), 401
    data = request.json
    updates = {}
    for field in ["site_name", "url", "username", "password", "notes"]:
        if field in data:
            updates[field] = data[field]
    if update_credential(cred_id, user_id, **updates):
        logger.info(f"[CREDENTIALS][EDIT] Credencial atualizada cred_id={cred_id}")
        return jsonify({"message": "Credencial atualizada!"})
    logger.error(f"[CREDENTIALS][EDIT] Erro ao atualizar credencial cred_id={cred_id}")
    return jsonify({"error": "Erro ao atualizar credencial."}), 404

@app.route("/api/credentials/<int:cred_id>", methods=["DELETE"])
def delete_cred(cred_id):
    user_id = get_user_id()
    logger.info(f"[CREDENTIALS][DELETE] user_id={user_id}, cred_id={cred_id}")
    if not user_id:
        logger.warning("[CREDENTIALS][DELETE] Não autenticado.")
        return jsonify({"error": "Não autenticado."}), 401
    if delete_credential(cred_id, user_id):
        logger.info(f"[CREDENTIALS][DELETE] Credencial excluída cred_id={cred_id}")
        return jsonify({"message": "Credencial excluída!"})
    logger.error(f"[CREDENTIALS][DELETE] Erro ao excluir credencial cred_id={cred_id}")
    return jsonify({"error": "Erro ao excluir credencial."}), 404

if __name__ == "__main__":
    env = os.environ.get("FLASK_ENV", "development")
    port = 5000
    print(f"\n[INFO] Gerenciador de Sites e Senhas - Flask API")
    print(f"[INFO] Ambiente: {env}")
    print(f"[INFO] Porta: {port}")
    if os.environ.get("SECRET_KEY", "dev_secret_key") == "dev_secret_key":
        print("[ATENÇÃO] Usando SECRET_KEY padrão! Defina uma chave forte no .env para produção.")
    print("[INFO] Variáveis de ambiente carregadas do .env (se existir).\n")
    app.run(debug=(env=="development"), port=port) 