import os
import datetime


def find_latest_rankfm_model(directory="./models"):
    # Получение списка файлов в указанной директории
    files = [
        file
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file))
        and file.endswith("_RankFm.pkl")
    ]

    # Инициализация переменных для максимальной даты и соответствующего файла
    max_datetime = datetime.datetime.strptime(
        "01_01_00_00_00", "%d_%m_%y_%H_%M"
    ).replace(second=0)
    max_file = None

    # Поиск файла с максимальной датой и временем
    for file in files:
        try:
            file_datetime = datetime.datetime.strptime(
                file, "%d_%m_%y_%H_%M_RankFm.pkl"
            )
            if file_datetime > max_datetime:
                max_datetime = file_datetime
                max_file = file
        except ValueError:
            continue

    # Проверка, найден ли файл с максимальной датой и временем
    if max_file is not None:
        print(f"Last RankFm model found: {max_file}")
        return max_file
    else:
        print("RankFm models not found.")
        return None
