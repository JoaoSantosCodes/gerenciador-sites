# Manual do Usuário

## Introdução
Este sistema permite gerenciar credenciais de sites e senhas de forma segura, via terminal.

## Como usar

1. **Inicie o programa:**
   ```bash
   python -m backend.app
   ```

2. **Menu inicial:**
   - 1: Cadastrar novo usuário
   - 2: Login
   - 3: Sair

3. **Cadastro:**
   - Informe um nome de usuário e senha forte.
   - Se o usuário já existir, será informado.

4. **Login:**
   - Informe usuário e senha cadastrados.
   - Se corretos, acesso ao menu de credenciais.

5. **Menu de credenciais:**
   - 1: Adicionar nova credencial (site, url, usuário, senha, notas)
   - 2: Listar credenciais
   - 3: Editar credencial (por ID)
   - 4: Excluir credencial (por ID)
   - 5: Logout

6. **Dicas de segurança:**
   - Use senhas fortes e únicas.
   - Nunca compartilhe sua senha mestre.
   - As senhas das credenciais são armazenadas de forma criptografada.

## Observações
- O sistema é beta e será expandido com interface gráfica e recursos avançados.
- Em caso de dúvidas, consulte a documentação técnica ou abra uma issue no GitHub. 