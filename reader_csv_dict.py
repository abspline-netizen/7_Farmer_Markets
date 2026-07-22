import csv
import math
import valid_check as ch




def reader_csv(file): #чтение из файла
    with open(file, 'r',encoding="utf-8", newline='') as f:
        content = csv.reader(f)
        rows=list(content)
        #for item in rows:
            #print(item)
            #print()
        return rows

def list_to_dict(rows): #запись в словари
    headers = rows[0]
    dict_market = {}

    for item in rows[1:]:
        key = item[0].strip()
        if not key.isdigit():
            print(f"Error key: {key}")

        inner = {headers[i]: item[i].strip() for i in range(1, len(item))} #генератор словарей
        dict_market[key] = inner

    return dict_market

def dict_to_list(dict_market):
    short_market_list = []
    for k,v in dict_market.items():
        row = [k] + list(v.values())
        short_market_list.append(row)
    return short_market_list

users_feadback =list_to_dict(reader_csv('users_data_file.csv'))
# print(users_feadback)


M_FILE_LIST = reader_csv('Export.csv') #глобальные значения для списка и словаря
M_FILE_DICT = list_to_dict(M_FILE_LIST)

union_dict = {}
for key in M_FILE_DICT:
    union_dict[key] = {**M_FILE_DICT[key], **users_feadback.get(key, {})}


#print(M_FILE_DICT)
def short_market_info(m_dict = union_dict): #выводит информацию из словаря в список.
    short_market_list = []
    for k, v in m_dict.items():  # укороченная информация о рынках
        row = [
            k,
            v['MarketName'],
            v['city'],
            v['State'],
            v['street'],
            v['zip'],
            v['y'], #latitude
            v['x'],
            v.get("Рейтинг рынка", "0")
        ]
        short_market_list.append(row)

    return short_market_list #Список затем подается для работы со страницей

short_market_list = short_market_info()
# print(short_market_list)


def page_bh(curr_page , cur_list, divider ):#поведение страницы - делает срез списка и печатает через пробелы
    # cur_list = short_market_list

    total_rows = len(cur_list) - 1  # минус заголовок
    total_pages = math.ceil(total_rows / divider)

    if curr_page < 1:
        curr_page = 1
    elif curr_page > total_pages:
        curr_page = total_pages


    start=1+(curr_page-1)*divider
    end = min(1 + curr_page * divider, len(cur_list))
    displ_vision = cur_list[start:end]

    for i in displ_vision:
        print(", ".join(map(str,i)))
        print()

    return curr_page

def displ_fn(curr_page, list_data, divider = 10, click = "n"): #если получает на вход n p -движется вперед назад
    # print(list_data)
    # list_data = short_market_list
    total_rows = len(list_data) - 1 #отнимаем первую строку заголовков
    total_pages = math.ceil(total_rows / divider)

    if click == "n":
        if curr_page < total_pages:
            curr_page += 1
        else:
            print(f"Вы уже на последней странице ({total_pages})")
    elif click == "p":
        if curr_page > 1:
            curr_page -= 1
        else:
            print("Вы уже на первой странице")
    elif click == "s":
        if curr_page != 1:
            curr_page = 1
        else:
            print("Вы уже на первой странице")
    elif click == "l":
        if curr_page != total_pages:
            curr_page = total_pages
        else:
            print("Вы уже на последней странице")

    curr_page = page_bh(curr_page, list_data, divider)
    # print(f'Вы на странице: {curr_page}')
    print(f'Всего страниц: {total_pages}')
    print(f'Строк на странице: {divider}')

    return curr_page



