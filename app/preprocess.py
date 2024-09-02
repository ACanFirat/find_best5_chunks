from engine import embedding_bge3
from engine.pinecone_connect import PineconeConnect as PC
from app import functions as f

PC = PC()


def query_to_pinecone(query, isExists):
    if not isExists:
        pdf_path = "documents/downloaded.pdf"
        text = f.extract_text_from_pdf(pdf_path)
        chunks = embedding_bge3.split_text(text)
        PC.check_index_exists()
        PC.send_chunks(chunks)

    result = PC.get_first5_chunks(query)
    return result
