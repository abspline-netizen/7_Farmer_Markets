#Controller принимает ввод → обращается к Model (чтобы посчитала/обработала) → получает результат → передает его во View (чтобы вывела)t.

import view as v
import model as m


class PageController:
    def __init__(self):
        self.text_widget = None
        self.l_pg_pos = None
        self.l_divader_pos = None
        self.selected_row = None
        self.selected_row = None
        self.pm = None

    def show_page(self):
        if self.pm is None or self.text_widget is None:
            return
        rows = self.pm.get_page(self.pm.current_page)
        v.print_page(rows,
                     self.pm.current_page,
                     self.pm.total_pages,
                     self.pm.divader,
                     self.text_widget
                     )
        if self.l_divader_pos is not None:
            v.update_divader_label(self.l_divader_pos,
                                   self.pm.divader)
        if self.l_pg_pos is not None:
            v.update_page_label(self.l_pg_pos,
                                self.pm.current_page,
                                self.pm.total_pages
                                )

    def update_rows(self, new_rows):
        self.pm = m.PageManager(new_rows)
        self.show_page()
        self.selected_row = None

    def next_page(self):
        if self.pm is None:
            return
        self.pm.current_page += 1
        self.show_page()

    def prev_page(self):
        if self.pm is None:
            return
        self.pm.current_page -= 1
        self.show_page()

    def go_first(self):
        if self.pm is None:
            return
        self.pm.current_page = 1
        self.show_page()

    def go_last(self):
        self.pm.current_page = self.pm.total_pages
        self.show_page()

    def set_divader(self, divader):
        if self.pm is None:
            return
        try:
            divader = int(divader)
        except ValueError:
            # print("Ошибка. Нужно ввести целое число")
            return

        self.pm.divader_fn(divader)
        self.show_page()

    def to_page(self, page_number):
        if self.pm is None:
            return
        try:
            page_number = int(page_number)
        except ValueError:
            print("Ошибка. Нужно ввести целое число")
            return

        self.pm.current_page = page_number
        self.show_page()

    def attach_view(self, text_widget, l_pg_pos, l_divader_pos):
        self.text_widget = text_widget
        self.l_pg_pos = l_pg_pos
        self.l_divader_pos = l_divader_pos

    def set_selected_row(self, row):
        self.selected_row = row






if __name__ == '__main__':
    pass

    # инициализация review_table
    # import os
    # from review_file.review_db import ReviewDatabase
    #
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # DB_PATH = os.path.join(BASE_DIR, 'farmer_markets.db')
    #
    # rw_db = ReviewDatabase(DB_PATH)
    # rw_db.init_review_table()