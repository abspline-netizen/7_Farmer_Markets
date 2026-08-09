import sqlite3
import math
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)




class DatabaseReader:
    def __init__(self, db_path: str): #передаем строку-путь к файлу бд
        self.db_path = resource_path(db_path)

    def get_connection(self): #уцстанавливаем соединение
        return sqlite3.connect(self.db_path)

    def read_table(self, table_name: str):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT t.*, avg_table.average_rating
                FROM {table_name} t
                LEFT JOIN (
                    SELECT fmid, AVG(rating) AS average_rating
                    FROM review_table
                    GROUP BY fmid
                ) AS avg_table
                ON t.fmid = avg_table.fmid
                """)
            rows = cursor.fetchall()
            dict_rows = [dict(row) for row in rows]
            return dict_rows

    def find_by_zip(self,table_name: str, zip_code: str):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE zip = ?", (zip_code,))
            rows = cursor.fetchall() #все найденные строки
            return [dict(row) for row in rows]

    def find_by_cs(self,table_name: str, city_name: str, state_name: str):#поиск по городу и штату
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE city = ? AND state = ?", (city_name,state_name))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def zip_to_coord(self,table_name: str, zip_code: str):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE zip = ?", (zip_code,))
            rows = cursor.fetchall()
            if not rows:
                return None
            for row in rows:
                if row["zip"] == zip_code:
                    return row["lat"], row["lon"]

            return None

    def hv_dist_miles(self, lat1, lon1, lat2, lon2): #определение расстояния меджу точками
        R = 3958.8 # Средний радиус Земли в милях
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2

        phi1 = math.radians(self.lat1) # Перевод координат из градусов в радианы
        phi2 = math.radians(self.lat2)
        delta_phi = math.radians(self.lat2 - self.lat1)
        delta_lambda = math.radians(self.lon2 - self.lon1)

        # Формула гаверсинусов
        a = (math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Кратчайшее расстояние
        distance = R * c
        return distance

    def dist_calculation(self,table_name: str, zip_code):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # получение координат исходной точки через зип
        coord = self.zip_to_coord("markets", zip_code)
        if coord is None:
            return None

        lat1, lon1 = coord
        lat1 = float(lat1)
        lon1 = float(lon1)
            # расчитываем дистанцию и складываем в словарь по fmid
        save_dist = {}
        for row in rows:
            lat2 = row["lat"]
            lon2 = row["lon"]

            if lat2 is None or lon2 is None:
                continue
            if lat2 == "" or lon2 == "":
                continue

            lat2 = float(lat2)
            lon2 = float(lon2)

            dist = self.hv_dist_miles(lat1, lon1, lat2, lon2)
            dist_key = (round(dist, 1))
            save_dist[dist_key] = dict(row)
        return save_dist

class PageManager:
    def __init__(self, data: list[dict], divader: int = 10):
        self.data = data
        self.divader = divader
        self.total_pages = ((len(data)-1)//divader)+1
        self.current_page = 1

    def get_page(self, page: int):
        if page<1:
            page = 1
        if page>=self.total_pages:
            page = self.total_pages

        self.current_page = page

        start = (page-1)*self.divader
        end = start + self.divader
        return self.data[start:end]

    def divader_fn(self, value: int):
        self.divader = value
        self.total_pages = math.ceil(len(self.data) / self.divader)

        if self.current_page > self.total_pages: #не далее суммы страниц
            self.current_page = self.total_pages

class MarketFinder:
    def __init__(self, db_reader: DatabaseReader):#композиция
              self.db_reader = db_reader
    def get_all(self):
        return self.db_reader.read_table("markets")

    def search_zip(self, zip_code):
        return self.db_reader.find_by_zip("markets", zip_code)

    def search_city_state(self, city, state):
        return self.db_reader.find_by_cs("markets", city, state)

    def get_dist(self, zip_code):
        return self.db_reader.dist_calculation("markets", zip_code)

    def dist_readius(self, dict_save, radius = 30, revers = False): #прнинемает словарь хранения результатов вычислений дистанции
        result = {}
        for dist, market in dict_save.items():
            if dist<=radius:
                result[dist] = market

        sorted_dict = dict(sorted(result.items(),reverse=revers ))

        sorted_list = []
        for dist, market in sorted_dict.items():
            new_dict = {"dist" : dist} #расстояния добавляются первыми
            new_dict.update(market) #затем остальные ключи
            sorted_list.append(new_dict)

        return sorted_list

if __name__ == '__main__':
    pass
    # db = DatabaseReader('farmer_markets.db')
    # print(db.dist_calculation("markets", "45402"))

    # db.find_by_zip('markets', '45402')
    # print(db.find_by_cs('markets', 'Dayton','Ohio'))


