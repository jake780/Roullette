import pygame
from objects import Chip

class Manager():
    """Manages Betting, Chips, Bank"""
    def __init__(self, game):
        self.game = game
        self.currentChip = None
        self.holdingChip = False

        self.betChipSize = 60

        self.singleBetMult = 36
        self.dualBetMult = 18
        self.triBetMult = 12
        self.quadBetMult = 9
        self.thirdsBetMult = 3

        # [x, y, width, height, value, mult]
        self.betBoxes = [[225, 400, 100, 250, "0"], [225, 150, 100, 250, "00"], [325, 150, 400, 100, "1-12"], [725, 150, 400, 100, "13-24"], [1125, 150, 400, 100, "25-36"], 
                                    [325, 550, 200, 100, "1-18"], [525, 550, 200, 100, "even"], [725, 550, 200, 100, "red"], [925, 550, 200, 100, "black"], [1125, 550, 200, 100, "odd"], [1325, 550, 200, 100, "19-36"],
                                    [325,250,100,100, "3"], [425,250,100,100, "6"], [525,250,100,100, "9"],[625,250,100,100, "12"], [725,250,100,100, "15"], [825,250,100,100, "18"], [925,250,100,100, "21"], [1025,250,100,100, "24"], [1125,250,100,100, "27"], [1225,250,100,100, "30"], [1325,250,100,100, "33"], [1425,250,100,100, "36"], 
                                    [325,350,100,100, "2"], [425,350,100,100, "5"], [525,350,100,100, "8"],[625,350,100,100, "11"], [725,350,100,100, "14"], [825,350,100,100, "17"], [925,350,100,100, "20"], [1025,350,100,100, "23"], [1125,350,100,100, "26"], [1225,350,100,100, "29"], [1325,350,100,100, "32"], [1425,350,100,100, "35"],
                                    [325,450,100,100, "1"], [425,450,100,100, "4"], [525,450,100,100, "7"],[625,450,100,100, "10"], [725,450,100,100, "13"], [825,450,100,100, "16"], [925,450,100,100, "19"], [1025,450,100,100, "22"], [1125,450,100,100, "25"], [1225,450,100,100, "28"], [1325,450,100,100, "31"], [1425,450,100,100, "34"]]
        
        self.chipBoxes = [[475, 660, 80, 80], [575, 660, 80, 80], [675, 660, 80, 80], [775, 660, 80, 80], [875, 660, 80, 80], [975, 660, 80, 80], [1075, 660, 80, 80], [1175, 655, 90, 90]]

        self.gameChips = []
        self.currentBets = []

        self.bank = 100

    def log(self):
        with open("log.csv", "a") as log:
            log.write(f"{self.bank},")

    def clearLog(self):
        with open("log.csv", "w") as log:
            log.write("")

    def payout(self, winningNum):
        """Payout all bets (Parses self.currentBets for winningBet)"""
        winAmount = 0

        for bet in self.currentBets:
            for label in bet[1]:
                # label is a special bet
                if (label == "00") and (winningNum == "00"):
                        winAmount += bet[0]
                elif (label == "black") and (winningNum in self.game.blacks):
                        winAmount += bet[0]
                elif (label == "red") and (winningNum in self.game.reds):
                        winAmount += bet[0]
                elif (label == "1-18") and (winningNum in range(1,19)):
                        winAmount += bet[0]
                elif (label == "19-36") and (winningNum in range(19,37)):
                        winAmount += bet[0]
                elif (label == "1-12") and (winningNum in range(1, 13)):
                        winAmount += bet[0] 
                elif (label == "13-24") and (winningNum in range(13, 25)):
                        winAmount += bet[0]
                elif (label == "25-36") and (winningNum in range(25, 37)):
                        winAmount += bet[0]
                elif (label == "even") and (winningNum not in ["00", "0"]) and ((int(winningNum) % 2) == 0):
                        winAmount += bet[0]
                elif (label == "odd") and ((int(winningNum) % 2) != 0):
                        winAmount += bet[0]
                else:
                    # label is a number
                    if (label not in ["black", "red", "1-18", "19-36", "even", "odd", "1-12", "13-24", "25-36"]) and (int(label) == winningNum):
                        winAmount += bet[0]
                    

        # Apply win amount
        self.bank += (winAmount)

        # Append to the log file
        self.log()

        # Display win amount
        self.game.d.winMessage(winAmount)

        # Reset betting Components
        self.currentBets = []
        self.gameChips = []

    def addBets(self, chipValue, bets):
        """Populates self.currentBets with a list of ['winAmount',[betlist]]"""
        # Subtract from bank
        self.bank -= chipValue
        # Remove Duplicates
        bets = list(dict.fromkeys(bets))
        
        for bet in bets:
            if (bet in ["red", "black", "odd", "even", "1-18", "19-36"]):
                betValue = 2
            elif (bet in ["1-12", "13-24", "25-36"]):
                betValue = 3
            else:
                betValue = int(36 / len(bets))
        self.currentBets.append([chipValue*betValue, bets])


    def draw(self, mousePos, click):
        """Draw current held chip and all game chips in play"""
        if self.currentChip != None:
            if self.holdingChip:
                self.currentChip.update(mousePos[0]-self.betChipSize/2, mousePos[1]-self.betChipSize/2)
            self.currentChip.draw()

        for chip in self.gameChips:
            chip.draw()

    def collide(self):
        """Determines bet chip collisions with betting boxes"""
        chipHitBox = [self.currentChip.x, self.currentChip.x+self.betChipSize, self.currentChip.y, self.currentChip.y+self.betChipSize]
        bets = []

        for box in self.betBoxes:
            # Top left
            if (chipHitBox[0] >= box[0]) and (chipHitBox[0] <=box[0]+box[2]) and (chipHitBox[2] >= box[1]) and (chipHitBox[2] <= box[1]+box[3]):
                bets.append(box[4])

            # Bottom left
            if (chipHitBox[0] >= box[0]) and (chipHitBox[0] <=box[0]+box[2]) and (chipHitBox[3] >= box[1]) and (chipHitBox[3] <= box[1]+box[3]):
                bets.append(box[4])

            # Top Right
            if (chipHitBox[1] >= box[0]) and (chipHitBox[1] <=box[0]+box[2]) and (chipHitBox[2] >= box[1]) and (chipHitBox[2] <= box[1]+box[3]):
                bets.append(box[4])

            # Bottom right
            if (chipHitBox[1] >= box[0]) and (chipHitBox[1] <=box[0]+box[2]) and (chipHitBox[3] >= box[1]) and (chipHitBox[3] <= box[1]+box[3]):
                bets.append(box[4])

        # if valid chip placement
        if len(bets) > 0:
            self.addBets(self.currentChip.value, bets) # called once per chip
            self.gameChips.append(self.currentChip)
        
        # Drop Chip
        self.holdingChip = False
        self.currentChip = None

                
    def input(self, mousePos, click):
        """Takes mouse input and allows for chip movement"""
        # Drop current chip
        if (click and self.holdingChip):
            self.collide()

        #Pickup Chips
        for box in self.chipBoxes:
            if (mousePos[0] >= box[0]) and (mousePos[0] <= box[0]+box[2]) and (mousePos[1] >= box[1]) and (mousePos[1] <= box[1]+box[3]) and click and (not self.holdingChip) and not (self.game.ball.spinning):
                if (box == self.chipBoxes[0]) and (self.bank >= 1):
                    self.currentChip = Chip(self.game, mousePos[0]-self.betChipSize/2, mousePos[1]-self.betChipSize/2, self.betChipSize, self.betChipSize, self.game.oneChipColor, 1)
                if (box == self.chipBoxes[1]) and (self.bank >= 2):
                    self.currentChip = Chip(self.game, mousePos[0]-self.betChipSize/2, mousePos[1]-self.betChipSize/2, self.betChipSize, self.betChipSize, self.game.twoChipColor, 2)
                if (box == self.chipBoxes[2]) and (self.bank >= 5):
                    self.currentChip = Chip(self.game, mousePos[0]-self.betChipSize/2, mousePos[1]-self.betChipSize/2, self.betChipSize, self.betChipSize, self.game.fiveChipColor, 5)
                if (box == self.chipBoxes[3]) and (self.bank >= 10):
                    self.currentChip = Chip(self.game, mousePos[0]-self.betChipSize/2, mousePos[1]-self.betChipSize/2, self.betChipSize, self.betChipSize, self.game.tenChipColor, 10)
                if (box == self.chipBoxes[4]) and (self.bank >= 20):
                    self.currentChip = Chip(self.game, mousePos[0]-self.betChipSize/2, mousePos[1]-self.betChipSize/2, self.betChipSize, self.betChipSize, self.game.twentyChipColor, 20)
                if (box == self.chipBoxes[5]) and (self.bank >= 50):
                    self.currentChip = Chip(self.game, mousePos[0]-self.betChipSize/2, mousePos[1]-self.betChipSize/2, self.betChipSize, self.betChipSize, self.game.fiftyChipColor, 50)
                if (box == self.chipBoxes[6]) and (self.bank >= 100):
                    self.currentChip = Chip(self.game, mousePos[0]-80/2, mousePos[1]-80/2, 80, 80, self.game.hundChipColor, 100)
                if (box == self.chipBoxes[7]) and (self.bank >= 1000):
                    self.currentChip = Chip(self.game, mousePos[0]-80/2, mousePos[1]-80/2, 90, 90, self.game.thouChipColor, 1000)

                # if ur broke
                if (self.currentChip != None):
                    self.holdingChip = True

                pygame.time.delay(250)
