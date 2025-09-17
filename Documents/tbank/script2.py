import os
import shutil

ROOT = 'dataset'
FRACTION = 0.3

images_train = os.path.join(ROOT, 'images', 'train')
images_val   = os.path.join(ROOT, 'images', 'val')
labels_train = os.path.join(ROOT, 'labels', 'train')
labels_val   = os.path.join(ROOT, 'labels', 'val')

names = [n for n in os.listdir(images_train) if os.path.isfile(os.path.join(images_train, n))]
# порядок как в os.listdir (в списке выше), не сортируем

total = len(names)
if total == 0:
    print("В images/train нет файлов.")
    raise SystemExit

n_move = int(total * FRACTION)
if n_move == 0:
    n_move = 1

moved_images = 0
moved_labels = 0

for name in names[:n_move]:
    src_img = os.path.join(images_train, name)
    dst_img = os.path.join(images_val, name)

    
    shutil.move(src_img, dst_img)
    moved_images += 1
    print(f"moved image: {name}")

    stem = os.path.splitext(name)[0]
    label_name = stem + '.txt'
    src_label = os.path.join(labels_train, label_name)
    dst_label = os.path.join(labels_val, label_name)

    shutil.move(src_label, dst_label)
    moved_labels += 1
    print(f"moved label: {label_name}")

print()
print(f"Done. Images moved: {moved_images}, labels moved: {moved_labels}")