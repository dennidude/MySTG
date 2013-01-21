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

from Hellflames.Hellcode import *

def main(winstyle = 0):
    this_game = HellGame("Hellflames")
    MySprite.game=this_game
    this_game.setup(winstyle)

if __name__ == '__main__': main()