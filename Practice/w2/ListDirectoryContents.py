from pathlib import Path

# define function to list a directory's contents
def ListDirectory(folderPath : str, pattern: str) -> list[str]:
    dir = Path(folderPath)

    if not dir.exists():
        raise FileNotFoundError("Directory not found")

    files = [item.name for item in dir.rglob(pattern) if item.is_file()]

    return files

if __name__ == "__main__":
    fileList = ListDirectory("C:\\Users\\bstea", "*.mdf")
    for file in fileList:
        print(file)