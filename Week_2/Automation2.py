from pathlib import Path 
import shutil #provides shell utilities for high-level file operations like copying, moving, removing

#  defines a function that copies one directory to another
def copyTree(srcDir: str, dstDir: str, dryRun: bool = True) -> None: 
    var1 = Path(srcDir) 
    var2 = Path(dstDir) 
    if not var1.exists(): 
        raise FileNotFoundError(f"Missing source: {srcDir}") 
    if dryRun: 
        print(f"[DRY] Would copy {var1} -> {var2}") 
        return # ends method execution before copying takes place

    # Create a directory for the destination
    # creates parent/nested directories if needed. If target exists, don't raise error
    # if target exists, contents will be merged
    var2.mkdir(parents=True, exist_ok=True)
    print(var1)
    print(var2)
    # iterate through all files in source path
    for ab in var1.rglob("*"):

        #remove the relative parent portion from the destination's file path
        var3 = var2 / ab.relative_to(var1)
        shutil.copy(ab, var3)
        # if the item is a directory, create it in the destination location
        # srcDir = /home/user/src
        # ab = /home/user/src/sub/file.txt
        # ab.relative_to(var1) -> sub/file.txt
        if ab.is_dir(): 
            var3.mkdir(parents=True, exist_ok=True) 
        else:
            # print a warning in the file already exists
            if var3.exists(): 
                print(f"[WARN] Overwrite {var3}")
            # copy the file to the destination
            shutil.copy2(ab, var3) 
 
if __name__ == "__main__": 
    copyTree("sample_data", "backup_data", dryRun=False)
 