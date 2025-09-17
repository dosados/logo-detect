import os
import random
from PIL import Image, ImageOps

# Папка с изображениями
folder = "dataset/images/train"

# Получаем список всех файлов изображений (по расширениям)
valid_ext = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
files = [f for f in os.listdir(folder) if f.lower().endswith(valid_ext)]

# Перемешиваем список и берём половину
random.shuffle(files)
to_invert = files[:len(files) // 2]

for filename in to_invert:
    path = os.path.join(folder, filename)
    try:
        img = Image.open(path)

        # Если картинка с альфа-каналом, разделяем, чтобы не инвертировать прозрачность
        if img.mode == "RGBA":
            r, g, b, a = img.split()
            rgb_image = Image.merge("RGB", (r, g, b))
            inverted = ImageOps.invert(rgb_image)
            r2, g2, b2 = inverted.split()
            final_image = Image.merge("RGBA", (r2, g2, b2, a))
        else:
            if img.mode != "RGB":
                img = img.convert("RGB")
            final_image = ImageOps.invert(img)

        final_image.save(path)  # заменяем оригинал
        print(f"Инвертировано: {filename}")

    except Exception as e:
        print(f"Ошибка с {filename}: {e}")