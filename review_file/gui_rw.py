from importlib.metadata import pass_none


from tkinter import *
from tkinter import font
from tkinter import messagebox, simpledialog
from tkinter import ttk

class ReviewWindow():
    def __init__(self, master, controller):
        self.master = master

        self.controller = controller
        self.font_main = font.Font(family="Arial", size=14) #стиль и размер шрифта
        self.font_settings = font.Font(family="Arial", size=12) #стиль и размер шрифта в окне настроек


#root=>self.master
    def comment_window(self, fmid=None):
        self.current_fmid = fmid

        cw = Toplevel(self.master)
        cw.title("Оставить отзыв о рынке")
        cw.geometry("800x600")


        cw.transient(self.master)
        cw.grab_set()  # делает окно модальным

        cw.grid_rowconfigure(0, weight=0)
        cw.grid_rowconfigure(1, weight=0)
        cw.grid_rowconfigure(2, weight=1)
        cw.grid_rowconfigure(3, weight=0)
        cw.grid_rowconfigure(4, weight=0, minsize=60)
        cw.grid_columnconfigure(0, weight=1)
        cw.grid_columnconfigure(1, weight=1)

        l_user_name = Label(cw, text="Ведите имя и фамилию *",  font = self.font_main)
        l_user_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        e_user_name = Entry(cw, width=20, font = self.font_main)
        e_user_name.grid(row=0, column=1, padx=0, pady=6, sticky="w")

        l_grade = Label(cw, text="Ведите рейтинг *", font = self.font_main)
        l_grade.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        # изменение размера шрифта
        spinbox = Spinbox(cw, from_=1, to=5, width=5, font=self.font_main)
        spinbox.grid(row=1, column=1, padx=0, pady=6, sticky="w")
        spinbox.delete(0, "end")
        spinbox.insert(0, "5")

        l_text_comment = Label(cw, text="Ведите текст отзыва", font = self.font_main)
        l_text_comment.grid(row=2, column=0, padx=10, pady=10, sticky="ne")

        t_text_comment = Text(cw, width=20, font = self.font_main)
        t_text_comment.grid(row=2, column=1, padx=0, pady=6, sticky="we")

        Label(cw, text="* обязательны к заполнению", font = self.font_main).grid(row=3, column=1, padx=0, pady=6, sticky="w")

        def save_comment():
            user_name = e_user_name.get().strip()
            rating = spinbox.get()
            comment = t_text_comment.get("1.0", END).strip()
            # Валидация
            if not user_name:
                messagebox.showwarning("Error", "Enter your username")
                return

            if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                messagebox.showwarning("Error", "Enter rating (1-5)")
                return

            success = self.controller.comment_add(user_name, int(rating), comment)
            if success:
                messagebox.showinfo("Successful")
                cw.destroy()
            else:
                messagebox.showerror("Save Error")

        Button(cw, text="Отменить", font=self.font_main, command=cw.destroy).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        Button(cw, text="Сохранить", font=self.font_main, command=save_comment).grid(row=4, column=1, padx=10, pady=10, sticky="e")


    def admin_window(self):
        aw = Toplevel(self.master)
        aw.title("Администратор - удаление отзывов")
        screen_width = aw.winfo_screenwidth()
        screen_height = aw.winfo_screenheight()

        aw.geometry(aw.geometry(f"{int(screen_width*0.8)}x{int(screen_height*0.8)}"))

        # чтобы окно было поверх
        aw.transient(self.master)
        aw.grab_set()  # делает окно модальным (опционально)

        aw.grid_rowconfigure(0, weight=1)
        aw.grid_rowconfigure(1, weight=0)
        aw.grid_columnconfigure(0, weight=1)
        aw.grid_columnconfigure(1, weight=0)

        table_frame = ttk.Frame(aw, borderwidth=6, relief="solid")
        table_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.grid(row=1, column=0, sticky="ew")

        style = ttk.Style()
        style.configure("Treeview", font=self.font_main)
        style.configure("Treeview.Heading", font=self.font_main)

        spr_sheet = ttk.Treeview(
                table_frame,
                columns=("id","user_name", "rating", "comment"),
                show="headings",
                yscrollcommand=y_scroll.set,
                xscrollcommand=x_scroll.set
            )
        spr_sheet.grid(row=0, column=0, sticky="nsew")

        y_scroll.config(command=spr_sheet.yview)
        x_scroll.config(command=spr_sheet.yview)
        spr_sheet.heading("id", text = "id")
        spr_sheet.heading("user_name", text="Имя пользователя")
        spr_sheet.heading("rating", text="Рейтинг")
        spr_sheet.heading("comment", text="Отзыв")

        spr_sheet.column("id", width=80)
        spr_sheet.column("user_name", width=150)
        spr_sheet.column("rating", width=80)
        spr_sheet.column("comment", width=600)

        all_rows = self.controller.comment_all()

        for row in all_rows:
            spr_sheet.insert("", "end", values=row)

        def save_admin():
            selected = spr_sheet.selection()
            if not selected:
                messagebox.showwarning("Выберите отзыв для удаления")
                return

            item = spr_sheet.item(selected[0])
            values = item["values"]
            review_id =  values[0]
            user_name = values[1]
            # rating = values[2]
            # comment = values[3]
            # avg_rating = values[4]

            password = simpledialog.askstring(
                "Подтверждение удаления",
                "Введите пароль администратора (12345):",
                show="*"
                )

            if password == "12345":
                self.controller.comment_delete(review_id)
                spr_sheet.delete(selected[0])
            else:
                messagebox.showerror("Ошибка", "Неверный пароль")

        Button(aw, text="Удалить", font=self.font_settings, command=save_admin).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        Button(aw, text="Выйти", font=self.font_settings, command=aw.destroy).grid(row=1, column=1, padx=10, pady=10, sticky="e")


if __name__ == "__main__":
    pass