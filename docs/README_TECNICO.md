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