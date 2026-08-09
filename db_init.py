
import sqlite3
import csv
import sys
import os

def resource_path(relative_path):
    # Работает и в Python, и в exe
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class DatabaseInit:
    def __init__(self, db_path, csv_path):
        self.db_path = resource_path(db_path)
        self.csv_path = resource_path(csv_path)

    def initialize(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS markets (
                fmid INTEGER PRIMARY KEY,
                MarketName TEXT NOT NULL,
                street TEXT,
                city TEXT,
                County TEXT,
                State TEXT,
                zip TEXT,
                lat REAL NOT NULL,
                lon REAL NOT NULL    
        
            )
        ''')
        # lat(x)
        # lon(y)
        # Читаем CSV с заголовками
        with open('Export.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)  # Первая строка — заголовки

            for row in csv_reader:
                cursor.execute('''
                    INSERT OR IGNORE INTO markets (fmid, MarketName, street, city, County, State, zip, lat, lon) 
                    VALUES (:FMID, :MarketName, :street, :city, :County, :State, :zip, :x, :y)
                ''', row)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    fm_db = DatabaseInit('farmer_markets.db', 'Export.csv')
    fm_db.initialize()