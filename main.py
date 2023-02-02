from security import Validation
from interface import UserGui, RootGui

# управляющая функция
def main():
    validation = Validation()
    validation.valid_win()
    try:
        if validation.success:
            # обращение к базе, где находится права доступа (user, admin) для пользователей по логину
            print(validation.user[1])
            if validation.user[1] == "admin":
                RootGui(validation.user)
            else:
                UserGui(validation.user)
    except TypeError:
        pass

if __name__ == "__main__":
    main()
