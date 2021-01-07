import pygame
#from pygame.locals import *
from net import Network
#from player import Player
from cardgame import Game

pygame.init()
w = 700
h = 600
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('client')
clientNumber = 0
ctext = None

class Cards:
    def __init__(self, num, x, y, count):
        self.num = num
        self.x = x
        self.y = y
        self.width, self.height = 80, 100
        self.count = count
        self.color = white
        self.coord = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, white, self.coord)
        font = pygame.font.SysFont('comicsans', 50)
        text = font.render(str(self.num), 1, black)
        win.blit(text, ((self.x + round(self.width/2)-round(text.get_width()/2)), (self.y + round(self.height/2) - round(text.get_height()/2))))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        #print('x: ', self.x)
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            #print('clicked')
            return True
        else:
            return False

startX, interval = 100, 25
cards = [Cards('1', startX, 500, 0), Cards('2', startX + interval + 80, 500, 1), Cards('3', startX + 160 + interval*2, 500, 2), Cards('4', startX + 240 + interval*3, 500, 3), Cards('5', startX + 320 + interval*4, 500, 4)]
erased = []

def CenteredText(txt):
    font = pygame.font.SysFont(None, 50)
    text = font.render(txt, 1, white)
    win.blit(win, (w/2 - text.get_width()/2, h/2 - text.get_height()/2))


def updateWindow(win, game, p):
    global ctext
    win.fill((100,100,100))
    font = pygame.font.SysFont(None, 50)
    #text = None
    if not (game.connected()):
        ctext = font.render('- Waiting for Player -', 1, white)
        #CenteredText('- Waiting for Player -')
        win.blit(ctext,(w/2 - ctext.get_width()/2, h/2 - ctext.get_height()/2))
    else:
        ctext = font.render('Pick a Card', 1, white)
        #win.blit(text, (w/2 - text.get_width()/2, h/2 - text.get_height()/2))
        move1 = game.get_card(0)
        move2 = game.get_card(1)
        #print(move1, ' and ', move2)
        if game.bothReady():
            ctext = font.render (move1 + ' vs ' + move2, 1, white)
            pygame.time.delay(2000)
        else:
            if game.p1Ready and p == 0:
                ctext = font.render('Waiting...', 1, white)
                #pygame.display.update()
            elif game.p2Ready and p ==1:
                ctext = font.render('Waiting...', 1, white)
                #pygame.display.update()
            else:
                pass
        #win.blit(text, (w/2 - text.get_width()/2, h/2 - text.get_height()/2))
    for card in cards:
        card.draw(win)
        #print(card)
    win.blit(ctext, (w/2 - ctext.get_width()/2, h/2 - ctext.get_height()/2))
    pygame.display.update()

def main():
    global ctext, cards, erased
    run = True
    n = Network()
    clock = pygame.time.Clock()
    player = int(n.getPlayerId())
    print('Player #', player)
    number = 0
    winCount1 = 0
    winCount2 = 0
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Failed game")
            break
        #pos = pygame.mouse.get_pos()
        #for a in cards:
        #    if pos[0] > a.x and pos[0] < a.x + a.width:
        #        if pos[1] > a.y and pos[1] < a.y + a.height:
        #            print('on btn')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #print('mouse: ', pos, '\n card: ',  cards[0].x, ' - ', cards[0].x + 80)
                for card in cards:
                    number += 1
                    if card.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Ready:
                                n.send(card.num)
                                erased.append(card)
                                del cards[number-1]
                                #print(card.num)
                                updateWindow(win, game, player)
                            else:
                                pass
                            #else:
                                #if not game.p2Ready:
                                    #n.send(card.num)
                                    #print(card.num)
                        else:
                            if not game.p2Ready:
                                n.send(card.num)
                                erased.append(card)
                                del cards[number-1]
                                #print(card.num)
                                updateWindow(win, game, player)
                                #print(card.num)
        if number != 0:
            number = 0
            #print('zeroed')

        if game.bothReady():
            updateWindow(win, game, player)
            pygame.time.delay(1000)
            try:
                game = n.send('reset')
            except:
                run = False
                print('Could not get a game')
                break

            font = pygame.font.SysFont(None, 50)

            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                ctext = font.render('You won!', 1, white)
                print(game.winner())
                if (game.winner() == 1 and player == 1):
                    winCount2 += 1
                    print('won 2')
                elif (game.winner() == 0 and player == 0):
                    winCount1 += 1
                    print('won 1')
            elif game.winner() == -1:
                ctext = font.render('Tie', 1, white)
            else:
                ctext = font.render('You Lost...', 1, white)
                if (game.winner() == 1 and player == 0):
                    winCount2 += 1
                    print('won 1')
                elif (game.winner() == 0 and player == 1):
                    winCount1 += 1
                    print('won 2')
            print(winCount1, ':', winCount2)

            if len(cards) == 0:
                cards = erased
                erased = []
                if (winCount1 > winCount2 and player ==0) or (winCount1 < winCount2 and player == 1):#game.Judge(player):#(player == 0 and game.winCount1 > game.winCount2) or (player == 1 and game.winCount1 < game.winCount2):
                    ctext = font.render('You Won the Game!', 1, white)

                elif winCount2 == winCount1:#game.winCount1 == game.winCount2:
                    ctext = font.render('Tie Game', 1, white)
                else:
                    ctext = font.render('You Lost the Game...', 1, white)
                win.blit(ctext, (w / 2 - ctext.get_width() / 2, h / 2 - ctext.get_height() / 2 + 100))
                pygame.display.update()
                pygame.time.delay(3000)
                winCount1, winCount2 = 0, 0

            win.blit(ctext, (w/2 - ctext.get_width()/2, h/2 - ctext.get_height()/2 + 100))
            pygame.display.update()
            pygame.time.delay(2000)
        updateWindow(win, game, player)

main()