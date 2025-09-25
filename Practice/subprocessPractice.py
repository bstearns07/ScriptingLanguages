import subprocess


# define function to execute any string list as a terminal command
def run_process(cmdString: list[str]):
    # create a live handler process that captures standard output, redirects errors to output, and returns as a str
    process = subprocess.Popen(cmdString, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # print the stdout of the process in real time
    for line in process.stdout:
        print(line.rstrip())
    # wait for the process to finish and return the return-code
    return process.wait()


if __name__ == "__main__":
    run_process(["ping", "127.0.0.1"])
