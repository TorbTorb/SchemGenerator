
from SchemGenerator import *
import time

def main():
    file = Schematic()
    print("Placing blocks...")
    timestartfill = time.perf_counter()

    file.open("main/Schematics/testopen2.schem")
    file.replace("gray_concrete", "white_concrete")
    file.setBlock("obsidian", (1, -1, 0))

    timeendfill = time.perf_counter()
    print("Generating and saving...")
    timestartsaving = time.perf_counter()
    file.save("main/Schematics/openTestResult.schem")
    timedone = time.perf_counter()

    print(f"Making took {round(timeendfill - timestartfill, 5)}s")
    print(f"Saving took {round(timedone -  timestartsaving, 5)}s")

if __name__ == "__main__":
    main()