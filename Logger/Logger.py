from datetime import datetime
import os.path

def createLogFile():
    now = datetime.now()
    f = open("Logs/" + now, "w")
    f.close()

def log(output, f):
    print(output)
    f = open("Logs/" + f, "a")
    f.write(output)
