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
import random


class WalkLeftRightFoe(Foe) :
    speedX = 10
    speedY = 1
    imageNames = [ 'BlueCirkel.png', 'BlueCirkel1.png', 'BlueCirkel2.png']

    def move(self,x,y) :
        Foe.move(self,x,y)

        if not (self.game.ScreenRect.left < self.rect.centerx and self.rect.centerx < self.game.ScreenRect.right) :
            self.speedX=-self.speedX

        if self.rect.centery > self.game.ScreenRect.bottom :
            self.impact(None)

    def impact(self,item) :
        Explosion(self)
        self.kill
        self.game.Score+=5