# Gerenciador de Sites e Senhas

Um aplicativo Python seguro para gerenciar credenciais de sites (URLs, nomes de usuário e senhas) com funcionalidades de login e criptografia.

## Documentação
- [Manual do Usuário](docs/README_USUARIO.md)
- [Documentação Técnica](docs/README_TECNICO.md)
- [Planejamento do Projeto](PLANNING.md)

## Como rodar
```bash
pip install -r requirements.txt
python -m backend.app
```

## Funcionalidades
- Sistema de autenticação seguro
- Gerenciamento de credenciais (CRUD)
- Criptografia (placeholder, será AES-256)
- Pronto para expansão com interface gráfica
- Backup e restauração de credenciais criptografadas
- Proteção contra duplicidade na importação
- Alerta visual para senhas fracas e senhas antigas

## Contribuição
Consulte a [documentação técnica](docs/README_TECNICO.md#como-contribuir).

## Licença
MIT

## Requisitos

- Python 3.x
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/gerenciador-sites.git
cd gerenciador-sites
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

[Instruções de uso serão adicionadas após a implementação]

## Segurança

- Todas as senhas são armazenadas com criptografia AES-256
- Senha mestre protegida com hashing seguro
- Autenticação em dois fatores (opcional)

## Contato

[Seu nome/email será adicionado]

## Configuração de variáveis de ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
SECRET_KEY=sua_chave_super_secreta
DATABASE_URL=sqlite:///database/password_manager.db
FLASK_ENV=development
```

O backend carrega automaticamente essas variáveis ao iniciar. Nunca compartilhe seu `.env` real, use `.env.example` para referência. 