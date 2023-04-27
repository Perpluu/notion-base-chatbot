import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from views import app

client = TestClient(app)


@pytest.fixture
async def mock_similarity_search():
    async with patch("main.docsearch.similarity_search") as async_mock:
        async_mock.return_value = ["doc1", "doc2"]
        yield async_mock


@pytest.fixture
async def mock_run():
    with patch("main.chain.run", new_callable=AsyncMock) as mock:
        mock.return_value = "test response"
        yield mock



@pytest.mark.asyncio
async def test_notion_bot_success(mock_similarity_search, mock_run):
    response = await client.post("/", data={"text": "test"})
    assert response.status_code == 200
    assert response.json() == {"text": "test response"}
    mock_similarity_search.assert_called_once_with("test")
    mock_run.assert_called_once_with(input_documents=["doc1", "doc2"], question="test")


@pytest.mark.asyncio
async def test_notion_bot_timeout(mock_similarity_search, mock_run):
    async def raise_timeout_error(*args, **kwargs):
        raise TimeoutError

    mock_run = AsyncMock(side_effect=raise_timeout_error)
    response = await client.post("/", data={"text": "test"})
    assert response.status_code == 200
    assert response.json() == {"text": "It took me too long to respond."}
    mock_similarity_search.assert_called_once_with("test")
    mock_run.assert_called_once_with(input_documents=["doc1", "doc2"], question="test")
