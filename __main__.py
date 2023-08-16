#!/usr/bin/env python3
import pygame, sys
from math import *
from pygame.locals import *
from TIDEntity.Unit import Unit
from TIDEntity.MouseCursor import MouseCursor
from TIDEntity.Ownship import Ownship
from TIDEntity.DataDisplay import DataDisplay
from TIDEntity.Waypoint import Waypoint
from TIDEntity.Util import *
from pynput.mouse import Controller
wgs84 = nv.FrameE(name='WGS84')
SCALE = 100
pygame.init()
pygame.mouse.set_visible(False) 

mouse = Controller()
t = pygame.time.Clock()
font = pygame.font.SysFont('Courier New', 14, True, False)
pygame.display.set_caption('Hello World!')
DISPLAYSURF = pygame.display.set_mode(
    (400, 400),  flags=(pygame.FULLSCREEN|pygame.SCALED)
)

FPS = 120

OWNSHIP = Ownship({
    "lat": 45.00472, "lon": 37.34778, "alt": 25_000.0, "hdg": 90.0, "spd": 250.0
})

TRACK_FILES = pygame.sprite.Group()
TRACK_FILES.add(Unit({
    "lat": 45.53778, "lon": 39.18806, "alt": 18_000, "hdg": 0, "spd": 125
}))

TRACK_FILES.add(Unit({
    "lat": 44.53778, "lon": 38.18806, "alt": 45_000, "hdg": 180,"spd": 250,
    "dolly_track": { "IFF": "HST" } 
}))
TRACK_FILES.add(Unit({
    "lat": 45.03778, "lon": 39.18806, "alt": 27_000, "hdg": 270, "spd": 250,
    "dolly_track": { "visible": True, "IFF": "HST"}
}))

ALL_SPRITES = TRACK_FILES.copy()
ALL_SPRITES.add(OWNSHIP)

BLACK = pygame.Surface([400,400])
BLACK.fill((0,0,0,0))
cur = MouseCursor()
dd1 = DataDisplay((20, 190), context=OWNSHIP, datum="Hlim", format="%01.0f")
dd2 = DataDisplay((20, 200), context=OWNSHIP, datum="EL_TOTAL")
dd3 = DataDisplay((20, 210), context=OWNSHIP, datum="Llim", format="%01.0f")
ALL_SPRITES.add([cur, dd1, dd2, dd3])
SELECTED = None

while True:
    for track in TRACK_FILES.sprites():
        track.selected = False
        if track == SELECTED:
            sprite.selected = True
    OWNSHIP.update()
    TRACK_FILES.update(OWNSHIP)
    dd1.update()
    dd2.update()
    dd3.update()
    
    ALL_SPRITES.clear(DISPLAYSURF, BLACK)
    ALL_SPRITES.draw(DISPLAYSURF)
     
    for i in Waypoint.WP1.value:
        pygame.draw.__dict__[i["func"]](DISPLAYSURF, (0, 255, 0), **i["params"])

    if pygame.mouse.get_pressed()[0]:
        cur.update(pygame.mouse.get_pos())
    else:
        cur.update((-50, -50))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            if event.button == 3:
                for sprite in pygame.sprite.spritecollide(cur, TRACK_FILES, False, pygame.sprite.collide_circle):
                    SELECTED = sprite
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse.position = (-1920+960, 1080 + 540)
                
        elif event.type == MOUSEWHEEL:
            pressed = pygame.key.get_pressed()
            if pressed[K_LCTRL]:
                adjustment = [-0.1, 0.1][event.y > 0] 
                if -4 < OWNSHIP.EL_VERNIER + adjustment < 4:
                    OWNSHIP.EL_VERNIER += adjustment 
            else:
                if event.y != 0:
                    adjustment = [-1, 1][event.y > 0]
                    if AZ_CONTROL_MIN < OWNSHIP.AZ_CTR + (adjustment * OWNSHIP.AZ_SCAN) + adjustment < AZ_CONTROL_MAX:
                        OWNSHIP.AZ_CTR += [-1, 1][event.y > 0] * 1
                if event.x != 0:
                    adjustment = [-1, 1][event.x > 0]
                    if EL_CONTROL_MIN < OWNSHIP.EL_CTR + adjustment < EL_CONTROL_MAX:
                        OWNSHIP.EL_CTR += adjustment
        elif event.type == KEYDOWN:
            if event.key in [K_DOWN, K_UP]:
                OWNSHIP.AZ_SCAN_INDEX += [[-1, 0][OWNSHIP.AZ_SCAN_INDEX == 0], [1, 0][OWNSHIP.AZ_SCAN_INDEX == 3]][event.key == K_UP]
            if event.key in [K_LEFT, K_RIGHT]:
                OWNSHIP.EL_BARS_INDEX += [[-1, 0][OWNSHIP.EL_BARS_INDEX == 0], [1, 0][OWNSHIP.EL_BARS_INDEX == 3]][event.key == K_RIGHT]
 
    pygame.display.update()
    t.tick(FPS)
