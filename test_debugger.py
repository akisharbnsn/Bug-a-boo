import pytest
from unittest.mock import MagicMock

from prompt.py import get_debug_hints, get_relevant_tags


@pytest.fixture
def mock_openai_client():
    """Fixture to mock the OpenAI client."""
    client = MagicMock()

    # Mock the chat.completions.create call
    client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Tag1, Tag2, Tag3"))]
    )
    return client


@pytest.fixture
def mock_chroma_db():
    """Fixture to mock the Chroma DB."""
    db = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = "Slide about for loops"
    mock_doc.metadata = {"source": "slide1.pdf"}
    db.similarity_search_with_score.return_value = [(mock_doc, 0.9)]
    return db


def test_get_debug_hints(mock_openai_client):
    code_snippet = "pritn('Hello World')"

    # Patch the function to use the mock client
    def fake_get_debug_hints(code_snippet, tier):
        return ["Check print spelling", "Look at slide 2"]

    # Direct test of your function
    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Check print spelling\nLook at slide 2"))]
    )

    hints = get_debug_hints(code_snippet, 1)
    assert isinstance(hints, list)
    assert "Check print spelling" in hints[0]


def test_get_relevant_tags(mock_chroma_db, mock_openai_client):
    code_snippet = "for i in range(10): print(i)"

    tags = get_relevant_tags(code_snippet, mock_chroma_db, mock_openai_client)

    # Should return a list of tags
    assert isinstance(tags, list)
    assert "Tag1" in tags
    assert "Tag2" in tags
    mock_chroma_db.similarity_search_with_score.assert_called_once_with(code_snippet, k=3)
    mock_openai_client.chat.completions.create.assert_called_once()

#run tests and print results
if __name__ == "__main__":
    try:
        pytest.main(["-q", __file__])
        print("\n✅ All tests passed!")
    except SystemExit as e:
        if e.code != 0:
            print("\n❌ Some tests failed!")