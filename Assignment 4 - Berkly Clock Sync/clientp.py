from dateutil import parser
import datetime
import threading
import socket
import time


def startSendingTime(slaveClient):
    while True:
        slaveClient.send(str(datetime.datetime.now()).encode())
        print("Time sent successfully")
        time.sleep(5)


def startRecvTime(slaveClient):
    while True:
        syncTime = parser.parse(slaveClient.recv(1024).decode())
        print("Synced Time Receiveed At Client :" + str(syncTime))


def initiateSlaveServer(port=8080):
    slaveClient = socket.socket()
    slaveClient.connect(('127.0.0.1',port))

    print("Starting to send time to server")
    sendThread = threading.Thread(target=startSendingTime,args=(slaveClient,))
    sendThread.start()

    print("Starting Receiving Time from server ")
    recvThread = threading.Thread(target=startRecvTime,args=(slaveClient,))
    recvThread.start()

if __name__ == '__main__':
    initiateSlaveServer(8080)