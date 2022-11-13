import socket
from threading import Thread
import time
SERVER = None
PORT = None
IP_ADDRESS = None
CLIENTS = {}
PLAYERNAMES = []
def acceptConnections():
    global CLIENTS
    global SERVER
    while(True):
        playerSocket, address = SERVER.accept()
        playerName = playerSocket.recv(1024).decode("utf-8").strip() #strip works like .split() in js, it will just take the name as playerSocket contains many other details as well
        print(playerSocket)
        if len(CLIENTS.keys()) == 0: #.keys() converts to list
            CLIENTS[playerName] = {"playerType": "player1"} #it will automatically create the key in the object
        else:
            CLIENTS[playerName] = {"playerType": "player2"}
        CLIENTS[playerName]["playerSocket"] = playerSocket
        CLIENTS[playerName]["playerAddress"] = address
        CLIENTS[playerName]["playerName"] = playerName
        CLIENTS[playerName]["turn"] = False;
        # PLAYERNAMES.append(playerName)
        print(f"Connection established with {playerName}: {address}")
        print(CLIENTS)

        thread = Thread(target=handleClient, args=(playerSocket, playerName))
        thread.start()

def handleClient(playerSocket, playerName):
    global CLIENTS
    global PLAYERNAMES
    playerType = CLIENTS[playerName]["playerType"] 
    if playerType == "player1":
        CLIENTS[playerName]["turn"] = True
        playerSocket.send(str({"playerType": playerType, "turn": CLIENTS[playerName]["turn"]}).encode("utf-8"))
    else:
        CLIENTS[playerName]["turn"] = False
        playerSocket.send(str({"playerType": playerType, "turn": CLIENTS[playerName]["turn"]}).encode("utf-8"))
    PLAYERNAMES.append({"name": playerName, "type": playerType})
    time.sleep(2)
    if len(PLAYERNAMES) > 0 and len(PLAYERNAMES) <= 2:
        for name in CLIENTS:
            clientSocket = CLIENTS[name]["playerSocket"]
            clientSocket.send(str({"playerNames": PLAYERNAMES}).encode("utf-8"))
    
    while(True):
        try:
            msg = playerSocket.recv(2048).decode("utf-8")
            if msg:
                for name in CLIENTS:
                    clientSocket = CLIENTS[name]["playerSocket"]
                    clientSocket.send(msg).encode("utf-8")
        except:
            pass



def setup():
    print("WELCOME TO LUDO LADDER")
    global SERVER 
    global PORT 
    global IP_ADDRESS 
    IP_ADDRESS = "127.0.0.1"
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(10)
    print("SERVER IS WAITING FOR PLAYERS")
    acceptConnections()
setup()
