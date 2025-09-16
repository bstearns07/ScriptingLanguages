from pathlib import Path

folder = "test_files"

for file in Path(folder).rglob("*.py"):
    new_file = file.with_name(f"{file.stem}_new.py")
    file.rename(new_file)
    print(f"Renamed: {file} -> {new_file}")
