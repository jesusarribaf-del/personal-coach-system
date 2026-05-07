import pytest
from unittest.mock import MagicMock, patch
from coach_bot.agents.base import BaseAgent, NO_CONTRIBUTION

class ConcreteAgent(BaseAgent):
    MEMORY_FILES = ["personal-profile.md"]
    EMOJI = "🧪"
    LABEL = "Test"

    def get_system_prompt(self) -> str:
        return "Eres un agente de prueba."

    def is_relevant(self, input_type: str) -> bool:
        return input_type == "test"

def test_no_contribution_constant():
    assert NO_CONTRIBUTION == "NO_APORTACION"

def test_is_relevant_true(tmp_path):
    agent = ConcreteAgent(str(tmp_path), "fake_key")
    assert agent.is_relevant("test") is True

def test_is_relevant_false(tmp_path):
    agent = ConcreteAgent(str(tmp_path), "fake_key")
    assert agent.is_relevant("other") is False

def test_memory_files_configured(tmp_path):
    agent = ConcreteAgent(str(tmp_path), "fake_key")
    assert "personal-profile.md" in agent.MEMORY_FILES

def test_get_system_prompt(tmp_path):
    agent = ConcreteAgent(str(tmp_path), "fake_key")
    assert len(agent.get_system_prompt()) > 0

def test_build_messages_text_only(tmp_path):
    agent = ConcreteAgent(str(tmp_path), "fake_key")
    context = {"text": "Hola", "input_type": "test"}
    msgs = agent._build_messages(context, "memoria", full=True)
    assert len(msgs) == 1
    assert msgs[0]["role"] == "user"
    assert "Hola" in msgs[0]["content"][-1]["text"]

def test_build_messages_brief_adds_instruction(tmp_path):
    agent = ConcreteAgent(str(tmp_path), "fake_key")
    context = {"text": "Hola", "input_type": "test"}
    msgs = agent._build_messages(context, "", full=False)
    assert NO_CONTRIBUTION in msgs[0]["content"][-1]["text"]

def test_build_messages_with_image(tmp_path):
    agent = ConcreteAgent(str(tmp_path), "fake_key")
    context = {"text": "Test", "input_type": "test", "image_base64": "abc123", "image_media_type": "image/jpeg"}
    msgs = agent._build_messages(context, "", full=True)
    content = msgs[0]["content"]
    assert content[0]["type"] == "image"
    assert content[0]["source"]["data"] == "abc123"
