import os
from tkinter import *
import pygame

def rightClick(event):
     lb.selection_clear(0,END)
     lb.delete(lb.nearest(event.y))
     lb.activate(lb.nearest(event.y))

def ExportVectors():
        with open("export.py","w") as f:
            f.write("import pygame\n")
            f.write("points = [\n")
            for i in range(lb.size()):
                r, phi = lb.get(i).replace('p(','').replace(')','').split(',')
                f.write(f"\tpygame.math.Vector2.from_polar(({r}, (270 + {phi}) % 360)),\n")
            f.write("]\n")

root = Tk()
root.geometry("+200+400")
pygame.init()
surf =  pygame.display.set_mode((400,400))
ORIGIN = pygame.math.Vector2((200,200))
def printInput():
    inp = coords.get(1.0, "end-1c")
    inp2 = coords2.get(1.0, "end-1c")
    lb.insert(END, f"p({inp},{inp2})")
f = Frame(root, height=75, width=200)

coords = Text(f,
                   height = 5,
                   width = 20)

coords.pack(side=LEFT)
coords2 = Text(f,
                    height=5,
                   width = 20)
coords2.pack(side=LEFT)
btn = Button(f,
                        text = "Print", 
                        command = printInput)
btn.pack(side=LEFT)
btn2 = Button(f,
                        text="Export",
                        command=ExportVectors)
btn2.pack(side=LEFT)
f.pack(side=BOTTOM)
def mag(deg):
    return (270 + deg) % 360
def p(a,b):
    return pygame.math.Vector2.from_polar((a,mag(b)))
lb = Listbox(root, width=75, height=200)
lb.insert(1, "p(10, 180)")
lb.insert(2, "p(150, 90)")
lb.bind('<Button-2>', rightClick)
lb.pack(side=BOTTOM)


while True:
    surf.fill((0,0,0))
    for i in range(lb.size()):
        if i == 0:
            pt1, pt2 = (eval(lb.get(i)), eval(lb.get(i+1)))
        else:
            pt1, pt2 = (eval(lb.get(i-1)), eval(lb.get(i)))
        print(pt1, pt2)
        print(type(pt1))
        pygame.draw.line(surf, (0,255,0), ORIGIN+pt1, ORIGIN+pt2)
        
    pygame.display.flip()
    root.update()
