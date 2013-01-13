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

class GoodGuy(Player) :
    speed=15
    imageNames = ['RedCirkel.png'];

    def shoot(self):
        TestShot((self.rect.centerx, self.rect.centery))

    def impact(self,item) :
        Explosion(self)
        self.kill()

class BadGuy(Foe) :
    speed=15
    imageNames = [ 'BlueCirkel.png', 'BlueCirkel1.png', 'BlueCirkel2.png']

    def do(self) :
        if(random.random()>0.99 ) :
            TestBomb(self)

    def impact(self,item) :
        Explosion(self)
        self.game.Score+=5

class TestShot(Shot) :
    imageNames = ['LittelYellowCirkel.png']

class TestBomb(Bomb) :
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
             BadGuy()
             self.Enemyreload = self.NextEnemyTime
