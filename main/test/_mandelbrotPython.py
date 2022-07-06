from math import  floor
from SchemGenerator import *
cr = 50
ci = 33
maxiterations = 20
blocks = ["black_concrete", "white_concrete"]
schem = Schematic()
def byteconv(number):
    return(floor(number*32)/32)
def mandeldraw(x,y):
    scaling = 32
    global cr, ci
    r = i = 0
    crn = cr / scaling
    cin = ci / scaling
    for e in range(maxiterations):
        r2 = byteconv(r*r)
        i2 = byteconv(i*i)
        ri = byteconv(2*r*i)
        if r2 >= 4 or i2 >= 4 or abs(ri) >= 4:
            return 1
        i = byteconv(ri - cin)
        r = byteconv(r2 - i2 - crn)
    return 0
def main():
    global cr,ci
    for y in range(33):
        ci -= 1
        cr = 50
        for x in range(64):
            cr -= 1
            color = mandeldraw(x, y)
            schem.setBlock(blocks[color], (x, -1, y))
            schem.setBlock(blocks[color], (x, -1, 64-y))
    schem.save("C:/Users/torbe/Documents/mandel.txt")
if __name__ == "__main__":
    main()