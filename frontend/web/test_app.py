import pytest
from frontend.web.app import app
from bs4 import BeautifulSoup

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_and_login(client):
    # Cadastro
    resp = client.post('/', data={'username': 'webuser', 'password': 'webpass', 'action': 'register'}, follow_redirects=True)
    data = resp.data.decode()
    assert 'Usuário cadastrado' in data or 'Usuário já existe' in data
    # Login
    resp = client.post('/', data={'username': 'webuser', 'password': 'webpass', 'action': 'login'}, follow_redirects=True)
    assert 'Dashboard' in resp.data.decode()

def test_dashboard_requires_login(client):
    resp = client.get('/dashboard')
    assert resp.status_code == 302  # Redireciona para login

def test_add_and_delete_credential(client):
    # Login
    client.post('/', data={'username': 'webuser2', 'password': 'webpass2', 'action': 'register'})
    client.post('/', data={'username': 'webuser2', 'password': 'webpass2', 'action': 'login'})
    # Adicionar credencial
    resp = client.post('/add', data={
        'site_name': 'SiteTest', 'url': 'http://test.com', 'username': 'user', 'password': '12345678', 'notes': 'nota'
    }, follow_redirects=True)
    assert 'SiteTest' in resp.data.decode()
    # Excluir credencial
    resp = client.get('/dashboard')
    soup = BeautifulSoup(resp.data, 'html.parser')
    cred_id = None
    for a in soup.find_all('a', string='Excluir'):
        href = a['href']
        if '/delete/' in href:
            cred_id = int(href.split('/delete/')[1])
            break
    assert cred_id is not None
    resp = client.get(f'/delete/{cred_id}', follow_redirects=True)
    # Verifica que não há mais nenhum <b>SiteTest</b> na lista de credenciais
    soup = BeautifulSoup(resp.data, 'html.parser')
    cred_list = soup.find_all('b')
    print('DEBUG <b> elements:', [b.text for b in cred_list])
    print('DEBUG HTML:', resp.data.decode())
    # Imprimir todos os <li> da lista de credenciais
    for li in soup.find_all('li', class_='list-group-item'):
        print('DEBUG <li>:', li.text)
    assert all(b.text != 'SiteTest' for b in cred_list) 