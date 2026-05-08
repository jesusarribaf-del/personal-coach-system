import os


class MemoryReader:
    def __init__(self, repo_path: str):
        self.memory_path = os.path.join(repo_path, "memory")

    def _read_file(self, path: str) -> str:
        """Read a file, trying utf-8 first then the system locale encoding."""
        for encoding in ("utf-8", None):  # None → locale default
            try:
                with open(path, "r", encoding=encoding) as f:
                    return f.read().strip()
            except (UnicodeDecodeError, LookupError):
                continue
        # Last resort: read with replacement characters
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()

    def read_files(self, filenames: list[str]) -> str:
        if not filenames:
            return ""
        sections = []
        for filename in filenames:
            path = os.path.join(self.memory_path, filename)
            if os.path.exists(path):
                try:
                    content = self._read_file(path)
                    sections.append(f"## {filename}\n{content}")
                except Exception as e:
                    print(f"[MemoryReader] Warning: could not read {filename}: {e}")
        return "\n\n---\n\n".join(sections)
