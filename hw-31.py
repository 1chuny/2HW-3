import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor


def copy_files(source_dir, target_dir='dist'):
    # Створюємо цільову директорію, якщо вона ще не існує
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Функція для обробки кожного файлу: копіює файл у відповідну піддиректорію за розширенням
    def copy_file(file_path):
        extension = file_path.split('.')[-1].lower()  # Отримуємо розширення файлу
        target_subdir = os.path.join(target_dir, extension)
        if not os.path.exists(target_subdir):
            os.makedirs(target_subdir)
        shutil.copy(file_path, target_subdir)

    # Функція для рекурсивного обходу директорії та копіювання файлів
    def process_directory(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                copy_file(file_path)

    # Запускаємо обробку головної директорії в пулі потоків
    with ThreadPoolExecutor() as executor:
        executor.map(process_directory, [source_dir])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py source_directory [target_directory]")
        sys.exit(1)

    source_directory = sys.argv[1]
    target_directory = sys.argv[2] if len(sys.argv) > 2 else 'dist'

    copy_files(source_directory, target_directory)
