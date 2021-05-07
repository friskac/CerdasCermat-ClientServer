import socket
import threading
import time

threadEvent = threading.Event()
threadShutdown = threading.Event()

def receving(name, sock):
    print("masuk")
    shutdown = False
    while not shutdown:
        try:
            data = sock.recvfrom(1024)
            print(str(data))
            if '?' in str(data):
                threadEvent.set()
            if "Cerdas Cermat telah selesai!" in str(data):  # message from server to stop
                shutdown = True
                threadShutdown.set()
        except:
            pass
        finally:
            pass

#host = '192.168.26.86'
host = '127.0.0.1'
port = 0 #pick any free port currently on the computer
server = (host, 65532)

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((host,port))
socket.setblocking(0)

# Start listener
readThread = threading.Thread(target=receving, args=("RecvThread", socket))
readThread.start()

# Join the game
alias = input("Nama Anda: ")
socket.sendto(alias.encode(), server)

time = 15
first = True
while not threadShutdown.is_set():
    if(first and time >= 0):
        print(time)
    if threadEvent.wait(1.0):
        first = False
        threadEvent.clear()
        message = input(alias + ", apa jawabannya ?  -> ")
        if message != '':
            socket.sendto(message.encode(), server)
    time -= 1

readThread.join()
socket.close()