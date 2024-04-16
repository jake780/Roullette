import pygame
from random import randint

class Display():
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("Roboto-Medium.ttf", 30)
        self.fgcolor = (255,255,255)

        self.barColor = (0, 0, 0)

        self.lastWinObjs = []

    def winMessage(self, amount):
        """Displays win amount after spin"""
        if amount > 0:
            for _ in range(40):
                color = (randint(0,255), randint(0,255), randint(0,255))

                self.win_text = self.font.render(f"Win: {amount}", True, self.fgcolor, color)
                self.win_rect = self.win_text.get_rect()
                self.win_rect.center = (1400, 700)

                self.game.draw()
                self.game.m.draw([0,0], 0) # Redraw chips

                pygame.draw.rect(self.game.window, color, (1300, 670, 200, 60))

                self.game.window.blit(self.win_text, self.win_rect)
                pygame.display.update()
                pygame.time.delay(100)


    def lastWinList(self):
        """Populates self.lastWinObjs with a list of previous wins"""
        # Update Previous Winning Numbers
        offset = 34
        #if len(self.game.winningNums) != len(self.lastWinObjs):
        for obj in self.game.winningNums:
            self.num_text = self.font.render(f"{obj.value}", True, self.fgcolor, obj.color)
            self.num_rect = self.num_text.get_rect()
            self.num_rect.center = (175, (150 + offset))
            self.lastWinObjs.append([self.num_text, self.num_rect, obj.value, obj.color])
            offset += 34

        if len(self.lastWinObjs) > 17:
            self.lastWinObjs.pop()

        if len(self.game.winningNums) > 17:
            self.game.winningNums.pop()
                                
    def draw(self):
        """Displays info text, titles, last wins"""
        # Display bank
        self.title_text = self.font.render(f"Bank: {self.game.m.bank}", True, self.fgcolor, self.game.background)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (350, 700)
        self.game.window.blit(self.title_text, self.title_rect)

        # Previous Winners Title
        self.title_text = self.font.render("Wins", True, self.fgcolor, self.game.background)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (175, 146)
        self.game.window.blit(self.title_text, self.title_rect)

        # Previous Winners List
        for obj in self.lastWinObjs:
            pygame.draw.rect(self.game.window, obj[3], (obj[1][0]-20, obj[1][1]-2, 70, 38))
            self.game.window.blit(obj[0], obj[1])

        # Draw sidebars
        pygame.draw.rect(self.game.window, self.barColor, (125, 160, 90, 7))
        pygame.draw.rect(self.game.window, self.barColor, (200, 160, 25, 590))
        pygame.draw.rect(self.game.window, self.barColor, (125, 160, 25, 590))
        pygame.draw.rect(self.game.window, self.barColor, (125, 744, 90, 6))
            
    def update(self):
        self.lastWinList()
