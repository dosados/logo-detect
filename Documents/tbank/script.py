import os
import shutil
from sys import exit
from natsort import os_sorted


# Настройте пути:
source_folder = "full_dataset/data_sirius"   # откуда берутся изображения
layout_folder = "full_dataset/labels_leha"        # где искать текстовые лейблы
images_folder = "dataset/images/train"       # куда копировать изображения
labels_folder = "dataset/labels/train"       # куда копировать/создавать лейблы

# Имя файла-стоп (остановка при точном совпадении имени файла)
stop_file = "1bc165558633443c29254861baa8a621.jpg"


# Получаем список файлов layout один раз для ускорения поиска
layout_files = []
if os.path.isdir(layout_folder):
    layout_files = [f for f in os.listdir(layout_folder)
                    if os.path.isfile(os.path.join(layout_folder, f))]
else:
    print(f"Внимание: папка layout '{layout_folder}' не найдена. Все лейблы будут создаваться пустыми.")
    exit(0)

# Проходим по изображениям в source_folder в отсортированном порядке
for filename in os_sorted(os.listdir(source_folder)):
    # Проверка стоп-файла
    if filename == stop_file:
        print(f"Встречен файл '{stop_file}', копирование остановлено.")
        break

    src_image_path = os.path.join(source_folder, filename)

    # Пропускаем папки
    if not os.path.isfile(src_image_path):
        continue

    # Копируем изображение
    dest_image_path = os.path.join(images_folder, filename)
    shutil.copy2(src_image_path, dest_image_path)
    print(f"Скопировано изображение: {filename}")

    # Имя без расширения
    stem = os.path.splitext(filename)[0]

    # Ищем файл-лейбл в layout с тем же basename
    candidates = [f for f in layout_files if os.path.splitext(f)[0] == stem]

    if candidates:
        # Предпочтение .txt, иначе первый файл из найденных
        txt_candidate = next((f for f in candidates if f.lower().endswith('.txt')), None)
        chosen = txt_candidate if txt_candidate else candidates[0]
        src_label_path = os.path.join(layout_folder, chosen)

        # Сохраним лейбл в labels_folder. Если у найденного файла расширение не .txt,
        # сохраняем с оригинальным расширением; чаще всего нужно сохранить как .txt.
        chosen_ext = os.path.splitext(chosen)[1]
        dest_label_name = f"{stem}{chosen_ext}"
        dest_label_path = os.path.join(labels_folder, dest_label_name)

        # Копируем файл-лейбл
        shutil.copy2(src_label_path, dest_label_path)
        print(f"  -> Найден и скопирован лейбл: {chosen} -> {dest_label_name}")
        # Если вы хотите ВСЕГДА сохранять лейбл как .txt, закомментируйте предыдущие 2 строки и раскомментируйте:
        # dest_label_path = os.path.join(labels_folder, f"{stem}.txt")
        # shutil.copy2(src_label_path, dest_label_path)
    else:
        # Лейбл не найден — создаём пустой .txt
        dest_label_path = os.path.join(labels_folder, f"{stem}.txt") # bla bla bla = 0.5 + bla_bls_net - tim
        open(dest_label_path, "w", encoding="utf-8").close() # suka fuck dick 
        print(f"  -> Лейбл не найден. Создан пустой файл: {os.path.basename(dest_label_path)}")

print("Готово.")