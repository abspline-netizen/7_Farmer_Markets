

from reader_csv_dict import short_market_list
from users_action import user_action
import math
ALL_DATA = short_market_list

def radius_coord(lat, lon, radius_miles ): #определяет диапазон координат, где проводиться поиск - работает как формула
    R = 3958.8
    rad_dist = radius_miles / R

    min_lat = lat - math.degrees(rad_dist)
    max_lat = lat + math.degrees(rad_dist)

    delta_lon = math.degrees(rad_dist / math.cos(math.radians(lat)))

    min_lon = lon - delta_lon
    max_lon = lon + delta_lon

    return min_lon, max_lon, min_lat, max_lat

def fmid_to_coord (fmid, radius_miles ): #находит диапазон координат для нужного рынка в радиусе

    for i in ALL_DATA:
        if fmid == i[0]:
            point_lat = float(i[6])
            point_lon = float(i[7])
            #print(point_lat, point_lon)
            point_coord_range  = radius_coord(point_lat, point_lon, radius_miles)
            return point_coord_range #возвращает список с диапазоном координат (4 значения), кот относятся к fmid

def coord_to_market(point_coord_range): #список с 4 значениями
    min_lon, max_lon, min_lat, max_lat = point_coord_range
    #print(f'it is point_coord_range {min_lon}, {max_lon}, {min_lat}, {max_lat}')

    find_market_l = []
    for item in ALL_DATA:
        if item[6].strip() == '' or item[7].strip() == '':
            continue

        lon = float(item[7])
        lat = float(item[6])
        #print(f'lon and lat in coord_to_market {lon}, {lat}')
        if min_lon < lon < max_lon and min_lat < lat < max_lat:
            #print(f'Find market: {item}')
            find_market_l.append(item)
    #print(find_market_l)
    for market in find_market_l:
        print(", ".join (market))
    return

def zip_fn():
   print(f"\t ===============================")
   print(f'\tПоиск по ZIP коду')

   while True:
       inp = str(input('Введите ZIP код для поиска (или end - выход): ').strip())
       if inp.lower() == 'end':
           break

       if not len(inp) ==5 and inp.isdigit():
           print('Ошибка ввода')
           continue

       print(f'Вы ввели {inp}')

       found = None
       for line in ALL_DATA: # прошли по всем строкам данных
            if  inp == line[5]:
                found = line
                break

       if not found:
            print('Не найдено!')
            continue

       fmid = line[0]# если введеное равно значению первого индекса

       print(f'ZIP Code {inp} относиться к населенному пункту {line[2]}, штат {line[3]}, Market: {line[1]}')
       wider = wide_commands(fmid)
       return fmid

def zip_to_coord(zip_code):# принимает zip, возвращает координаты
    try:
        if len(zip_code) != 5 or not zip_code.isdigit():
            print("Не подходящий формат ZIP code")
            return None

        for item in short_market_list:
            if item[5] == zip_code:
                lat = item[6]
                lon = item[7]
                item_info = item

                if lat == "" or lon == "":
                    print(f"Координаты отсутствуют для ZIP {zip_code}")
                    return None

                return lat, lon, item_info[1:-1:]

        print(f"ZIP {zip_code} не найден в базе")
        return None

    except:
        print(f"Ошибка при обработке ZIP {zip_code}: {e}")
        return None

def inp_city():
    list_cs = []
    permit_ch = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .'-")
    while True:

        inp_city = input('Введите название города для поиска (или end - выход): ').strip()
        print(inp_city)

        if inp_city.lower() == 'end':
            return None
        if not all(ch in permit_ch for ch in inp_city):
            print('Ошибка ввода названия города')
            continue

        inp_city = inp_city.lower().title()
        list_cs.append(inp_city)

        while True:
            inp_state = input('Введите название штата: ').strip()
            print(inp_state)
            if inp_state.lower() == 'end':
                return None
            if not all(ch in permit_ch for ch in inp_city):
                print('Ошибка ввода названия штата')
                continue

            inp_state = inp_state.lower().title()
            list_cs.append(inp_state)
            break
            # print(list_cs)
        return list_cs


def city_to_zip():
    list_cs = inp_city()
    if list_cs is not None:
        print(list_cs)
        for line in ALL_DATA:
            if len(line)>=6:
                if (line[2]==list_cs[0]) and (line[3]==list_cs[1]):
                    zip_code = line[5]
                    print(zip_code)
                    return zip_code
    else:
        print("Выполнение end")


