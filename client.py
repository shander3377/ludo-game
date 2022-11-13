import socket
from threading import Thread
from tkinter import *
import random
from PIL import ImageTk, Image

SCREENWIDTH = None
SCREENHEIGHT = None
PORT = None
IP_ADDRESS = None
CLIENT = None
WINNING_FUNCTION_CALL = None
CANVAS1 = None
PLAYERNAME = None
NAME_ENTRY = None
NAME_WINDOW = None
CANVAS2 = None
GAME_WINDOW = 0
DICE = 0
LEFTBOXES = []
RIGHTBOXES = []
FINISHBOX = None
PLAYER_TURN=None
PLAYER_TYPE = None
PLAYER_NAME = None
PLAYER1_NAME= "JONING"
PLAYER2_NAME= "JOINING"
PLAYER1_LABEL= None
PLAYER2_LABEL= None
PLAYER1_SCORE= 0
PLAYER2_SCORE= 0
PLAYER1_SCORE_LABEL= None
ROLL_BUTTON=None
RESET_BUTTON = None
PLAYER2_SCORE_LABEL= None
TOTAL_STEPS = 10
WINNING_MSG = None

def leftBoard():
    global LEFTBOXES
    global GAME_WINDOW
    global SCREENHEIGHT

    xpos = 5
    for i in range(0, 11):
        if i == 0:
            box_Label = Label(GAME_WINDOW, font="sans-serif 30", width=2, height=1, relief="ridge", bd=1, bg="red")
            box_Label.place(x=xpos, y=SCREENHEIGHT/2.5)
            LEFTBOXES.append(box_Label)
            xpos += 40
        else:
            box_Label = Label(GAME_WINDOW, font="sans-serif 30", width=2, height=1, relief="ridge", bd=1, bg="white")
            box_Label.place(x=xpos, y=SCREENHEIGHT/2.5)
            LEFTBOXES.append(box_Label)
            xpos += 55
        

def rightBoard():
    global RIGHTBOXES
    global GAME_WINDOW
    global SCREENHEIGHT
    xpos = 770
    for i in range(0, 11):
        if i == 10:
            box_Label = Label(GAME_WINDOW, font="sans-serif 30", width=2, height=1, relief="ridge", bd=1, bg="yellow")
            box_Label.place(x=xpos, y=SCREENHEIGHT/2.5)
            RIGHTBOXES.append(box_Label)
            xpos += 40
        else:
            box_Label = Label(GAME_WINDOW, font="sans-serif 30", width=2, height=1, relief="ridge", bd=1, bg="white")
            box_Label.place(x=xpos, y=SCREENHEIGHT/2.5)
            RIGHTBOXES.append(box_Label)
            xpos += 55
def finishBox():
    global GAME_WINDOW
    global FINISHBOX
    global SCREENHEIGHT
    global SCREENWIDTH
    FINISHBOX = Label(GAME_WINDOW, font="sans-serif 32", text="HOME", width=6, height=3, bd=1, bg="green", fg="white")
    FINISHBOX.place(x=SCREENWIDTH/2-80, y=SCREENHEIGHT/2.75)

