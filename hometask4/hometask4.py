import configparser
import psutil
import datetime
import time
import json
import schedule

config = configparser.ConfigParser()
config.read('conf.ini')
timeint = config.get('setup', 'int')
filetype = config.get('setup', 'filetype')

snapshot = 1

class var(object):
    def __init__(self):
        self.cpu = psutil.cpu_times(percpu=True)
        self.cpu_p = psutil.cpu_percent(percpu=True)
        self.mem = psutil.virtual_memory()
        self.disk = psutil.disk_usage('/')
        self.disk_io = psutil.disk_io_counters()
        self.net_count = psutil.net_io_counters(pernic=True)

class var1(var):
    def __init__(self):
        super(var1, self).__init__()
    def kfdict(self, kf):
        a = list(kf)
        b = kf._fields
        final_dict = dict(zip(a, b))
        return final_dict

class kf1(var1):
    def __init__(self):
        super(kf1, self).__init__()
    def txttop(self, myfile='top.txt'):
        global snapshot
        print("info >> top(SNAPSHOT {0})".format(snapshot))
        fmt = '%Y-%m-%d %H:%M:%S %Z'
        currtime = datetime.datetime.now()
        tstmp = datetime.datetime.strftime(currtime, fmt)
        f = open(myfile, "a")
        f.write("Snapshot {0}:, timestamp - {1}:\n".format(snapshot, tstmp))
        f.write("CPU: {0}\n".format(super().cpu[0]))
        f.write("CPU: {0}%\n".format(super().cpu_p[0]))
        f.write("VMem: {0}Mb\n".format(super().mem[0] / 1048576))
        f.write("Disk {}Mb\n".format(super().disk[0] / 1048576))
        f.write("Disk IO {0}Mb\n".format(super().disk_io[0] / 1048576))
        f.write("NetCount {}\n".format(super().net_count))
        f.write("\n")
        f.close()
        snapshot += 1

class kf2(var1):
    def __init__(self):
        super(kf2, self).__init__()
    def jsontop(self, myfile="top.json"):
        self.__init__()
        global snapshot
        print("info >> top(SNAPSHOT {0})".format(snapshot))
        fmt = '%Y-%m-%d %H:%M:%S %Z'
        currtime = datetime.datetime.now()
        tstmp = datetime.datetime.strftime(currtime, fmt)
        jsonf = open(myfile, "a")
        jsonf.write("\nSnapshot #{0}, tstmp - {1}\n".format(snapshot, tstmp))
        jsonf.write("\nCPU\n")
        json.dump(self.cpu, jsonf, indent=1)
        jsonf.write("\nCPU\n")
        json.dump(self.cpu_p, jsonf, indent=1)
        jsonf.write("\nVMem\n")
        json.dump(self.mem, jsonf, indent=1)
        jsonf.write("\nDisk\n")
        json.dump(self.kfdict(self.disk), jsonf, indent=1)
        jsonf.write("\nDisk IO\n")
        json.dump(self.kfdict(self.disk_io), jsonf, indent=1)
        jsonf.write("\nNetCount\n")
        json.dump(self.net_count, jsonf, indent=1)
        jsonf.write("\n\n")
        jsonf.close()
        snapshot += 1

def txtjob():
    x = kf1()
    x.txttop()
def jsonjob():
    y = kf2()
    y.jsontop()

if filetype == "txt":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).minutes.do(txtjob)
elif filetype == "json":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).minutes.do(jsonjob)
else:
    print("check type in conf")
    quit()
while True:
    schedule.run_pending()
    time.sleep(7)