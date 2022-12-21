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


# def arc(path_folder: Path):                # розархівування
#     for file in path_folder.glob("**/*"):
#         if file.suffix in [".zip", ".tar", ".xztar", ".gztar", "bztar"]:
#             shutil.unpack_archive(file, path_folder / "archives")
#     return Path


def delete_folders(path_folder: Path):    # видалимо порожні папки
    path_folder = Path(path_folder)
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
    for file in work_dir.glob("**/*"):

        normalize_name = normalize(file.name)
        count += 1

        # ітеруємо словник і переносимо файли в нові папки
        for new_folder, list_extension in cat.items():
            try:
                if str(file.suffix) in cat["archives"]:
                    shutil.unpack_archive(
                        file, work_dir / "archives" / file.stem)
                    file.replace(work_dir / "archives" / file.name)
                elif file.suffix in list_extension:
                    try:
                        shutil.move(file, work_dir /
                                    new_folder / normalize_name)
                    except FileExistsError:
                        new_name = f"_{count}.".join(
                            normalize_name.split("."))
                        shutil.move(file, work_dir / new_folder / new_name)
                elif file.suffix not in cat and file.is_file():
                    shutil.move(file, work_dir / "Others")
            except Exception as err:
                # print(f"[ERROR]: {err}")
                continue


# головна функція
def main() -> str:
    try:
        folder = sys.argv[1]
        sort_files(folder)
        delete_folders(folder)
        print(f"File in {folder} were sorted successfully!")
        print(f"All files: {count}")

    except IndexError:
        print("No parameter")


if __name__ == "__main__":
    main()
