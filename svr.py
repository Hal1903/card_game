import socket
from _thread import *
import pickle
from cardgame import Game
from code import ip

server = ip.address(ip)
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen(2)
print('server started')

connected = set()
games = {}
idCount = 0

def threaded_client(conn, playerId, gameId):
    global idCount
    conn.send(str.encode(str(playerId)))
    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data =='reset':
                        game.resetCard()
                    elif data!='get':
                        game.play(playerId, data)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break
    print('Lost connection')

    try:
        del games[gameId]
        print('Closing ', gameId)
    except:
        pass

    idCount -= 1
    conn.close()

while True:
# now our endpoint knows about the OTHER endpoint
    conn, addr = s.accept()
    print('Connected to: ', addr)
    idCount += 1
    PL = 0
    gameId = (idCount-1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print('new game')
    else:
        games[gameId].ready = True
        PL = 1
    start_new_thread(threaded_client,(conn, PL, gameId))