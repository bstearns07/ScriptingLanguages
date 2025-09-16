import subprocess
import shutil

def runWithTimeout(cmdList: list[str], timeoutSec: int) -> None:
    if not cmdList:
        print("No command given.")
        return
    if shutil.which(cmdList[0]) is None:
        print(f"Command not found: {cmdList[0]}")
        return
    try:
        ab = subprocess.run(cmdList, capture_output=True, text=True, timeout=timeoutSec)
        out = (ab.stdout or "").strip().splitlines()
        first = out[0] if out else ""
        print(f"Exit: {ab.returncode}")
        if first:
            print(f"First: {first}")
        if ab.stderr:
            print(f"Err: {ab.stderr.strip()}")
    except subprocess.TimeoutExpired:
        print(f"Timeout after {timeoutSec}s; process terminated.")

if __name__ == "__main__":
    #prints Python version or times out if blocked
    runWithTimeout(["dir", ""], 5)
