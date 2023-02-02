from tkinter import Tk, Button, Entry, Label
from tk_options import resize_window, grid_region
from database import get_users


class Validation:
    def __init__(self):

        self.user = None
        self.success = True
        self.true_data = get_users()
        self.app = None
    # открывает окно авторизации
    def valid_win(self):
        self.app = Tk()
        resize_window(self.app, 400, 200)
        grid_region(self.app, rows=4, colums=3)

        lbl_welcome = Label(text="Добро пожаловать в систему 'Писатели'")
        lbl_welcome.grid(row=0, column=0, columnspan=3)

        lbl_login = Label(text="Логин:", width=6)
        lbl_login.grid(row=1, column=0, sticky="nwse")
        ent_login = Entry()
        ent_login.grid(row=1, column=1, sticky="nwse")

        lbl_pass = Label(text="Пароль:", width=6)
        lbl_pass.grid(row=2, column=0, sticky="nwse")
        ent_pass = Entry(show="*")
        ent_pass.grid(row=2, column=1, sticky="nwse")

        lbl_status = Label(text="", width=6)
        lbl_status.grid(row=1, rowspan=2, column=2, sticky="nwse")

        btn_login = Button(text="Войти", command=lambda: self.enter(ent_login, ent_pass, lbl_status))
        btn_login.grid(row=3, column=1, sticky="nwse")

        self.app.mainloop()
    # проверяет логин и пароль
    def check_enter(self, login, password):
        for user in self.true_data:
            if [login, password] == [user[3],user[4]]:
                self.user = user
                return True
        return False
    # выводит результат проверки
    def enter(self, login, password, status):
        if not self.check_enter(login.get(), password.get()):
            status["text"] = "Неверный\n логин\nили пароль"
        else:
            self.app.destroy()
