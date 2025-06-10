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