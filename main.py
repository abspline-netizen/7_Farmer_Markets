import sys
import os
from tkinter import *
from controller import PageController
from model import DatabaseReader, MarketFinder
from gui_mw import MainWindow
from review_file.review_model import ReviewManager
from review_file.review_controller import ReviewController

def resource_path(relative_path):
    # Работает и в Python, и в exe
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    root = Tk()
    root.title("Фермерские рынки")
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Адаптивный размер окна
    win_w = max(1000, int(screen_w * 1.0))
    win_h = max(700, int(screen_h * 0.90))

    # Центрирование
    pos_x = (screen_w - win_w) // 2
    pos_y = (screen_h - win_h) // 2

    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    root.minsize(900, 600)
    # Создаем объекты
    db_path =  resource_path("farmer_markets.db")
    db = DatabaseReader(db_path)
    mfr = MarketFinder(db)
    cnt = PageController()

    model = ReviewManager(db_path, fmid=None)
    rwc = ReviewController(model)

    app = MainWindow(root, cnt, mfr)
    root.mainloop()

if __name__ == "__main__":
    main()