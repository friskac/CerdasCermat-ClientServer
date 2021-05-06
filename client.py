import socket
import threading
import time

tEv = threading.Event()
tShutdown = threading.Event()

def receving(name, sock):
    print("masuk")
    shutdown = False
    while not shutdown:
        try:
            data = sock.recvfrom(1024)
            print(str(data))
            if '?' in str(data):
                tEv.set()
            if "The game is finished" in str(data):  # message from server to stop
                shutdown = True
                tShutdown.set()
        except:
            pass
        finally:
            pass

#host = '192.168.26.86'
host = '127.0.0.1'
port = 0 #pick any free port currently on the computer
server = (host, 65534)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

# Start listener
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

# Join the game
alias = input("Name: ")
s.sendto(alias.encode(), server)

time = 15
first = True
while not tShutdown.is_set():
    if(first and time >= 0):
        print(time)
    if tEv.wait(1.0):
        first = False
        tEv.clear()
        message = input(alias + ", what is your answer ?  -> ")
        if message != '':
            s.sendto(message.encode(), server)
    time -= 1

rT.join()
s.close()