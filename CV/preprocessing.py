import cv2


# Ресайз изображения
def resize_image(image, size=(32, 32)):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

# Преобразование в оттенки серого
def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Выравнивание контраста
def histogram_equalization(image):
    return cv2.equalizeHist(image)

# Уменьшение шума
def denoise_image(image):
    return cv2.GaussianBlur(image, (5, 5), 0)
# Выделения контуров объектов
def detect_edges(image):
    return cv2.Canny(image, 100, 200)
