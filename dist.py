
from seacher import zip_to_coord, city_to_zip, inp_city
from seacher import hv_dist_miles
from reader_csv_dict import short_market_list, print_list_fn
from reader_csv_dict import short_dict
from reader_csv_dict import union_dict, short_market_info
from reader_csv_dict import page_bh, displ_fn, page_vision_fn
import valid_check as ch



def filtr_fn(union_dict = union_dict):
    current_page = 0
    divider=10
    current_page = displ_fn(current_page, short_market_list, divider, "n")
    print(f"Это страница номер: {current_page}")
    print(f'Количество строк в одной странице: {divider} ')

    while True:
        fl_input = input(f"                  \n"
                         f"Доступные фильтры:\n"
                         f"g or grade - по рейтингу рынков (min -> max) \n"
                         f"rg or rgrade - по рейтингу рынков (реверс, max -> min) \n"                         
                         f"s or state -  по названию города и штата  (a -> z) \n"
                         f"rs or rstate -  по названию города и штата (реверс, z -> a) \n" 
                         f"z or zip -  по удаленности от точки, заданной zip-кодом, в милях  (min -> max) \n"
                         f"rz or rzip -  по удаленности от точки, заданной zip-кодом (реверс), в милях (max -> min) \n"
                         f"d or dist -  по удаленности от точки, заданной по названию города и штата, в милях  (min -> max) \n"
                         f"rd or rdist -  по удаленности от точки, заданной по названию города и штата (реверс), в милях (max -> min) \n"
                         f"(Первое значение из вывода - критерий фильтрации) \n"
                                                  
                         f"===================================== \n"
                         f"end - выход  \n"
                         f"===================================== \n"
                         f"Выполните ввод команды =>: ").strip()

        valid_commands ={"g","grade","rg","rgrade","s", "state","rs", "rstate", "z","zip", "rz","rzip", "rd","rdist", "d","dist", 'end', }
        if not  ch.check_inp(valid_commands, fl_input):
            continue


        if fl_input in ("g", "grade"):
            sorted_list = []
            for key, v in sorted(short_dict.items(), key=lambda item: int(item[1]['Рейтинг рынка'])):
                row = [
                    v["Рейтинг рынка"],
                    v["MarketName"],
                    v["street"],
                    v["city"],
                    v["State"],
                    v["zip"],
                ]
                sorted_list.append(row)
            current_page = page_vision_fn(sorted_list)
            print(f"Вы на странице: {current_page}")


            # print_list_fn(sort_filtered)

        elif fl_input in ("rg","rgrade"):
            sorted_list = []
            for key, v in sorted(short_dict.items(), key=lambda item: int(item[1]['Рейтинг рынка']), reverse=True):
                row = [
                    v["Рейтинг рынка"],
                    v["MarketName"],
                    v["street"],
                    v["city"],
                    v["State"],
                    v["zip"],
                ]
                sorted_list.append(row)
            current_page = page_vision_fn(sorted_list)
            print(f"Вы на странице: {current_page}")

        elif fl_input in ("s", "state"):
            sorted_list = []
            for key, v in sorted(short_dict.items(),
                                 key=lambda item: (
                                    item[1].get("city", "").lower(),
                                    item[1].get("State", "").lower()
                                 ),
                                 reverse=False):
                row = [
                    v["city"],
                    v["State"],
                    v["MarketName"],
                    v["street"],
                    v["zip"],
                    v["Рейтинг рынка"],
                    ]
                sorted_list.append(row)
            current_page = page_vision_fn(sorted_list)
            print(f"Вы на странице: {current_page}")

        elif fl_input in ("rs", "rstate"):
            sorted_list = []
            for key, v in sorted(short_dict.items(),
                                 key=lambda item: (
                                    item[1].get("city", "").lower(),
                                    item[1].get("State", "").lower()
                                 ),
                                 reverse=True):
                row = [
                    v["city"],
                    v["State"],
                    v["MarketName"],
                    v["street"],
                    v["zip"],
                    v["Рейтинг рынка"],
                    ]
                sorted_list.append(row)
            current_page = page_vision_fn(sorted_list)
            print(f"Вы на странице: {current_page}")


        elif fl_input in ("z","zip"):
            inp_arg = inp_zip()
            print("Расст., FMID, Название рынка, Город, Штат, Адрес, lat, lon, Рейтинг")
            var = dist_calculation(inp_arg)
            # print(f'var = {var}')
            sorted_list = sorted(var, key=lambda x: x[0])
            # print(f'sorted_dist = {sorted_dist}')
            # for row in sorted_dist:
            #     print(', '.join(map(str, row)))
            current_page = page_vision_fn(sorted_list)
            print(f"Вы на странице: {current_page}")

        elif fl_input in ("rz","rzip"):
            inp_arg = inp_zip()
            print("Расст., FMID, Название рынка, Город, Штат, Адрес, lat, lon, Рейтинг")
            var = dist_calculation(inp_arg)
            # print(f'var = {var}')
            sorted_list = sorted(var, key=lambda x: x[0], reverse=True)
            # print(f'sorted_dist = {sorted_dist}')
            # for row in sorted_dist:
            #     print(', '.join(map(str, row)))
            current_page = page_vision_fn(sorted_list)
            print(f"Вы на странице: {current_page}")

        elif fl_input in ("rd","rdist"):
            print('Для отладки')
            print(short_market_list[10])
            inp_list = inp_city() #возвращает список город, штат
            for item in short_market_list:
                # print(item)
                if item[2] == inp_list[0] and item[3] == inp_list[1]:
                    zip_city = item[5]
                    print(zip_city)
                    var = dist_calculation(zip_city)
                    sorted_list = sorted(var, key=lambda x: x[0], reverse=True)
                    # print(f'sorted_dist = {sorted_list}')
                    # for row in sorted_list:
                    #     print(', '.join(map(str, row)))
                    current_page = page_vision_fn(sorted_list)
                    print(f"Вы на странице: {current_page}")

        elif fl_input in ("d","dist"):
            print('Для отладки')
            print(short_market_list[5])
            inp_list = inp_city() #возвращает список город, штат
            flag = False
            for item in short_market_list:
                # print(item)
                if item[2] == inp_list[0] and item[3] == inp_list[1]:
                    flag = True
                    zip_city = item[5]
                    print(zip_city)
                    var = dist_calculation(zip_city)
                    sorted_list = sorted(var, key=lambda x: x[0])
                    # print(f'sorted_list = {sorted_list}')
                    # for row in sorted_list:
                    #     print(', '.join(map(str, row)))
                    current_page = page_vision_fn(sorted_list)
                    print(f"Вы на странице: {current_page}")


            if flag == False:
                print("Город или штат н не найдены")

        elif fl_input in ('end'):
            print('Выход из раздела')
            break  # Выход из внутреннего цикла, возврат в главное меню



