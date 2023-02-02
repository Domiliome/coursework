import io
import re
from tkinter import *
from tkinter.ttk import Combobox

import _tkinter
from PIL import Image, ImageTk

from tk_options import *
from database import *


class Gui:
    def __init__(self, user):

        self.status_about = False
        self.user = user
        self.app = Tk()
        self.app.title(f"Главная | {self.user[2]}")
        resize_window(self.app, 800, 600)

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=6)
        self.app.grid_columnconfigure(0, weight=1)

        self.mm_frame = Frame(self.app)
        self.mm_frame.grid(row=0, column=0, sticky="nwe")
        grid_region(self.mm_frame, 1, 4)

        self.page_frame = Frame(self.app)
        self.page_frame.grid(row=1, column=0, sticky="nwse")

        btn_main = Button(self.mm_frame, text="Главная", relief="ridge")
        btn_main.grid(row=0, column=0, sticky="nwse")
        btn_main.bind('<Double-Button-1>', self.main_page)

        btn_authors = Button(self.mm_frame, text="Писатели", relief="ridge")
        btn_authors.grid(row=0, column=1, sticky="nwse")
        btn_authors.bind('<Double-Button-1>', self.authors_page)

        btn_works = Button(self.mm_frame, text="Произведения", relief="ridge")
        btn_works.grid(row=0, column=2, sticky="nwse")
        btn_works.bind('<Double-Button-1>', self.works_page)

        btn_ref = Button(self.mm_frame, text="Справка", relief="ridge")
        btn_ref.grid(row=0, column=3, sticky="nwse")
        btn_ref.bind('<Double-Button-1>', self.ref_page)
        self.active_page = btn_main
        self.active_page["bg"] = "#D8D8D8"
        self.main_page("eventless")

    # интерфейс главной страницы
    def main_page(self, event):
        if event != "eventless":
            self.change_page(event.widget)
        self.page_frame.grid_rowconfigure(0, weight=1)
        self.page_frame.grid_columnconfigure(0, weight=2)
        self.page_frame.grid_columnconfigure(1, weight=1)
        self.page_frame.grid_columnconfigure((2, 3), weight=0)

        frame_1 = Frame(self.page_frame)
        frame_1.grid(row=0, column=0, sticky="nwse")

        lbl_hello = Label(frame_1, text="Добро пожаловать!")
        lbl_hello.grid(row=0, column=0)

        frame_2 = Frame(self.page_frame)
        frame_2.grid(row=0, column=1, sticky="nwse")

        grid_region(frame_1, 3, 1)
        frame_1.grid_rowconfigure(1, weight=4)
        self.lbl_about = Label(frame_1, text="", font="30")
        self.lbl_about.grid(row=1, column=0)
        btn_about = Button(frame_1, text="Сведение об авторе")
        btn_about.bind('<Double-Button-1>', self.about)
        btn_about.grid(row=2, column=0)

        grid_region(frame_2, 2, 1)

        data_frame = Frame(frame_2)
        data_frame.grid(row=0, column=0, sticky="nwe")
        grid_region(data_frame, 4, 2)

        img = Image.open(io.BytesIO(self.user[7]))
        img = img.resize((125, 125), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)

        lbl_title = Label(data_frame, text="Профиль\n", image=photo, compound="bottom")
        lbl_title.image = photo
        lbl_title.grid(row=0, column=0, columnspan=2, sticky="nwse", pady=25)

        lbl_name = Label(data_frame, text=f"Имя пользователя:  {self.user[2]}")
        lbl_name.grid(row=1, column=0, sticky="nsw")

        lbl_login = Label(data_frame, text=f"Логин:  {self.user[3]}")
        lbl_login.grid(row=2, column=0, sticky="nsw")

        lbl_warn = Label(data_frame, text="")
        lbl_warn.grid(row=3, column=0, sticky="nsw")

        password_frame = Frame(frame_2)
        password_frame.grid(row=1, column=0, sticky="nwe")
        grid_region(password_frame, 5, 2)

        lbl_change_pass = Label(password_frame, text="Смена пароля")
        lbl_change_pass.grid(row=0, column=0, columnspan=2, sticky="nswe", pady=25)

        lbl_old_pass = Label(password_frame, text="Старый пароль")
        lbl_old_pass.grid(row=1, column=0, sticky="nws")

        self.ent_old_pass = Entry(password_frame, show='*')
        self.ent_old_pass.grid(row=1, column=1)

        lbl_new_pass = Label(password_frame, text="Новый пароль")
        lbl_new_pass.grid(row=2, column=0, sticky="nws")

        self.ent_new_pass = Entry(password_frame, show='*')
        self.ent_new_pass.grid(row=2, column=1)

        lbl_re_pass = Label(password_frame, text="Повторите")
        lbl_re_pass.grid(row=3, column=0, sticky="nws")

        self.ent_re_pass = Entry(password_frame, show='*')
        self.ent_re_pass.grid(row=3, column=1)

        btn_change_pass = Button(password_frame, text="Изменить")
        btn_change_pass.bind('<Double-Button-1>', self.check_pass)
        btn_change_pass.grid(row=4, column=0, columnspan=2, sticky="ns", pady=25)

        self.lbl_err = Label(password_frame, text="", )
        self.lbl_err.grid(row=5, column=0, columnspan=2)

    # отвечает за вывод информации об авторе
    def about(self, event):
        if not self.status_about:
            self.status_about = True
            self.lbl_about["text"] = "Рейш Евгений\n20-ИЭ-2"
        else:
            self.status_about = False
            self.lbl_about["text"] = ""

    # проверяет данные для изменения пароля
    def check_pass(self, event):
        old_pass = str(self.ent_old_pass.get())
        new_pass = str(self.ent_new_pass.get())
        re_pass = str(self.ent_re_pass.get())
        if old_pass == self.user[4]:

            if new_pass == re_pass:
                if len(new_pass) < 6:
                    self.lbl_err["text"] = "В новом пароле меньше 6 знаков"
                else:
                    change_pass(self.user, new_pass)
                    self.lbl_err["text"] = "Успешно"
            else:
                self.lbl_err["text"] = "Новые пароли не совпадают"

        else:
            self.lbl_err["text"] = "Неправильный старый пароль"
        self.ent_old_pass.delete(0, END)
        self.ent_new_pass.delete(0, END)
        self.ent_re_pass.delete(0, END)

    # интерфейс страницы справки
    def ref_page(self, event):
        self.change_page(event.widget)
        self.page_frame.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.page_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.page_frame.grid_columnconfigure(0, weight=1)
        lbl_title = Label(self.page_frame, text="Как пользоваться системой.", font="25")
        lbl_title.grid(row=0, column=0)

        lbl_watch_authors = Label(self.page_frame, text="Просмотр авторов.", font="25")
        lbl_watch_authors.grid(row=1, column=0)
        btn_watch_authors = Button(self.page_frame, text="Открыть",
                                   command=lambda: self.ref("1. Откройте вкладку 'Писатели'.\n"
                                                            "2. Здесь вы увидите список добавленных\nв систему писателей с их портретами\n"
                                                            "а также датами рождения и странами.\n"
                                                            "3. Нажав на 'показать больше' дважды\nу вас откроется окно с биографией\n"
                                                            "и списком литературы писателя\n"
                                                            "4. Данное окно можно закрыть или \nсвернуть и пользоваться системой дальше"
                                                            , "Просмотр писателей"))
        btn_watch_authors.grid(row=2, column=0, pady=10)

        lbl_find_authors = Label(self.page_frame, text="Поиск авторов.", font="25")
        lbl_find_authors.grid(row=3, column=0)
        btn_find_authors = Button(self.page_frame, text="Открыть",
                                  command=lambda: self.ref("1. Откройте вкладку 'Писатели'.\n"
                                                           "2. Здесь вы увидите строку ввода\nпосле надписи поиск\n"
                                                           "3. Нажав на выпадающий список\n"
                                                           "выберите по какому критерию искать,\n"
                                                           "вводите соответствующие данные,\n"
                                                           "и дважды клинките по 'Показать'\n"
                                                           "4. Чтобы получить список без критериев\n"
                                                           "осуществите поиск с пустой строкой", "Поиск авторов"))
        btn_find_authors.grid(row=4, column=0, pady=10)

        lbl_find_works = Label(self.page_frame, text="Поиск произведений.", font="25")
        lbl_find_works.grid(row=5, column=0)
        btn_find_works = Button(self.page_frame, text="Открыть",
                                command=lambda: self.ref("1. Откройте вкладку 'Произведения'.\n"
                                                         "2. Здесь вы увидите строку ввода\nпосле надписи поиск\n"
                                                         "3. Нажав на выпадающий список\n"
                                                         "выберите по какому критерию искать,\n"
                                                         "вводите соответствующие данные,\n"
                                                         "и дважды клинките по 'Найти'\n"
                                                         "4. Чтобы получить список без критериев\n"
                                                         "осуществите поиск с пустой строкой", "Поиск произведений"))
        btn_find_works.grid(row=6, column=0, pady=10)

        lbl_change_pass = Label(self.page_frame, text="Смена пароля.", font="25")
        lbl_change_pass.grid(row=7, column=0)
        btn_change_pass = Button(self.page_frame, text="Открыть",
                                 command=lambda: self.ref("1. Откройте вкладку 'Главная'.\n"
                                                          "2. Здесь вы увидите строки ввода\nв правом нижнем углу\n"
                                                          "3. Введите верные данные\n"
                                                          "нажмите на кнопку 'Изменить'\n"
                                                          "4.Пароль можно менять один раз в сессии", "Смена пароля"))
        btn_change_pass.grid(row=8, column=0, pady=10)
    # выводит окно справки определённого раздела
    def ref(self, text, title):
        window = Toplevel(self.app)
        window.title(f"Справка | {title}")
        resize_window(window, 310, 200)
        window.grid_rowconfigure((0, 1), weight=1)
        window.grid_columnconfigure(0, weight=1)
        lbl = Label(window, justify="left", font="20", text=text)
        lbl.grid(row=0, sticky="w")
        btn_close = Button(window, text="Закрыть", command=window.destroy)
        btn_close.grid(row=1, sticky="we")
    # отвечает за переход по страницам
    def change_page(self, page):
        self.active_page["bg"] = "#F0F0F0"
        self.active_page = page
        self.active_page["bg"] = "#D8D8D8"
        list = self.page_frame.grid_slaves()
        for i in list:
            i.destroy()
        self.page_frame.grid_columnconfigure((0, 1), weight=0)
        self.page_frame.grid_rowconfigure((0, 1), weight=0)
        self.page_frame.grid_columnconfigure(0, weight=1)
        self.page_frame.grid_rowconfigure(0, weight=1)


