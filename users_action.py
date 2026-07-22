import csv
import logging #log
import sys
from reader_csv_dict import short_market_list
from logging_config import setup_logging #log
import valid_check as ch

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
logger = logging.getLogger(__name__) #log


filename = "users_data_file.csv"


try:
    with open(filename, "r", encoding="utf-8") as fh:
        logger.debug("Файл %s уже существует", filename)
        pass
except FileNotFoundError:
    logger.info("Файл %s не найден, создаю новый", filename) # Создаём файл только если его нет
    with open(filename, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_ALL)
        writer.writerow(["FMID","Market_name","Имя пользователя", "Отзыв о рынке", "Рейтинг рынка"])
        logger.debug("Записаны заголовки в %s", filename)

def user_action(fmid):
    logger.info("Начало user_action для FMID=%s", fmid)
    while True:
        user_name = input("Введите имя пользователя: ").strip()
        if user_name:
            break
        print("Имя обязательно для ввода, попробуйте еще раз.")
        logger.warning("Пользователь ввёл пустое имя")

    feadback_m = input("Введите отзыв о рынке: ").strip()

    while True:
        try:
            grate_m = int(input("Поставьте оценку рынку от 1 до 5: "))
        except ValueError:
            print("Оценка обязательно для ввода, попробуйте еще раз.")
            logger.warning("Пользователь ввёл некорректную оценку (не число)")
            continue

        if 1 <= grate_m <= 5:
            break
        print("Оценка должна быть от 1 до 5, попробуйте еще раз.")
        logger.warning("Пользователь ввёл оценку вне диапазона: %s", grate_m)

    market_name = None
    # Ищем рынок
    for item in short_market_list:
        if item[0] == fmid:
            market_name = item[1]
            break

    if market_name is None:
        print("Такого рынка не найдено")
        logger.error("Рынок с FMID=%s не найден", fmid)
        return None

    # Добавление отзыва
    with open(filename, "a", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_ALL)
        writer.writerow([fmid, market_name, user_name, feadback_m, grate_m])
        logger.info("Отзыв сохранён: FMID=%s, user=%s, rating=%s",
                    fmid, user_name, grate_m)
    print("Отзыв сохранен")
    return user_name, feadback_m, grate_m

def all_feadback():
     with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(", ".join(row))


def delete_row():
    fmid = str(input("Введите FMID рынка =>"))
    user_name = str(input("Введите имя пользователя (user_name) отзыва =>"))
    new_rows = []

    bed_commands_a = {'Имя пользователя', 'FMID'}
    if ch.check_inp(bed_commands_a,fmid):
        print ("Заголовки таблицы не удаляются. Выход из команды del")
        return

    elif ch.check_inp(bed_commands_a,user_name):
        print ("Заголовки таблицы не удаляются. Выход из команды del")
        return

    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not (str(row[0]) == str(fmid).strip() and row[2].strip() == str(user_name).strip()):
                new_rows.append(row)

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    print(f"Оставшиеся отзывы\n"
          f"==================================== \n")
    all_feadback()

if __name__ == "__main__":
    setup_logging()
    # a = delete_row()
    # b = all_feadback()
    # c = user_action("1018304")



