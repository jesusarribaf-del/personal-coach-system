import pytest
import os
from coach_bot.memory_reader import MemoryReader

@pytest.fixture
def tmp_repo(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "personal-profile.md").write_text(
        "# Perfil personal\n\n- Nombre: Jesús\n- Edad: 30\n"
    )
    (memory_dir / "sleep-energy-log.md").write_text(
        "# Log sueño\n\n| 2026-05-07 | 7h | ok |\n"
    )
    return str(tmp_path)

def test_read_single_file(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files(["personal-profile.md"])
    assert "Jesús" in content
    assert "## personal-profile.md" in content

def test_read_multiple_files(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files(["personal-profile.md", "sleep-energy-log.md"])
    assert "Jesús" in content
    assert "Log sueño" in content

def test_missing_file_skipped(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files(["personal-profile.md", "nonexistent.md"])
    assert "Jesús" in content
    assert "nonexistent" not in content

def test_empty_list(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files([])
    assert content == ""

def test_memory_path_is_repo_subdir(tmp_repo):
    reader = MemoryReader(tmp_repo)
    assert reader.memory_path.endswith("memory")
    assert os.path.dirname(reader.memory_path) == tmp_repo

def test_all_files_missing_returns_empty(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files(["nonexistent1.md", "nonexistent2.md"])
    assert content == ""