def city_st_fn():
    print(f"\t ===============================")
    print(f'\t Поиск по городу и штату')
    list_cs = inp_city()
    if list_cs is not None:
        # print(list_cs)
        mrt_list = []
        for line in ALL_DATA:
            if len(line)>=6:
                if (line[2]==list_cs[0]) and (line[3]==list_cs[1]):
                    mrt_list.append(line)

        if not mrt_list:
            print("Рынок не найден")
            return

        if len(mrt_list)==1:
            # print(mrt_list)
            item = mrt_list[0]
            # print(item)
            print(f"\nРезультат 1 из 1")
            print(f"Рынок: {item[0]}, {item[1]}, {item[2]}, {item[4]}")
            fmid = item[0]
            wider = wide_commands(fmid)
            return


        index = 0
        total = len(mrt_list)
        print(f'Всего найдено {total} рынков')
        while index < total:
            item = mrt_list[index]
            print(f"\nРезультат {index+1} из {total}")
            print(f"Рынок: {item[0]}, {item[1]}, {item[2]}, {item[4]}")
            fmid = item[0]# если введеное равно значению первого индекса

            print(f"\t Доступна команда n or next для просмотра следующего рынка\n"
                  f'\t m or more - переход в расширенное меню'
                  )

            inp_next = input("Введите команду, end - выход => ")
            if inp_next in ("n", 'next'):
                index +=1
                continue
            elif inp_next in ("m", 'more'):
                wider = wide_commands(fmid)
                continue
            elif inp_next in ('end'):
                break
            else:
                print("Неизвестная команда")
                continue

    else:
        print("Выполнение end")

def more_info(fmid):
    fmid = fmid
    # print(fmid)
    need_line = []
    for item in ALL_DATA:
        #print(item)
        if fmid==item[0]:
            need_line = item

    while True:
            m_info = input(f"\t\t   \n"
                           f'\t\t  Расширенные команды:  \n'
                           f"\t\t  ---------------------------- \n"
                           f'\t\t  m or more - больше информации о рынке \n'
                           f'\t\t  r or rad - поиск других рынков в радиусе 30 миль \n'
                           f'\t\t  d or dif - поиск других рынков в заданном пользователем радиусе, миль (например, 50) \n'                           
                           f'\t\t  end - выход  \n'
                           f"\t\t  ---------------------------- \n"
                           f"\t\t  u or user - добавить отзыв о найденном рынке \n"
                           f"\t\t  ---------------------------- \n"
                           f'\t\t  Введите команду => ')

            if m_info.lower() in ('m', 'more'):
                print(', '.join(need_line))

            elif m_info.lower() in ('r', 'rad'):
                radius_mils = 30
                # print(fmid)
                search_range = fmid_to_coord(fmid, radius_mils) #координаты берет из ALL_DATA, нужен только fmid
                # print(f'search_range ={search_range}')
                markets_found = coord_to_market(search_range)
                # print(markets_found)

            elif m_info.lower() in ('d', 'dif'):
                radius_mils = int(input('Enter radius mails(exemple, 50): '))

                search_range = fmid_to_coord(fmid, radius_mils) #спислок с 4 координатами на выходе
                markets_in_radius = coord_to_market(search_range)

            elif m_info.lower() in ('end'):
                break

            elif m_info.lower() in ('u', 'user'):
                var=user_action(fmid)
                print(var)

def wide_commands(fmid):
        fmid = fmid
        while True:
           inp_w = input(f'\t Начать работу с расширенным меню - команды w or wide:  \n'
                          f"\t end - выход из команды\n"
                          f"\t -----------------------\n"
                          f'\t Введите команду => ').strip().lower()

           if inp_w.lower() in ('w', 'wide'):
               whid_opts = more_info(fmid)

           elif inp_w.lower() in ('end'):
               break
           else:
               print("Ошибка. Проверьте ввод команды")

def hv_dist_miles(lat1, lon1, lat2, lon2): #определение расстояния меджу точками
    R = 3958.8 # Средний радиус Земли в милях

    phi1 = math.radians(lat1) # Перевод координат из градусов в радианы
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Формула гаверсинусов
    a = (math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Кратчайшее расстояние
    distance = R * c
    return distance


if __name__ == '__main__':
    # pass
    # b= inp_city()
    # a = city_st_fn()
    # c= zip_fn()

    d = city_st_fn()
    # print(ALL_DATA[3])
    # radius_and_coord = radius_coord(34.135760, -116.058946, 30 )
    # print(f'radius_and_coord = {radius_and_coord}')
    # find_by_fmid_coord = fmid_to_coord('1019956', 30)
    # print(f'find_by_fmid_coord = {find_by_fmid_coord}')
    # market_in_radius = coord_to_market(find_by_fmid_coord )
    # zip_fnd = zip_fn()
    # print(zip_fnd)
    # city_fnd = city_st_fn()
    # print(city_fnd)
    # wide_opt = more_info('1021442')


    # print(zip_fn(False))
    # radius_mils = 3000
    # # print(fmid)
    # search_range = fmid_to_coord(zip_fn(False), 3000) #координаты берет из ALL_DATA, нужен только fmid
    # print(f'search_range ={search_range}')
    # markets_found = coord_to_market(search_range)
    # print(markets_found)
    # # # print(markets_found)







