# Documentação Técnica

## Estrutura do Projeto

```
gerenciador-sites/
├── backend/
│   ├── app.py                # Ponto de entrada do app (terminal)
│   ├── auth/                 # Autenticação de usuários
│   ├── crypto/               # (Futuro) Criptografia avançada
│   └── database/             # Modelos e serviços de banco de dados
├── database/                 # Arquivos do banco SQLite
├── frontend/                 # (Futuro) Interface desktop/web
├── docs/                     # Documentação
├── requirements.txt          # Dependências
├── README.md                 # Resumo do projeto
└── PLANNING.md               # Planejamento detalhado
```

## Como rodar o projeto

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o app:
   ```bash
   python -m backend.app
   ```

## Principais módulos

- **backend/auth/auth_service.py**: Cadastro e login de usuários, hash seguro de senha.
- **backend/database/models.py**: Modelos User e Credential, configuração do banco.
- **backend/database/credential_service.py**: CRUD de credenciais (adicionar, listar, editar, excluir).
- **backend/app.py**: Menu de interação via terminal.

## Como contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua feature/correção
3. Faça commits claros e objetivos
4. Abra um Pull Request

## Próximos passos
- Implementar criptografia AES-256 real
- Interface gráfica (Tkinter ou Flask)
- Testes automatizados 

## Segurança e Criptografia

- As senhas das credenciais são criptografadas com AES-256 (Fernet) usando a biblioteca cryptography.
- A chave de criptografia é gerada automaticamente e armazenada no arquivo `.env` na raiz do projeto (variável FERNET_KEY).
- O módulo responsável é `backend/crypto/crypto_service.py`.
- O CRUD de credenciais utiliza as funções `encrypt` e `decrypt` para proteger os dados sensíveis. 

## Backup e Restauração
- O sistema permite exportar todas as credenciais do usuário autenticado para um arquivo `.backup` criptografado.
- O backup pode ser restaurado em qualquer instalação do sistema, desde que a chave de criptografia seja a mesma.
- Durante a importação, o sistema evita duplicidade de credenciais (mesmo site, usuário e URL).

## Segurança Adicional
- Cada credencial armazena a data da última alteração (last_modified).
- O sistema alerta visualmente o usuário sobre senhas consideradas fracas e senhas não alteradas há mais de 90 dias. 

## Interface Web (Flask)
- O sistema pode ser acessado via navegador executando:
  ```bash
  python frontend/web/app.py
  ```
- Rotas principais:
  - `/` login/cadastro
  - `/dashboard` dashboard do usuário
  - `/add`, `/edit/<id>`, `/delete/<id>` CRUD de credenciais
  - `/export` exporta backup criptografado
  - `/import` importa backup criptografado
- A interface web utiliza Bootstrap para visual moderno e responsivo.
- Toda a lógica de autenticação, criptografia e backup é compartilhada com o backend desktop. 