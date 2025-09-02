import subprocess # python module for launching external commands/programs and interacting with them
import shutil # find executables and handle shell utilities

# defines a function that executes a command
def runOneShot(cmdList: list[str], timeoutSec: int = 15) -> tuple[int, str, str]:

    # checks if command exists in system PATH. If not raise and error
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