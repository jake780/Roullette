import pygame
from random import randint

class Square():
    def __init__(self, game, x, y, width, height, color, value):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.value = value

        if self.value in self.game.reds:
            self.color = self.game.red
        if self.value in self.game.blacks:
            self.color =self.game.black

        #Font
        self.fgcolor = ((255,255,255))
        self.bgcolor = ((0,0,0))
        self.font = pygame.font.Font("Roboto-Medium.ttf", 30)
        self.font2 = pygame.font.Font("Roboto-Medium.ttf", 20)


    def draw(self):
        # Outline
        pygame.draw.rect(self.game.window, self.game.white, (self.x, self.y, self.width, self.height))
        # Fill
        pygame.draw.rect(self.game.window, self.color, (self.x+2, self.y+2, self.width-4, self.height-4))
        # Text
        self.value_text = self.font.render(f"{self.value}", True, self.fgcolor, self.color)
        self.value_rect = self.value_text.get_rect()
        self.value_rect.center = ((self.x+(self.width/2), self.y+(self.height/2)))
        self.game.window.blit(self.value_text, self.value_rect)

class wheelSquare(Square):
    def __init__(self, game, x, y, width, height, color, value):
        super().__init__(game, x, y, width, height, color, value)

class Chip(Square):
    def __init__(self, game, x, y, width, height, color, value):
        super().__init__(game, x, y, width, height, color, value)
        self.color = color

    def update(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.ellipse(self.game.window, self.game.white, (self.x ,self.y, self.width, self.height))
        pygame.draw.ellipse(self.game.window, self.color, (self.x+4 ,self.y+4, self.width-8, self.height-8))

        self.value_text = self.font.render(f"{self.value}", True, self.fgcolor, self.color)
        self.value_rect = self.value_text.get_rect()
        self.value_rect.center = ((self.x+(self.width/2), self.y+(self.height/2)))
        self.game.window.blit(self.value_text, self.value_rect)

class Ball():
    def __init__(self, game, x, y, width, height, color):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.spinning = False
        self.startingIndex = randint(0,37)
        self.currentSquareIndex = self.startingIndex
        self.loops = 0
        self.totalDelay = 1

    def draw(self):
        pygame.draw.ellipse(self.game.window, self.game.white, (self.x ,self.y, self.width, self.height), 40)

    def move(self):
        if self.spinning:
            # Set Ball Square
            self.x = self.game.wheelSquares[self.currentSquareIndex].x +11
            self.y = self.game.wheelSquares[self.currentSquareIndex].y + 10

            #Loop index
            if self.currentSquareIndex == 37:
                self.currentSquareIndex = 0
            else:
                self.currentSquareIndex += 1

            if self.currentSquareIndex == self.startingIndex:
                self.loops += 1

            # Slow down
            # if self.loops > 4:
            #     pygame.time.delay(self.totalDelay)
            #     self.totalDelay += 2
            
            # Final Ball Location
            # if self.totalDelay >= 200:
            if self.loops >= 6:
                self.spinning = False
                self.totalDelay = 1

                # show last position
                self.game.draw()
                pygame.display.update()

                winningSquare = self.game.wheelSquares[self.currentSquareIndex-1]

                # Payout
                self.game.m.payout(winningSquare.value)

                #Store Winning Num
                self.game.winningNums.insert(0, winningSquare)
                self.game.d.update()

                # Reset next random starting num
                self.startingIndex = randint(0,37)
                self.currentSquareIndex = self.startingIndex
                self.loops = 0
            