import os
from rembg import remove
from PIL import Image
import cv2
import numpy as np
import io

image_folder = 'downloaded_images'
output_folder = 'processed_images_back'

def remove_background_with_rembg(input_path, output_path):
    with open(input_path, 'rb') as input_file:
        input_data = input_file.read()
    # Удаляем фон с помощью rembg
    output_data = remove(input_data)
    output_image = Image.open(io.BytesIO(output_data))
    output_image.save(output_path, format="PNG")


def grabcut_remove_background(image_path, output_path):
    image = cv2.imread(image_path)
    # Создаем маску
    mask = np.zeros(image.shape[:2], np.uint8)
    # Инициализируем фоновый и передний план
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    # Применяем алгоритм GrabCut
    rect = (10, 10, image.shape[1] - 10, image.shape[0] - 10)  # Рамка вокруг объекта
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    # Маска фона будет содержать значения 0 (фон) и 2 (неизвестный фон)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')



    result = image * mask2[:, :, np.newaxis]
    cv2.imwrite(output_path, result)


def remove_background_images(image_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)

        if not filename.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp')):
            continue

        try:
            output_path = os.path.join(output_folder, filename)
            remove_background_with_rembg(file_path, output_path)

        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

remove_background_images(image_folder, output_folder)

# придумать классы объектов, с помощью pychorm classification разнести. sber clip