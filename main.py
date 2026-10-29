"""Консольное меню лабораторной работы № 2."""

from time_validator import find_in_file, is_valid_time


def main():
    while True:
        print("\n1. Проверить время")
        print("2. Найти время в файле")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            value = input("Введите время в формате ЧЧ:ММ:СС: ")
            if is_valid_time(value):
                print("Время записано правильно.")
            else:
                print("Неверное время. Пример правильной записи: 09:30:05.")
        elif choice == "2":
            filename = input("Введите путь к текстовому файлу: ").strip()
            try:
                times = find_in_file(filename)
            except UnicodeError:
                print("Не удалось прочитать файл. Нужна кодировка UTF-8.")
            except OSError as error:
                print(f"Не удалось открыть файл: {error}")
            else:
                if times:
                    print(f"Найдено записей: {len(times)}")
                    for value in times:
                        print(value)
                else:
                    print("Время в файле не найдено.")
        elif choice == "0":
            print("Работа завершена.")
            break
        else:
            print("Такого пункта нет. Введите 1, 2 или 0.")


if __name__ == "__main__":
    main()
