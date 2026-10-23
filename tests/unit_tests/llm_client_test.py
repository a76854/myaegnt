import pytest

from myagent.core.config import LLMSettings
from myagent.core.llm import LLMClient

def test_llm_client_chat():
    # Create an instance of LLMClient
    llm_client = LLMClient(LLMSettings())

    # Define test messages
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    # Call the chat method
    response = llm_client.chat(messages=test_messages)

    # Assert that the response is not None and has expected attributes
    assert response is not None
    assert hasattr(response, 'choices')
    assert len(response.choices) > 0