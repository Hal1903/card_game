class Game:

    def __init__(self, id):
        self.winCount = [int(0), int(0)]
        self.p1Ready = False
        self.p2Ready = False
        self.ready = False
        self.id = id
        self.cards = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        #winCount1 = 0
        #winCount2 = 0

    def get_card(self, p):
        return self.cards[p]

    def play(self, player, move):
        self.cards[player] = move
        if player == 0:
            self.p1Ready = True
        else:
            self.p2Ready = True

    def connected(self):
        return self.ready

    def bothReady(self):
        return self.p1Ready and self.p2Ready

    def winner(self):
        p1 = int(self.cards[0])
        p2 = int(self.cards[1])
        winner = -1
        if (p1 > p2):
            winner = 0
        if (p1 < p2):
            winner = 1
        return winner
        
    def Judge(self, player):
        if (player == 0 and self.winCount[0] > self.winCount[1]) or (player == 1 and self.winCount[0] < self.winCount[1]):
            return 0
        elif self.winCount[0] == self.winCount[1]:
            return -1
        else:
            return 1


    def resetCard(self):
        self.p1Ready = False
        self.p2Ready = False



    def counting(self, player):
        if self.winner() == 0:
            self.winCount[0] += 1
        elif self.winner() == 1:
            self.winCount[1] += 1
        else:
            pass
        return self.winCount[player]