import re
from tkinter import *
from tkinter import font
from tkinter import messagebox

from review_file.gui_rw import ReviewWindow
from review_file.review_controller import ReviewController
from review_file.review_model import ReviewManager

class MainWindow(Frame):
    def __init__(self, master, page_controller, market_finder, db_path="farmer_markets.db"):
        super().__init__(master)
        self.master = master
        self.page_controller = page_controller
        self.market_finder = market_finder

        self.text_widget = None
        self.l_divader_pos = None
        self.l_pg_pos = None
        self.zip_cs_visibl_frame = None
        self.entr_visibl_frame = None
        #к отзывам
        self.selected_fmid = None
        self.review_button = None

        self.db_path = db_path
        self.review_model = None
        self.review_controller = None
        self.font_main = font.Font(family="Arial", size=14)
        self.font_settings = font.Font(family="Arial", size=12)

        self.master.after(10, self.init_sizes_mw)
        self.pack(fill="both", expand=True)

    def init_sizes_mw(self):
        self.screen_width = self.master.winfo_width()
        self.screen_height = self.master.winfo_height()
        div = 21
        self.r_h = self.screen_height // div #relative_height
        self.r_w = self.screen_width // div #relative_width

        self.build_ui()

    def open_settings(self):
        win = Toplevel(self.master)
        win.title("Настройки")
        win.geometry("400x300")

        # чтобы окно было поверх
        win.transient(self.master)
        win.grab_set()  # делает окно модальным

        Label(win, text="Настройки приложения",  font = self.font_settings).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(win, text="Размер шрифта:", font = self.font_settings).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # изменение размера шрифта
        spinbox = Spinbox(win, from_=8, to=20, width=5, font=self.font_settings)
        spinbox.grid(row=1, column=1, padx=10, pady=10, sticky="e")