def page_vision_fn(short_market_list ):
    current_page = 0
    divider=10

    current_page = displ_fn(current_page, short_market_list, divider, "n")
    print(f"Это страница номер: {current_page}")
    print(f'Количество строк на одной странице: {divider} ')

    while True:
        user_typing2 = input(f"                  \n"
                        f"Вывод информации по страницам\n"
                        f"===================================== \n"
                        f"Доступны следующие действия: \n"
                        f"n or next - следующая страница \n"
                        f"p or prev - предыдущая страница \n"
                        f"s or start - первая страница \n"
                        f"l or last - последняя страница \n"
                        f"d or divid - количество строк в одной странице (по умолчанию 10) \n"
                        f"t or to - перейти на страницу \n"        
                        f"===================================== \n"     
                        f"end - выход из раздела \n"
                        f"===================================== \n"
                        f"Выполните ввод команды =>: ")

        valid_commands2 ={'n','next','p', 'prev', 's', 'start', 'l', 'last', 'd', 'divid','t', 'to', 'end', }
        if not ch.check_inp(valid_commands2,user_typing2):
            continue

        if user_typing2 in ("n", "next"):
            click = 'n'
            current_page = displ_fn(current_page, short_market_list, divider, click)
            print(f"Вы на странице: {current_page}")

        elif user_typing2 in ("p", "prev"):
            click = 'p'
            current_page = displ_fn(current_page, short_market_list, divider, click)
            print(f"Вы на странице: {current_page}")

        elif user_typing2 in ("s", "start"):
            click = 's'
            current_page = displ_fn(current_page, short_market_list, divider, click)
            print(f"Это первая страница. Вы на странице: {current_page}")

        elif user_typing2 in ("l", "last"):
            click = 'l'
            current_page = displ_fn(current_page, short_market_list, divider, click)
            print(f"Это последняя страница. Вы на странице: {current_page}")

        elif user_typing2 in ("d", "divid"):
            try:
                divider = int(input("Введите количество строк на странице: "))
                print(f"Установлено {divider} строк на странице")
                current_page = displ_fn(current_page, short_market_list, divider, "n")
            except ValueError:
                print("Ошибка: введите число")

        elif user_typing2 in ("t", "to"):
            try:
                page = int(input("Введите номер страницы: "))
                current_page = page-1 #n прибавляет 1 далее
                current_page = displ_fn(current_page, short_market_list, divider, "n")
                print(f"Переход на страницу. Вы на странице: {current_page}")
            except ValueError:
                print("Ошибка: введите число")

        elif user_typing2 in ('end'):
            print('Выход из раздела')
            break  # Выход из внутреннего цикла, возврат в главное меню

        else:
            print('Ошибка. Введена неизвестная команда')
            print()



def print_list_fn (some_list):
    for item in some_list:
        print(item)
        return (item)


def print_list_join(some_list):
    for item in some_list:
        print(', '.join(item))

short_dict = {}
for k, v in union_dict.items():
    short_dict[k] = {
        "MarketName": v.get("MarketName", ""),
        "street": v.get("street", ""),
        "city": v.get("city", ""),
        "County": v.get("County", ""),
        "State": v.get("State", ""),
        "zip": v.get("zip", ""),
        "x": v.get("x", ""),
        "y": v.get("y", ""),
        "Рейтинг рынка": v.get("Рейтинг рынка", "0")
    }




if __name__ == '__main__':
    pass
    a=page_vision_fn(short_market_list)
    # zip_code = '45402'
    # for k, v in short_dict.items():
    #     zip_code = v.get("zip", "")
    #
    #     from seacher import zip_to_coord
    #     from seacher import hv_dist_miles
    #     list_for_dist = []
    #     for k,v in short_dict.items():
    #         if not v['x'] or not v['y']:
    #             continue
    #         try:
    #             lat1 = float(v['y'])
    #             lon1 = float(v['x'])
    #         except ValueError:
    #             continue
    #
    #     if zip_to_coord(zip_code) is None:
    #         continue
    #     lat2, lon2, item_row = zip_to_coord(zip_code) # коорд, коорд, список
    #     lat2 = float(lat2)
    #     lon2 = float(lon2)
    #
    #     dist_result = hv_dist_miles(lat1, lon1, lat2, lon2 )
    #     if dist_result > 0:
    #         result = [round(dist_result, 2)] + item_row
    #         # result = item_row.append(round(dist_result, 2))
    #         list_for_dist.append(result)
    #
    #
    #     for item in list_for_dist:
    #
    #         print(', '.join(map(str, item)))