def gameWindow():
    global GAME_WINDOW
    global SCREENHEIGHT
    global SCREENWIDTH
    global DICE
    global PLAYERNAME
    global CANVAS2
    global PLAYER_TURN
    global PLAYER_TYPE
    global PLAYER1_NAME
    global PLAYER2_NAME
    global PLAYER1_LABEL
    global PLAYER2_LABEL
    global PLAYER1_SCORE
    global PLAYER2_SCORE
    global PLAYER1_SCORE_LABEL
    global PLAYER2_SCORE_LABEL
    global RESET_BUTTON
    global ROLL_BUTTON
    GAME_WINDOW = Tk()
    GAME_WINDOW.title("Ludo Ladder")
    GAME_WINDOW.attributes("-fullscreen", True)
    print(SCREENWIDTH)
    SCREENWIDTH = GAME_WINDOW.winfo_screenwidth()
    SCREENHEIGHT = GAME_WINDOW.winfo_screenheight()
    bg = ImageTk.PhotoImage(file='assets/background.png')
    CANVAS2 = Canvas(GAME_WINDOW, width=500, height=500)
    CANVAS2.pack(fill="both", expand=True) #fill is for space of window
    CANVAS2.create_image(0,0, image=bg, anchor="nw") #nw is northwest
    CANVAS2.create_text(SCREENWIDTH/2, SCREENHEIGHT/5, text="LUDO LADDER", font="sans-serif 100", fill="white")
    GAME_WINDOW.resizable(True, True)
    leftBoard()
    rightBoard()
    finishBox()
    DICE = CANVAS2.create_text(SCREENWIDTH/2, SCREENHEIGHT/1.5+50, text="\u2680", font="sans-serif 250", fill="white") #u2680 is dice symbol
    RESET_BUTTON = Button(GAME_WINDOW, text="Reset Game", fg="black", font="sans-serif 15")
    ROLL_BUTTON = Button(GAME_WINDOW, text="Roll Dice", fg="black", font="sans-serif 15", bg="grey", command=rollDice, width=20, height=5)
    
    if(PLAYER_TYPE == "PLAYER1" and PLAYER_TURN):
        ROLL_BUTTON.place(x=SCREENWIDTH/3-80, y=SCREENHEIGHT/2+250)
    else:
        ROLL_BUTTON.pack_forget()
    
    PLAYER1_LABEL=CANVAS2.create_text(400, SCREENHEIGHT/2+100, text=PLAYER1_NAME, font="sans-serif 80", fill="red")
    PLAYER2_LABEL=CANVAS2.create_text(SCREENWIDTH-300, SCREENHEIGHT/2+100, text=PLAYER2_NAME, font="sans-serif 80", fill="red")
    PLAYER1_SCORE_LABEL=CANVAS2.create_text(400, SCREENHEIGHT/2-160, text=PLAYER1_SCORE, font="sans-serif 80", fill="red")
    PLAYER2_SCORE_LABEL=CANVAS2.create_text(SCREENWIDTH-300, SCREENHEIGHT/2-160, text=PLAYER1_SCORE, font="sans-serif 80", fill="red")
    

    GAME_WINDOW.mainloop()
    

def rollDice():
    global CLIENT
    global PLAYER_TYPE
    global ROLL_BUTTON
    global PLAYER_TURN

    dicechoices = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    value = random.choice(dicechoices)
    ROLL_BUTTON.destory()
    PLAYER_TURN = False
    if PLAYER_TYPE == "player1":
        CLIENT.send(f"{value} PLAYER2_TURN".encode("utf-8"))
    elif PLAYER_TYPE == "player2":
        CLIENT.send(f"{value} PLAYER1_TURN".encode("utf-8"))
def handleWin(msg):
    global SCREENHEIGHT
    global SCREENWIDTH
    global CANVAS2
    global PLAYER_TURN
    global PLAYER_TYPE
    global RESET_BUTTON
    global ROLL_BUTTON
    global WINNING_MSG
    if ("RED" in msg):
        if PLAYER_TYPE == "player2":
            ROLL_BUTTON.destroy()
    if ("YELLOW" in msg):
        if PLAYER_TYPE == "player1":
            ROLL_BUTTON.destroy()
    print(msg)
    msg = msg.split(".")[0]+"."
    CANVAS2.item_configure(WINNING_MSG, text=msg)
    RESET_BUTTON.place(x=SCREENWIDTH/2-80, y=SCREENHEIGHT-220)


def updateScore(msg):
    global CANVAS2
    global PLAYER1_SCORE
    global PLAYER1_SCORE_LABEL
    global PLAYER2_SCORE_LABEL
    global PLAYER2_SCORE

    if ("RED" in msg):
        PLAYER1_SCORE += 1
    if("YELLOW" in msg):
        PLAYER2_SCORE +=1
    CANVAS2.itemconfigure(PLAYER1_SCORE_LABEL, text=PLAYER1_SCORE)
    CANVAS2.itemconfigure(PLAYER2_SCORE_LABEL, text=PLAYER2_SCORE)

def resetGame(msg):
    global CLIENT
    CLIENT.send("RESET GAME".encode("utf-8"))

