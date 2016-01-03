import os, subprocess, time

def compile(codename, lang):
    os.system("g++ " + codename + "." + lang + " -o out")
    f = os.popen("find out")
    if(f.read() == "out\n"):
        return True
    else:
        return False

def execute():
    starttime = time.time()
    proc = subprocess.Popen("./out < input.txt > output.txt", shell = True)
    try:
        proc.communicate(timeout = 3)
        t = proc.returncode
    except subprocess.TimeoutExpired:
        proc.terminate()
        t = 124
    endtime = time.time()
    timediff = endtime - starttime
    print(timediff)
    return t

ret = "Compile error"

if compile("ab", "cpp") == True:
    t = execute()
    
    if t == 124:
        ret = "Time limit exceeded"
    elif t == 139:
        ret = "SIGSEGV"
    elif t == 136:
        ret = "SIGFPE"
    elif t == 134:
        ret = "SIGABRT"
    elif t != 0:
        ret = "NZEC"
    else:
        os.system("diff output.txt answer.txt > diff.txt")
        if os.stat("diff.txt").st_size == 0:
            ret = "Accepted"
        else:
            ret = "Wrong answer"
        os.system("rm diff.txt")
    os.system("rm out")
    os.system("rm output.txt")
else:
    print(0.0)
print(ret)