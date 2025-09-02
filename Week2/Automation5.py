import subprocess 
 
def streamProcess(cmdList: list[str]) -> int: 
    ab = subprocess.Popen(cmdList, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) 
    for cd in ab.stdout: 
        print(cd.rstrip()) 
    return ab.wait() 
 
if __name__ == "__main__": 
    # Example: ping 4 packets cross-platform 
    # Windows: ping -n 4 127.0.0.1; Unix: ping -c 4 127.0.0.1 
    # Try to be adaptive: 
    import platform 
    countFlag = "-n" if platform.system() == "Windows" else "-c" 
    exitCode = streamProcess(["ping", countFlag, "4", "127.0.0.1"]) 
    print("Exit:", exitCode) 