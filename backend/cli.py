from backend.auth.auth_service import create_user, authenticate_user, change_master_password
from backend.database.credential_service import add_credential, list_credentials, update_credential, delete_credential
from backend.database.models import SessionLocal, User
import getpass
import sys

def get_user_id(username):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user.id if user else None

def print_menu():
    print("\n=== Gerenciador de Sites e Senhas ===")
    print("1. Cadastrar novo usuário")
    print("2. Login")
    print("3. Sair")
    return input("Escolha uma opção: ")

def print_credential_menu():
    print("\n=== Gerenciamento de Credenciais ===")
    print("1. Adicionar nova credencial")
    print("2. Listar credenciais")
    print("3. Editar credencial")
    print("4. Excluir credencial")
    print("5. Alterar senha mestra")
    print("6. Logout")
    return input("Escolha uma opção: ")

def handle_credentials(user_id):
    while True:
        opcao = print_credential_menu()
        
        if opcao == '1':
            site = input("Site/App: ")
            url = input("URL: ")
            username = input("Usuário: ")
            password = getpass.getpass("Senha: ")
            notes = input("Notas: ")
            
            if add_credential(user_id, site, url, username, password, notes):
                print("Credencial adicionada com sucesso!")
            else:
                print("Erro ao adicionar credencial.")
                
        elif opcao == '2':
            creds = list_credentials(user_id)
            if not creds:
                print("Nenhuma credencial encontrada.")
            else:
                print("\nSuas credenciais:")
                for c in creds:
                    print(f"\nID: {c['id']}")
                    print(f"Site: {c['site_name']}")
                    print(f"URL: {c['url']}")
                    print(f"Usuário: {c['username']}")
                    print(f"Senha: {c['password']}")
                    if c['notes']:
                        print(f"Notas: {c['notes']}")
                    print("-" * 30)
                    
        elif opcao == '3':
            cred_id = input("ID da credencial a editar: ")
            try:
                cred_id = int(cred_id)
                print("Deixe em branco para não alterar.")
                site = input("Novo Site/App: ")
                url = input("Nova URL: ")
                username = input("Novo Usuário: ")
                password = getpass.getpass("Nova Senha: ")
                notes = input("Novas Notas: ")
                
                updates = {}
                if site: updates['site_name'] = site
                if url: updates['url'] = url
                if username: updates['username'] = username
                if password: updates['password'] = password
                if notes: updates['notes'] = notes
                
                if update_credential(cred_id, user_id, **updates):
                    print("Credencial atualizada com sucesso!")
                else:
                    print("Erro ao atualizar credencial.")
            except ValueError:
                print("ID inválido!")
                
        elif opcao == '4':
            cred_id = input("ID da credencial a excluir: ")
            try:
                cred_id = int(cred_id)
                if delete_credential(cred_id, user_id):
                    print("Credencial excluída com sucesso!")
                else:
                    print("Erro ao excluir credencial.")
            except ValueError:
                print("ID inválido!")
                
        elif opcao == '5':
            old_pass = getpass.getpass("Senha atual: ")
            new_pass = getpass.getpass("Nova senha: ")
            confirm_pass = getpass.getpass("Confirme a nova senha: ")
            
            if new_pass != confirm_pass:
                print("As senhas não coincidem!")
                continue
                
            if change_master_password(username, old_pass, new_pass):
                print("Senha mestra alterada com sucesso!")
            else:
                print("Erro ao alterar senha mestra.")
                
        elif opcao == '6':
            print("Logout realizado.")
            break
            
        else:
            print("Opção inválida!")

def main():
    while True:
        opcao = print_menu()
        
        if opcao == '1':
            username = input("Usuário: ")
            password = getpass.getpass("Senha: ")
            confirm_pass = getpass.getpass("Confirme a senha: ")
            
            if password != confirm_pass:
                print("As senhas não coincidem!")
                continue
                
            if create_user(username, password):
                print("Usuário cadastrado com sucesso!")
            else:
                print("Erro ao cadastrar usuário.")
                
        elif opcao == '2':
            username = input("Usuário: ")
            password = getpass.getpass("Senha: ")
            
            if authenticate_user(username, password):
                print("Login realizado com sucesso!")
                user_id = get_user_id(username)
                handle_credentials(user_id)
            else:
                print("Usuário ou senha inválidos!")
                
        elif opcao == '3':
            print("Saindo...")
            sys.exit(0)
            
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main() 