import subprocess #run and interact with external programs
import shutil 
 
def runOneShot(cmdList: list[str], timeoutSec: int = 15) -> tuple[int, str, str]: 
    # Uses shell=False; relies on PATH resolution 
    if shutil.which(cmdList[0]) is None: 
        raise FileNotFoundError(f"Command not found: {cmdList[0]}") 
    ab = subprocess.run( 
        cmdList, 
        capture_output=True, # see if any errors occur
        text=True, # allows to view text
        timeout=timeoutSec, 
        check=False 
    ) 
    return ab.returncode, ab.stdout, ab.stderr 
 
if __name__ == "__main__": 
    code, out, err = runOneShot(["python", "--version"]) 
    print("Exit:", code) 
    print("Out:", out.strip()) 
    print("Err:", err.strip()) 