from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-en")
model = AutoModel.from_pretrained("BAAI/bge-small-en")


def split_text(text, chunk_size=100):
    sentences = text.split()
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    return chunks


def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state[:, 0, :]
    return embeddings


def find_most_similar_chunks(query, chunks, top_n=5):
    query_embedding = embed_text(query)
    chunk_embeddings = torch.cat([embed_text(chunk) for chunk in chunks])

    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]

    return [(chunks[i], similarities[i]) for i in top_indices]
