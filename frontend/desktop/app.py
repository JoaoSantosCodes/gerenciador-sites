import tkinter as tk
from frontend.desktop.login_view import LoginView
from frontend.desktop.dashboard_view import DashboardView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gerenciador de Sites e Senhas')
        self.geometry('400x300')
        self.resizable(False, False)
        self.current_frame = None
        self.show_login()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginView(self, self.show_dashboard)
        self.current_frame.pack(fill='both', expand=True)

    def show_dashboard(self, username):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = DashboardView(self, username)
        self.current_frame.pack(fill='both', expand=True)

if __name__ == '__main__':
    app = App()
    app.mainloop() 