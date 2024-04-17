# Jacob Eazarsky

import pygame
from objects import Square, wheelSquare, Chip, Ball
from display import Display
from manager import Manager

class Game():
    def __init__(self):
        self.width = 1750
        self.height = 875
        self.frame_rate = 5
        pygame.display.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Roullette")

        self.wheelNums = ["00", 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2, 0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1]
        self.reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

        self.squares = []
        self.wheelSquares  = []
        self.chips = []

        self.boardxOffset = 225
        self.boardyOffset = 150

        # Colors
        self.background = (0,100,25) #Green
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.white = (255,255,255)
        self.grey = (150,150,150)

        self.oneChipColor = self.grey
        self.twoChipColor = (200,0,0)
        self.fiveChipColor = (0,0,200)
        self.tenChipColor = (0,200,0)
        self.twentyChipColor = (50,50,50)
        self.fiftyChipColor = (128,0,128)
        self.hundChipColor = (255, 100, 0)
        self.thouChipColor = (255,0,255)

        self.setup()
        self.sortWheelSquares()
        self.ball = Ball(self, 11, 10, 100,100, self.white)

        self.winningNums = []

        self.d = Display(self)
        self.m = Manager(self)

        self.m.bankLog(clear=True)


    def setup(self):
        """Setup and position all betting board squares and wheel squares"""

        # BOARD
        # Left side zeros
        self.squares.append(Square(self, self.boardxOffset, self.boardyOffset, 100, 250, (self.background), "00"))
        self.squares.append(Square(self, self.boardxOffset, self.boardyOffset+250, 100, 250, (self.background), "0"))

        # 1st row
        self.squares.append(Square(self, 0+self.boardxOffset+100, self.boardyOffset, 400, 100, (self.background), "1 - 12"))
        self.squares.append(Square(self, 400+self.boardxOffset+100, self.boardyOffset, 400, 100, (self.background), "13 - 24"))
        self.squares.append(Square(self, 800+self.boardxOffset+100, self.boardyOffset, 400, 100, (self.background), "25 - 36"))

        # middle rows
        for i in range(0,12):
            self.squares.append(Square(self, 100*i+self.boardxOffset+100, self.boardyOffset+100, 100, 100, (self.red), 3*i+3))
            self.squares.append(Square(self, 100*i+self.boardxOffset+100, self.boardyOffset+200, 100, 100, (self.black), 3*i+2))
            self.squares.append(Square(self, 100*i+self.boardxOffset+100, self.boardyOffset+300, 100, 100, (self.red), 3*i+1))

        #5th row
        self.squares.append(Square(self, 100+self.boardxOffset, self.boardyOffset+400, 200, 100, (self.background), "1 - 18"))
        self.squares.append(Square(self, 300+self.boardxOffset, self.boardyOffset+400, 200, 100, (self.background), "Even"))
        self.squares.append(Square(self, 500+self.boardxOffset, self.boardyOffset+400, 200, 100, (self.red), "Red"))
        self.squares.append(Square(self, 700+self.boardxOffset, self.boardyOffset+400, 200, 100, (self.black), "Black"))
        self.squares.append(Square(self, 900+self.boardxOffset, self.boardyOffset+400, 200, 100, (self.background), "Odd"))
        self.squares.append(Square(self, 1100+self.boardxOffset, self.boardyOffset+400, 200, 100, (self.background), "19 - 36"))

        # Wheel
        for i in range(14):
            self.wheelSquares.append(wheelSquare(self, i*125, 0, 125, 125, self.background, self.wheelNums[i]))
            self.wheelSquares.append(wheelSquare(self, i*125, 750, 125, 125, self.background, self.wheelNums[-i-6]))
        
        for i in range(1,6):
            self.wheelSquares.append(wheelSquare(self, 0, i*125, 125, 125, self.background, self.wheelNums[-i]))
            self.wheelSquares.append(wheelSquare(self, 1625, i*125, 125, 125, self.background, self.wheelNums[i+13]))
            
        # Display Chips
        self.chips.append(Chip(self, 475, 660, 80, 80, self.oneChipColor, 1))
        self.chips.append(Chip(self, 575, 660, 80, 80, self.twoChipColor, 2))
        self.chips.append(Chip(self, 675, 660, 80, 80, self.fiveChipColor, 5))
        self.chips.append(Chip(self, 775, 660, 80, 80, self.tenChipColor, 10))
        self.chips.append(Chip(self, 875, 660, 80, 80, self.twentyChipColor, 20))
        self.chips.append(Chip(self, 975, 660, 80, 80, self.fiftyChipColor, 50))
        self.chips.append(Chip(self, 1075, 660, 80, 80, self.hundChipColor, 100))
        self.chips.append(Chip(self, 1175, 655, 90, 90, self.thouChipColor, 1000))

    def getWheelSquare(self, value):
        """Returns a wheel square with value"""
        for w in self.wheelSquares:
            if w.value == value:
                return w

    def sortWheelSquares(self):
        """Sets the ordering of self.wheelSquares"""
        sortedSquares = []
        for wheelNum in self.wheelNums:
            sortedSquares.append(self.getWheelSquare(wheelNum))
        self.wheelSquares = sortedSquares

    def spin(self):
        """Spin the ball on the wheel"""
        self.draw()
        self.ball.spinning = True

    def move(self):
        """Move game objects"""
        self.ball.move()

    def draw(self):
        """Draw all game objects"""
        # Betting Squares
        for square in self.squares:
            square.draw()

        # Wheel Squares
        for square in self.wheelSquares:
            square.draw()

        # Chips
        for chip in self.chips:
            chip.draw()

        # Ball
        self.ball.draw()
        # Display
        self.d.draw()

    def run(self):
            # Mainloop
            run = True
            while run:
                pygame.event.pump()
                pygame.display.update()
                pygame.time.delay(self.frame_rate)
                key = pygame.key.get_pressed()
                mousePos = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()[0]

                # Clear Previous Frame
                self.window.fill(self.background)

                # Game events
                self.move()
                self.draw()

                self.m.input(mousePos, click)
                self.m.draw(mousePos, click)

                if key[27]:
                    self.m.updateStats()
                    run = False

                if key[32]:
                    self.spin()

                pygame.time.delay(self.frame_rate)

               