def handleResetGame(msg):
    global SCREENHEIGHT
    global SCREENWIDTH
    global CANVAS2
    global PLAYER_TURN
    global PLAYER_TYPE
    global RESET_BUTTON
    global ROLL_BUTTON
    global WINNING_MSG
    global WINNING_FUNCTION_CALL
    global FINISHBOX
    global RIGHTBOXES
    global LEFTBOXES
    global GAME_WINDOW
    global DICE

    CANVAS2.itemconfigure(DICE, text="\u2680")
    if PLAYER_TYPE == "player1":
        ROLL_BUTTON= Button(GAME_WINDOW, text="ROLL DICE", fg="black", bg="grey", font="sans-serif 15 bold", width=20, height=5, command=rollDice)
        ROLL_BUTTON.place(x=SCREENWIDTH/2-80, y=SCREENHEIGHT/2+250)

        PLAYER_TURN= True
    if PLAYER_TYPE == "player2":
        PLAYER_TURN= False
    for rboxes in RIGHTBOXES[-2::-1]:
        rboxes.configure(bg="white")
    for lboxes in LEFTBOXES[1:]:
        lboxes.configure(bg="white")
    FINISHBOX.configure(bg="green")
    CANVAS2.itemconfigure(WINNING_MSG, text="")
    RESET_BUTTON.destroy()
    WINNING_FUNCTION_CALL = 0
    RESET_BUTTON = Button(GAME_WINDOW, text="Reset Game", fg="black", font="sans-serif 15")


    


def saveName():
    global PLAYERNAME
    global CLIENT
    global NAME_ENTRY
    global NAME_WINDOW
    PLAYERNAME= NAME_ENTRY.get()
    NAME_ENTRY.delete(0, END) #remove from starting till last
    NAME_WINDOW.destroy()
    CLIENT.send(PLAYERNAME.encode("utf-8"))
    gameWindow()

def checkColorPosition(color, boxes):
    for box in boxes:
        boxColor = box.cget("bg")
        if boxColor == color:
            return boxes.index(box)
    return False;

def movePlayer1(steps):
    global LEFTBOXES
    global TOTAL_STEPS
    global CLIENT
    global PLAYER_NAME
    global FINISHBOX
    boxPos = checkColorPosition("red", LEFTBOXES[1:]) #1: means first onward because first one will be red onyl
    if boxPos:
        dicevalue = steps
        colorBoxIndex = boxPos
        remaining_steps = TOTAL_STEPS-colorBoxIndex
        if steps == remaining_steps:
            for box in LEFTBOXES[1:]:
                box.configure(bg="white")
            FINISHBOX.configure(bg="red")
            greetmsg = f"RED WINS THE GAME!"
            CLIENT.send(greetmsg.encode("utf-8"))
        elif steps < remaining_steps:
            for box in LEFTBOXES[1:]:
                box.configure(bg="white")
            next_step = (colorBoxIndex+1)+dicevalue
            LEFTBOXES[next_step].configure(bg="red")
        else:
            print("MOVE FALSE")
    else:
        LEFTBOXES[steps].configure(bg="red")

def movePlayer2(steps):
    global RIGHTBOXES
    global CLIENT
    global FINISHBOX
    global PLAYER_NAME
    global TOTAL_STEPS
    temp_boxes = RIGHTBOXES[-2::-1] #:: means reverse
    boxPos = checkColorPosition("yellow", temp_boxes)
    if boxPos:
        dice_value = steps
        colorBoxIndex =boxPos
        remaining_steps = TOTAL_STEPS-colorBoxIndex
        if steps == remaining_steps:
            for box in temp_boxes:
                box.configure(bg="white")
            FINISHBOX.configure(bg="yellow", fg="black")
            greetmsg = f"YELLOW WINS THE GAME!"
            CLIENT.send(greetmsg.encode("utf-8"))
        elif steps < remaining_steps:
             for box in temp_boxes:
                box.configure(bg="white")
             next_step= (colorBoxIndex+1)+dice_value
             temp_boxes[next_step].configure(bg="yellow")
        else:
            print("MOVE FALSE")
    else:
        temp_boxes[steps].configure(bg="yellow")


def askName():
    global PLAYERNAME
    global NAME_ENTRY
    global CANVAS1
    global NAME_WINDOW
    global SCREENWIDTH
    global SCREENHEIGHT
    NAME_WINDOW = Tk()
    NAME_WINDOW.title("Ludo Ladder")
    NAME_WINDOW.attributes("-fullscreen", True)
    SCREENWIDTH = NAME_WINDOW.winfo_screenwidth()
    SCREENHEIGHT = NAME_WINDOW.winfo_screenheight()
    bg = ImageTk.PhotoImage(file='assets/background.png')
    CANVAS1 = Canvas(NAME_WINDOW, width=500, height=500)
    CANVAS1.pack(fill="both", expand=True) #fill is for space of window
    CANVAS1.create_image(0,0, image=bg, anchor="nw") #nw is northwest
    CANVAS1.create_text(SCREENWIDTH/2, SCREENHEIGHT/5, text="Enter your name", font="sans-serif 14", fill="white")
    NAME_ENTRY = Entry(NAME_WINDOW, width=15, font="sans-serif 50", justify="center", bd=5, bg="white") #bd is forb order
    NAME_ENTRY.place(x=SCREENWIDTH/3, y=(SCREENHEIGHT/4)+50)
    button= Button(NAME_WINDOW, text="Save", font="sans-serif 30", width=15, height=2, command=saveName, bg="cyan", bd=3)
    button.place(x=SCREENWIDTH/2.5,y=SCREENHEIGHT/2)
    NAME_WINDOW.mainloop() #make everything visible

