from tkinter import Label, Entry, Frame, Text, END

def print_page(rows, current_page, total_pages, divader,  text_widget):
    text_widget.delete("1.0", "end")  # очистить текстовое поле

    text_widget.tag_configure("center", justify='center')#центрирование

    width = 30  # значение по умолчанию

    # Создаем разделительную линию динамической длины
    separator = '.' * width

    if not rows:
        text_widget.insert("end", "Нет данных для отображения","center")
        return

    for row in rows:
        line = ",    ".join(str(v) for v in row.values())
        text_widget.insert("end", f"{line}\n")
        text_widget.insert("end", f"{separator}\n", "center")


def update_page_label(label, current_page, total_page):
    label.config(text=f"Страница {current_page} из {total_page}")

def update_divader_label(label, divader):
    label.config(text=f"Строк на странице {divader}")



