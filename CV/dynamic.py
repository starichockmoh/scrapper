import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

crop_size = 32
log_brightness_list = []
image_folder = "dynamic_test"
image_files = sorted(os.listdir(image_folder))

for filename in image_files:
    image_path = os.path.join(image_folder, filename)
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray_image is None:
        print(f"Ошибка загрузки изображения: {image_path}")
        continue

    height, width = gray_image.shape
    x = width // 2 - crop_size // 2
    y = height // 2 - crop_size // 2
    center_crop = gray_image[y:y + crop_size, x:x + crop_size]
    average_brightness = np.mean(center_crop)
    log_brightness = np.log(average_brightness)
    log_brightness_list.append(log_brightness)

ev_values = np.linspace(-2, 2, len(log_brightness_list))

plt.plot(ev_values, log_brightness_list, marker='o')
plt.xlabel('EV')
plt.ylabel('Логарифм яркости')
plt.title('Зависимость логарифма яркости от EV')
plt.grid(True)
plt.show()