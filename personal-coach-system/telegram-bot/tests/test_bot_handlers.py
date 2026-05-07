from unittest.mock import MagicMock, AsyncMock, patch
import pytest

from coach_bot.bot_handlers import build_agents, AGENT_LABELS, BotHandlers


@pytest.fixture
def tmp_repo(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "personal-profile.md").write_text("# Perfil\n- Test")
    return str(tmp_path)


def make_update(chat_id: int):
    update = MagicMock()
    update.effective_chat.id = chat_id
    update.message.reply_text = AsyncMock()
    update.message.chat_id = chat_id
    update.message.text = None
    update.message.caption = None
    update.message.photo = []
    return update


def make_context():
    context = MagicMock()
    context.bot.send_chat_action = AsyncMock()
    context.bot.get_file = AsyncMock()
    return context


# ─── Test 1 ───────────────────────────────────────────────────────────────────

def test_build_agents_returns_all_keys(tmp_repo):
    expected_keys = [
        "sleep", "strength", "nutrition", "meditation", "decisions",
        "motivation", "productivity", "identity", "memory_curator", "life_coworker",
    ]
    agents = build_agents(tmp_repo, "fake")
    assert set(agents.keys()) == set(expected_keys)
    assert len(agents) == 10


# ─── Test 2 ───────────────────────────────────────────────────────────────────

def test_agent_labels_has_all_keys(tmp_repo):
    agents = build_agents(tmp_repo, "fake")
    assert set(AGENT_LABELS.keys()) == set(agents.keys())


# ─── Test 3 ───────────────────────────────────────────────────────────────────

def test_is_authorized_matching_chat_id(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    update = make_update(12345)
    assert handlers._is_authorized(update) is True


# ─── Test 4 ───────────────────────────────────────────────────────────────────

def test_is_authorized_wrong_chat_id(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    update = make_update(99999)
    assert handlers._is_authorized(update) is False


# ─── Test 5 ───────────────────────────────────────────────────────────────────

async def test_cmd_start_replies_when_authorized(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    update = make_update(12345)
    context = make_context()

    await handlers.cmd_start(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args
    text = call_args[0][0] if call_args[0] else call_args[1].get("text", "")
    assert "Personal Coach activo" in text


# ─── Test 6 ───────────────────────────────────────────────────────────────────

async def test_cmd_start_ignores_unauthorized(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    update = make_update(99999)
    context = make_context()

    await handlers.cmd_start(update, context)

    update.message.reply_text.assert_not_called()


# ─── Test 7 ───────────────────────────────────────────────────────────────────

async def test_cmd_agentes_lists_all_agents(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    update = make_update(12345)
    context = make_context()

    await handlers.cmd_agentes(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args
    text = call_args[0][0] if call_args[0] else call_args[1].get("text", "")
    assert "Agentes activos" in text
    for key, (emoji, name) in AGENT_LABELS.items():
        assert name in text


# ─── Test 8 ───────────────────────────────────────────────────────────────────

async def test_handle_message_unauthorized_returns_early(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    update = make_update(99999)
    context = make_context()

    await handlers.handle_message(update, context)

    context.bot.send_chat_action.assert_not_called()


# ─── Test 9 ───────────────────────────────────────────────────────────────────

def test_extract_memory_proposal_detects_actualizar_pattern(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    text = "Análisis completo.\n\nACTUALIZAR → memory/body-training-profile.md\nPeso: 79kg (2026-05-07)"
    proposal = handlers._extract_memory_proposal(text)
    assert proposal is not None
    assert "body-training-profile.md" in proposal["file"]
    assert "79kg" in proposal["content"]


# ─── Test 10 ──────────────────────────────────────────────────────────────────

def test_extract_memory_proposal_returns_none_when_no_pattern(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    text = "Análisis normal sin propuesta de memoria."
    assert handlers._extract_memory_proposal(text) is None


# ─── Test 11 ──────────────────────────────────────────────────────────────────

def test_extract_memory_proposal_detects_actualizar_memoria_pattern(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    text = "ACTUALIZAR MEMORIA → memory/nutrition-progress.md\nPeso: 80kg"
    proposal = handlers._extract_memory_proposal(text)
    assert proposal is not None
    assert "nutrition-progress.md" in proposal["file"]


# ─── Test 12 ──────────────────────────────────────────────────────────────────

async def test_handle_message_rejects_pending_memory_with_no(tmp_repo):
    handlers = BotHandlers(tmp_repo, "fake", 12345)
    handlers._pending_memory[12345] = {"file": "memory/test.md", "content": "test content"}

    update = make_update(12345)
    update.message.text = "no"
    context = make_context()

    await handlers.handle_message(update, context)

    assert 12345 not in handlers._pending_memory
    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args
    text = call_args[0][0] if call_args[0] else ""
    assert "descartada" in text.lower()
