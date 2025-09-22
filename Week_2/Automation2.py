from pathlib import Path 
import shutil # provides shell utilities for high-level file operations like copying, moving, removing

#  defines a function that copies one directory to another
def copyTree(srcDir: str, dstDir: str, dryRun: bool = True) -> None: 
    src = Path(srcDir)
    dst = Path(dstDir)
    if not src.exists():
        raise FileNotFoundError(f"Missing source: {srcDir}") 
    if dryRun: 
        print(f"[DRY] Would copy {src} -> {dst}")
        return # ends method execution before copying takes place

    # Create a directory for the destination
    # creates parent/nested directories if needed. If target exists, don't raise error
    # if target exists, contents will be merged
    dst.mkdir(parents=True, exist_ok=True)
    print(f"var 1: {src}")
    print(f"var 2: {dst}")
    # iterate through all files in source path
    for file in src.rglob("*"):

        #remove the relative parent portion from the destination's file path
        dstFilePath = dst / file.relative_to(src)
        print(f"Var 3: {dstFilePath}")
        shutil.copy(file, dstFilePath)
        # if the item is a directory, create it in the destination location
        # srcDir = /home/user/src
        # ab = /home/user/src/sub/file.txt
        # ab.relative_to(var1) -> sub/file.txt
        if file.is_dir():
            dstFilePath.mkdir(parents=True, exist_ok=True)
        else:
            # print a warning in the file already exists
            if dstFilePath.exists():
                print(f"[WARN] Overwrite {dstFilePath}")
            # copy the file to the destination
            shutil.copy2(file, dstFilePath)
 
if __name__ == "__main__": 
    copyTree("sample_data", "backup_data", dryRun=False)
 