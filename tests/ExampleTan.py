
from math import tan
import time
from SchemGenerator.SchemGenerator import *

def main():
    # this generates a schematic of tan(x^2 + y^2) <= some threshold#
    # https://youtu.be/IbYZ027zBlM?t=340
    print("Placing blocks...")
    timestartfill = time.perf_counter()
    schematic = Schematic()

    #you can play with these
    exponent = 3
    size = 254
    zoom = 10
    threshold = 0.5
    ########

    for pixely in range(size):
        for pixelx in range(size):
            result = abs(tan((((pixelx/size*zoom) - zoom/2)**exponent)+(((pixely/size*zoom) - zoom/2))**exponent))
            if result <= threshold: block = "light_gray_concrete"
            else: block = "gray_concrete"
            schematic.setBlock((pixelx, -1, pixely), block)

    timeendfill = time.perf_counter()
    print("Generating and saving...")
    timestartsaving = time.perf_counter()
    schematic.save("main/Schematics/tanTest.schem")
    timedone = time.perf_counter()
    print(f"Making took {round(timeendfill - timestartfill, 5)}s")
    print(f"Saving took {round(timedone -  timestartsaving, 5)}s")

if __name__ == '__main__':
    main()

