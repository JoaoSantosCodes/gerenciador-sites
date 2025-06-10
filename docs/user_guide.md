# Guia do Usuário - Gerenciador de Sites e Senhas

## Instalação

1. Certifique-se de ter Python 3.8 ou superior instalado
2. Clone o repositório
3. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
4. Ative o ambiente virtual:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando o Aplicativo

### Interface de Linha de Comando (CLI)

Para iniciar o aplicativo, execute:
```bash
python backend/cli.py
```

### Menu Principal
1. **Cadastrar novo usuário**
   - Crie sua conta com um nome de usuário e senha mestra
   - A senha mestra é usada para criptografar todas as suas credenciais
   - Guarde sua senha mestra em local seguro!

2. **Login**
   - Acesse sua conta usando seu nome de usuário e senha mestra

3. **Sair**
   - Encerra o aplicativo

### Menu de Credenciais
Após fazer login, você terá acesso às seguintes opções:

1. **Adicionar nova credencial**
   - Site/App: Nome do site ou aplicativo
   - URL: Endereço do site
   - Usuário: Seu nome de usuário no site
   - Senha: Sua senha no site
   - Notas: Informações adicionais (opcional)

2. **Listar credenciais**
   - Mostra todas as suas credenciais salvas
   - As senhas são mostradas descriptografadas apenas durante sua sessão

3. **Editar credencial**
   - Selecione a credencial pelo ID
   - Deixe em branco os campos que não deseja alterar

4. **Excluir credencial**
   - Selecione a credencial pelo ID para excluí-la

5. **Alterar senha mestra**
   - Altera sua senha mestra
   - Todas as suas credenciais serão re-criptografadas automaticamente
   - Não esqueça a nova senha mestra!

6. **Logout**
   - Encerra sua sessão atual

## Dicas de Segurança

1. **Senha Mestra**
   - Use uma senha forte e única
   - Não compartilhe sua senha mestra
   - Não use a mesma senha mestra em outros serviços

2. **Credenciais**
   - Use senhas diferentes para cada site
   - Ative autenticação em dois fatores quando disponível
   - Mantenha suas notas atualizadas

3. **Backup**
   - Faça backup regular do arquivo do banco de dados
   - Mantenha seu backup em local seguro

## Solução de Problemas

1. **Não consigo fazer login**
   - Verifique se o nome de usuário está correto
   - Certifique-se de que a senha mestra está correta
   - Tente criar uma nova conta se necessário

2. **Erro ao adicionar credencial**
   - Verifique se todos os campos obrigatórios foram preenchidos
   - Certifique-se de que está logado

3. **Erro ao alterar senha mestra**
   - Verifique se a senha atual está correta
   - Certifique-se de que a nova senha foi digitada corretamente duas vezes

## Suporte

Para reportar problemas ou sugerir melhorias:
1. Abra uma issue no repositório do projeto
2. Descreva o problema detalhadamente
3. Inclua passos para reproduzir o problema, se possível 