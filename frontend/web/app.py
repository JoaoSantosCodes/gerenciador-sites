from flask import Flask, render_template_string, request, redirect, session, url_for, flash, send_file
from backend.auth.auth_service import create_user, authenticate_user
from backend.database.credential_service import list_credentials, add_credential, update_credential, delete_credential
from backend.database.models import get_user_id
from datetime import datetime, timedelta
from backend.crypto.crypto_service import encrypt, decrypt
import io, json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Troque para produção

# Templates simples inline para protótipo
login_template = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Login / Cadastro</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container mt-5" style="max-width: 400px;">
  <div class="card shadow">
    <div class="card-body">
      <h2 class="mb-4">Login / Cadastro</h2>
      <form method="post">
        <div class="mb-3">
          <label class="form-label">Usuário:</label>
          <input name="username" class="form-control">
        </div>
        <div class="mb-3">
          <label class="form-label">Senha:</label>
          <input name="password" type="password" class="form-control">
        </div>
        <button name="action" value="login" class="btn btn-primary">Login</button>
        <button name="action" value="register" class="btn btn-secondary ms-2">Cadastrar</button>
      </form>
      {% if msg %}<div class="alert alert-info mt-3">{{ msg }}</div>{% endif %}
    </div>
  </div>
</div>
</body>
</html>
'''

def is_weak_password(password):
    if len(password) < 8:
        return True
    if password.isalpha() or password.isdigit():
        return True
    return False

dash_template = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Dashboard</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container mt-4">
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h2>Dashboard - {{ user }}</h2>
    <a href="{{ url_for('logout') }}" class="btn btn-outline-danger">Logout</a>
  </div>
  <div class="row">
    <div class="col-md-7">
      <h4>Credenciais</h4>
      <ul class="list-group mb-4">
      {% for c in creds %}
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <b>{{ c.site_name }}</b>
            {% if c.weak %}<span class="badge bg-warning text-dark ms-2" title="Senha fraca">⚠️</span>{% endif %}
            {% if c.old %}<span class="badge bg-danger ms-1" title="Senha antiga">⏰</span>{% endif %}<br>
            <small>Usuário: {{ c.username }}<br>Senha: {{ c.password }}</small>
          </div>
          <div>
            <a href="{{ url_for('edit_cred', cred_id=c.id) }}" class="btn btn-sm btn-warning me-1">Editar</a>
            <a href="{{ url_for('delete_cred', cred_id=c.id) }}" class="btn btn-sm btn-danger">Excluir</a>
          </div>
        </li>
      {% endfor %}
      </ul>
      <form method="post" action="{{ url_for('import_backup') }}" enctype="multipart/form-data" class="mt-3">
        <label class="form-label">Importar backup (.backup):</label>
        <input type="file" name="backupfile" accept=".backup" class="form-control mb-2" required>
        <button type="submit" class="btn btn-secondary">Importar</button>
        <a href="{{ url_for('export_backup') }}" class="btn btn-success ms-2">Exportar/Backup</a>
      </form>
    </div>
    <div class="col-md-5">
      <h4>Adicionar nova</h4>
      <form method="post" action="{{ url_for('add_cred') }}">
        <div class="mb-2">
          <label class="form-label">Site:</label>
          <input name="site_name" class="form-control">
        </div>
        <div class="mb-2">
          <label class="form-label">URL:</label>
          <input name="url" class="form-control">
        </div>
        <div class="mb-2">
          <label class="form-label">Usuário:</label>
          <input name="username" class="form-control">
        </div>
        <div class="mb-2">
          <label class="form-label">Senha:</label>
          <input name="password" class="form-control">
        </div>
        <div class="mb-2">
          <label class="form-label">Notas:</label>
          <input name="notes" class="form-control">
        </div>
        <button type="submit" class="btn btn-success">Adicionar</button>
      </form>
    </div>
  </div>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if request.form['action'] == 'login':
            if authenticate_user(username, password):
                session['user'] = username
                return redirect(url_for('dashboard'))
            else:
                msg = 'Usuário ou senha inválidos!'
        elif request.form['action'] == 'register':
            if create_user(username, password):
                msg = 'Usuário cadastrado! Faça login.'
            else:
                msg = 'Usuário já existe!'
    return render_template_string(login_template, msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    user_id = get_user_id(user)
    creds = list_credentials(user_id)
    # Marcar senhas fracas e antigas
    for c in creds:
        c['weak'] = is_weak_password(c['password'])
        last_mod = c.get('last_modified')
        c['old'] = False
        if last_mod:
            try:
                dt = datetime.fromisoformat(last_mod)
                if dt < datetime.utcnow() - timedelta(days=90):
                    c['old'] = True
            except Exception:
                pass
    return render_template_string(dash_template, user=user, creds=creds)

@app.route('/add', methods=['POST'])
def add_cred():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id(session['user'])
    add_credential(user_id, request.form['site_name'], request.form['url'], request.form['username'], request.form['password'], request.form['notes'])
    return redirect(url_for('dashboard'))

@app.route('/edit/<int:cred_id>', methods=['GET', 'POST'])
def edit_cred(cred_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id(session['user'])
    creds = list_credentials(user_id)
    cred = next((c for c in creds if c['id'] == cred_id), None)
    if not cred:
        return 'Credencial não encontrada', 404
    if request.method == 'POST':
        updates = {k: request.form[k] for k in ['site_name', 'url', 'username', 'password', 'notes']}
        update_credential(cred_id, user_id, **updates)
        return redirect(url_for('dashboard'))
    # Formulário simples de edição
    form = f'''
    <h2>Editar Credencial</h2>
    <form method="post">
      Site: <input name="site_name" value="{cred['site_name']}"><br>
      URL: <input name="url" value="{cred['url']}"><br>
      Usuário: <input name="username" value="{cred['username']}"><br>
      Senha: <input name="password" value="{cred['password']}"><br>
      Notas: <input name="notes" value="{cred['notes']}"><br>
      <button type="submit">Salvar</button>
    </form>
    <a href="{url_for('dashboard')}">Voltar</a>
    '''
    return form

@app.route('/delete/<int:cred_id>')
def delete_cred(cred_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id(session['user'])
    delete_credential(cred_id, user_id)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/export')
def export_backup():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id(session['user'])
    creds = list_credentials(user_id)
    data_json = json.dumps(creds)
    data_encrypted = encrypt(data_json)
    buf = io.BytesIO()
    buf.write(data_encrypted.encode())
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name='backup_credenciais.backup', mimetype='application/octet-stream')

@app.route('/import', methods=['POST'])
def import_backup():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id(session['user'])
    file = request.files.get('backupfile')
    if not file:
        flash('Arquivo não selecionado!', 'danger')
        return redirect(url_for('dashboard'))
    try:
        data_encrypted = file.read().decode()
        data_json = decrypt(data_encrypted)
        creds = json.loads(data_json)
        existentes = list_credentials(user_id)
        def is_duplicate(c):
            for e in existentes:
                if (c['site_name'] == e['site_name'] and c['username'] == e['username'] and c['url'] == e['url']):
                    return True
            return False
        count = 0
        for c in creds:
            if not is_duplicate(c):
                add_credential(user_id, c['site_name'], c['url'], c['username'], c['password'], c['notes'])
                count += 1
        flash(f'Backup importado com sucesso! {count} credenciais adicionadas.', 'success')
    except Exception as e:
        flash(f'Erro ao importar backup: {e}', 'danger')
    return redirect(url_for('dashboard'))

# Função utilitária para obter o user_id
from backend.database.models import SessionLocal, User

def get_user_id(username):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user.id if user else None

if __name__ == '__main__':
    app.run(debug=True) 