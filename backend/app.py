from backend.auth.auth_service import create_user, authenticate_user
from backend.database.credential_service import (
    add_credential, list_credentials, update_credential, delete_credential
)
from backend.database.models import SessionLocal, User

def get_user_id(username):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user.id if user else None

def cred_menu(user_id):
    while True:
        print("\n--- Gerenciamento de Credenciais ---")
        print("1. Adicionar nova credencial")
        print("2. Listar credenciais")
        print("3. Editar credencial")
        print("4. Excluir credencial")
        print("5. Logout")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            site = input("Site/App: ")
            url = input("URL: ")
            username = input("Usuário: ")
            password = input("Senha: ")
            notes = input("Notas: ")
            add_credential(user_id, site, url, username, password, notes)
            print("Credencial adicionada!")
        elif opcao == '2':
            creds = list_credentials(user_id)
            if not creds:
                print("Nenhuma credencial encontrada.")
            for c in creds:
                print(f"ID: {c['id']} | Site: {c['site_name']} | URL: {c['url']} | Usuário: {c['username']} | Senha: {c['password']} | Notas: {c['notes']}")
        elif opcao == '3':
            cred_id = int(input("ID da credencial a editar: "))
            print("Deixe em branco para não alterar.")
            site = input("Novo Site/App: ")
            url = input("Nova URL: ")
            username = input("Novo Usuário: ")
            password = input("Nova Senha: ")
            notes = input("Novas Notas: ")
            updates = {}
            if site: updates['site_name'] = site
            if url: updates['url'] = url
            if username: updates['username'] = username
            if password: updates['password'] = password
            if notes: updates['notes'] = notes
            if update_credential(cred_id, user_id, **updates):
                print("Credencial atualizada!")
            else:
                print("Credencial não encontrada.")
        elif opcao == '4':
            cred_id = int(input("ID da credencial a excluir: "))
            if delete_credential(cred_id, user_id):
                print("Credencial excluída!")
            else:
                print("Credencial não encontrada.")
        elif opcao == '5':
            print("Logout realizado.")
            break
        else:
            print("Opção inválida!")

def main():
    print("=== Gerenciador de Sites e Senhas (Beta) ===")
    while True:
        print("\n1. Cadastrar novo usuário")
        print("2. Login")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            username = input("Usuário: ")
            password = input("Senha: ")
            if create_user(username, password):
                print("Usuário cadastrado com sucesso!")
            else:
                print("Usuário já existe!")
        elif opcao == '2':
            username = input("Usuário: ")
            password = input("Senha: ")
            if authenticate_user(username, password):
                print("Login realizado com sucesso!")
                user_id = get_user_id(username)
                cred_menu(user_id)
            else:
                print("Usuário ou senha inválidos!")
        elif opcao == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main() 