class UserGui(Gui):
    def __init__(self, user):
        super().__init__(user)
        # код интерфейса пользователя
        self.work_records_frame = None
        self.works_records = None
        self.ent_find_work = None
        self.canvas_work = None
        self.cbox_works = None
        self.ent_find_author = None
        self.cbox_writers = None
        self.user = user
        self.canvas = None
        self.records_frame = None
        self.writer_records = None
        self.app.mainloop()
    # отбор строки по потерну
    def parsing(self, pattern, new_val):
        try:
            result = re.match(pattern, new_val[-1])
        except IndexError:
            return True
        if result is not None:
            return True
        else:
            return False
    # интерфейс страницы авторов
    def authors_page(self, event):
        self.change_page(event.widget)
        self.page_frame.grid_rowconfigure(0, weight=1)
        self.page_frame.grid_rowconfigure(1, weight=10)

        self.page_frame.grid_columnconfigure((1, 2, 3), weight=3)
        lbl_find_author = Label(self.page_frame, text="Поиск")
        lbl_find_author.grid(column=0, row=0, sticky="nswe", pady=20)
        # ограничение поиска по критериям
        def is_valid_author(new_val):
            if self.cbox_writers.get() in ("По имени", "По стране"):
                return self.parsing(r"[а-яА-Я ]", new_val)
            elif self.cbox_writers.get() in ("Раньше даты", "Позже даты"):
                try:
                    if int(new_val) <= 2023:
                        return self.parsing(r"[\d]", new_val)
                    else:
                        return False
                except ValueError:
                    return self.parsing(r"[\d]", new_val)

        check = (self.app.register(is_valid_author), "%P")
        self.ent_find_author = Entry(self.page_frame, font="Tahoma, 14", validate="key", validatecommand=check)
        self.ent_find_author.grid(row=0, column=1, sticky="we")
        self.cbox_writers = Combobox(self.page_frame, values=["По имени", "Раньше даты", "Позже даты", "По стране"])
        self.cbox_writers.grid(row=0, column=2, sticky="we")
        self.cbox_writers.current(0)
        btn_find_author = Button(self.page_frame, text="Найти")
        btn_find_author.bind('<Double-Button-1>', self.find_authors)
        btn_find_author.grid(row=0, column=3, sticky="we")

        self.canvas = Canvas(self.page_frame, highlightthickness=0)
        self.canvas.grid(column=0, columnspan=4, row=1, sticky="nwse")
        self.canvas.grid_columnconfigure(0, weight=1)

        scrollbar = Scrollbar(self.canvas, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.records_frame = Frame(self.canvas)
        self.canvas.create_window((5, 0), window=self.records_frame, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", self.on_mw_authors)
        self.update_writers()
    # поиск авторов
    def find_authors(self, event):

        if self.cbox_writers.get() == "По имени":
            self.update_writers(name=self.ent_find_author.get().capitalize())
        elif self.cbox_writers.get() == "Раньше даты":
            self.update_writers(sign="<", date=self.ent_find_author.get())
        elif self.cbox_writers.get() == "Позже даты":
            self.update_writers(date=self.ent_find_author.get())
        elif self.cbox_writers.get() == "По стране":
            self.update_writers(country=self.ent_find_author.get().capitalize())
    # обновление страницы писателей
    def update_writers(self, name="", sign=">", date=0, country=""):

        widgets = self.records_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
        self.writer_records = get_writers_data("writers", name=name, sign=sign, date=date, country=country)
        for i in range(len(self.writer_records)):
            img = Image.open(io.BytesIO(self.writer_records[i][5]))
            img = img.resize((125, 125), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.author_button(self.records_frame, photo, self.writer_records[i], i)
    # создание списка авторов
    def author_button(self, master, image, data, row):
        btn = Button(master, image=image, font="16", bg="#fff",
                     text=data[1] + "\nГод Рождения:" + str(data[2]) + "                          "
                                                                       "                          "
                                                                       "                          "
                                                                       "Больше об авторе          \nСтрана: " + data[3],
                     compound="left", anchor="nw", justify="left")
        btn.image = image
        btn.bind('<Double-Button-1>', lambda e: self.author_info(e, data, image))
        btn.grid(row=row, column=0, columnspan=2, sticky="nwse", pady=5, padx=5)
    # интерфейс информации об авторе
    def author_info(self, event, data, image):
        window = Toplevel(self.app)
        window.title(data[1])
        window.iconphoto(False, image)
        resize_window(window, 800, 600)
        window.grid_rowconfigure((1, 3), weight=1)
        window.grid_columnconfigure(0, weight=1)
        lbl_text = Label(window, text="Биография")
        lbl_text.grid(row=0, column=0, sticky="nwse")
        text = Text(window, wrap=WORD, font="14")
        text.insert(1.0, data[4].decode("utf-8"))
        text.grid(row=1, column=0, sticky="nwse")
        lbl_works = Label(window, text="Произведения")
        lbl_works.grid(row=2, column=0, sticky="nwse")
        box_works = Listbox(window, font="14")
        box_works.grid(row=3, column=0, sticky="nwse")
        works = get_author_works(data[0])
        for work in works:
            box_works.insert(END, work[0])
        btn_close = Button(window, text="Закрыть", command=window.destroy)
        btn_close.grid(row=4, column=0)
    # отвечает за прокрутку списка авторов
    def on_mw_authors(self, event):
        try:
            if str(self.app.focus_get())[:3] in ".!frame2.!entry":
                if len(self.writer_records) > 3:
                    self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except _tkinter.TclError:
            pass
    # интерфейс страницы произведений
    def works_page(self, event):
        self.change_page(event.widget)
        self.page_frame.grid_rowconfigure(0, weight=1)
        self.page_frame.grid_rowconfigure(1, weight=10)

        self.page_frame.grid_columnconfigure((1, 2, 3), weight=3)
        lbl_find_works = Label(self.page_frame, text="Поиск")
        lbl_find_works.grid(column=0, row=0, sticky="nswe", pady=20)
        # ограничение поиска произведения по критериям
        def is_valid_work(new_val):
            if self.cbox_works.get() in ("По названию", "По жанру"):
                return self.parsing(r"[а-яА-Я ]", new_val)
            elif self.cbox_works.get() in ("Раньше даты", "Позже даты"):
                try:
                    if int(new_val) <= 2023:
                        return self.parsing(r"[\d]", new_val)
                    else:
                        return False
                except ValueError:
                    return self.parsing(r"[\d]", new_val)

        check = (self.app.register(is_valid_work), "%P")
        self.ent_find_work = Entry(self.page_frame, font="Tahoma, 14", validate="key", validatecommand=check)
        self.ent_find_work.grid(row=0, column=1, sticky="we")
        self.cbox_works = Combobox(self.page_frame, values=["По названию", "Раньше даты", "Позже даты", "По жанру"])
        self.cbox_works.grid(row=0, column=2, sticky="we")
        self.cbox_works.current(0)
        btn_find_work = Button(self.page_frame, text="Найти", )
        btn_find_work.grid(row=0, column=3, sticky="we")
        btn_find_work.bind('<Double-Button-1>', self.find_works)
        self.canvas_work = Canvas(self.page_frame, highlightthickness=0)
        self.canvas_work.grid(column=0, columnspan=4, row=1, sticky="nwse")
        self.canvas_work.grid_columnconfigure(0, weight=1)
        scrollbar = Scrollbar(self.canvas_work, orient=VERTICAL, command=self.canvas_work.yview)
        self.canvas_work.configure(yscrollcommand=scrollbar.set)
        self.canvas_work.bind('<Configure>',
                              lambda e: self.canvas_work.configure(scrollregion=self.canvas_work.bbox("all")))

        self.work_records_frame = Frame(self.canvas_work)
        self.canvas_work.create_window((175, 0), window=self.work_records_frame, anchor="nw")
        self.canvas_work.bind_all("<MouseWheel>", self.on_mw_work)
        self.update_works()
    # поиск произведений
    def find_works(self, event):

        if self.cbox_works.get() == "По названию":
            self.update_works(name=self.ent_find_work.get().capitalize())
        elif self.cbox_works.get() == "Раньше даты":
            self.update_works(sign="<", date=self.ent_find_work.get())
        elif self.cbox_works.get() == "Позже даты":
            self.update_works(date=self.ent_find_work.get())
        elif self.cbox_works.get() == "По жанру":
            self.update_works(genre=self.ent_find_work.get().capitalize())
    # обновление страницы произведений
    def update_works(self, name="", sign=">", date=0, genre=""):
        widgets = self.work_records_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()
        self.works_records = get_works_data("works", name=name, sign=sign, date=date, genre=genre)
        for i in range(len(self.works_records)):
            self.work_label(self.work_records_frame, self.works_records[i], i)
    # создание списка произведений
    def work_label(self, master, data, row):
        btn = Label(master, font="20", bg="#fff",
                    text=f"{data[3]}\n\n{author_name(data[1])}\n\n"
                         f"Год написания: {data[4]}                    "
                         f"Жанр: {genre_name(data[2])}                 ",
                    compound="left", anchor="nw", justify="left", borderwidth=3,
                    highlightthickness=3, highlightbackground="#000")
        btn.grid(row=row, column=0, columnspan=2, sticky="nwse", pady=5, padx=5)
    # отвечает за прокрутку списка произведений
    def on_mw_work(self, event):
        try:
            if str(self.app.focus_get())[:3] in ".!frame2.!entry":
                if len(self.works_records) > 4:
                    self.canvas_work.yview_scroll(-1 * (event.delta // 120), "units")
                self.canvas_work.configure(scrollregion=self.canvas_work.bbox("all"))
        except _tkinter.TclError:
            pass


class RootGui(Gui):
    def __init__(self, user):
        super().__init__(user=user)
        # код интерфейса администратора
        self.lbl_add_work_error = None
        self.app.mainloop()
    # интерфейс страницы авторов для администратора
    def authors_page(self, event):
        self.change_page(event.widget)
        self.page_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.page_frame.grid_columnconfigure((1, 2, 3), weight=1)

        lbl_title = Label(self.page_frame, text="Добавить автора")
        lbl_title.grid(row=0, column=0, columnspan=4)

        lbl_full_name = Label(self.page_frame, text="Полное имя автора: ")
        lbl_full_name.grid(row=1, column=0, sticky="e")
        ent_full_name = Entry(self.page_frame)
        ent_full_name.grid(row=1, column=1, columnspan=2, sticky="we")

        lbl_year_of_birth = Label(self.page_frame, text="Год рождения: ")
        lbl_year_of_birth.grid(row=2, column=0, sticky="e")
        ent_year_of_birth = Entry(self.page_frame)
        ent_year_of_birth.grid(row=2, column=1, columnspan=2, sticky="we")

        lbl_country = Label(self.page_frame, text="Страна: ")
        lbl_country.grid(row=3, column=0, sticky="e")
        ent_country = Entry(self.page_frame)
        ent_country.grid(row=3, column=1, columnspan=2, sticky="we")

        lbl_biography = Label(self.page_frame, text="Имя файла биографии в формате .txt: ")
        lbl_biography.grid(row=4, column=0, sticky="e")
        ent_biography = Entry(self.page_frame)
        ent_biography.grid(row=4, column=1, columnspan=2, sticky="we")

        lbl_portrait = Label(self.page_frame, text="Имя файла портрета в формате .png: ")
        lbl_portrait.grid(row=5, column=0, sticky="e")
        ent_portrait = Entry(self.page_frame)
        ent_portrait.grid(row=5, column=1, columnspan=2, sticky="we")

        btn_add_author = Button(self.page_frame, text="Добавить")
        btn_add_author.bind('<Double-Button-1>', lambda e: self.add_author(
            ent_full_name.get(),
            ent_year_of_birth.get(),
            ent_country.get(),
            ent_biography.get(),
            ent_portrait.get()))

        btn_add_author.grid(row=6, column=0, columnspan=4)
    # добавление автора в систему
    def add_author(self, author="", year="", country="", biography_path="", portrait_path=""):
        data = [author, year, country, biography_path, portrait_path]
        add_author_record(data)
    # интерфейс страницы произведений для администратора
    def works_page(self, event):
        self.change_page(event.widget)

        self.page_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.page_frame.grid_columnconfigure((1, 2, 3), weight=1)

        lbl_title = Label(self.page_frame, text="Добавить произведение")
        lbl_title.grid(row=0, column=0, columnspan=4)

        lbl_name = Label(self.page_frame, text="Название: ")
        lbl_name.grid(row=1, column=0, sticky="e")
        ent_name = Entry(self.page_frame)
        ent_name.grid(row=1, column=1, columnspan=2, sticky="we")

        lbl_year_of_writing = Label(self.page_frame, text="Год написания: ")
        lbl_year_of_writing.grid(row=2, column=0, sticky="e")
        ent_year_of_writing = Entry(self.page_frame)
        ent_year_of_writing.grid(row=2, column=1, columnspan=2, sticky="we")

        lbl_genre = Label(self.page_frame, text="Жанр: ")
        lbl_genre.grid(row=3, column=0, sticky="e")
        ent_genre = Entry(self.page_frame)
        ent_genre.grid(row=3, column=1, columnspan=2, sticky="we")

        lbl_author = Label(self.page_frame, text="Полное имя автора: ")
        lbl_author.grid(row=4, column=0, sticky="e")
        ent_author = Entry(self.page_frame)
        ent_author.grid(row=4, column=1, columnspan=2, sticky="we")

        btn_add_author = Button(self.page_frame, text="Добавить")
        btn_add_author.bind('<Double-Button-1>', lambda e: self.add_work(
            ent_author.get(),
            ent_genre.get(),
            ent_name.get(),
            ent_year_of_writing.get()))
        btn_add_author.grid(row=5, column=0, columnspan=4)
        self.lbl_add_work_error = Label(self.page_frame, text="")
        self.lbl_add_work_error.grid(row=6, column=0, columnspan=4)
    # добавление произведения в систему
    def add_work(self, author, genre, name, year):
        try:
            data = [author, genre, name, year]
            add_work_record(data)
            self.lbl_add_work_error["text"] = f"Произведение '{data[2]}' успешно добавлено"
        except sqlite3.IntegrityError:
            self.lbl_add_work_error["text"] = "Произведение уже есть в системе"

        except TypeError:
            self.lbl_add_work_error["text"] = "Поля не заполнены"
