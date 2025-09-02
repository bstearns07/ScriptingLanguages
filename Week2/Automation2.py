from pathlib import Path 
import shutil #provides shell utilities
 
def copyTree(srcDir: str, dstDir: str, dryRun: bool = True) -> None: 
    var1 = Path(srcDir) 
    var2 = Path(dstDir) 
    if not var1.exists(): 
        raise FileNotFoundError(f"Missing source: {srcDir}") 
    if dryRun: 
        print(f"[DRY] Would copy {var1} -> {var2}") 
        return 
    # If target exists, merge contents; create if absent 
    var2.mkdir(parents=True, exist_ok=True) 
    for ab in var1.rglob("*"): 
        var3 = var2 / ab.relative_to(var1) #takes some of path off
        if ab.is_dir(): 
            var3.mkdir(parents=True, exist_ok=True) 
        else: 
            if var3.exists(): 
                print(f"[WARN] Overwrite {var3}") 
            shutil.copy2(ab, var3) 
 
if __name__ == "__main__": 
    copyTree("sample_data", "backup_data", dryRun=True)
 