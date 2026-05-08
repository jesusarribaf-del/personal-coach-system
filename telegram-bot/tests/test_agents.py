import pytest
from coach_bot.agents.sleep import SleepCoach
from coach_bot.agents.strength import StrengthCoach
from coach_bot.agents.nutrition import NutritionCoach
from coach_bot.agents.meditation import MeditationGuide
from coach_bot.agents.decisions import DecisionAdvisor
from coach_bot.agents.motivation import MotivationCoach
from coach_bot.agents.productivity import ProductivityBuilder
from coach_bot.agents.identity import IdentityCoach
from coach_bot.agents.memory_curator import MemoryCurator
from coach_bot.agents.life_coworker import LifeCoworker

@pytest.fixture
def tmp_repo(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "personal-profile.md").write_text("# Perfil\n- Nombre: Jesús")
    return str(tmp_path)

# --- SleepCoach ---
def test_sleep_relevant_for_sleep(tmp_repo): assert SleepCoach(tmp_repo, "k").is_relevant("sleep") is True
def test_sleep_relevant_for_strength(tmp_repo): assert SleepCoach(tmp_repo, "k").is_relevant("strength") is True
def test_sleep_not_relevant_for_report(tmp_repo): assert SleepCoach(tmp_repo, "k").is_relevant("report") is False

# --- StrengthCoach ---
def test_strength_relevant_for_cardio(tmp_repo): assert StrengthCoach(tmp_repo, "k").is_relevant("cardio") is True
def test_strength_relevant_for_sleep(tmp_repo): assert StrengthCoach(tmp_repo, "k").is_relevant("sleep") is True

# --- NutritionCoach ---
def test_nutrition_relevant_for_sleep(tmp_repo): assert NutritionCoach(tmp_repo, "k").is_relevant("sleep") is True
def test_nutrition_relevant_for_strength(tmp_repo): assert NutritionCoach(tmp_repo, "k").is_relevant("strength") is True

# --- MeditationGuide ---
def test_meditation_relevant_for_sleep(tmp_repo): assert MeditationGuide(tmp_repo, "k").is_relevant("sleep") is True
def test_meditation_not_relevant_for_strength(tmp_repo): assert MeditationGuide(tmp_repo, "k").is_relevant("strength") is False

# --- DecisionAdvisor ---
def test_decisions_relevant_for_text(tmp_repo): assert DecisionAdvisor(tmp_repo, "k").is_relevant("text") is True
def test_decisions_not_relevant_for_sleep(tmp_repo): assert DecisionAdvisor(tmp_repo, "k").is_relevant("sleep") is False

# --- MotivationCoach ---
def test_motivation_relevant_for_strength(tmp_repo): assert MotivationCoach(tmp_repo, "k").is_relevant("strength") is True
def test_motivation_not_relevant_for_sleep(tmp_repo): assert MotivationCoach(tmp_repo, "k").is_relevant("sleep") is False

# --- ProductivityBuilder ---
def test_productivity_relevant_for_text(tmp_repo): assert ProductivityBuilder(tmp_repo, "k").is_relevant("text") is True
def test_productivity_not_relevant_for_strength(tmp_repo): assert ProductivityBuilder(tmp_repo, "k").is_relevant("strength") is False

# --- IdentityCoach ---
def test_identity_relevant_for_text(tmp_repo): assert IdentityCoach(tmp_repo, "k").is_relevant("text") is True
def test_identity_not_relevant_for_sleep(tmp_repo): assert IdentityCoach(tmp_repo, "k").is_relevant("sleep") is False

# --- MemoryCurator ---
def test_memory_curator_never_relevant(tmp_repo): assert MemoryCurator(tmp_repo, "k").is_relevant("text") is False

# --- LifeCoworker ---
def test_life_coworker_always_relevant(tmp_repo): assert LifeCoworker(tmp_repo, "k").is_relevant("sleep") is True

# --- System prompts not empty ---
def test_all_agents_have_system_prompts(tmp_repo):
    agents = [
        SleepCoach(tmp_repo, "k"), StrengthCoach(tmp_repo, "k"), NutritionCoach(tmp_repo, "k"),
        MeditationGuide(tmp_repo, "k"), DecisionAdvisor(tmp_repo, "k"), MotivationCoach(tmp_repo, "k"),
        ProductivityBuilder(tmp_repo, "k"), IdentityCoach(tmp_repo, "k"),
        MemoryCurator(tmp_repo, "k"), LifeCoworker(tmp_repo, "k"),
    ]
    for agent in agents:
        assert len(agent.get_system_prompt()) > 100, f"{agent.__class__.__name__} system prompt too short"
