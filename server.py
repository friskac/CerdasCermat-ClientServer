import numpy as np
from numpy.random import shuffle
from random import randint
import socket
import time
import select

#LIST OF QUESTIONS AND ANSWERS
question2 = ["Apakah nama sungai terpanjang di dunia?",
            "Negara manakah yang memiliki wilayah terluas di dunia?",
            "Berasal dari manakah bunga Tulip?",
            "Dimanakah kantor PBB?",
            "Bahasa yang digunakan di Uruguay?"]
answer2 = [["Nil","Amazon","Yangtze","Kongo"],
        ["Rusia","China","South America","Europe"],
        ["Turkey","Netherlands","South America","German"],
        ["New York","UK","USA","Japan"],
        ["Spanish","English","French","Arabic"]]
question_done=[0]*(len(question2))

res = "no winner"


#SHOW THE POSSIBLE ANSWERS
def displayA(question,answer,i):
    a = answer[i]
    order = np.arange(4)
    shuffle(order) #create list from 1 to 4 in different order --> to print the answers in random order
    a_display = [[a[order[0]],a[order[1]]],[a[order[2]],a[order[3]]]]
    print(a_display)


#CHOOSE RANDOMLY A QUESTION IN THE LIST
def chooseQuestion(question,answer):
    k = randint(0,len(question)-1)
    if (question_done[k]!=0):
        while(question_done[k]!=0):
            k = randint(0,len(question)-1)
        question_done[k]=1
    else :
        question_done[k]=1
    print(question[k])
    print(answer[k])
    return k


#CHECK IF GOOD ANSWER OR NOT
def checkAnswer(answer,agiven,qnb,player,score):
    cli_ans = agiven.decode()
    test = False
    if(answer[qnb][0] == cli_ans):
        # print(score[player])
        test = True
        score[player]=score[player]+1
    print("score player", i, ": ", score[player])
    #print("ANSWER")
    return score



#END OF GAME, DISPLAY OF SCORES
def final_score(score):
    print("Skornya adalah {}".format(score))
    global res
    maxi = max(score)
    if(score.count(maxi)==1):
        print("Pemenangnya adalah player {}".format(score.index(max(score))+1))
        result = "Pemenangnya adalah player {}".format(score.index(max(score))+1)
        
        res = "" + result
    else :
        winners = []
        for i in range(len(score)):
            if(score[i]==maxi):
                winners.append(i+1)
        print("Pemenangnya adalah player {}".format(winners))
        result = "Pemenangnya adalah player {}".format(winners)
        
        res = "" + result
    

    
# result to client   
def result_client():
    #print("hasil dari tdi " + res)
    return res
host = '127.0.0.1'

port = 65532

#list for all the players
players = []

#creation of socket object UDP and bind
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((host, port))
#socket non blocking --> will always try to grab datas from the stream
#not block it
socket.setblocking(0)

print("Server Started.")

#INITIAL SETUP PERIOD
secs = 20
max_players = 5

# WAIT FOR PLAYERS TO JOIN
while ((secs > 0) and (len(players) < max_players)):
    ready = select.select([socket], [], [], 1)
    if ready[0]:
        data, addr = socket.recvfrom(1024)
        print("FIRST RECV {}".format(data))
        if addr not in players:
            players.append(addr)
            print("listed players {}".format(players))
            pesan = "Menunggu Cerdas Cermat dimulai.. "
            socket.sendto(pesan.encode(),players[len(players)-1])
        print(time.ctime(time.time()) +  ":" + str(data))
    secs = secs - 1

#START GAME
print("Cerdas Cermat dimulai!")
score = [0] * len(players)
for i in range(len(players)):
    try:
        pesan = "Cerdas Cermat dimulai!"
        socket.sendto(pesan.encode(), players[i])
    except:
        pass

#ASK QUESTIONS
nb = 3
for k in range(nb):
    print("Nomor {}".format(k+1))
    question_answer = chooseQuestion(question2,answer2)
    #print("ENTER FOR")
    for i in range(len(players)):
        try:
            pesan = str(question2[question_answer]) + str(answer2[question_answer])
            socket.sendto(pesan.encode(), players[i])
            #print("BEFORE GET ANSWER")
            agiven = ""
            ready = select.select([socket], [], [], 10)
            # print(ready[0].values)
            if ready[0]:
                agiven, addr = socket.recvfrom(1024)
                print("GOT ANSWER")
            print("agiven is : {}".format(agiven))
            score = checkAnswer(answer2,agiven, question_answer, i, score)
        except:
            pass

    
final_score(score)

for i in range(len(players)):
    try:
        pesan = "Cerdas Cermat telah selesai!" + result_client()
        socket.sendto(pesan.encode(), players[i])
    except:
        pass

socket.close()