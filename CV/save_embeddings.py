import torch
import clip
import faiss
import os
import numpy as np
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device)

image_folder = "processed_images_back"
image_paths = []
image_embeddings = []

for filename in os.listdir(image_folder):
    if filename.endswith(("jpg", "png", "jpeg")):
        img_path = os.path.join(image_folder, filename)
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = model.encode_image(image).cpu().numpy()

        image_paths.append(img_path)
        image_embeddings.append(embedding)

image_embeddings = np.vstack(image_embeddings)

# Нормализация image эмбеддинга
faiss.normalize_L2(image_embeddings)
# Индекс, который поддерживает косинусное сходство.
# IndexFlatIP (Inner Product) с нормализованными эмбеддингами эквивалентен косинусному сходству.
index = faiss.IndexFlatIP(image_embeddings.shape[1])
index.add(image_embeddings)

faiss.write_index(index, "image_index.faiss")
np.save("image_paths.npy", np.array(image_paths))
