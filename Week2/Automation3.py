from pathlib import Path 
import os 
import tempfile # creates secure the temporary directories
 
def atomicWrite(pathStr: str, text: str) -> None: 
    var1 = Path(pathStr) 
    var1.parent.mkdir(parents=True, exist_ok=True) 
    with tempfile.NamedTemporaryFile("w", delete=False, dir=var1.parent) as ab: #cant delete
        ab.write(text) 
        var2 = ab.name #renames file
    os.replace(var2, var1)  # atomic on same filesystem 
 
if __name__ == "__main__": 
    atomicWrite("out/reports/summary.txt", "Hello\n") 