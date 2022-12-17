import json
import sys
import shutil
import os
from pathlib import Path
from normalize import normalize


# створення цільових тек
def create_target_folders(path_folder: Path) -> dict:
    # створення категорій з файла catalog.json
    def create_categories(path_folder: str) -> dict:
        with open(path_folder) as f:
            result = json.load(f)
        return result
# створення тек з назвою ключа в категорії
    CATEGORIES = create_categories("catalog.json")
    for i in CATEGORIES:
        # якщо такої теки немає, то стоворюєио її
        if not path_folder.joinpath(i).exists():
            path_folder.joinpath(i).mkdir()

    return CATEGORIES       # повертає словник з категоріями та розширенням

# # читання тестової теки
# def read_folder(path: Path) -> list:
#     list_files = []

#     # ітеруємо по всіх папках всі об'єкти
#     for item in path.glob("**/*"):
#         # нормалізуємо назву файлу
#         normalize_name = normalize(item.name)
#         list_files.append(normalize_name)  # список всіх файлів
#     return list_files


def arc(path_folder: Path):                # розархівування
    for file in path_folder.glob("**/*"):
        if file.suffix in [".zip", ".tar", ".xztar", ".gztar", "bztar"]:
            shutil.unpack_archive(file, path_folder / "archives")
    return Path


def delete_folders(path_folder: Path):              # видалимо порожні папки
    for file in path_folder.glob("**/*"):
        if file.is_dir():
            if len(os.listdir(file)) == 0:
                os.rmdir(file)


count = 0


def sort_files(path_folder: Path) -> str:  # отримаємо список цільових елементів
    work_dir = Path(path_folder)
    # словник з папками та розширенням
    cat = create_target_folders(work_dir)
    # тестова тека

    global count
    for file in path_folder.glob("**/*"):

        normalize_name = normalize(file.name)
        count += 1

        # ітеруємо словник і переносимо файли в нові папки
        for new_folder, list_extension in cat.items():
            for extension in list_extension:
                if file.suffix == extension:
                    try:
                        shutil.move(file, work_dir /
                                    new_folder / normalize_name)
                    except FileExistsError:
                        new_name = f"_{count}.".join(
                            normalize_name.split("."))
                        shutil.move(file, work_dir / new_folder / new_name)
                else:
                    if file.is_file():
                        shutil.move(file, work_dir / "Others")


# головна функція
def main() -> str:
    try:
        sort_files(sys.argv[1])
        delete_folders(sys.argv[1])

    except IndexError:
        print("No parameter")


if __name__ == "__main__":
    main()
