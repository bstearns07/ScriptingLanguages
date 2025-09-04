import shutil
from pathlib import Path

def CopyDirectory(src:str, dst:str, dryRun: bool) -> None:
    sourcePath = Path(src)
    destinationPath = Path(dst)

    if dryRun:
        print(f'Copying {sourcePath} to {destinationPath}')
        return