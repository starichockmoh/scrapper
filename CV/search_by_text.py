import torch
import clip
import faiss
import numpy as np
import os
import argparse

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device)


def search_by_text(query, index_path="image_index.faiss", paths_path="image_paths.npy", top_k=5):
    if not os.path.exists(index_path) or not os.path.exists(paths_path):
        print("Ошибка: Индекс или список изображений не найдены.")
        return []

    index = faiss.read_index(index_path)
    image_paths = np.load(paths_path, allow_pickle=True)

    text_tokens = clip.tokenize([query]).to(device)

    with torch.no_grad():
        text_embedding = model.encode_text(text_tokens).cpu().numpy()

    # Нормализация текстового эмбеддинга
    faiss.normalize_L2(text_embedding)

    distances, indices = index.search(text_embedding, top_k)
    results = []
    for i, distance in zip(indices[0], distances[0]):
        if i < len(image_paths):  # Проверка, чтобы индекс не выходил за пределы
            results.append((image_paths[i], distance))
        else:
            print(f"Предупреждение: Индекс {i} выходит за пределы списка изображений.")

    return results



parser = argparse.ArgumentParser(description="Поиск изображений по тексту с помощью CLIP.")
parser.add_argument("query", type=str, help="Текстовый запрос для поиска изображений.")
parser.add_argument("--top_k", type=int, default=5, help="Количество возвращаемых результатов (по умолчанию 5).")
args = parser.parse_args()
results = search_by_text(args.query, top_k=args.top_k)
if results:
    print("\nНайденные изображения:")
    for path, distance in results:
        print(f"Изображение: {path}, Расстояние: {distance:.4f}")
else:
    print("\nПо вашему запросу ничего не найдено.")
