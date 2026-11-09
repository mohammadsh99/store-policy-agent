from pathlib import Path
from sentence_transformers import SentenceTransformer
import json
import faiss

document = Path("store-policy.txt").read_text(encoding="utf-8")
chunks = document.strip().split("\n\n")

#for chunk in chunks:
#  print(chunk)
records = []

for chunk_id, text in enumerate(chunks, start=1):
    records.append({
        "id": chunk_id,
        "text": text,
        "source": "store-policy.txt",
    })


#print(records[1])    
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
texts = []
for record in records:
    texts.append(record["text"])
    

#vectors = model.encode(texts)
#print(vectors.shape)
#print(vectors[1][:5])
vectors = model.encode(texts, normalize_embeddings=True).astype("float32")
index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)

faiss.write_index(index, "store.faiss")

Path("chunks.json").write_text(
    json.dumps(records, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(f"Saved {index.ntotal} vectors.")

