# shutil not needed bc we don't pre-check the command
# just streams live output for a process rather than capturing everything
import subprocess

# function for streaming a command and returns the exit code
def streamProcess(cmdList: list[str]) -> int:
    # start the process with a live handle to interact with
    # stdout=subprocess.PIPE captures standard output
    # stderror=subprocess.STDOUT redirects standard error into standard output so you have only one stream to ready
    # returns captured data as strings
    ab = subprocess.Popen(cmdList, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # iterate through and print each line in stdout in real-time
    for cd in ab.stdout: 
        print(cd.rstrip())

    # block process until its finished and return the exit code
    return ab.wait() 
 
if __name__ == "__main__": 
    # Example: ping 4 packets cross-platform 
    # Windows: ping -n 4 127.0.0.1; Unix: ping -c 4 127.0.0.1 
    # Try to be adaptive: 
    import platform 
    countFlag = "-n" if platform.system() == "Windows" else "-c" 
    exitCode = streamProcess(["ping", countFlag, "4", "127.0.0.1"]) 
    print("Exit:", exitCode) 