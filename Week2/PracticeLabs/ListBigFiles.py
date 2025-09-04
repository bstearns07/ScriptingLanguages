from pathlib import Path

def listBigFiles(rootPath: str, minBytes: int) -> None:
    var1 = Path(rootPath)
    if not var1.exists():
        print(f"Missing: {rootPath}")
        return
    var2 = []
    for ab in var1.rglob("*"):
        if ab.is_file():
            try:
                sz = ab.stat().st_size
                if sz >= minBytes:
                    var2.append((sz, ab))
            except Exception as ex:
                print(f"[WARN] {ab}: {ex}")
    var2.sort(key=lambda cd: cd[0], reverse=True)
    for ef, gh in var2:
        print(f"{ef:>12}  {gh}")

if __name__ == "__main__":
    # Example: list files >= 1 MB
    listBigFiles(".", 10)
