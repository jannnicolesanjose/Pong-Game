#PONG GAME
#GROUP 3

import pygame
from pygame import Rect
import tkinter
from pygame.locals import *
from pygame import mixer
from tkinter import*
from PIL import ImageTk, Image

pygame.init()

screen_width = 600
screen_height = 500


fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

#START-UP WINDOW
window=Tk()	
window.title('Menu')
window.geometry("1050x600")
window.wm_attributes('-transparentcolor', 'purple')


#BACKGROUND IMAGE
image = ImageTk.PhotoImage(file="Background.png")
canvas = Canvas(window, width=10, height=1000)
canvas.pack(expand=True, fill=BOTH)
canvas.create_image(0, 0, image=image, anchor=NW)


#RESIZE BACKGROUND IMAGE
def resize_image(e):
   global image, resized, image2
   image = Image.open("C:\\Users\\sanjose\\Desktop\\pong game\\Background.png")
   resized = image.resize((e.width, e.height))
   image2 = ImageTk.PhotoImage(resized)
   canvas.create_image(0, 0, image=image2, anchor='nw')


#OPEN THE GAME DIRECTLY FROM START BUTTON
def open(filename):
    import os
    import sys
    os.chdir("C:\\Users\\sanjose\\Desktop\\pong game\\Official pong game.py") #CHANGE THIS PATH TO YOUR PATH WHERE YOUR f1.py AND f2.py IS LOCATED
    #PRINT("current dir "+os.getcwd())
    os.system('pong game '+"Official pong game.py") #RUNNING THE PYTHON COMMAND ON CMD TO EXECUTE BOTH WINDOW

#START BUTTON
    
btn = Button(text="Start",
                font=("Courier",14),
                height=1,
                width=10,
                bg='#7f73e7',
                fg="white",
		command=lambda: open("Official pong game.py"))

btn.pack()
btn.place(x=250, y=430)


#DEFINE FONT
font = pygame.font.SysFont('Constantia', 30)


#DEFINE GAME VARIABLES
margin = 50
cpu_score = 0
player_score = 0
fps = 60
live_ball = False
winner = 0
speed_increase = 0


#DEFINE COLOURS
bg = (50, 25, 50)
white = (255, 255, 255)

#BACKGROUND MUSIC
mixer.music.load('bg music.wav') #CHANGE TO YOUR PREFERRED BG MUSIC
mixer.music.play(-1)


def draw_board():
        screen.fill(bg)
        pygame.draw.line(screen, white, (0, margin), (screen_width, margin), 2)



def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


class paddle():
        def __init__(self, x, y):
                self.x = x
                self.y = y
                self.rect = pygame.Rect(x, y, 20, 100)
                self.speed = 5
                self.ai_speed = 5

        def move(self):
                key = pygame.key.get_pressed()
                if key[pygame.K_UP] and self.rect.top > margin:
                        self.rect.move_ip(0, -1 * self.speed)
                if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
                        self.rect.move_ip(0, self.speed)

        def draw(self):
                pygame.draw.rect(screen, white, self.rect)

        def ai(self):
                #AI TO MOVE THE PADDLE AUTOMATICALLY
                #MOVE DOWN
                if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
                        self.rect.move_ip(0, self.ai_speed)
                #MOVE UP
                if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
                        self.rect.move_ip(0, -1 * self.ai_speed)


class ball(pygame.sprite.Sprite):
        def __init__(self, x, y):
                self.reset(x, y)


        def move(self):

                #CHECK COLLISION WITH TOP MARGIN
                if self.rect.top < margin:
                        self.speed_y *= -1
                        #TOP COLLISION SFX
                        topcollisionsound = mixer.Sound('collisionsfx.wav')
                        topcollisionsound.play()
                #CHECK COLLISION WITH BOTTOM OF THE SCREEN
                if self.rect.bottom > screen_height:
                        self.speed_y *= -1
                        #BOTTOM COLLISION SFX
                        botcollisionsound = mixer.Sound('collisionsfx.wav')
                        botcollisionsound.play()
                if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
                        self.speed_x *= -1
                        #SOUND EFFECT WHEN HIT
                        bounce_sound = mixer.Sound('pingpongsfx.wav')
                        bounce_sound.play()

                #CHECK FOR OUT OF BOUNDS
                if self.rect.left < 0:
                        self.winner = 1
                if self.rect.left > screen_width:
                        self.winner = -1

                #UPDATE BALL POSITION
                self.rect.x += self.speed_x
                self.rect.y += self.speed_y

                return self.winner


        def draw(self):
                pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)


        def reset(self, x, y):
                self.x = x
                self.y = y
                self.ball_rad = 8
                self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
                self.speed_x = -4
                self.speed_y = 4
                self.winner = 0# 1 IS THE PLAYER AND -1 IS THE CPU


