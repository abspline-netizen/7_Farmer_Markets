
def check_inp(valid_commands, user_typing):
    if user_typing not in valid_commands:
        print('Ошибка. Введена неизвестная команда\n')
        return False
    return True