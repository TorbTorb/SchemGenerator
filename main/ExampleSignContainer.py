
from SchemGenerator import *
import time

# generates a colletion of containers with some signal strangth from 0 to 15 in order
# signs above tell the signal strength
def main():
    file = Schematic()
    print("Placing blocks...")
    timestartfill = time.perf_counter()

    for i in range(16):
        file.setSSContainer("barrel[facing=up]" , (i,-1,0), i)
        file.setSSContainer("white_shulker_box[facing=north]", (i, -2, 0), i)
        file.setSSContainer("composter", (i, -3, 0), i)
        file.setSSContainer("dropper", (i, -4, 0), i)
        file.setSign((i, 0, 0), str(i))

    timeendfill = time.perf_counter()
    print("Generating and saving...")
    timestartsaving = time.perf_counter()
    file.save("Schematics/ssTest.schem")
    timedone = time.perf_counter()

    print(f"Making took {round(timeendfill - timestartfill, 5)}s")
    print(f"Saving took {round(timedone -  timestartsaving, 5)}s")

if __name__ == "__main__":
    main()