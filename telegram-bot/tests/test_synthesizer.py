import datetime
from coach_bot.synthesizer import synthesize

def test_primary_only():
    result = synthesize("Sueño profundo 7h. HRV 65.", "💤 Descanso", [])
    assert "💤 Descanso" in result
    assert "Sueño profundo" in result
    assert "📊" in result

def test_primary_plus_secondary():
    result = synthesize(
        "HRV bajo. Día de carga reducida.",
        "💤 Descanso",
        [("🏋️ Entreno", "Sesión técnica hoy."), ("🥗 Nutrición", "Prioriza carbohidratos.")]
    )
    assert "💤 Descanso" in result
    assert "🏋️ Entreno" in result
    assert "🥗 Nutrición" in result

def test_none_secondary_filtered():
    result = synthesize("Todo bien.", "💤 Descanso", [("🏋️ Entreno", None)])
    assert "🏋️ Entreno" not in result

def test_empty_string_secondary_filtered():
    result = synthesize("Todo bien.", "💤 Descanso", [("🏋️ Entreno", "   ")])
    assert "🏋️ Entreno" not in result

def test_header_contains_emoji():
    result = synthesize("Test.", "💤 Descanso", [])
    assert "📊" in result

def test_contains_date():
    result = synthesize("Test.", "💤 Descanso", [])
    year = str(datetime.date.today().year)
    month = datetime.date.today().strftime("%b")
    assert month in result
