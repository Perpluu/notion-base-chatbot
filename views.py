import requests
from fastapi import FastAPI, Request, Form
import httpx
import asyncio
from slack_bolt import App
from main import loader, docsearch, chain, embeddings

app = FastAPI()

@app.post("/")
async def notion_bot(request: Request, text: str = Form()):
    query = text.strip()
    docs = docsearch.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    return {"text": response}