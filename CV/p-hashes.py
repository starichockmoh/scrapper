import os
import cv2
import imagehash
import shutil
from PIL import Image
from preprocessing import resize_image, convert_to_grayscale, denoise_image

# Порог для определения схожести изображений (чем ниже значение, тем более похожими считаются изображения)
threshold = 6
image_folder = 'downloaded_images_urls'
output_folder = 'processed_images'
unique_folder = 'unique_images'


def preprocess_image(image, size=(32, 32)):
    image = resize_image(image, size)           # Ресайз изображения
    image = convert_to_grayscale(image)         # Преобразование в оттенки серого
    # image = histogram_equalization(image)       # Выравнивание контраста
    image = denoise_image(image)                # Уменьшение шума
    # image = detect_edges(image)
    return image

# Функция для нахождения похожих изображений
def find_similar_images(image_folder, output_folder, unique_folder, threshold=5):
    # Словарь для хранения хэшей изображений
    image_hashes = {}
    duplicate_groups = {}

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists(unique_folder):
        os.makedirs(unique_folder)

    # Проходим по всем файлам в папке
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)

        # Пропускаем файлы, которые не являются изображениями
        if not filename.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp')):
            continue

        try:
            image = cv2.imread(file_path)

            image = preprocess_image(image)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)

            phash = imagehash.phash(Image.fromarray(image))

            found_duplicate = False
            for existing_filename, existing_hash in image_hashes.items():
                if phash - existing_hash <= threshold:
                    found_duplicate = True
                    duplicate_groups.setdefault(existing_filename, []).append(filename)
                    break

            if not found_duplicate:
                image_hashes[filename] = phash
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

    # Копируем только по одному экземпляру из каждой группы дубликатов
    saved_files = set()
    for original, duplicates in duplicate_groups.items():
        if original not in saved_files:
            shutil.copy(os.path.join(image_folder, original), os.path.join(unique_folder, original))
            saved_files.add(original)

     # Также копируем остальные уникальные файлы
    for filename in image_hashes.keys():
        if filename not in saved_files:
            shutil.copy(os.path.join(image_folder, filename), os.path.join(unique_folder, filename))
            saved_files.add(filename)

    return duplicate_groups


duplicates = find_similar_images(image_folder, output_folder, unique_folder, threshold)


if duplicates:
    print("Найдены группы дубликатов:")
    for original, dup_list in duplicates.items():
        print(f"Оригинал: {original}, Дубликаты: {', '.join(dup_list)}")
else:
    print("Дубликаты не найдены. Все изображения уникальны.")
