from pathlib import Path
import datetime
import shutil
import random
filename = "app.log"
numLine = 100000
def addData():
    try:
        with open(filename, "a") as file:
            for x in range(numLine):
                randomInt = random.randint(1,100)
                file.write(str(randomInt) + "\n")
        print("Succeful add ", numLine)
    except IOError as e:
        print("Error")


def timeStamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def rotateLogIfLarge(logPath: str, maxBytes: int) -> None:
    var1 = Path(logPath)
    if not var1.exists():
        var1.parent.mkdir(parents=True, exist_ok=True)
        var1.write_text("")  # create empty
        print("Created new log.")
        return
    try:
        sz = var1.stat().st_size
    except Exception as ex:
        print(f"[ERROR] stat failed: {ex}")
        return
    if sz <= maxBytes:
        print("No rotate needed.")
        return
    var2 = var1.with_name(f"{var1.stem}-{timeStamp()}{var1.suffix}")
    shutil.move(str(var1), str(var2))
    Path(logPath).write_text("")
    print(f"Rotated -> {var2}")

if __name__ == "__main__":
    addData()
    rotateLogIfLarge("app.log", 1024 * 1024)  # 1 MB
