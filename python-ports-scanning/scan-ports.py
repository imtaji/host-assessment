import socket, threading, time, subprocess
from queue import Queue

#Clear the terminal screen
subprocess.call('clear', shell=True)

print_lock = threading.Lock()

#Ask for the host IP 
target = input ('Enter host: ')

#Log the start time
start_time = time.time()

#print 50 '-' lines and display banner
print ("-" * 50)
print (f"Checking state of all 65k ports\n\nHost: {target}")
print (f'\nTimestamp: {time.ctime(time.time())}')
print ("-" * 50)


def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #wait for response time
    s.settimeout(0.5)
    try:
        #make connect to each port starting from 1 to 65536
        con = s.connect((target,port))
        with print_lock:
            print('port',port,'is open!')
        con.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()

#Define no. of threads to run, example 100 in this script
for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

#ports range from 1 to 65536
for worker in range(1,65536):
    q.put(worker)

q.join()

#Print the scanning time
print("\nScanning time: %s Seconds " % (time.time() - start_time))