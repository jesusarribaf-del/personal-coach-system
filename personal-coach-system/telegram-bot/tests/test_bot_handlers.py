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
