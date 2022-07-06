
from math import tan
import time
from SchemGenerator import *

def main():
    # this generates a schematic of tan(x^2 + y^2)#
    # https://youtu.be/IbYZ027zBlM?t=340
    print("Placing blocks...")
    timestartfill = time.perf_counter()
    schematic = Schematic()

    #play with these
    exponent = 2
    size = 254
    zoom = 50
    threshold = 0.5


    for pixely in range(size):
        for pixelx in range(size):
            result = abs(tan((((pixelx/size*zoom) - zoom/2)**exponent)+(((pixely/size*zoom) - zoom/2))**exponent))
            if result <= threshold: block = "light_gray_concrete"
            else: block = "gray_concrete"
            schematic.setBlock(block, (pixelx, -1, pixely))

    timeendfill = time.perf_counter()
    print("Generating and saving...")
    timestartsaving = time.perf_counter()
    schematic.save("Schematics/tanTest.schem")
    timedone = time.perf_counter()
    print(f"Making took {round(timeendfill - timestartfill, 5)}s")
    print(f"Saving took {round(timedone -  timestartsaving, 5)}s")

if __name__ == '__main__':
    main()

