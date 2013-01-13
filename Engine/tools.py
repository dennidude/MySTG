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

import os.path
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, '..\Test\Image', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    surface.set_colorkey((255,255,255))
    return surface.convert()

def load_images(files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs