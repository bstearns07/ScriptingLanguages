# pathlib is a polished, OO version of os library. Treats file paths as Path objects rather than strings
from pathlib import Path


# defines a function to list all files in a given path
def listFiles(rootPath: str, pattern: str) -> list[str]:

    # Walks rootPath recursively and returns all files matching pattern

    #cast rootPath to a Path object
    var1 = Path(rootPath)

    # if path doesn't exist, raise an error
    if not var1.exists():
        raise FileNotFoundError(f"Path not found: {rootPath}")

    # glob and rglob are methods of pathLib that match file paths using patterns
    # uses recursive glob to search all subdirectories for files matching the pattern
    # returns an iteration of Path objects then cast to a list of str
    # only includes files, not directories
    var2 = [str(ab) for ab in var1.rglob(pattern) if ab.is_file()]
    return var2

if __name__ == "__main__":

    #retrieve all files in the current directory matching the desired pattern
    var3 = listFiles(".", "*.log")
    for ab in var3:
        print(ab)
