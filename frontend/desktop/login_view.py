import tkinter as tk
from tkinter import messagebox
from backend.auth.auth_service import create_user, authenticate_user

class LoginView(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='Usuário:').pack(pady=(40, 5))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        tk.Label(self, text='Senha:').pack(pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()
        tk.Button(self, text='Login', command=self.login).pack(pady=10)
        tk.Button(self, text='Cadastrar', command=self.cadastrar).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate_user(username, password):
            self.on_login_success(username)
        else:
            messagebox.showerror('Erro', 'Usuário ou senha inválidos!')

    def cadastrar(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if create_user(username, password):
            messagebox.showinfo('Sucesso', 'Usuário cadastrado!')
        else:
            messagebox.showerror('Erro', 'Usuário já existe!') 