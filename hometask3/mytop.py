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
cpu = psutil.cpu_times(percpu=True)
cpu_p = psutil.cpu_percent(percpu=True)
mem = psutil.virtual_memory()
disk = psutil.disk_usage('/')
disk_io = psutil.disk_io_counters()
net_count = psutil.net_io_counters(pernic=True)


def txttop(myfile='top.txt'):
    global snapshot
    print("info >> top(SNAPSHOT {0})".format(snapshot))
    fmt = '%Y-%m-%d %H:%M:%S %Z'
    currtime = datetime.datetime.now()
    tstmp = datetime.datetime.strftime(currtime, fmt)
    f = open(myfile, "a")
    f.write("Snapshot {0}:, timestamp - {1}:\n".format(snapshot, tstmp))
    f.write("CPU: {0}\n".format(cpu[0]))
    f.write("CPU: {0}%\n".format(cpu_p[0]))
    f.write("VMem: {0}Mb\n".format(mem[0] / 1048576))
    f.write("Disk {}Mb\n".format(disk[0] / 1048576))
    f.write("Disk IO {0}Mb\n".format(disk_io[0] / 1048576))
    f.write("NetCount {}\n".format(net_count))
    f.write("\n")
    f.close()
    snapshot += 1


def kfdict(kf):
    a = list(kf)
    b = kf._fields
    final_dict = dict(zip(a, b))
    return final_dict


def jsontop(myfile="top.json"):
    global snapshot
    print("info >> top(SNAPSHOT {0})".format(snapshot))
    fmt = '%Y-%m-%d %H:%M:%S %Z'
    currtime = datetime.datetime.now()
    tstmp = datetime.datetime.strftime(currtime, fmt)
    jsonf = open(myfile, "a")
    jsonf.write("\nSnapshot #{0}, tstmp - {1}\n".format(snapshot, tstmp))
    jsonf.write("\nCPU\n")
    json.dump(cpu, jsonf, indent=1)
    jsonf.write("\nCPU\n")
    json.dump(cpu_p, jsonf, indent=1)
    jsonf.write("\nVMem\n")
    json.dump(mem, jsonf, indent=1)
    jsonf.write("\nDisk\n")
    json.dump(kfdict(disk), jsonf, indent=1)
    jsonf.write("\nDisk IO\n")
    json.dump(kfdict(disk_io), jsonf, indent=1)
    jsonf.write("\nNetCount\n")
    json.dump(net_count, jsonf, indent=1)
    jsonf.write("\n\n")
    jsonf.close()
    snapshot += 1

if filetype == "txt":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).minutes.do(txttop)
elif filetype == "json":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).minutes.do(jsontop)
else:
    print("check type in conf")
    quit()
while True:
    schedule.run_pending()
    time.sleep(7)
