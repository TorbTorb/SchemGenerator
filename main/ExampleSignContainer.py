
import SchemGenerator.SchemGenerator as schem
import time

# generates a colletion of containers with some signal strangth from 0 to 15 in order
# signs above tell the signal strength
def main():
    file = schem.Schematic()
    print("Placing blocks...")
    timestartfill = time.perf_counter()

    for i in range(16):
        file.setSSContainer((i,-1,0), "barrel[facing=up]" , i)
        file.setSSContainer((i, -2, 0), "white_shulker_box[facing=north]", i)
        file.setSSContainer((i, -3, 0), "composter", i)
        file.setSSContainer((i, -4, 0), "dropper", i)
        file.setSign((i, 0, 0), str(i))

    timeendfill = time.perf_counter()
    print("Generating and saving...")
    timestartsaving = time.perf_counter()
    file.save("main/Schematics/ssTest.schem")
    timedone = time.perf_counter()

    print(f"Making took {round(timeendfill - timestartfill, 5)}s")
    print(f"Saving took {round(timedone -  timestartsaving, 5)}s")

if __name__ == "__main__":
    main()