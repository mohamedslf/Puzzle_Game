##
## EPITECH PROJECT, 2021
## JAM
## File description:
## A puzzle game
##

# -*- coding: utf-8 -*-

import pygame, sys, os
from tkinter import filedialog
from tkinter import *
from random import shuffle

class SlidePuzzle:
    def __init__(self, gs, ts, ms):
        self.gs, self.ts, self.ms = gs, ts, ms
        self.tiles_len = (gs[0]*gs[1]) - 1
        self.tiles = [(x,y) for x in range(gs[0]) for y in range(gs[1])]
        self.tilesOG = [(x,y) for x in range(gs[0]) for y in range(gs[1])]
        self.tilespos = {(x,y):(x*(ts+ms)+ms,y*(ts+ms)+ms) for y in range(gs[1]) for x in range(gs[0])}
        self.font = pygame.font.Font(None, 120)
        w,h = gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms
        root = Tk()
        root.filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        pic = pygame.image.load(root.filename)
        pic = pygame.transform.scale(pic, (w,h))
        root.destroy()
        self.images = []
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            image = pic.subsurface(x,y,ts,ts)
            self.images += [image]
        self.temp = self.tiles[:-1]
        shuffle(self.temp)
        self.temp.insert(len(self.temp), self.tiles[-1])
        self.tiles = self.temp

    def getBlank(self):
        return self.tiles[-1]

    def setBlank(self, pos):
        self.tiles[-1] = pos

    opentile = property(getBlank, setBlank)
    def switch(self, tile):
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]
        if self.tiles == self.tilesOG:
            background_colour = (1,1,1)
            (width, height) = (800, 600)
            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption('Congratulations !!!')
            screen.fill(background_colour)
            my_image = pygame.image.load('assets/nyan.gif')
            screen.blit(my_image, (200, 100))
            pygame.display.flip()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
            print("COMPLETE")

    def is_grid(self, tile):
        return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1]

    def adjacent(self):
        x,y = self.opentile;
        return (x-1, y), (x+1,y), (x,y-1), (x,y+1)

    def update(self, dt):
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if mouse[0]:
            tile = mpos[0]//self.ts, mpos[1]//self.ts
            if self.is_grid(tile):
                if tile in self.adjacent():
                    self.switch(tile)

    def draw(self, screen):
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            screen.blit(self.images[i], (x,y))

def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Cover Puzzle")
    screen = pygame.display.set_mode((800,600))
    cool = pygame.font.Font("Fonts/robus.otf", 50)
    cool_txt = cool.render("COVER PUZ", True, (1,1,1))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle((3,3), 150, 5)
    while True:
        dt = fpsclock.tick()/1000
        screen.fill((255,255,0))
        screen.blit(cool_txt, (500, 50))
        program.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit();
        program.update(dt)

if __name__ == '__main__':
    main()
