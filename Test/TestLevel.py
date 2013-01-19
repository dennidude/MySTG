#!/usr/bin/env python
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

from Engine.stg import *
from Engine.enemies import *

class GoodGuy(Player) :
    speedX = 10
    speedY = 0
    imageNames = ['RedCirkel.png'];

    def shoot(self):
        TestShot((self.rect.centerx, self.rect.centery))

    def impact(self,item) :
        Explosion(self)
        self.kill()

class BadGuy(WalkLeftRightFoe) :
    speedX = 10
    speedY = 1
    imageNames = [ 'BlueCirkel.png', 'BlueCirkel1.png', 'BlueCirkel2.png']

    def do(self) :
        if(random.random()>0.99 ) :
            TestBomb(self)


class TestShot(Shot) :
    speedX = 0
    speedY = -10
    imageNames = ['LittelYellowCirkel.png']

class TestBomb(Bomb) :
    speedX = 0
    speedY = 10
    imageNames = ['LittelBlackCirkel.png']

    def impact(self,item) :
        Explosion(self)
        self.kill()
        self.game.Score+=1

class TestLevel(MyGame) :
    Enemyreload = 0
    NextEnemyTime=12
    MaxShots     = 5
    WindowsCornerX = 0
    WindowsCornerY = 0
    WindowsHigh = 480
    WindowsWidth = 680

    def createPlayer(self):
        return GoodGuy();

    def createEnemy(self):
        if self.Enemyreload:
            self.Enemyreload = self.Enemyreload - 1
        else :
             BadGuy(0,0)
             self.Enemyreload = self.NextEnemyTime