# python 3.5.1
import configparser
import psutil
import datetime
import time
import json
import schedule
import logging
import sys

config = configparser.ConfigParser()
config.read('conf.ini')
timeint = config.get('setup', 'int')
filetype = config.get('setup', 'filetype')
log = config.get('log', 'loging')

logging.basicConfig(filename='logfortask5.log', level=log)
logging.debug('let me check them all')
logging.warning('Alarmaaaaaaa')

snapshot = 1


def kfdeco(foo):
    def wrapper(*args):
        print("<(John): Ok google, what number does this snapshot have?>")
        foo(*args)
        print("<(John): Thank you, google.)>")

    return wrapper


class var(object):
    def __init__(self):
        self.cpu = psutil.cpu_times(percpu=True)
        self.cpu_p = psutil.cpu_percent(percpu=True)
        self.mem = psutil.virtual_memory()
        self.disk = psutil.disk_usage('/')
        self.disk_io = psutil.disk_io_counters()
        self.net_count = psutil.net_io_counters(pernic=True)
logging.info('some variables are created')

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

    @kfdeco
    def txttop(self, myfile='top.txt'):
        try:
            global snapshot
            print("<(Google): info >> top(SNAPSHOT {0})>".format(snapshot))
            fmt = '%Y-%m-%d %H:%M:%S %Z'
            currtime = datetime.datetime.now()
            tstmp = datetime.datetime.strftime(currtime, fmt)
            f = open(myfile, "a")
            f.write("Snapshot {0}:, timestamp - {1}:\n".format(snapshot, tstmp))
            f.write("CPU: {0}\n".format(self.cpu[0]))
            f.write("CPU: {0}%\n".format(self.cpu_p[0]))
            f.write("VMem: {0}Mb\n".format(self.mem[0] / 1048576))
            f.write("Disk {}Mb\n".format(self.disk[0] / 1048576))
            f.write("Disk IO {0}Mb\n".format(self.disk_io[0] / 1048576))
            f.write("NetCount {}\n".format(self.net_count))
            f.write("\n")
            f.close()
            snapshot += 1
        except Exception as e:
            print("Ooops, some problems detected, try log file")
            logging.exception('My exception occurred, {}'.format(e))
            sys.exit(1)

class kf2(var1):
    def __init__(self):
        super(kf2, self).__init__()

    @kfdeco
    def jsontop(self, myfile="top.json"):
        try:
            self.__init__()
            global snapshot
            print("<(Google): info >> top(SNAPSHOT {0})>".format(snapshot))
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
        except Exception as e:
            print("Ooops, some problems detected, try log file")
            logging.exception('My exception occurred, {}'.format(e))
            sys.exit(1)

def txtjob():
    x = kf1()
    x.txttop()


def jsonjob():
    y = kf2()
    y.jsontop()


if filetype == "txt":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).seconds.do(txtjob)
elif filetype == "json":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).seconds.do(jsonjob)
else:
    print("check type in conf")
    logging.error("WTF, check config")
    quit()
while True:
    schedule.run_pending()
    time.sleep(3)