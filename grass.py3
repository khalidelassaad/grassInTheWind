import curses
from math import e
from time import sleep
import random

# y, x, height all range from 0 to 1 and are fractions of the screen dimensions
# elast ranges from 0 to 1, where 0 is rigid and 1 is completely blown over
# wind is from -1 to 1
# bend = |wind| * elast
# graph will be x = sign(wind) * (e^(bend*y)-1)

def sign(x):
    if x == 0:
        return 0
    return int(x/abs(x))

class Grass:
    def __init__(self, y, x, height, elast, string):
        self.y = y
        self.x = x
        self.height = height
        self.elast = elast
        self.string = string
        self.color = curses.color_pair(1)

    def draw(self, stdscr,  wind):
        MAX_Y, MAX_X = stdscr.getmaxyx()
        MAX_Y -= 1
        MAX_X -= 1
        curr_y = self.y*MAX_Y
        curr_x = self.x*MAX_X
        bend = abs(wind)*self.elast
        old_x = int(curr_x)
        max_count = int(self.height*MAX_Y)
        count = 0
        for h in range(int(self.height*MAX_Y)):
            if count >= max_count:
                break
            addlist=[]
            x = sign(wind)*(e**(bend*h)-1)*0.5
            int_x = int(curr_x-x)
            int_y = int(curr_y-h)
            if int_x < 0 or int_x >= MAX_X or int_y < 0 or int_y >= MAX_Y: #Don't draw off screen
                break
            if abs(int_x-old_x)>1: #Fill in gaps
                gap = int_x - old_x 
                segments = list(range(1,abs(gap)))
                segments.reverse()
                for i in segments:
                    addlist.append((int_y,old_x+(abs(gap)-i)*sign(gap)))
                    count += 1
                    if count >= max_count:
                        break
            if count < max_count:
                addlist.append((int_y,int_x))
                count += 1
            old_x = int_x
            for coords in addlist: 
                stdscr.addstr(coords[0], coords[1], self.string, self.color)

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_GREEN)
    curses.curs_set(False)
    blades = []
    for x in range(24):
        y = (1-random.random()*0.4) 
        x = random.random()
        h = random.random()*0.1 + 0.2
        e = 1 + (random.random()-0.5)*0.1
        blades.append(Grass(y, x, h, 1, "||"))
    #blades.append(Grass(1, 0.4, 0.3 , 1, "X"))
    wind = 0
    while True:
        stdscr.clear()
        for blade in blades:
            blade.draw(stdscr, wind+(random.random()-0.5)*0.4)
        stdscr.refresh()
        sleep(0.05)
        wind +=(random.random()-0.5)*0.05
    stdscr.getkey()

curses.wrapper(main)
