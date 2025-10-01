from pathlib import Path
import os
import tempfile

# define a function that writes text to a given txt filepath
def atomic_write(path:str,text:str) -> None:
    # cast path to a Path object
    path = Path(path)
    # create any needed parent directories to the path's destination. Ok if directories already exist
    path.parent.mkdir(parents=True,exist_ok=True)
    # create a temporary file containing the new data in the path's location that doesn't delete
    with tempfile.NamedTemporaryFile('w',delete=False,dir=path.parent) as t:
        t.write(text)
        temp_filepath = t.name
    # replace old file with temp file atomically
    os.replace(temp_filepath,path)
    print(f"Replaced {path} with {temp_filepath}")

atomic_write(r"C:\Users\bstea\OneDrive\Desktop\secret.txt","Ben was here lol")