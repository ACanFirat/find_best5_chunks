from fastapi import FastAPI, Form
from app import functions as f, preprocess as p
from uvicorn import run

app = FastAPI()
last_url = ""
answer = ""


@app.post("/query_to_pinecone")
async def query_to_pinecone(
        url: str = Form(...),
        query: str = Form(...)
):
    global last_url
    global answer

    try:
        isExist = True

        if not f.check_url_is_same(url, last_url):
            f.download_file(url)
            isExist = False

        last_url = url
        answer = p.query_to_pinecone(query, isExist)
        return {"message": f"{answer}"}

    except Exception as e:
        return {"message": str(e)}

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8008)
