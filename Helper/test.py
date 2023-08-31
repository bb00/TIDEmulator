import pygame, os
from ALPHA_A import points as a
from ALPHA_R import points as r
alpha = {x.split('.')[0].split('_')[1]: __import__(x.split('.')[0]).points for x in os.listdir() if 'ALPHA' in x}
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,400))
while True:
    DISPLAYSURF.fill((0,0,0))
    [pygame.draw.lines(DISPLAYSURF, (0, 255, 0), False, [p+pygame.math.Vector2(200+i*25, 200) for p in alpha[x]]) for (i,x) in enumerate("THVMPR")]
    pygame.display.flip()
