import json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


folder = Path(__file__).resolve().parent
index_bytes = (folder / "store.faiss").read_bytes()
index = faiss.deserialize_index(np.frombuffer(index_bytes, dtype=np.uint8))
records = json.loads(
    (folder / "chunks.json").read_text(encoding="utf-8")
)

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def search_policy(query, top_k=2):
    query_vector = model.encode(
        [query], normalize_embeddings=True
    ).astype("float32")

    _, positions = index.search(query_vector, min(top_k, index.ntotal))

    passages = []
    for position in positions[0]:
        record = records[position]
        passages.append(f"[{record['id']}] {record['text']}")

    return "\n".join(passages)

if __name__ == "__main__":
    print(search_policy("How much does shipping to Sakhnin cost?"))