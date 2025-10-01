from pathlib import Path 
import os 
import tempfile # creates secure temporary files/directories

# defines a function to write text to a file at a given file path
def atomicWrite(pathStr: str, text: str) -> None: 
    var1 = Path(pathStr)

    # create any possible missing parent directories
    var1.parent.mkdir(parents=True, exist_ok=True)

    # create a temporary file in the same folder as the final file
    # uses write mode for writing to the file
    # temp files doesn't delete once closed to allow for renaming the file
    with tempfile.NamedTemporaryFile("w", delete=False, dir=var1.parent) as ab:
        ab.write(text) 
        var2 = ab.name # store temp file's name

    # replace the old file with the temporary one atomically
    # Atomic writing: either a file is completely written or not changed at all
    # The original file stays intact until the new one is fully ready
    # Prevents partially written files if the app crashes during writing
    # os.replace(src temp file, target file to replace)
    os.replace(var2, var1)  # atomic on same filesystem 
 
if __name__ == "__main__": 
    atomicWrite("out/reports/summary.txt", "Hello\n") 