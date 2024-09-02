from pinecone import Pinecone, ServerlessSpec
from engine import embedding_bge3

pc = Pinecone(api_key="YOUR-PINECONE-APIKEY-HERE")


class PineconeConnect:
    def __init__(self):
        self.index_name = f"myindex"
        self.check_index_exists()
        self.index = pc.Index(index_name=self.index_name, host=pc.describe_index(self.index_name).host)

    def create_index(self):
        pc.create_index(
            name=self.index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("New index created.")

    def delete_index(self, url):
        pc.delete_index(self.index_name)
        print("Old index deleted.")
        return True

    def send_chunks(self, chunks):
        for i, chunk in enumerate(chunks):
            embedding = embedding_bge3.embed_text(chunk).numpy().flatten()
            metadata = {"text": chunk}
            self.index.upsert(vectors=[(f"chunk-{i}", embedding, metadata)])

        print(f"{i} chunks added to the Pinecone DB")

    def get_first5_chunks(self, query):
        query_embedding = embedding_bge3.embed_text(query).numpy().flatten()
        query_embedding = [query_embedding.tolist()]
        result = self.index.query(vector=query_embedding, top_k=5, include_metadata=True)
        return result

    def check_index_exists(self):
        list_index = pc.list_indexes().names()
        if self.index_name in list_index:
            self.delete_index(self.index_name)
        self.create_index()
