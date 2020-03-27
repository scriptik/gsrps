#!/usr/bin/python
import pygame
import sys
import time
import random
import math
#import json
from pygame.locals import *
from spritesheet_functions import SpriteSheet
from boot_screen import BootScreen
from wrjson import *
from checkwin import gscheckWin

config = read()
game_mode = config[0]['game_mode']

if game_mode == "network":
   from network import Network
   import pickle
   n = Network()
   player = int(n.getP())
   print("You are player", player)



#from boot_screen import BootScreen

# Call this function so the Pygame library can initialize itself
pygame.init()
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h
#print(display_width, display_height)
if display_width == 320 and display_height == 240:
   screen = pygame.display.set_mode([320, 240], pygame.FULLSCREEN)
else :
   screen = pygame.display.set_mode([320, 240])

# This sets the name of the window
pygame.display.set_caption('rpsgs')

clock = pygame.time.Clock()

# Before the loop, load the sounds:
#checkPoint_sound = pygame.mixer.Sound('checkPoint.wav')

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics.
background_image = pygame.image.load("rpsbg.png").convert()
rpssign_image = SpriteSheet("rpssign.png")

class play_rps(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rockImg = rpssign_image.get_image(5, 10, 120, 130)
        self.paperImg = rpssign_image.get_image(130, 10, 120, 130)
        self.scissorsImg = rpssign_image.get_image(255, 10, 120, 130)
        self.rockSelect = rpssign_image.get_image(5, 145, 50, 50)
        self.paperSelect = rpssign_image.get_image(60, 145, 50, 50)
        self.scissorsSelect = rpssign_image.get_image(115, 145, 50, 50)
        self.wonTXT = rpssign_image.get_image(165, 145, 120, 25)
        self.equalTXT = rpssign_image.get_image(285, 145, 120, 25)
        self.lostTXT = rpssign_image.get_image(165, 170, 120, 25)

        self.netlockImg = rpssign_image.get_image(380, 10, 120, 130)
        self.wait4pactImg = rpssign_image.get_image(505, 10, 120, 130)
        self.wait4playerImg = rpssign_image.get_image(410, 145, 185, 90)
        self.readyImg = rpssign_image.get_image(285, 170, 120, 25)

        self.continuePlaying = True
        self.result_listImg =[self.rockImg,self.paperImg,self.scissorsImg]
        self.result_listTXT =[self.wonTXT,self.lostTXT,self.equalTXT]
        self.netstat_listImg =[self.wait4playerImg,self.readyImg,self.netlockImg,self.wait4pactImg]

    def pressX(self):
        #print(self.continuePlaying)
        self.playerChosenImg = self.rockSelect
        if game_mode == "easy":
           self.gameshell_chosen("rock")
        elif game_mode == "network":
           n.send("Rock")
        return 210,30
        pass

    def pressA(self):
        #print(self.continuePlaying)
        self.playerChosenImg = self.paperSelect
        if game_mode == "easy":
           self.gameshell_chosen("paper")
        elif game_mode == "network":
           n.send("paper")
        return 215,85
        #pass

    def pressB(self):
        #print(self.continuePlaying)
        self.playerChosenImg = self.scissorsSelect
        if game_mode == "easy":
           self.gameshell_chosen("scissors")
        elif game_mode == "network":
           n.send("Scissors")
        return 208,140
        #

    def gameshell_chosen(self,key):
        rps_list = ["rock","paper","scissors"]
        rps_num = {"rock": 0,"paper": 1,"scissors": 2}
        #if game_mode == "easy":
        gs_choice = random.choice(rps_list)
        #print(gs_choice)
        keyn = rps_num[key]
        gs_choicen = rps_num[gs_choice]
        self.resultImg = self.result_listImg[gs_choicen]
        result = gscheckWin(keyn, gs_choicen)
        self.result_listTXT =[self.wonTXT,self.lostTXT,self.equalTXT]
        self.resultTXT = self.result_listTXT[result]

    def client(self,game, player):
        p = player
        if not(game.connected()):
            print("Waiting for Player...")
            self.netstatus = self.netstat_listImg[0]
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        #self.netstatus = self.netstat_listImg[1]
        if game.bothWent():
            text1 = move1
            text2 = move2
        else:
            if game.p1Went and p == 0:
                text1 = move1
            elif game.p1Went:
                text1 = "Locked In"
                self.netstatus = self.netstat_listImg[2]
            else:
                text1 = "Waiting..."
                self.netstatus = self.netstat_listImg[3]

            if game.p2Went and p == 1:
                text2 = move2
            elif game.p2Went:
                text2 = "Locked In"
                self.netstatus = self.netstat_listImg[2]
            else:
                text2 = "Waiting..."
                self.netstatus = self.netstat_listImg[3]
        if p == 1:
            print(text2)
            print(text1)
        else:
            print(text1)
            print(text2)
        #pass


    def getgame(self):
        try:
            game = n.send("get")
        except:
            #run = False
            print("Couldn't get game")
            #break

        if game.bothWent():
            self.client(game, player)
            #redrawWindow(win, game, player)
            try:
                game = n.send("reset")
            except:
                #run = False
                print("Couldn't get game")
                #break

            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                #text = font.render("You Won!", 1, (255,0,0))
                text = "You Won!"
                self.result_listTXT[0]
            elif game.winner() == -1:
                #text = font.render("Tie Game!", 1, (255,0,0))
                text = "Tie Game!"
                self.result_listTXT[2]
            else:
                #text = font.render("You Lost...", 1, (255, 0, 0))
                text = "You Lost..."
                self.result_listTXT[1]
            print(text)

            #pygame.time.delay(2000)
        self.client(game, player)


    def update(self):
        print(clock)
        pass


play_rps = play_rps()
BootScreen = BootScreen(screen)

BootScreen.main()
done = False
while not done:
    if game_mode == "network":
       play_rps.getgame()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == pygame.K_u and play_rps.continuePlaying:
                 play_rps.continuePlaying = False
                 x = play_rps.pressX()
            if event.key == pygame.K_j and play_rps.continuePlaying:
                 play_rps.continuePlaying = False
                 x = play_rps.pressA()
            if event.key == pygame.K_k and play_rps.continuePlaying:
                 play_rps.continuePlaying = False
                 x = play_rps.pressB()
            if event.key == pygame.K_i:
                 play_rps.continuePlaying = True



    screen.blit(background_image, background_position)

    time = pygame.time.get_ticks()/1000
    if play_rps.continuePlaying and game_mode == "easy":
       if (time%2) == 0:
          screen.blit(play_rps.paperImg, (35,20))
       elif (time%3) == 0:
          screen.blit(play_rps.rockImg, (35,20))
       else:
          screen.blit(play_rps.scissorsImg, (35,20))
    elif not play_rps.continuePlaying and game_mode == "easy":
      #if game_mode == "easy":
       screen.blit(play_rps.playerChosenImg, x)
       screen.blit(play_rps.resultImg, (35,20))
       screen.blit(play_rps.resultTXT, (35,160))
    elif play_rps.continuePlaying and game_mode == "network":
       screen.blit(play_rps.netstatus, (25,50))
    elif not play_rps.continuePlaying and game_mode == "network":
       screen.blit(play_rps.netstatus, (25,50))
       screen.blit(play_rps.playerChosenImg, x)

    pygame.display.flip()
    clock.tick(30)


pygame.quit()
