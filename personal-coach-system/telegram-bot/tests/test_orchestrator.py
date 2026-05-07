import pytest
from unittest.mock import MagicMock
from coach_bot.orchestrator import Orchestrator, InputType

def make_message(text=None, has_photo=False, caption=None):
    msg = MagicMock()
    msg.text = text
    msg.caption = caption
    msg.photo = [MagicMock()] if has_photo else []
    return msg

def test_classify_plain_text():
    orc = Orchestrator()
    assert orc.classify(make_message(text="no quiero entrenar hoy")) == InputType.TEXT

def test_classify_report_command():
    orc = Orchestrator()
    assert orc.classify(make_message(text="/reporte semanal")) == InputType.REPORT

def test_classify_photo_no_caption_defaults_to_sleep():
    orc = Orchestrator()
    result = orc.classify(make_message(has_photo=True))
    assert result == InputType.SLEEP_IMAGE

def test_classify_photo_autosleep_caption():
    orc = Orchestrator()
    assert orc.classify(make_message(has_photo=True, caption="autosleep")) == InputType.SLEEP_IMAGE

def test_classify_photo_jefit_caption():
    orc = Orchestrator()
    assert orc.classify(make_message(has_photo=True, caption="jefit")) == InputType.WORKOUT_STRENGTH

def test_classify_photo_strava_caption():
    orc = Orchestrator()
    assert orc.classify(make_message(has_photo=True, caption="strava")) == InputType.WORKOUT_CARDIO

def test_classify_text_with_sleep_keyword():
    orc = Orchestrator()
    assert orc.classify(make_message(text="llevo 3 días durmiendo mal, hrv bajo")) == InputType.SLEEP_IMAGE

def test_classify_text_with_cardio_keyword():
    orc = Orchestrator()
    assert orc.classify(make_message(text="acabo de terminar mi cardio en strava")) == InputType.WORKOUT_CARDIO

def test_primary_key_for_sleep():
    orc = Orchestrator()
    assert orc.get_primary_key(InputType.SLEEP_IMAGE) == "sleep"

def test_primary_key_for_strength():
    orc = Orchestrator()
    assert orc.get_primary_key(InputType.WORKOUT_STRENGTH) == "strength"

def test_primary_key_for_cardio():
    orc = Orchestrator()
    assert orc.get_primary_key(InputType.WORKOUT_CARDIO) == "strength"

def test_primary_key_for_text():
    orc = Orchestrator()
    assert orc.get_primary_key(InputType.TEXT) == "life_coworker"

def test_secondary_keys_for_sleep_include_strength_and_nutrition():
    orc = Orchestrator()
    keys = orc.get_secondary_keys(InputType.SLEEP_IMAGE)
    assert "strength" in keys
    assert "nutrition" in keys

def test_secondary_keys_for_report_empty():
    orc = Orchestrator()
    assert orc.get_secondary_keys(InputType.REPORT) == []

def test_secondary_keys_for_strength_include_nutrition():
    orc = Orchestrator()
    keys = orc.get_secondary_keys(InputType.WORKOUT_STRENGTH)
    assert "nutrition" in keys
    assert "sleep" in keys
