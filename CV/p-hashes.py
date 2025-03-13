import os
import cv2
import imagehash
from PIL import Image
from preprocessing import resize_image, convert_to_grayscale, denoise_image

# Порог для определения схожести изображений (чем ниже значение, тем более похожими считаются изображения)
threshold = 6
image_folder = 'downloaded_images_urls'
output_folder = 'processed_images'


def preprocess_image(image, size=(32, 32)):
    image = resize_image(image, size)           # Ресайз изображения
    image = convert_to_grayscale(image)         # Преобразование в оттенки серого
    # image = histogram_equalization(image)       # Выравнивание контраста
    image = denoise_image(image)                # Уменьшение шума
    # image = detect_edges(image)
    return image

# Функция для нахождения похожих изображений
def find_similar_images(image_folder, output_folder, threshold=5):
    # Словарь для хранения хэшей изображений
    image_hashes = {}

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

            image_hashes[filename] = phash
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

    similar_images = []
    hash_items = list(image_hashes.items())
    for i in range(0, len(hash_items)):
        for j in range(i + 1, len(hash_items)):
            image1, hash1 = hash_items[i]
            image2, hash2 = hash_items[j]
            # Вычисляем расстояние Хэмминга между хэшами
            hamming_distance = hash1 - hash2

            # Если изображения похожи, добавляем их в список
            if hamming_distance <= threshold:
                similar_images.append((image1, image2, hamming_distance))


    return similar_images


similar_images = find_similar_images(image_folder, output_folder, threshold)

if similar_images:
    print("Найдены похожие изображения:")
    for img1, img2, dist in similar_images:
        print(f"Изображения: {img1} и {img2} - Расстояние Хэмминга: {dist}")
else:
    print("Похожие изображения не найдены.")
