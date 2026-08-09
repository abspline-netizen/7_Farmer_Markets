
import sqlite3
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class ReviewManager:
    def __init__(self, db_path, fmid):
        self.db_path = resource_path(db_path)
        self.fmid = fmid

    def review_add(self, user_name, rating, comment):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO review_table (user_name, fmid, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (user_name, self.fmid, rating, comment))

        conn.commit()
        conn.close()

        self.average_rating()
        return True

    def review_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, user_name, rating, comment, average_rating
            FROM review_table     
            WHERE rating IS NOT NULL AND rating > 0       
            ORDER BY id             
        ''', )

        rows = cursor.fetchall()
        conn.close()
        return rows

    def review_get(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_name, rating, comment, average_rating
            FROM review_table
            WHERE fmid = ?
            ORDER BY rating DESC
        ''', (self.fmid,))

        rows = cursor.fetchall()
        conn.close()
        return rows

    def average_rating(self):
        with sqlite3.connect(self.db_path) as conn:

            cursor = conn.cursor()

            cursor.execute('''
            SELECT AVG(rating)
                FROM review_table
                WHERE fmid = ?
            ''', (self.fmid,))

            avg = cursor.fetchone()[0]
            avg = round(avg, 1) if avg is not None else None

            cursor.execute('''
                UPDATE review_table
                SET average_rating = ?
                WHERE fmid = ?
            ''', (avg, self.fmid))


    def delete_review(self, review_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM review_table WHERE id=?", (review_id,))

        conn.commit()
        conn.close()
        self.average_rating()
        return True