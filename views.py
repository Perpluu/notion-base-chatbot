import asyncio

import httpx
import requests
from fastapi import FastAPI, Form, Request
from slack_bolt import App

from main import chain, docsearch, embeddings

app = FastAPI()

@app.post("/")
async def notion_bot(request: Request, text: str = Form(), status_code: int = 200):
    query = text.strip()
    docs = docsearch.similarity_search(query)
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(chain.run, input_documents=docs, question=query), timeout=3
        )
    except TimeoutError:
        return {"text": "It took me too long to respond."}
    
    return {"text": response}
