#!/usr/bin/env python
#
# MySTG 0.0.0
# stg.py
# https://github.com/magnuskronnas/MySTG
#
# Copyright 2012,2013 Magnus Kronnas
# Licensed under GPL Version 2 licenses.
#
# Date: 2013-01-13
#

import random, os.path

import pygame
from pygame.locals import *
from Engine.tools import *


class MySprite(pygame.sprite.Sprite):
    game = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

class ActionSprite(MySprite):
    speedX = 10
    speedY = 10
    images = []
    imageNames=[]

    def __init__(self):
        MySprite.__init__(self)
        self.images=load_images(self.game.GameName,self.imageNames)
        self.image = self.images[0]

    def impact(self):
        pass

class Animate():
    frameDuration=[]

    def __init__(self):
        self.frame = 0
        self.timeToNextFrame = 0

    def update(self):
        self.timeToNextFrame += 1
        if not self.timeToNextFrame < self.frameDuration[self.frame] :
            self.image = self.images[self.frame]
            self.frame += 1
            self.timeToNextFrame = 0
        if not self.frame < len(self.images)-1 :
                self.frame = 0

class Player(ActionSprite):

    def __init__(self):
        ActionSprite.__init__(self)
        self.rect = self.image.get_rect(midbottom=self.game.ScreenRect.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(direction*self.speedX, 0)
        self.rect = self.rect.clamp(self.game.ScreenRect)

    def shoot(self):
        pass


class Foe(ActionSprite,Animate):

    def __init__(self,x,y):
        ActionSprite.__init__(self)
        Animate.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.left = y

    def move(self,x,y):
        self.rect.move_ip(x,y)

    def update(self):
        self.move(self.speedX, self.speedY)
        Animate.update(self)

    def do(self) :
        pass


class Shot(ActionSprite):
    imageNames = ['bullet1_edited']

    def __init__(self, pos):
        ActionSprite.__init__(self)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speedX=-self.speedX

    def update(self):
        self.rect.move_ip(self.speedX, self.speedY)
        if self.rect.top <= 0:
            self.kill()


class Bomb(ActionSprite):
    imageNames = []

    def __init__(self, Shooter):
        ActionSprite.__init__(self)
        self.rect = self.image.get_rect(midbottom=
                    Shooter.rect.move(0,5).midbottom)

    def update(self):
        self.rect.move_ip(self.speedX, self.speedY)
        if self.rect.bottom >= 470:
            self.impact(None)


class Explosion(ActionSprite,Animate):
    duration = 2
    timeLeft=0
    imageName=[];
    images = []

    def __init__(self, actor):
        ActionSprite.__init__(self)
        Animate.__init__(self)
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.timeLeft = self.duration

    def update(self):
        Animate.update(self)
        self.timeLeft = self.timeLeft - 1
        if self.timeLeft <= 0: self.kill()

class Score(MySprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        if self.game.Score != self.lastscore:
            self.lastscore =  self.game.Score
            msg = "Score: %d" % self.game.Score
            self.image = self.font.render(msg, 0, self.color)

class MyGame() :
    Enemyreload = 0
    MaxShots     = 5
    LeftKey=K_a
    WindowsCornerX = 0
    WindowsCornerY = 0
    WindowsHigh = 100
    WindowsWidth = 100
    GameExplosion=None
    GameName=""
    Score = 0

    def __init__(self,gameName):
        self.GameName=gameName;
        self.ScreenRect     = Rect(self.WindowsCornerX,
                                   self.WindowsCornerY,
                                   self.WindowsWidth,
                                   self.WindowsHigh)

    def setup(self, winstyle = 0):

        # Initialize pygame
        pygame.init()
        if pygame.mixer and not pygame.mixer.get_init():
            print ('Warning, no sound')
            pygame.mixer = None

        # Set the display mode
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(self.ScreenRect.size, winstyle, 32)
        screen = pygame.display.set_mode(self.ScreenRect.size, winstyle, bestdepth)

        #decorate the game window
        pygame.display.set_caption('Pygame Enemys')
        pygame.mouse.set_visible(0)

        #create the background, tile the bgd image
        #  bgdtile = load_image('background.gif')
        background = pygame.Surface(self.ScreenRect.size)
        #   for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        #       background.blit(bgdtile, (x, 0))
        #   screen.blit(background, (0,0))
        #   pygame.display.flip()

        # Initialize Game Groups
        Enemys = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        bombs = pygame.sprite.Group()
        all = pygame.sprite.RenderUpdates()
        lastEnemy = pygame.sprite.GroupSingle()

        #assign default groups to each sprite class
        Player.containers = all
        Foe.containers = Enemys, all, lastEnemy
        Shot.containers = shots, all
        Bomb.containers = bombs, all
        Explosion.containers = all
        Score.containers = all

        #Create Some Starting Values
        global score

        kills = 0
        clock = pygame.time.Clock()

        #initialize our starting sprites
        global SCORE
        player = self.createPlayer()
        if pygame.font:
            all.add(Score())

        while player.alive():

            #get input
            for event in pygame.event.get():
             if event.type == QUIT or \
                 (event.type == KEYDOWN and event.key == K_ESCAPE):
                     return
            keystate = pygame.key.get_pressed()

            # clear/erase the last drawn sprites
            all.clear(screen, background)

            #update all the sprites
            all.update()

            #handle player input
            direction = keystate[K_RIGHT] - keystate[self.LeftKey]
            player.move(direction)
            firing = keystate[K_SPACE]
            if not player.reloading and firing and len(shots) < self.MaxShots:
                player.shoot()
            player.reloading = firing

            # Create new Enemy
            self.createEnemy();

            # Drop bombs
            for Enemy in pygame.sprite.Group(Enemys):
             Enemy.do();

            # Detect collisions
            for Enemy in pygame.sprite.spritecollide(player, Enemys, 1):
                Enemy.impact(player)
                player.impact(Enemy)

            collide_list = pygame.sprite.groupcollide(Enemys,shots, 1, 1)
            for Enemy in collide_list.keys():
                Enemy.impact(collide_list[Enemy])

            for bomb in pygame.sprite.spritecollide(player, bombs, 1):
                bomb.impact(player)
                player.impact(bomb)


            #draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)

            #cap the framerate
            clock.tick(10)

        pygame.time.wait(1000)
        pygame.quit()