#CREATE PADDLES
player_paddle = paddle(screen_width - 40, screen_height // 2)
cpu_paddle = paddle(20, screen_height // 2)

#CREATE PONG BALL
pong = ball(screen_width - 60, screen_height // 2 + 50)


#BACKGROUND
bg = pygame.image.load('space.png')


#CREATE GAME LOOP
run = True
while run:

        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        fpsClock.tick(fps)


        draw_text('CPU: ' + str(cpu_score), font, white, 20, 15)
        draw_text('P1: ' + str(player_score), font, white, screen_width - 100, 15)
        draw_text('BALL SPEED: ' + str(abs(pong.speed_x)), font, white, screen_width // 2 - 100 , 15)


        #DRAW PADDLES
        player_paddle.draw()
        cpu_paddle.draw()

        if live_ball == True:
                speed_increase += 1
                winner = pong.move()
                if winner == 0:
                        #DRAW BALL
                        pong.draw()
                        #MOVE PADDLES
                        player_paddle.move()
                        cpu_paddle.ai()
                else:
                        live_ball = False
                        if winner == 1:
                                player_score += 1
                                sfx = mixer.Sound('scoresfx.wav')
                                sfx.play()
                        elif winner == -1:
                                sfx = mixer.Sound('scoresfx.wav')
                                sfx.play()
                                cpu_score += 1


        #PRINT PLAYER INSTRUCTIONS
        if live_ball == False:
                if winner == 0:
                        draw_text("PRESS 'SPACE' TO CONTINUE", font, white, 100, screen_height // 2 -100)
                if winner == 1:
                        draw_text("PRESS 'SPACE' TO CONTINUE", font, white, 100, screen_height // 2 -50)
                if winner == -1:
                        draw_text("PRESS 'SPACE' TO CONTINUE", font, white, 100, screen_height // 2 -50)
                if player_score == 5:
                        draw_text('YOU WON!', font, white, 220, screen_height // 2 -100)
                        draw_text("PRESS 'SPACE' TO CONTINUE", font, white, 100, screen_height // 2 -50)
                        draw_text("PRESS 'ESC' TO EXIT", font, white, 150, screen_height // 2)
                if cpu_score == 5:
                        draw_text('CPU WON!', font, white, 220, screen_height // 2 -100)
                        draw_text("PRESS 'SPACE' TO CONTINUE", font, white, 100, screen_height // 2 -50)
                        draw_text("PRESS 'ESC' TO EXIT", font, white, 150, screen_height // 2)
                

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                if event.type == pygame.KEYDOWN and live_ball == False:
                        if event.key == pygame.K_SPACE:
                                #SFX AT START
                                sfx = mixer.Sound('startsfx.wav')
                                sfx.play()
                                live_ball = True
                                pong.reset(screen_width - 60, screen_height // 2 + 50)
                #RESTART WHEN SCORE OF 5 IS REACHED
                if event.type == pygame.KEYDOWN and cpu_score == 5 or player_score == 5:
                        if event.key == pygame.K_SPACE:
                                cpu_score = 0
                                player_score = 0
                                live_ball = False
                                pong.reset(screen_width - 60, screen_height // 2 + 50)
                #QUIT WHEN SCORE OF 5 IS REACHED
                if event.type == pygame.KEYDOWN and cpu_score == 5 or player_score == 5:
                        if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                        

        if speed_increase > 500:
                speed_increase = 0
                if pong.speed_x < 0:
                        pong.speed_x -= 1
                if pong.speed_x > 0:
                        pong.speed_x += 1
                if pong.speed_y < 0:
                        pong.speed_y -= 1
                if pong.speed_y > 0:
                        pong.speed_y += 1


        pygame.display.update()

pygame.quit()
