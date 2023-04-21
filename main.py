import pinecone
import langchain
from notion_client import Client
from langchain.document_loaders import NotionDBLoader
from langchain.docstore.document import Document
from langchain.document_loaders.notiondb import BLOCK_URL, PAGE_URL
from langchain.vectorstores import Pinecone, Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from typing import List, Dict, Any
import os

# Initialize Pinecone
pinecone.init(api_key="PINECONE_KEY", environment="PINECONE_ENV")
index_name = "pinecone1"
# Initialize Notion API client
notion = Client(auth="NOTION_SECRET")

# Retrieve the Notion page and its properties
page_id = "NOTION_PAGE"

page = notion.pages.retrieve(page_id=page_id)
class NotionPage(NotionDBLoader):
    def load(self) -> List[Document]:
        """Load documents from the Notion database.
        Returns:
            List[Document]: List of documents.
        """
        return self.load_page(self.database_id)

    def load_page(self, page_id: str, pages=None) -> Document:
        """Read a page."""
        data = self._request(PAGE_URL.format(page_id=page_id))

        # load properties as metadata
        metadata: Dict[str, Any] = {}

        for prop_name, prop_data in data["properties"].items():
            prop_type = prop_data["type"]

            if prop_type == "rich_text":
                value = (
                    prop_data["rich_text"][0]["plain_text"]
                    if prop_data["rich_text"]
                    else None
                )
            elif prop_type == "title":
                value = (
                    prop_data["title"][0]["plain_text"] if prop_data["title"] else None
                )
            elif prop_type == "multi_select":
                value = (
                    [item["name"] for item in prop_data["multi_select"]]
                    if prop_data["multi_select"]
                    else []
                )
            else:
                value = None

            metadata[prop_name.lower()] = value

        metadata["id"] = page_id
        page_content, page_ids = self._load_blocks(page_id)

        pages = pages or [Document(page_content=page_content, metadata=metadata)]

        for page_id in page_ids:
            pages.append(self.load_page(page_id, pages))
        return pages

    def _load_blocks(self, block_id: str, num_tabs: int = 0):
        """Read a block and its children."""
        result_lines_arr: List[str] = []
        cur_block_id: str = block_id
        page_ids = []

        while cur_block_id:
            data = self._request(BLOCK_URL.format(block_id=cur_block_id))

            for result in data["results"]:
                result_obj = result[result["type"]]

                # if "rich_text" not in result_obj:
                #     continue

                cur_result_text_arr: List[str] = []

                for rich_text in result_obj.get("rich_text", []):
                    if "text" in rich_text:
                        cur_result_text_arr.append(
                            "\t" * num_tabs + rich_text["text"]["content"]
                        )

                if result["has_children"] and result["type"] == "child_page":
                    page_ids.append(result["id"])
                elif result["has_children"]:
                    children_text, rec_page_ids = self._load_blocks(
                        result["id"], num_tabs=num_tabs + 1
                    )
                    cur_result_text_arr.append(children_text)
                    page_ids.extend(rec_page_ids)

                result_lines_arr.append("\n".join(cur_result_text_arr))

            cur_block_id = data.get("next_cursor")

        return "\n".join(result_lines_arr), page_ids
    
NotionPage1 = NotionPage('NOTION_SECRET', 'NOTION_PAGE')
loader = NotionPage1
docs = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key="OPENAI_KEY")
search = Pinecone.from_texts(docs, embeddings, index_name=index_name)
query = "questions"
docs1 = search.similarity_search(query, include_metadata=True)

llm = OpenAI(temperature=0, openai_api_key="OPENAI_KEY")
chain = load_qa_chain(llm, chain_type="stuff")
chain.run(input_documents=docs, question=query)