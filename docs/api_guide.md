# Guia Rápido da API Web - Gerenciador de Sites e Senhas

A API está disponível em `http://localhost:5000` por padrão.

## Endpoints Principais

### 1. Cadastro de Usuário
- **POST** `/api/register`
- **Body (JSON):**
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```
- **Resposta:**
  - 200: `{ "message": "Usuário cadastrado com sucesso!" }`
  - 409: `{ "error": "Usuário já existe." }`

---

### 2. Login
- **POST** `/api/login`
- **Body (JSON):**
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```
- **Resposta:**
  - 200: `{ "message": "Login realizado com sucesso!" }`
  - 401: `{ "error": "Usuário ou senha inválidos." }`

> **Importante:** O login cria uma sessão (cookie) que deve ser mantida nas próximas requisições.

---

### 3. Listar Credenciais
- **GET** `/api/credentials`
- **Headers:**
  - Envie o cookie de sessão retornado no login
- **Resposta:**
  - 200: Lista de credenciais do usuário autenticado
  - 401: `{ "error": "Não autenticado." }`

---

### 4. Adicionar Credencial
- **POST** `/api/credentials`
- **Body (JSON):**
```json
{
  "site_name": "Nome do Site",
  "url": "https://site.com",
  "username": "usuario_no_site",
  "password": "senha_do_site",
  "notes": "anotacoes opcionais"
}
```
- **Resposta:**
  - 200: `{ "message": "Credencial adicionada!" }`
  - 401: `{ "error": "Não autenticado." }`

---

### 5. Editar Credencial
- **PUT** `/api/credentials/<id>`
- **Body (JSON):**
```json
{
  "site_name": "Novo Nome",
  "password": "nova senha"
}
```
- **Resposta:**
  - 200: `{ "message": "Credencial atualizada!" }`
  - 401: `{ "error": "Não autenticado." }`
  - 404: `{ "error": "Erro ao atualizar credencial." }`

---

### 6. Excluir Credencial
- **DELETE** `/api/credentials/<id>`
- **Resposta:**
  - 200: `{ "message": "Credencial excluída!" }`
  - 401: `{ "error": "Não autenticado." }`
  - 404: `{ "error": "Erro ao excluir credencial." }`

---

### 7. Logout
- **POST** `/api/logout`
- **Resposta:**
  - 200: `{ "message": "Logout realizado." }`

---

## Dicas para Testar
- Use Postman, Insomnia ou qualquer cliente HTTP.
- Sempre faça login antes de acessar rotas protegidas.
- Mantenha o cookie de sessão entre as requisições.
- Para testar no navegador, você pode usar extensões como "REST Client" ou "Talend API Tester".

---

## Exemplo de Fluxo
1. **Cadastrar usuário**
2. **Fazer login**
3. **Adicionar credencial**
4. **Listar credenciais**
5. **Editar ou excluir credencial**
6. **Logout**

Pronto! Agora você pode testar a API web do seu gerenciador de senhas. 