def inp_zip():
    zip_inp = input('Введите пятизначный числовой ZIP-code =>')
    print(f'Ввод значения ZIP-code = {zip_inp}')
    return zip_inp

def dist_calculation(zip_inp):# зип код
    zip_inp = str(zip_inp)
    # print(f'zip_inp = {zip_inp}')
    # zip_code = '45402'
    for k, v in short_dict.items():
        if zip_inp == v.get("zip", ""):
            # print(f"Найдено = {v.get("zip", "")}")
            first2_coord = zip_to_coord(zip_inp)
            lat1, lon1, item_row = first2_coord
            # print(f'first2_coord = {first2_coord}')
    # print(short_market_list)

    list_for_dist = []
    for i in short_market_list:
        if not i[6] or not i[7]:
            continue
        # print(i)
        lat2 = float(i[6])
        lon2 = float(i[7])
        # print(f'Locality {i} lat2 = {lat2}, lon2 = {lon2}')

        # print("Coordinats")
        # print(float(lat1), float(lon1), float(lat2), float(lon2))
        dist_result = hv_dist_miles(float(lat1), float(lon1), float(lat2), float(lon2))
        # print(dist_result)
        dist_markets = [round(dist_result, 1)] + i
        # print(f'dist_markets = {dist_markets}')
        list_for_dist.append(dist_markets)
        # print(list_for_dist)
        # print('\n'.join(map(str, list_for_dist)))
        # return list_for_dist
    # print(f'list_for_dist = {list_for_dist}')
    return list_for_dist

# def dist_page(sorted_list):
#     len_list = len(sorted_list)
#     divider = 20
#     total_page = len_list /divider




if __name__ == '__main__':
    # pass
    a=filtr_fn()

    # a=dist_calculation(inp_zip())
