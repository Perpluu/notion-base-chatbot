import os
from typing import Any, Dict, List

import langchain
import pinecone
import requests
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from langchain.document_loaders import NotionDBLoader
from langchain.document_loaders.notiondb import BLOCK_URL, PAGE_URL
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma, Pinecone
from langchain.vectorstores.pinecone import Embeddings, Optional
from notion_client import Client

import views
from notion_page import NotionPage

load_dotenv()

PINECONE_KEY = os.environ.get('PINECONE_KEY')
PINECONE_ENV = os.environ.get('PINECONE_ENV')
NOTION_SECRET = os.environ.get('NOTION_SECRET')
NOTION_PAGE = os.environ.get('NOTION_PAGE')
OPENAI_KEY = os.environ.get('OPENAI_KEY')
PINECONE_IDX = os.environ.get('PINECONE_IDX')


# Initialize Pinecone
pinecone.init(api_key=PINECONE_KEY, environment=PINECONE_ENV)
index_name = PINECONE_IDX
# Initialize Notion API client
notion = Client(auth=NOTION_SECRET)

def get_notion_page_loader():
    notion_page = NotionPage(NOTION_SECRET, NOTION_PAGE)
    loader = get_notion_page_loader(NOTION_SECRET, NOTION_PAGE)
    docs = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)


llm = OpenAI(temperature=0, openai_api_key=OPENAI_KEY)
chain = load_qa_chain(llm, chain_type="stuff")
# print(chain.run(input_documents=docs, question=query))