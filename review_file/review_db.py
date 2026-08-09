import sqlite3
import os

import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ReviewDatabase:
    def __init__(self, db_path):
        self.db_path = resource_path(db_path)

    def init_review_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
             CREATE TABLE IF NOT EXISTS review_table (
             ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             user_name TEXT NOT NULL,
             fmid INTEGER NOT NULL,
             rating INTEGER NOT NULL,
             comment TEXT,
             average_rating REAL,
             created_at TEXT DEFAULT CURRENT_TIMESTAMP,
             FOREIGN KEY (fmid) REFERENCES markets(fmid))
        ''')

        conn.commit()
        conn.close()

if __name__ == '__main__':
    pass
    # rw_db = ReviewDatabase('farmer_markets.db')
    # rw_db.init_review_table()
