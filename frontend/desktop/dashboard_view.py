import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from backend.database.credential_service import list_credentials, add_credential, delete_credential, update_credential
from backend.database.models import SessionLocal, User
import threading
import random
import string
from backend.crypto.crypto_service import encrypt, decrypt
import json
from datetime import datetime, timedelta

def get_user_id(username):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user.id if user else None

def is_weak_password(password):
    # Critérios simples: <8 caracteres ou só letras/números
    if len(password) < 8:
        return True
    if password.isalpha() or password.isdigit():
        return True
    return False

def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        pwd = ''.join(random.choice(chars) for _ in range(length))
        # Garante pelo menos uma letra, um número e um símbolo
        if (any(c.islower() for c in pwd) and any(c.isupper() for c in pwd)
            and any(c.isdigit() for c in pwd) and any(c in string.punctuation for c in pwd)):
            return pwd

class DashboardView(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.user_id = get_user_id(username)
        tk.Label(self, text=f'Bem-vindo, {username}!', font=('Arial', 16)).pack(pady=10)
        # Campo de busca
        search_frame = tk.Frame(self)
        search_frame.pack(pady=2)
        tk.Label(search_frame, text='Buscar:').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.refresh_list())
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        # Lista de credenciais
        self.cred_listbox = tk.Listbox(self, width=60)
        self.cred_listbox.pack(pady=5)
        self.cred_listbox.bind('<<ListboxSelect>>', self.show_details)
        # Detalhes
        details_frame = tk.Frame(self)
        details_frame.pack(pady=5)
        self.details_text = tk.Text(details_frame, height=5, width=54, state='disabled', bg='#f5f5f5')
        self.details_text.pack(side='left')
        self.copy_btn = tk.Button(details_frame, text='Copiar senha', command=self.copy_password)
        self.copy_btn.pack(side='left', padx=5)
        # Botões
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text='Adicionar', command=self.add_cred).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Editar', command=self.edit_cred).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Excluir', command=self.del_cred).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Logout', command=master.show_login).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Exportar/Backup', command=self.export_backup).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Importar/Restaurar', command=self.import_backup).pack(side='left', padx=5)
        self.refresh_list()

    def refresh_list(self):
        self.cred_listbox.delete(0, tk.END)
        self.creds = list_credentials(self.user_id)
        filtro = self.search_var.get().lower()
        for c in self.creds:
            if filtro in c['site_name'].lower() or filtro in c['username'].lower():
                self.cred_listbox.insert(tk.END, f"ID:{c['id']} | Site: {c['site_name']} | Usuário: {c['username']} | Senha: {c['password']}")
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)
        self.details_text.config(state='disabled')

    def show_details(self, event=None):
        sel = self.cred_listbox.curselection()
        if not sel:
            self.details_text.config(state='normal')
            self.details_text.delete('1.0', tk.END)
            self.details_text.config(state='disabled')
            return
        cred_id = int(self.cred_listbox.get(sel[0]).split('|')[0].replace('ID:', '').strip())
        cred = next((c for c in self.creds if c['id'] == cred_id), None)
        if not cred:
            return
        details = f"Site/App: {cred['site_name']}\nURL: {cred['url']}\nUsuário: {cred['username']}\nSenha: {cred['password']}\nNotas: {cred['notes']}"
        if is_weak_password(cred['password']):
            details += "\n\n⚠️ Senha considerada fraca! Considere alterá-la."
        # Alerta para senha antiga
        last_mod = cred.get('last_modified')
        if last_mod:
            try:
                dt = datetime.fromisoformat(last_mod)
                if dt < datetime.utcnow() - timedelta(days=90):
                    details += "\n\n⚠️ Senha não alterada há mais de 90 dias! Considere atualizar."
            except Exception:
                pass
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert(tk.END, details)
        self.details_text.config(state='disabled')

    def add_cred(self):
        def fill_pwd():
            pwd_entry.delete(0, tk.END)
            pwd_entry.insert(0, generate_strong_password())
        dialog = tk.Toplevel(self)
        dialog.title('Nova Credencial')
        dialog.geometry('350x320')
        tk.Label(dialog, text='Site/App:').pack()
        site_entry = tk.Entry(dialog)
        site_entry.pack()
        tk.Label(dialog, text='URL:').pack()
        url_entry = tk.Entry(dialog)
        url_entry.pack()
        tk.Label(dialog, text='Usuário:').pack()
        user_entry = tk.Entry(dialog)
        user_entry.pack()
        tk.Label(dialog, text='Senha:').pack()
        pwd_entry = tk.Entry(dialog)
        pwd_entry.pack()
        tk.Button(dialog, text='Gerar senha forte', command=fill_pwd).pack(pady=2)
        tk.Label(dialog, text='Notas:').pack()
        notes_entry = tk.Entry(dialog)
        notes_entry.pack()
        def submit():
            site = site_entry.get()
            if not site:
                messagebox.showwarning('Atenção', 'Informe o nome do site/app.')
                return
            add_credential(self.user_id, site, url_entry.get(), user_entry.get(), pwd_entry.get(), notes_entry.get())
            dialog.destroy()
            self.refresh_list()
            messagebox.showinfo('Sucesso', 'Credencial adicionada!')
        tk.Button(dialog, text='Salvar', command=submit).pack(pady=8)

    def edit_cred(self):
        sel = self.cred_listbox.curselection()
        if not sel:
            messagebox.showwarning('Atenção', 'Selecione uma credencial para editar.')
            return
        cred_id = int(self.cred_listbox.get(sel[0]).split('|')[0].replace('ID:', '').strip())
        creds = list_credentials(self.user_id)
        cred = next((c for c in creds if c['id'] == cred_id), None)
        if not cred:
            messagebox.showerror('Erro', 'Credencial não encontrada.')
            return
        def fill_pwd():
            pwd_entry.delete(0, tk.END)
            pwd_entry.insert(0, generate_strong_password())
        dialog = tk.Toplevel(self)
        dialog.title('Editar Credencial')
        dialog.geometry('350x320')
        tk.Label(dialog, text='Site/App:').pack()
        site_entry = tk.Entry(dialog)
        site_entry.insert(0, cred['site_name'])
        site_entry.pack()
        tk.Label(dialog, text='URL:').pack()
        url_entry = tk.Entry(dialog)
        url_entry.insert(0, cred['url'])
        url_entry.pack()
        tk.Label(dialog, text='Usuário:').pack()
        user_entry = tk.Entry(dialog)
        user_entry.insert(0, cred['username'])
        user_entry.pack()
        tk.Label(dialog, text='Senha:').pack()
        pwd_entry = tk.Entry(dialog)
        pwd_entry.insert(0, cred['password'])
        pwd_entry.pack()
        tk.Button(dialog, text='Gerar senha forte', command=fill_pwd).pack(pady=2)
        tk.Label(dialog, text='Notas:').pack()
        notes_entry = tk.Entry(dialog)
        notes_entry.insert(0, cred['notes'])
        notes_entry.pack()
        def submit():
            updates = {}
            if site_entry.get(): updates['site_name'] = site_entry.get()
            if url_entry.get(): updates['url'] = url_entry.get()
            if user_entry.get(): updates['username'] = user_entry.get()
            if pwd_entry.get(): updates['password'] = pwd_entry.get()
            if notes_entry.get(): updates['notes'] = notes_entry.get()
            if update_credential(cred_id, self.user_id, **updates):
                dialog.destroy()
                self.refresh_list()
                messagebox.showinfo('Sucesso', 'Credencial atualizada!')
            else:
                messagebox.showerror('Erro', 'Não foi possível atualizar a credencial.')
        tk.Button(dialog, text='Salvar', command=submit).pack(pady=8)

    def del_cred(self):
        sel = self.cred_listbox.curselection()
        if not sel:
            messagebox.showwarning('Atenção', 'Selecione uma credencial para excluir.')
            return
        cred_id = int(self.cred_listbox.get(sel[0]).split('|')[0].replace('ID:', '').strip())
        if delete_credential(cred_id, self.user_id):
            self.refresh_list()
            messagebox.showinfo('Sucesso', 'Credencial excluída!')
        else:
            messagebox.showerror('Erro', 'Não foi possível excluir a credencial.')

    def copy_password(self):
        sel = self.cred_listbox.curselection()
        if not sel:
            messagebox.showwarning('Atenção', 'Selecione uma credencial para copiar a senha.')
            return
        cred_id = int(self.cred_listbox.get(sel[0]).split('|')[0].replace('ID:', '').strip())
        cred = next((c for c in self.creds if c['id'] == cred_id), None)
        if not cred:
            return
        self.clipboard_clear()
        self.clipboard_append(cred['password'])
        messagebox.showinfo('Copiado', 'Senha copiada para o clipboard! Será limpa em 15 segundos.')
        threading.Timer(15, self.clear_clipboard_notify).start()

    def clear_clipboard_notify(self):
        self.clipboard_clear()
        self.master.after(0, lambda: messagebox.showinfo('Clipboard limpo', 'O clipboard foi limpo automaticamente por segurança.'))

    def export_backup(self):
        creds = list_credentials(self.user_id)
        if not creds:
            messagebox.showwarning('Atenção', 'Nenhuma credencial para exportar.')
            return
        # Criptografa o JSON das credenciais
        data_json = json.dumps(creds)
        data_encrypted = encrypt(data_json)
        file_path = filedialog.asksaveasfilename(defaultextension='.backup', filetypes=[('Backup Files', '*.backup')])
        if not file_path:
            return
        with open(file_path, 'w') as f:
            f.write(data_encrypted)
        messagebox.showinfo('Backup', 'Backup exportado com sucesso! Guarde o arquivo em local seguro.')

    def import_backup(self):
        file_path = filedialog.askopenfilename(filetypes=[('Backup Files', '*.backup')])
        if not file_path:
            return
        try:
            with open(file_path, 'r') as f:
                data_encrypted = f.read()
            data_json = decrypt(data_encrypted)
            creds = json.loads(data_json)
            # Importa cada credencial para o usuário autenticado, evitando duplicatas
            existentes = list_credentials(self.user_id)
            def is_duplicate(c):
                for e in existentes:
                    if (c['site_name'] == e['site_name'] and c['username'] == e['username'] and c['url'] == e['url']):
                        return True
                return False
            count = 0
            for c in creds:
                if not is_duplicate(c):
                    add_credential(self.user_id, c['site_name'], c['url'], c['username'], c['password'], c['notes'])
                    count += 1
            self.refresh_list()
            messagebox.showinfo('Restauração', f'Backup importado com sucesso! {count} credenciais adicionadas.')
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao importar backup: {e}') 