#!/usr/bin/env python
#
# MySTG 0.0.0
# stg.py
# https://github.com/magnuskronnas/MySTG
#
# Copyright 2012,2013 Dennis Sarafiloski
# Licensed under GPL Version 2 licenses.
#
# Date: 2013-01-13
#

from Engine.stg import *
from Engine.enemies import *

class GoodGuy(Player) :
    speedX = 10
    speedY = 5
    imageNames = ['playership1_idle1_edited.png', 'playership1_idle2_edited.png'];
    frameDuration=[5,5]

    def shoot(self):
        TestShot((self.rect.centerx, self.rect.centery))

    def impact(self,item) :
        self.game.GameExplosion(self)
        self.kill()

class BadGuy(WalkLeftRightFoe) :
    speedX = 10
    speedY = 1
    imageNames = [ 'eye_edited.png']
    frameDuration=[5]

    def do(self) :
        if(random.random()>0.99 ) :
            TestBomb(self)


class TestShot(Shot) :
    speedX = 0
    speedY = -10
    imageNames = ['bullet1_edited.png']


class TestBomb(Bomb) :
    speedX = 0
    speedY = 10
    imageNames = ['LittelBlackCirkel.png']

    def impact(self,item) :
        TestExplosion(self)
        self.kill()
        self.game.Score+=1

class TestExplosion(Explosion):
    duration = 10
    imageNames=['YellowCirkel.png'];
    frameDuration=[8]

class HellGame(MyGame) :
    Enemyreload = 0
    NextEnemyTime=12
    MaxShots     = 3
    WindowsCornerX = 0
    WindowsCornerY = 0
    WindowsHigh = 720
    WindowsWidth = 1280
    GameExplosion=TestExplosion

    def createPlayer(self):
        return GoodGuy();

    def createEnemy(self):
        if self.Enemyreload:
            self.Enemyreload = self.Enemyreload - 1
        else :
             BadGuy(0,0)
             self.Enemyreload = self.NextEnemyTime