def recievedMsg():
    global CLIENT
    global GAME_WINDOW
    global SCREENHEIGHT
    global SCREENWIDTH
    global DICE
    global PLAYERNAME
    global CANVAS2
    global PLAYER_TURN
    global PLAYER_TYPE
    global PLAYER1_NAME
    global PLAYER2_NAME
    global PLAYER1_LABEL
    global PLAYER2_LABEL
    global PLAYER1_SCORE
    global PLAYER2_SCORE
    global PLAYER1_SCORE_LABEL
    global PLAYER2_SCORE_LABEL
    global WINNING_FUNCTION_CALL
    global ROLL_BUTTON

    while(True):
        msg = CLIENT.recv(2048).decode("utf-8")
        if("PLAYER_TYPE" in msg):
            recvmsg = eval(msg)
            PLAYER_TYPE = recvmsg["PLAYER_TYPE"]
            PLAYER_TURN = recvmsg["PLAYER_TURN"]
        elif("PLAYER_NAMES" in msg):
            players = eval(msg)
            players = players["PLAYER_NAMES"]
            for p in players:
                if p["PLAYER_TYPE"] == ["PLAYER_1"]:
                    PLAYER1_NAME= p["PLAYER_NAME"]
                if p["PLAYER_TYPE"] == ["PLAYER_2"]:
                    PLAYER2_NAME= p["PLAYER_NAME"]
        elif("⚀" in msg):
            CANVAS2.itemconfigure(DICE, text="\u2680")
        elif("⚁" in msg):
            CANVAS2.itemconfigure(DICE, text="\u2681")
        elif("⚂" in msg):
            CANVAS2.itemconfigure(DICE, text="\u2682")
        elif("⚃" in msg):
            CANVAS2.itemconfigure(DICE, text="\u2683")
        elif("⚄" in msg):
            CANVAS2.itemconfigure(DICE, text="\u2684")
        elif("⚅" in msg):
            CANVAS2.itemconfigure(DICE, text="\u2685")             
        elif("WINS THE GAME" in msg and WINNING_FUNCTION_CALL==0):
            WINNING_FUNCTION_CALL+=1
            handleWin(msg)
            updateScore(msg)
        elif("RESET GAME" in msg):
            handleResetGame(msg)
        if("PLAYER1_TURN" in msg and PLAYER_TYPE=="PLAYER1"):
            PLAYER_TURN = True
            ROLL_BUTTON = Button(GAME_WINDOW, text="Roll Dice", fg="black", font="sans-serif 15", bg="grey", command=rollDice, width=20, height=5)
            ROLL_BUTTON.place(x=SCREENWIDTH/2, y=SCREENHEIGHT/1.5)
        elif("PLAYER2_TURN" in msg and PLAYER_TYPE=="PLAYER2"):
            PLAYER_TURN = True
            ROLL_BUTTON = Button(GAME_WINDOW, text="Roll Dice", fg="black", font="sans-serif 15", bg="grey", command=rollDice, width=20, height=5)
            ROLL_BUTTON.place(x=SCREENWIDTH/2, y=SCREENHEIGHT/1.5)
        if("PLAYER1_TURN" in msg or "PLAYER2_TURN" in msg):
            dicechoices = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            diceValue = dicechoices.index(msg[0])+1
            if("PLAYER2_TURN" in msg):
                movePlayer2(diceValue)
            if("PLAYER1_TURN" in msg):
                movePlayer1(diceValue)
        if(PLAYER1_NAME != "JOINING" and CANVAS2):
            CANVAS2.itemconfigure(PLAYER1_LABEL, text=PLAYER1_NAME)
        if(PLAYER2_NAME != "JOINING" and CANVAS2):
            CANVAS2.itemconfigure(PLAYER1_LABEL, text=PLAYER2_NAME)
       


def setup():
    global CLIENT
    global IP_ADDRESS
    global PORT
    PORT = 5000
    IP_ADDRESS = "127.0.0.1"
    CLIENT=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT.connect((IP_ADDRESS, PORT))
    askName()
setup()

    


