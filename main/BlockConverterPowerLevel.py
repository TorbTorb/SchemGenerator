
import SchemGenerator.SchemGenerator as schem
import time

#replaces hardpowered blocks with different ones
#do not copy with redstone dust
def main():
    file = schem.Schematic()
    print("Placing blocks...")
    timestartfill = time.perf_counter()



    replace = {"gray_concrete":"orange_concrete",
    "white_concrete":"orange_concrete",
    "purple_concrete":"orange_concrete",
    "smooth_quartz":"orange_concrete"}

    file.open("main/Schematics/dataloop.schem")
    direction = {"north": (0, 0, 1), "east": (-1, 0, 0), "south": (0, 0, -1), "west": (1, 0, 0)}
    for pos in file._blocks.keys():
        block = file.getBlock(pos)
        if  "repeater" in block or "comparator" in block:
            #get the direction the rep is facing
            block = block.split("[")[1].removesuffix("]")
            blocklist = block.split(",")
            for i in blocklist:
                if i[:6] == "facing":
                    dir = direction[i[7:]]
                    break
            #offset position
            pos = *(pos[i] + dir[i] for i in range(3)), #tuple comprehension ig
            blocktoreplace = file.getBlock(pos)
            newblock = replace.get(blocktoreplace)
            if newblock != None:
                file.setBlock(pos, newblock)

        elif "redstone_wall_torch" in block or "redstone_torch" in block:
            pos = (pos[0], pos[1]+1, pos[2])
            blocktoreplace = file.getBlock(pos)
            newblock = replace.get(blocktoreplace)
            if newblock != None:
                file.setBlock(pos, newblock)
    timeendfill = time.perf_counter()
    print("Generating and saving...")
    timestartsaving = time.perf_counter()
    file.save("main/Schematics/dataloopConv.schem")
    timedone = time.perf_counter()

    print(f"Making took {round(timeendfill - timestartfill, 5)}s")
    print(f"Saving took {round(timedone -  timestartsaving, 5)}s")

if __name__ == "__main__":
    main()