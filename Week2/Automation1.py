from pathlib import Path


def listFiles(rootPath: str, pattern: str) -> list[str]:
    # Walks rootPath recursively and returns all files matching pattern
    var1 = Path(rootPath)
    if not var1.exists():
        raise FileNotFoundError(f"Path not found: {rootPath}")
    var2 = [str(ab) for ab in var1.rglob(pattern) if ab.is_file()]
    return var2

if __name__ == "__main__":
    var3 = listFiles(".", "*.log")
    for ab in var3:
        print(ab)
