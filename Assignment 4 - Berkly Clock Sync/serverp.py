from dateutil import parser
import datetime
import threading
import socket
import time

clientData = {}

def startRecvTime(connector,addr):
    while True:
        clockTimeString = connector.recv(1024).decode()
        clockTime = parser.parse(clockTimeString)
        clockTimeDiff = datetime.datetime.now() - clockTime

        clientData[addr] = {
            "clientTime":clockTime,
            "clientTimeDiff":clockTimeDiff,
            "connector":connector
        }
        print("Client data updated with :"+ str(addr))
        time.sleep(5)

def startConnecting(master_server):
    while True:
        masterSlaveConn , addr = master_server.accept()
        slaveAddr = str(addr[0]) + ":"+ str(addr[1])
        print(slaveAddr + " got connected successfully")
        currentThread = threading.Thread(target=startRecvTime,args=(masterSlaveConn,slaveAddr,))
        currentThread.start()

def getAvgClockDiff():
    timeDiffList = list(client['clientTimeDiff'] for clientAddr,client in clientData.items())
    sumTimeDiff = sum(timeDiffList,datetime.timedelta(0,0))
    avgTimeDiff = sumTimeDiff / len(clientData)
    return avgTimeDiff

def syncAllClocks():
    while True:
        print("New Sync Cycle")
        print("No of clients to be synced "+ str(len(clientData)))
        if len(clientData) > 0:
            avgTimeDiff = getAvgClockDiff()
            for clientAddr, client in clientData.items():
                try:
                    syncTime = datetime.datetime.now() + avgTimeDiff
                    client['connector'].send(str(syncTime).encode())
                except Exception as e:
                    print(e)
        else:
            print("No client to be synced")

        time.sleep(5)

def initiateClockServer(port=8080):
    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    print("Server Node Socket created Successfully")
    master_server.bind(('',port))
    master_server.listen(10)
    print("Server Listening")
    print("Started Making connections")
    connectThread = threading.Thread(target=startConnecting,args=(master_server,))
    connectThread.start()
    print("Syncing Time")
    syncThread  = threading.Thread(target=syncAllClocks,args=())
    syncThread.start()

if __name__ == '__main__':
    initiateClockServer(8080)

