#! /usr/bin/env python

import pygame, math
from pygame.locals import *
from pygame import gfxdraw


import gtk, sys

# Change number for change colors (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

class PlanetsGame():
    def __init__(self):
        self.planets = []


    def run(self):
        velScale = 1    #Velocity scale
        FPS = 60
        dt = 1.0/FPS

        pygame.init()
        fpsClock = pygame.time.Clock()
        #self.window = 
        surface = pygame.display.get_surface()

        info = pygame.display.Info()
        WIDTH = info.current_w
        HEIGHT = info.current_h

        selectedPlanet = -1

        font = pygame.font.SysFont(None, 20)
        text = font.render('Press "h" for help', True, (255,255,255))
        textRect = text.get_rect()
        textRect.left = 0
        textRect.bottom = HEIGHT

        helpString = """ 
        HELP:
        Click and hold anywhere on the screen to create a planet.
        Click again to give speed to that planet, speed depends on the distance between
        the planet and the second click. Try placing a big planet with no speed and a smaller
        one with speed some distance from the first one, watch how they orbit!

        KEY SHORTCUTS:
        h - Open this menu
        c - Center view on planet
        s - Show selected planet
        d - Delete selected planet
        r - Delete all planets

        With a planet selected, you can create a second one and in the second click, instead of
        using the left mouse button, use the right mouse button to give it speed relative to the
        selected planet. This is useful if you want to make a planet orbit another one in motion."""

        planetGrowing = False;
        planetEditing = -1
        G = 10

        showSelPlanet = False
        showHelp = False

        print (dt)

        while True: # main game loop
            while gtk.events_pending():
                gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit("Game end")

                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    info = pygame.display.Info()
                    WIDTH = info.current_w
                    HEIGHT = info.current_h

                elif event.type == MOUSEBUTTONDOWN:
                    if planetGrowing == False and planetEditing == -1:   #Ready to draw new planet
                        newPlanet = {'center': (event.pos[0],event.pos[1]), 'radius': 2.0, 'density': 1, 'velx': 0.0, 'vely': 0.0, 'traces': []}
                        self.planets.append(newPlanet)
                        planetEditing = self.planets.index(newPlanet)
                        planetGrowing = True

                elif event.type == MOUSEBUTTONUP:
                    if planetGrowing == True:   #Planet finished growing, now waiting for click to give it speed
                        planetGrowing = False

                    else:   #Click to give speed and direction
                        planet = self.planets[planetEditing]
                        dX, dY = planet['center']
                        dX, dY = event.pos[0] - dX, event.pos[1] - dY
                        planet['velx'] = dX*velScale
                        planet['vely'] = dY*velScale
                        if event.button == 3 and planetEditing != selectedPlanet:   #Right click, make vel relative to selected planet
                            planet['velx'] += self.planets[selectedPlanet]['velx']
                            planet['vely'] += self.planets[selectedPlanet]['vely']

                        print ('velX' + str(planet['velx']))
                        planetEditing = -1   #Next click draws new planet

                elif event.type == KEYDOWN:
                    if event.key == ord('r'):
                        self.planets = []
                        planetGrowing = False
                        selectedPlanet = -1
                        planetEditing = -1

                    elif event.key == ord('c'):  #Center screen on one planet
                        selectedPlanet += 1
                        if selectedPlanet >= len(self.planets):
                            selectedPlanet = 0

                        if len(self.planets) > 0:
                            x, y = self.planets[selectedPlanet]['center']
                            self.planets[selectedPlanet]['center'] = WIDTH/2,HEIGHT/2
                            dX, dY = self.planets[selectedPlanet]['center'][0] - x, self.planets[selectedPlanet]['center'][1] - y
                            for planet in self.planets:
                                i = self.planets.index(planet)
                                if i != selectedPlanet:
                                    planet['center'] = planet['center'][0] + dX, planet['center'][1] + dY
                                for i in range(len(planet['traces'])):
                                    planet['traces'][i] = planet['traces'][i][0] + dX, planet['traces'][i][1] + dY

                    elif event.key == ord('s'):  #Show selected planet
                        if showSelPlanet == True:
                            showSelPlanet = False
                        else:
                            showSelPlanet = True

                    elif event.key == ord('d'):  #Show selected planet
                        if showSelPlanet == True and selectedPlanet != -1:
                            self.planets.pop(selectedPlanet)
                            planetEditing = -1
                            planetGrowing = False
                            selectedPlanet = -1

                    elif event.key == ord('h'):
                        helpShowing = True
                        
                        helpLines = helpString.split("\n")
                        helpHeight = len(helpLines) * 20
                        startx, starty = WIDTH/2, HEIGHT/2 - helpHeight/2

                        for line in helpLines:
                            textLine = font.render(line, True, (255,255,255),(0,0,0))
                            textLineRect = textLine.get_rect()
                            textLineRect.midtop = (startx,starty)
                            starty += 20
                            surface.blit(textLine, textLineRect)

                        pygame.display.update()

                        while helpShowing:
                            while gtk.events_pending():
                                gtk.main_iteration()
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    exit("Game end")

                                elif event.type == pygame.VIDEORESIZE:
                                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                                    info = pygame.display.Info()
                                    WIDTH = info.current_w
                                    HEIGHT = info.current_h

                                elif event.type == KEYDOWN:
                                    if event.key == ord('h'):
                                        helpShowing = False
                         


            if planetGrowing == True:
                planet = self.planets[planetEditing]
                planet['radius'] += 1.01**planet['radius']
                if planet['radius'] > 200:
                    planet['radius'] = 2.0

            if planetEditing == -1:
                for planet0 in self.planets:   #Calc forces for each pair, calc accel from forces, calc speed from accel
                    forceX = 0.0
                    forceY = 0.0
                    mass0 =  planet0['radius']**3*math.pi*(3/4.0)*planet0['density']
                    for planet1 in self.planets:
                        if planet0 != planet1:
                            mass1 =  planet1['radius']**3*math.pi*(3/4.0)*planet1['density']
                            distX, distY = planet1['center'][0] - planet0['center'][0], planet1['center'][1] - planet0['center'][1]
                            dist = math.sqrt(distX**2 + distY**2)
                            if dist > 5:
                                force = (G * mass0 * mass1)/dist**2
                                forceX += force * (distX/dist)
                                forceY += force * (distY/dist)

                    planet0['velx'] += forceX/mass0 * dt
                    planet0['vely'] += forceY/mass0 * dt

            surface.fill((0,0,0))

            for planet in self.planets:   #Calc new position for each planet
                if planetEditing == -1:
                    x,y = planet['center']
                    planet['center'] = (x+planet['velx']*dt, y+planet['vely']*dt)
                    planet['traces'].append((planet['center'][0], planet['center'][1]))
                    if len(planet['traces']) > 150:
                        planet['traces'] = planet['traces'][1:]

                if planet['center'][0] > 10000 or planet['center'][0] < -10000 or planet['center'][1] > 10000 or planet['center'][1] < -10000:
                    self.planets.pop(self.planets.index(planet))
                    planetEditing = -1
                    planetGrowing = False
                    selectedPlanet = -1
                    continue

                traces = planet['traces']
                for i in range(len(traces)):
                    if i != 0:
                        intensity = 255*i/len(traces)
                        planetColor = (intensity,intensity,intensity)
                        if self.planets.index(planet) == selectedPlanet and showSelPlanet == True:
                            planetColor = (0,intensity,0)
                        pygame.draw.aaline(surface,planetColor,traces[i], traces[i-1])

            for planet in self.planets:
                planetColor = (255,255,255)
                if self.planets.index(planet) == selectedPlanet and showSelPlanet == True:
                    planetColor = (128,255,128)

                #pygame.draw.circle(surface, (255,255,255), (int(planet['center'][0]), int(planet['center'][1])), planet['radius'])
                pygame.gfxdraw.aacircle(surface, int(planet['center'][0]), int(planet['center'][1]), int(planet['radius']), planetColor)

            for planet in self.planets:
                planetColor = (255,255,255)
                if self.planets.index(planet) == selectedPlanet and showSelPlanet == True:
                    planetColor = (128,255,128)

                pygame.gfxdraw.filled_circle(surface, int(planet['center'][0]), int(planet['center'][1]), int(planet['radius']), planetColor)

            surface.blit(text, textRect)

            pygame.display.update()
            fpsClock.tick(FPS)

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass   #TO-DO: Save to journal

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass


if __name__ == "__main__":
    PlanetsGame()