#панель аминистратора.

        self.review_model = ReviewManager("farmer_markets.db", None)
        self.review_controller = ReviewController(self.review_model)
        Button(win, text="Панель администратора", command=self.open_admin_panel).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        def save_settings():
            font_size = int(spinbox.get())
            self.font_main.configure(size=font_size)
            win.destroy()
        Button(win, text="Отменить", font=self.font_settings, command=win.destroy).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        Button(win, text="Сохранить", font=self.font_settings, command=save_settings).grid(row=3, column=1, padx=10, pady=10, sticky="e")

    def open_admin_panel(self):
        self.review_model = ReviewManager(self.db_path, None)
        self.review_controller = ReviewController(self.review_model)

        admin_window = ReviewWindow(self.master, self.review_controller)
        admin_window.admin_window()

    def highlight_line(self,event):
        # убрать старую подсветку
        self.text_widget.tag_remove("sel_line", "1.0", "end")

        # получить индекс строки по координатам клика
        index = self.text_widget.index(f"@{event.x},{event.y}")
        line = index.split(".")[0]

        # подсветить строку
        self.text_widget.tag_add("sel_line", f"{line}.0", f"{line}.end")
        self.text_widget.tag_config("sel_line", background="lightblue")

        # получить текст строки
        row_text = self.text_widget.get(f"{line}.0", f"{line}.end")
        # print("Выбрана строка:", row_text)
        self.page_controller.selected_row = row_text

        self.selected_fmid = self.extract_fmid(row_text)
        #управление активностью кнопки отзывов
        if self.review_button:
            self.review_button.config(state="normal")
            self.selected_fmid
        elif self.review_button:
            self.review_button.config(state="disabled")

    def extract_fmid(self,row_text):
        match = re.search(r'\b(\d{7,})\b', row_text)
        if match:
            return match.group(1)
        return None

    def open_review_window(self):
        if not self.selected_fmid:
            messagebox.showwarning("Предупреждение", "Сначала выберите рынок из списка")
            return
        if self.selected_fmid:
            # Передаем FMID в окно отзывов
            self.review_model = ReviewManager("farmer_markets.db", self.selected_fmid)
            self.review_controller = ReviewController(self.review_model)

            review_window = ReviewWindow(self.master,self.review_controller)
            review_window.comment_window(fmid=self.selected_fmid)
        else:
            messagebox.showwarning("Предупреждение", "Сначала выберите рынок из списка")

    def build_ui(self):
            self.top_bar()
            self.navi_bar()
            self.zip_cs_frame()

            self.page_controller.attach_view(
                            self.text_widget,
                            self.l_pg_pos,
                            self.l_divader_pos
                        )
            rows = self.market_finder.get_all()
            self.page_controller.update_rows(rows)
            self.page_controller.show_page()

            Button(self.master, text="Открыть настройки",
                   command=self.open_settings,
                   font=self.font_settings
                   ).place(x=10, y=10)
            #кнопка Отзывы
            self.review_button = Button(self.entr_visibl_frame, text="Оставить отзыв",
                   command=self.open_review_window,
                   font=self.font_main, state="disabled")
            self.review_button.grid(row=4, column=6, padx=0, pady=0, sticky="e")

    def top_bar(self):
    #   выбор режима обработки данных о фермерских рынках
        self.mode_var = IntVar(value=1) #изменяеться от 1 до 3

        radio_frame = Frame(
            self.master,
            highlightthickness=0,
            highlightbackground="gray",
            highlightcolor="gray",
            padx = 10,
            pady = 10,
            bg=self.master["bg"]
        )

        radio_frame.place(
            x= (self.screen_width - self.r_w * 20) // 2,  # центрируем блок радиокнопок
            y=self.r_h,
            width=self.r_w * 20,
            height=self.r_h * 2
        )

        radio_frame.columnconfigure(0, weight=1)
        radio_frame.columnconfigure(1, weight=1)
        # radio_frame.columnconfigure(2, weight=1)

        radio_frame.rowconfigure(0, weight=1)
        #изменяет mode_var
        Radiobutton(radio_frame, text="Просмотр всех фермерских рынков", variable=self.mode_var, value=1, font = self.font_main).grid(row=0, column=0, sticky="nsew", padx=10)
        Radiobutton(radio_frame, text="Поиск фермерских рынков", variable=self.mode_var, value=2, font = self.font_main).grid(row=0, column=1, sticky="nsew", padx=10)

        #поле для вывода основного текста
        text_frame = Frame(master=self.master,
                        relief=SUNKEN,
                        borderwidth=5,
                        bg="white",
                        padx=10,
                        pady=10
                        )
        text_frame.pack(fill=X)
        self.frame_height = self.r_h * 10
        self.frame_width = self.r_w * 20
        text_frame.place(x=((self.screen_width - self.frame_width) // 2) , #Позиция по ширине
                    y=((self.screen_height - self.frame_height) // 2) - 2*self.r_h, #Позиция по высоте
                    width=self.frame_width,
                    height=self.frame_height)

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_widget = Text(text_frame, font=self.font_main, yscrollcommand=scrollbar.set)
        self.text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_widget.yview)

        # привязка события
        self.text_widget.bind("<Button-1>", self.highlight_line)
        self.mode_var.trace_add("write", self.text_fild_update)

        self.mode_var.trace('w', self.rb_main_change)
        self.rb_main_change()
     # Обновление текстового поля
    def text_fild_update(self, *args):
        concurrent = self.mode_var.get()
        if concurrent == 1:
            rows = self.market_finder.get_all()
            self.page_controller.update_rows(rows)

    def navi_bar(self):
    #кнопки навигации
        navi_frame = Frame(
            self.master,
            highlightthickness=2, # толщина рамки
            highlightbackground="gray",# цвет рамки
            highlightcolor="gray",# цвет рамки при фокусе
            padx = 10,
            pady = 6,
            bg=self.master["bg"] # фон совпадает с фоном окна
        )

        navi_frame.place(
            x= (self.screen_width - self.r_w * 20) // 2,
            y=13*self.r_h,

            width=self.r_w * 20,
            height=self.r_h * 2
        )
        navi_frame.grid_rowconfigure(0, weight=1)
        navi_frame.grid_rowconfigure(1, weight=1)

        l_prev_pg = Label(navi_frame, text="<<< Назад", font = self.font_main)
        l_prev_pg.grid(row=0, column=0, padx=10, pady=6, sticky="w")

        l_start = Label(navi_frame, text="||<< К первой странице", font = self.font_main)
        l_start.grid(row=1, column=0, padx=10, pady=6, sticky="w")

        self.l_pg_pos = Label(navi_frame, text= "Вы на странице  __ из __", font =self.font_main)
        self.l_pg_pos.grid(row=0, column=1, padx=10, pady=6)

        self.l_divader_pos = Label(navi_frame, text= "Показано строк на странице __", font = self.font_main)
        self.l_divader_pos.grid(row=1, column=1, padx=10, pady=6)

        l_pg_jamp = Label(navi_frame, text= "Перейти на страницу:", font = self.font_main)
        l_pg_jamp.grid(row=0, column=2, padx=0, pady=6, sticky="e")

        l_divader_inp = Label(navi_frame, text= "Показывать строк на странице:", font =self.font_main)
        l_divader_inp.grid(row=1, column=2, padx=0, pady=6, sticky="e")

        self.e_pg_jamp = Entry(navi_frame, width=10, font = self.font_main)
        self.e_pg_jamp.grid(row=0, column=3, padx=0, pady=6, sticky="w")

        self.e_divader_inp = Entry(navi_frame, width=10, font = self.font_main)
        self.e_divader_inp.grid(row=1, column=3, padx=0, pady=6, sticky="w")

        l_ahead = Label(navi_frame, text= "Вперед >>>", font =self.font_main)
        l_ahead.grid(row=0, column=4, padx=10, pady=6, sticky="e")

        l_to_last = Label(navi_frame, text= "К последней странице >>||", font = self.font_main)
        l_to_last.grid(row=1, column=4, padx=10, pady=6, sticky="e")

        for i in range(5):
            navi_frame.columnconfigure(i, weight=1)

        l_ahead.bind("<Button-1>", lambda e: self.page_controller.next_page())
        l_prev_pg.bind("<Button-1>", lambda e: self.page_controller.prev_page())
        l_to_last.bind("<Button-1>", lambda e: self.page_controller.go_last())
        l_start.bind("<Button-1>", lambda e: self.page_controller.go_first())

        self.e_divader_inp.bind("<Return>", self.divader_inp)
        self.e_pg_jamp.bind("<Return>", self.pg_jump)


    def divader_inp(self, event):
        divader = self.e_divader_inp.get()
        self.page_controller.set_divader(divader)

    def pg_jump(self, event):
        page = self.e_pg_jamp.get()
        self.page_controller.to_page(page)

#проверка ввода (валидация)
    def validate_zip(self, input_value):
        if input_value == "" or (input_value.isdigit() and len(input_value) <=5):
            return True
        return False

    def validate_cs(self, input_value):
        permit_ch = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .'-")
        if input_value == "":
            return True
        return all(ch in permit_ch for ch in input_value)

    def validate_dist(self, input_value):
        if input_value == "" or input_value.isdigit():
            return True
        return False

    def zip_cs_frame(self):
    # поиск рынков по зип коду и городу и штату - переключение режимов радиокнопок
        self.zcs_var = IntVar(value=1) #изменяеться от 1 до 3

        self.zip_cs_frame = Frame( # для позиционирования по блокам
            self.master,
            highlightthickness=2,
            highlightbackground="gray",
            highlightcolor="gray",
            padx = 10,
            pady = 10,
            bg=self.master["bg"]
        )

        self.zip_cs_frame.place( #для размещения блока на экране
            x= (self.screen_width - self.r_w * 20) // 2,
            y=15*self.r_h,
            width=self.r_w * 20,
            height=self.r_h * 2
        )
        self.zip_cs_visibl_frame = Frame( # для регулировки видимости
            self.zip_cs_frame,
            highlightthickness=0,
            highlightbackground="gray",
            highlightcolor="gray",
            padx = 0,
            pady = 0,
            bg=self.master["bg"]
        )

        self.zip_cs_visibl_frame.grid(row=0, column=0, sticky="nsew", pady=0)
    # Чтобы grid растягивался на весь zip_cs_frame
        self.zip_cs_frame.grid_rowconfigure(0, weight=1)
        self.zip_cs_frame.grid_columnconfigure(0, weight=1)

        self.zip_cs_visibl_frame.columnconfigure(0, weight=1)
        self.zip_cs_visibl_frame.columnconfigure(1, weight=1)
        self.zip_cs_visibl_frame.columnconfigure(2, weight=1)

        Radiobutton(self.zip_cs_visibl_frame, text="По названию города и штата", variable=self.zcs_var, value=1, font = self.font_main).grid(row=0, column=0, sticky="", padx=10)
        Radiobutton(self.zip_cs_visibl_frame, text="По zip коду", variable=self.zcs_var, value=2, font = self.font_main).grid(row=0, column=1, sticky="", padx=10)


    # поля ввода для поиска
        self.entr_fields_frame = Frame(
            self.master,
            highlightthickness=2,# толщина рамки
            highlightbackground="gray",# цвет рамки
            highlightcolor="gray",# цвет рамки при фокусе
            padx = 10,
            pady = 10,
            bg=self.master["bg"]# фон совпадает с фоном окна
        )

        self.entr_fields_frame.place(
            x= (self.screen_width - self.r_w * 20) // 2,
            y=16*self.r_h,
            width=self.r_w * 20,
            height=self.r_h * 4
        )
        self.entr_visibl_frame = Frame(self.entr_fields_frame, highlightthickness=0, bg=self.master["bg"])
        self.entr_visibl_frame.grid(row=0, column=0, sticky="nsew")
    #растягивание одной ячейки внутри entr_fields_frame
        self.entr_fields_frame.grid_rowconfigure(0, weight=1)
        self.entr_fields_frame.grid_columnconfigure(0, weight=1)

        self.entr_visibl_frame.grid_rowconfigure(0, weight=1)
        self.entr_visibl_frame.grid_rowconfigure(1, weight=1)
        self.entr_visibl_frame.grid_rowconfigure(2, weight=0)
        self.entr_visibl_frame.grid_rowconfigure(3, weight=0)
        self.entr_visibl_frame.grid_rowconfigure(4, weight=0)

        self.entr_visibl_frame.grid_columnconfigure(0, weight=1)
        self.entr_visibl_frame.grid_columnconfigure(1, weight=1)
        self.entr_visibl_frame.grid_columnconfigure(2, weight=1)
        self.entr_visibl_frame.grid_columnconfigure(3, weight=1)
        self.entr_visibl_frame.grid_columnconfigure(4, weight=1)
        self.entr_visibl_frame.grid_columnconfigure(5, weight=1)
        self.entr_visibl_frame.grid_columnconfigure(6, weight=0)
    #использование валидации
        val_cmnd_zip = (self.entr_visibl_frame.register(self.validate_zip), '%P')
        val_cmnd_cs = (self.entr_visibl_frame.register(self.validate_cs), '%P')
        val_cmnd_dist = (self.entr_visibl_frame.register(self.validate_dist), '%P')
    #ввод названия города и штата
        self.l_city_name = Label(self.entr_visibl_frame, text="Ведите название города", font = self.font_main)
        self.l_city_name.grid(row=0, column=0, padx=10, pady=6, sticky="e")

        self.e_city_name = Entry(self.entr_visibl_frame, width=20, font = self.font_main, validate="key", validatecommand = val_cmnd_cs)
        self.e_city_name.grid(row=0, column=1, padx=0, pady=6, sticky="ew")

        self.l_state_name = Label(self.entr_visibl_frame, text="Введите название штата", font=self.font_main)
        self.l_state_name.grid(row=1, column=0, padx=10, pady=6, sticky="e")

        self.e_state_name = Entry(self.entr_visibl_frame, width=20, font = self.font_main, validate="key", validatecommand = val_cmnd_cs)
        self.e_state_name.grid(row=1, column=1, padx=0, pady=6, sticky="ew")

        self.b_cs_entr = Button(self.entr_visibl_frame, text="Поиск", command=self.on_search_cs, font=self.font_main)
        self.b_cs_entr.grid(row=1, column=2, padx=0, pady=0, sticky="w")

        #ввод зип кода
        self.l_zip = Label(self.entr_visibl_frame, text="Ведите zip код", font = self.font_main)
        self.l_zip.grid(row=3, column=0, padx=10, pady=6, sticky="e")

        self.e_zip = Entry(self.entr_visibl_frame, width=20, font = self.font_main,  validate="key", validatecommand = val_cmnd_zip )
        self.e_zip.grid(row=3, column=1, padx=0, pady=6, sticky="ew")

        self.b_zip_entr = Button(self.entr_visibl_frame, text="Поиск", command=self.on_search_zip, font=self.font_main)
        self.b_zip_entr.grid(row=3, column=2, padx=0, pady=0, sticky="w")

        #поиск по расстоянию
        self.l_dist = Label(self.entr_visibl_frame, text="Найти все рынки на расстоянии, миль", font = self.font_main)
        self.l_dist.grid(row=4, column = 0, padx=10, pady=6, sticky="e")

        dist_var = StringVar(value="30")
        self.e_dist = Entry(self.entr_visibl_frame,textvariable=dist_var, width=20, font = self.font_main, validate="key", validatecommand = val_cmnd_dist)
        self.e_dist.grid(row=4, column=1, padx=0, pady=6, sticky="ew")


        self.b_dist = Button(self.entr_visibl_frame, text="Поиск", command=lambda: self.radius_switch(False), font=self.font_main)
        self.b_dist.grid(row=4, column=2, padx=0, pady=0, sticky="w")

        self.b_min_max = Button(self.entr_visibl_frame, text="min=>max", command=lambda: self.radius_switch(False), font=self.font_main)
        self.b_min_max.grid(row=4, column=3, padx=0, pady=0, sticky="e")

        self.b_max_min = Button(self.entr_visibl_frame, text="max=>min", command=lambda: self.radius_switch(True), font=self.font_main)
        self.b_max_min.grid(row=4, column=4, padx=0, pady=0, sticky="w")

        self.zcs_var.trace("w", self.zip_cs_switch)
        self.zip_cs_switch()

        self.rb_main_change()

    #привязываем controller--gui
    def on_search_zip(self):
        self.page_controller.selected_row = None
        zip_code = self.e_zip.get()
        rows = self.market_finder.search_zip(zip_code)
        self.page_controller.update_rows(rows)

    def zip_fild_or_line(self):
        line_text = self.page_controller.selected_row
        if line_text:
            self.zip_code = self.zip_from_str(line_text)
            return self.zip_code
        else:
            self.zip_code = self.e_zip.get().strip()
            return self.zip_code

    def on_search_cs(self): #берет значения из полей ввода и находит рынок
        self.page_controller.selected_row = None
        city = self.e_city_name.get().strip()
        state = self.e_state_name.get().strip()
        rows = self.market_finder.search_city_state(city, state)
        # print(f"rows = {rows}")
        self.page_controller.update_rows(rows)

    def radius_search_zip(self, revers=False): #ищет рынке в радиусе
        self.zip_code = self.zip_fild_or_line()
        if not (self.zip_code and self.zip_code.isdigit() and len(self.zip_code) == 5):
            return
        get_radius = float(self.e_dist.get())
        dist_result = self.market_finder.get_dist(self.zip_code)
        sort_dist = self.market_finder.dist_readius(dist_result, get_radius, revers) #нужно соединить с кнопкой
        self.page_controller.update_rows(sort_dist)
    #получение зип от выбранной строки
    def zip_from_str(self, line_text): #ищет зип по выбранной строке по признакам (5 цифр)
        match = re.search(r'\b\d{5}\b', line_text)
        # print(f'line_text from zip_from_str = {self.line_text}')
        return match.group(0) if match else None

    def radius_search_cs(self, revers=False):#берет строку, вычисляет дистанции от нее, сортирует по возрастанию
        self.zip_code = self.cs_fild_or_line()
        get_radius = float(self.e_dist.get())
        dist_result = self.market_finder.get_dist(self.zip_code)

        sort_dist = self.market_finder.dist_readius(dist_result, get_radius, revers) #нужно соединить с кнопкой
        self.page_controller.update_rows(sort_dist)

    def cs_fild_or_line(self):
        line_text = self.page_controller.selected_row
        if line_text:
            self.zip_code = self.zip_from_str(line_text)
            # zip_code = line_text.get("zip")
            return self.zip_code
        else:
            city = self.e_city_name.get().strip()
            state = self.e_state_name.get().strip()
            rows = self.market_finder.search_city_state(city, state)
            if not rows:
                return None
            # print(f"rows = {rows}")
            self.page_controller.update_rows(rows)
            self.page_controller.selected_row = rows[0]
            self.zip_code = rows[0].get("zip")
            return self.zip_code


    def radius_switch(self, revers):
        mode = self.zcs_var.get()

        if mode == 1:
            self.radius_search_cs(revers)
            print(f"mode revers 1= {revers}")
        elif mode == 2:
            self.radius_search_zip(revers)

    #переключатель режимов ввода город-штат/зип-код
    def zip_cs_switch(self,*arg):
        zip_cs_mode = self.zcs_var.get()

        if zip_cs_mode == 1:
            self.l_city_name.grid()
            self.e_city_name.grid()
            self.l_state_name.grid()
            self.e_state_name.grid()
            self.b_cs_entr.grid()
            self.l_zip.grid_remove()
            self.e_zip.grid_remove()
            self.b_zip_entr.grid_remove()# видимое - город и штат
        elif zip_cs_mode == 2:
            self.l_zip.grid()
            self.e_zip.grid()
            self.b_zip_entr.grid()
            self.b_cs_entr.grid_remove()
            self.l_city_name.grid_remove()
            self.e_city_name.grid_remove()
            self.l_state_name.grid_remove()
            self.e_state_name.grid_remove()# видимое - зип код

    # переменная для выбора режима после переключения радиокнопок верхнего ряда (основных)
    def rb_main_change(self, *args):
        current_condition = self.mode_var.get()

        if current_condition == 1:
            if self.zip_cs_visibl_frame:
                self.zip_cs_visibl_frame.grid_remove()
            if self.entr_visibl_frame:
                self.entr_visibl_frame.grid_remove()
        elif current_condition == 2:
            if self.zip_cs_visibl_frame:
                self.zip_cs_visibl_frame.grid()
            if self.entr_visibl_frame:
                self.entr_visibl_frame.grid()



