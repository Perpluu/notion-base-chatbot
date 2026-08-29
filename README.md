# Notion-Base Chatbot

A conversational AI chatbot that uses your Notion workspace as a knowledge base to answer questions. The bot retrieves relevant documents from Notion using semantic search and generates context-aware responses powered by OpenAI's language models.

## Overview

This project combines Notion's document management capabilities with modern LLM technology to create an intelligent chatbot. It leverages vector embeddings and retrieval-augmented generation (RAG) to provide accurate, context-grounded answers based on your Notion content.

## Features

- Notion API integration for seamless database and page access
- Vector embeddings and semantic search via Pinecone
- RAG-powered response generation with OpenAI
- FastAPI backend with async request handling
- Slack integration support
- Configurable timeouts and response limits
- Comprehensive test coverage

## Architecture

The application consists of three main components:

1. **Notion Integration** - Loads documents from your Notion database
2. **Vector Search** - Stores embeddings in Pinecone for fast semantic retrieval
3. **LLM Chain** - Uses OpenAI to generate answers based on retrieved context

## Prerequisites

- Python 3.10 or higher
- Notion workspace with admin access
- OpenAI API key
- Pinecone account for vector storage

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Perpluu/notion-base-chatbot.git
cd notion-base-chatbot
```

### 2. Set Up Notion Integration

1. Visit [Notion Developers](https://www.notion.so/profile/integrations)
2. Create a new internal integration and copy the API key
3. Share the target database or pages with your integration
4. Save the database ID from the Notion URL

### 3. Create Environment File

Copy the environment template and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
NOTION_SECRET=your_notion_integration_token
NOTION_PAGE=your_notion_database_id
OPENAI_KEY=your_openai_api_key
PINECONE_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
PINECONE_IDX=your_pinecone_index_name
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
uvicorn views:app --reload
```

The API will be available at `http://localhost:8000`

### Making Requests

Send a POST request to the root endpoint with your question:

```bash
curl -X POST http://localhost:8000 \
  -d "text=What information do you have about project X?"
```

Response:

```json
{
  "text": "Based on your Notion documents, project X is..."
}
```

### Running Tests

```bash
pytest test_views.py -v
```

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `NOTION_SECRET` | Your Notion integration API token |
| `NOTION_PAGE` | The Notion database ID to query |
| `OPENAI_KEY` | OpenAI API key for LLM access |
| `PINECONE_KEY` | Pinecone API key for vector storage |
| `PINECONE_ENV` | Pinecone environment (e.g., `us-west1-gcp`) |
| `PINECONE_IDX` | Name of your Pinecone index |

### Timeout Settings

The API has a built-in 3-second timeout for LLM responses. Adjust this in `views.py` if needed.

## Project Structure

```
notion-base-chatbot/
├── main.py              # Core initialization and chain setup
├── views.py             # FastAPI endpoints
├── notion_page.py       # Notion loader implementation
├── test_views.py        # API tests
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## How It Works

1. **Document Loading** - Fetches pages and database entries from Notion
2. **Embedding** - Converts documents to vector embeddings using OpenAI
3. **Storage** - Stores embeddings in Pinecone for fast retrieval
4. **Query Processing** - Converts user queries to embeddings
5. **Semantic Search** - Finds the most relevant documents
6. **Answer Generation** - Sends retrieved documents to OpenAI to generate a response

## Dependencies

- `langchain` - LLM orchestration and document processing
- `notion_client` - Official Notion API client
- `pinecone_client` - Vector database client
- `openai` - OpenAI API integration
- `fastapi` - Web framework
- `slack-bolt` - Slack integration
- `python-dotenv` - Environment variable management

## Error Handling

The API gracefully handles timeouts and returns a default message if the LLM takes too long to respond:

```json
{
  "text": "It took me too long to respond."
}
```

## Future Improvements

- Support for multiple vector databases
- Streaming responses for long-form answers
- Improved caching strategies
- Advanced prompt engineering
- Rate limiting and usage tracking
- Multi-workspace support

## Troubleshooting

**Issue: "Unauthorized" error from Notion**
- Verify your integration token is correct
- Ensure the integration is shared with the database
- Check that the database ID matches the Notion URL

**Issue: Empty or incorrect responses**
- Verify Pinecone is properly initialized
- Check that documents were indexed successfully
- Ensure OpenAI API key has sufficient credits

**Issue: Timeout errors**
- Increase the timeout value in `views.py`
- Check network connectivity to OpenAI and Pinecone
- Reduce the number of context documents being passed

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
