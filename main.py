
from seacher import zip_fn, city_st_fn
from reader_csv_dict import short_market_list
from reader_csv_dict import page_vision_fn
import valid_check as ch
from users_action import all_feadback, delete_row
import dist as d


def main():
    while True:

        user_typing = input(f"                  \n"
                            f"Доступные разделы:\n"
                            f"l or list - список всех рынков \n"
                            f"f or find - найти рынок по зип коду или по названию города и штата \n"
                            f"s or sort - сортировка рынков \n"
                            f"a or admin - вход для админа (удаление отзывав) \n"
                            f"===================================== \n"
                            f"end - выход  \n"
                            f"===================================== \n"
                            f"Выполните ввод команды =>: ").strip()


        valid_commands ={'list','l','find', 'f', 's', 'sort', 'end', 'a', 'admin' }
        if not ch.check_inp(valid_commands,user_typing):
            continue

        if user_typing == 'end':
            print('end')
            print('Работа программы завершена')
            return 0

        elif user_typing == 'end':
            print('end')
            print('Работа программы завершена')
            return 0

        elif user_typing in ("l", "list"):
            print(f"# Раздел list. Просмотр информации о фермерских рынках.\n")
#начало работу ф-ции по отображению страниц
            page_vision_fn(short_market_list)
#окончание работу ф-ции по отображению страниц

        elif user_typing in ("a", "admin"):

            while True:
                print(f"# Раздел для администратора.\n")
                inp_pass = input("Введите пароль администратора (пароль 12345). end - выход: =>")
                if inp_pass == '12345':
                    print("Доступно удаление отзывов")
                    print()
                    print(f"Просмотр всех отзывов\n"
                          f"==================================== \n")
                    all_feadback()
                    user_typing_a = input(f"                  \n"
                                        f"del - удаление отзыва \n"
                                        f"end - выход из раздела \n"
                                        f"==================================== \n"
                                        f"Введите команду => ")

                    valid_commands_a ={'del', 'end'}
                    if not ch.check_inp(valid_commands_a,user_typing_a):
                            continue

                    elif user_typing_a in ('end'):
                            print('Выход из раздела')
                            break

                    elif user_typing_a in ('del'):
                            delete_row()
                            print('Удалено')
                            continue

                elif inp_pass in ('end'):
                        print('Выход из раздела')
                        break

        elif user_typing in ('f', 'find'):
            print('find')
            user_typing3 = user_typing

            if user_typing3 == 'find' or user_typing3 == 'f':


                while True:
                    user_typing3 = input(f"                  \n"
                                f"# Раздел find. Поиск информации о фермерских рынках.\n"
                                f"Доступны следующие действия: \n"
                                f"z or zip - поиск по zip коду \n"
                                f"c or city - поиск по городу и штату \n"
                                f"==================================== \n"         
                                f"end - выход из раздела \n"
                                f"==================================== \n"
                                f"Введите команду => ")

                    valid_commands3 ={'z', 'zip', 'c', 'city', 'end'}
                    if not ch.check_inp(valid_commands3,user_typing3):
                        continue

                    if user_typing3 in ("z", "zip"):
                        zip_res = zip_fn()
                        break

                    if user_typing3 in ("c", "city"):
                        print(f'Для отладки: {short_market_list[5]}')
                        print(f'Для отладки: {short_market_list[8]}')
                        # print(f'Для отладки: {short_market_list[20]}')
                        city_result = city_st_fn()

                    elif user_typing3 in ('end'):
                        print('Выход из раздела')
                        break  # Выход из внутреннего цикла, возврат в главное меню


                    else:
                        print('Ошибка. Введена неизвестная команда')
                        print()

        elif user_typing in ('s', 'sort'):
            print('sort')
            d.filtr_fn()


        else:
            print('Ошибка. Введите подходящее значение')
            print('или "end" - выход ')

if __name__ == "__main__":
    main()
# while True:
#     result = main()
#     if result == 0:
#         break