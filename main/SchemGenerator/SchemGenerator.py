from math import ceil, floor
from nbt.nbt import *

#schematic generator by Torb
#this tool allows you to easily create and modify schematics without having to worry about all the nbttags and whatnot
#you must use a atleast python 3.9.0 for this tool to work
#if you want it to work on a lower version you need to remove the type hints (more specifically the tuple[] hint)
class Schematic:
    def __init__(self):
        #pallete is a dictionary where the key is the blocktype and value is the id
        self._palette:dict[str, int] = {"air":0}
        #blocks is a dictionary where the key is the position and the value is the id of the block in the palette {(x, y, z): id}
        #containers are stored in there too. but like {(x, y, z): (id, ss)}
        #signs are stored there too. but like {(x, y, z): (id, text, color, isGlowing)}
        self._blocks:dict[tuple[int, int, int], int | tuple[int, int] | tuple[int, str, str, bool]] = {}

    def __str__(self):
        return self._generateSchematic().pretty_tree()

    def _getminmaxcoords(self):
        #gets the minimum and maximum coords for creating the schem
        #quite expensive method but the using append seems to be the fastest
        if len(self._blocks) == 0: return 0, 0, 0, 0, 0, 0  #stupid check if the user tries to save/print empty schematic
        keyx = []
        keyy = []
        keyz = []
        for key in self._blocks.keys():
            keyx.append(key[0])
            keyy.append(key[1])
            keyz.append(key[2])
        return (min(keyx), min(keyy), min(keyz), max(keyx), max(keyy), max(keyz))

    def _generateSchematic(self):
        #generates the schematic
        if len(self._palette) > 256:
            raise Exception("Too many different blocks you dumdum")
        #i couldnt find any documentation on how schematics handle palettes with over 256 blocks so i just throw an error :/
        #get the min and max coords
        xmin, ymin, zmin, xmax, ymax, zmax = self._getminmaxcoords()
        height = ymax - ymin + 1
        length = zmax - zmin + 1
        width = xmax - xmin + 1
        #create NBT file
        nbtfile = NBTFile()
        nbtfile.name = "Schematic"

        #create metadata (WE offsets)
        nbtfile.tags.append(TAG_Compound(name = "Metadata"))
        nbtfile["Metadata"].tags.extend([
        TAG_Int(name = "WEOffsetX", value = xmin),    #xmin 
        TAG_Int(name = "WEOffsetY", value = ymin),    #ymin
        TAG_Int(name = "WEOffsetZ", value = zmin)])   #zmin

        #create palette
        nbtfile.tags.append(TAG_Compound(name = "Palette"))
        for palettesingle in self._palette.items():
            nbtfile["Palette"].tags.append(TAG_Int(name = f"minecraft:{palettesingle[0]}", value = palettesingle[1]))

        #create BlockEntityList
        nbtfile.tags.append(TAG_List(name = "BlockEntities", type = TAG_Compound))

        #Create other and BlockDataArray
        nbtfile.tags.extend([TAG_Int(name = "DataVersion", value = 2730),
        TAG_Short(name = "Height", value = height),
        TAG_Short(name = "Length", value = length),
        TAG_Short(name = "Width", value = width),
        TAG_Int(name = "PaletteMax", value = len(self._palette)),
        TAG_Int(name = "Version", value = 2),
        TAG_Byte_Array(name = "BlockData")])

        #invert the palette {id: block} should be faster than looking through the palette for each container
        invertedpalette = {}
        for i in self._palette.items():
            invertedpalette[i[1]] = i[0]
        #create actual Blockdata
        blockdata = [self._palette.get("air", 0)] * (width*length*height)
        for block in self._blocks.items():
            if type(block[1]) == int:   #its a normal block
                blockdata[((block[0][1] - ymin) * length + block[0][2] - zmin) * width + block[0][0] - xmin] = block[1]

            elif type(block[1][1]) == int:    #its a container
                blockdata[((block[0][1] - ymin) * length + block[0][2] - zmin) * width + block[0][0] - xmin] = block[1][0]
                #get container type
                container = invertedpalette.get(block[1][0])
                if container == None:    #this executes if the block has NOT been found in the palette. 
                    raise Exception(f"Could not find{block} in the palette")    #i dont think this can happen but wont hurt adding it
                #get amount of slots and whether to use dust or totems
                if container[:5] == "chest" or container[:6] == "barrel" or "shulker_box" in container:
                    slots = 27
                    mult = 1
                    easy = True
                elif container[:6] == "hopper":
                    slots = 5
                    mult = 64
                    easy = False
                elif "furnace" in container or container[:6] == "smoker":
                    slots = 3
                    mult = 64
                    easy = False
                elif container[:7] == "dropper" or container[:9] == "dispenser":
                    slots = 9
                    mult = 64
                    easy = False
                else:
                    raise Exception("Container of type " + container + " is not supported / valid")
                #calc items for ss
                itemamount = max(block[1][1],ceil(slots*mult/14*(block[1][1]-1)))
                #block entity template
                nbtfile["BlockEntities"].tags.append(TAG_Compound())
                nbtfile["BlockEntities"][-1].tags.extend([
                    TAG_List(name = "Items", type = TAG_Compound),
                    TAG_String(name = "CustomName", value = str(block[1][1])),
                    TAG_String(name = "Id", value = "minecraft:" + container),
                    TAG_Int_Array(name = "Pos")])
                nbtfile["BlockEntities"][-1]["Pos"].value = [block[0][0] - xmin, block[0][1] - ymin, block[0][2] - zmin]
                if easy:
                    nbtfile["BlockEntities"][-1]["Items"].tags.append(TAG_Compound())
                    nbtfile["BlockEntities"][-1]["Items"][0].tags.extend([
                        TAG_Byte(name="Count", value = itemamount),
                        TAG_String(name="id", value = "minecraft:totem_of_undying"),
                        TAG_Byte(name="Slot", value = 0)])
                else:
                    for i in range((itemamount//64) + 1):
                        nbtfile["BlockEntities"][-1]["Items"].tags.append(TAG_Compound())
                        nbtfile["BlockEntities"][-1]["Items"][-1].tags.extend([
                            TAG_Byte(name="Count", value = min(itemamount, 64)),
                            TAG_String(name="id", value = "minecraft:redstone"),
                            TAG_Byte(name="Slot", value = i)])
                        itemamount = itemamount - 64

            elif type(block[1][1]) == str:  #its a sign
                blockdata[((block[0][1] - ymin) * length + block[0][2] - zmin) * width + block[0][0] - xmin] = block[1][0]
                nbtfile["BlockEntities"].tags.append(TAG_Compound())
                nbtfile["BlockEntities"][-1].tags.extend([
                    TAG_String(name = "Color", value = block[1][2]),
                    TAG_Byte(name = "GlowingText", value = block[1][3] * 1),
                    TAG_String(name = "Id", value = "minecraft:sign"),
                    TAG_Int_Array(name = "Pos")])
                nbtfile["BlockEntities"][-1]["Pos"].value = [block[0][0] - xmin, block[0][1] - ymin, block[0][2] - zmin]
                text = block[1][1].split("\n")
                text.extend(["","",""])
                for i in range(4):
                    nbtfile["BlockEntities"][-1].tags.append(TAG_String(name = f"Text{i+1}", value = '{"text":"' + text[i]+ '"}'))

        nbtfile["BlockData"].value = blockdata
        return nbtfile

    def _sortposition(self, pos1:tuple[int,int,int], pos2:tuple[int,int,int]):
        #sorts the positions so that pos1 has all the smaller coords ((5,5,5), (1,5,10) would be converted to (1,5,5), (5,5,10))
        #due to cubic selection there are no problems
        #this needs to happen so the for loops function correctly
        pos1 = list(pos1)
        pos2 = list(pos2)
        for i in range(3):
            if pos1[i] > pos2[i]:   #swap
                pos1[i], pos2[i] = pos2[i], pos1[i]
        return tuple(pos1), tuple(pos2)

    def _addtopalette(self, blocktype:str):
        #check to see if block is in the palette, if it isnt add it
        id = self._palette.get(blocktype)
        if id == None:  #block doesnt exist in palette yet
            self._palette[blocktype] = len(self._palette)

    def getBlock(self, pos:tuple[int, int, int]) -> str | None:
        "Returns the current block at some position. Returns None if that block hasnt been set. If the block is a sign/container then it will return (<blocktype>, (<other information like ss or text))"
        id = self._blocks.get(pos, None)
        if type(id) == tuple:   #container/sign
            for blocktype in self._palette.items():
                if blocktype[1] == id[0]:
                    return blocktype[0], id[1:]
        else:
            for blocktype in self._palette.items():
                if blocktype[1] == id:
                    return blocktype[0]
        return None

    def setBlock(self, pos:tuple[int, int, int], blocktype:str) -> None:
        "Sets a block at the specified position. You can add additional data like: stone_slab[type=top]"
        # add the block to _blocks
        blocktype = blocktype.removeprefix("minecraft:")
        self._addtopalette(blocktype)
        #place the block
        self._blocks[pos] = self._palette.get(blocktype)

    def setSSContainer(self, pos:tuple[int, int, int], containertype:str,  ss:int = 0) -> None:
        "Sets a container with a specified ss at some positon. Additional data can be give like barrel[facing=up]. Working containers are: barrels, chests, hoppers, composters, droppers, dispensers, all types of furnaces and shulker boxes."
        containertype = containertype.removeprefix("minecraft:")
        if  type(ss) != int or ss>15 or ss<0:   #invalid ss detection
            raise Exception(f"Given signal strength of '{ss}' is invalid")
        if containertype == "composter":        #special case for composter since its not a blockentity but a normal block instead
            containertype = f"composter[level={ss%9}]"
            self._addtopalette(containertype)
            self._blocks[pos] = self._palette.get(containertype)
            return
        self._addtopalette(containertype)
        self._blocks[pos] = (self._palette.get(containertype), ss)

    def setSign(self, pos:tuple[int, int, int], text:str = "", rotation:int = 0, iswall = False, woodtype:str = "birch", color = "black", isGlowing = False):
        "Places a sign. Rotation 0 is text facing north increasing the number will rotate is clockwise. Seperate text with newlines."
        facinglist = ["north", "east", "south", "west"]
        if iswall:
            woodtype = f"{woodtype}_wall_sign[facing={facinglist[rotation % 4]}]"
        else:
            woodtype = f"{woodtype}_sign[rotation={((rotation + 8) % 16)}]"
        self._addtopalette(woodtype)
        self._blocks[pos] = (self._palette[woodtype], text, color, isGlowing)

    def fill(self, blocktype:str, pos1:tuple[int, int, int], pos2:tuple[int, int, int]) -> None:
        "Fills the space between the 2 position with a cube with the given block"
        blocktype = blocktype.removeprefix("minecraft:")
        self._addtopalette(blocktype)
        id = self._palette.get(blocktype)

        pos1, pos2 = self._sortposition(pos1, pos2)
        for x in range(pos1[0], pos2[0]+1):
            for y in range(pos1[1], pos2[1]+1):
                for z in range(pos1[2], pos2[2]+1):
                    self._blocks[(x, y, z)] = id

    def stack(self, vector:tuple[int, int, int], amount:int = 1,  pos1:tuple[int, int, int] = None, pos2:tuple[int, int, int] = None) -> None:
        #idk if ill ever implement this method
        #because it seems kinda useless when you can just do a for loop yourself
        pass

    def move(self, vector:tuple[int, int, int] = (0,0,0), moveair = True, pos1:tuple[int, int, int] = None, pos2:tuple[int, int, int] = None) -> None:
        "Moves the blocks inside the selection by the vector. If no positions are given then the whole schematic will be moved."
        if vector == (0,0,0):
            return
        if pos1 == None or pos2 == None:   #move all. we nees to use a temporary dict here because we could otherwise overwrite blocks
            blocksnew = {}
            for i in self._blocks.items():
                blocksnew[(i[0][0] + vector[0], i[0][1] + vector[1], i[0][2] + vector[2])] = i[1]
            self._blocks = blocksnew
            return
        #move only some area
        #first thing: make copy of area we want to move and clear it
        copyarea = {}
        pos1, pos2 = self._sortposition(pos1, pos2)
        for x in range(pos1[0], pos2[0]+1):
            for y in range(pos1[1], pos2[1]+1):
                for z in range(pos1[2], pos2[2]+1):
                    id = self._blocks.get((x,y,z), None)
                    if id != None:
                        copyarea[x, y, z] = id
                        self._blocks.pop((x, y, z))

        #second thing: clear area we want to move to (but only if we move air too)
        if moveair:
            pos1v = (pos1[0] + vector[0], pos1[1] + vector[1], pos1[2] + vector[2])
            pos2v = (pos2[0] + vector[0], pos2[1] + vector[1], pos2[2] + vector[2])
            for x in range(pos1v[0], pos2v[0]+1):
                for y in range(pos1v[1], pos2v[1]+1):
                    for z in range(pos1v[2], pos2v[2]+1):
                        if self._blocks.get((x, y, z)) != None:     #couldnt find a faster way to do it
                            self._block.pop((x, y, z))

        #paste the copied blocks into the new area
        for i in copyarea.items():
            self._blocks[(i[0][0] + vector[0], i[0][1] + vector[1], i[0][2] + vector[2])] = i[1]

    def replace(self, old:str, new:str, pos1:tuple[int, int, int] = None, pos2:tuple[int, int, int] = None) -> None:
        "Replaces the old blocks with new block in the selection. If no positions are given it will replace all instances of the old block with the new one"
        #replace all (we can just change the palette)
        old = old.removeprefix("minecraft:")
        new = new.removeprefix("minecraft:")
        if (pos1 == None or pos2 == None) and old != "air":
            oldid = self._palette.pop(old, None)
            if oldid == None: return
            self._palette[new] = oldid
            return
        #replace in one area
        elif pos1 == None or pos2 == None:  #replace air only in whole area (very special case)
            positions = self._getminmaxcoords()
            pos1 = (positions[0], positions[1], positions[2])
            pos2 = (positions[3], positions[4], positions[5])
        self._addtopalette(new)
        pos1, pos2 = self._sortposition(pos1, pos2)
        oldid = self._palette.get(old)
        newid = self._palette.get(new)
        if old == "air" or old == "minecraft:air":  #special case if old = air
            default = oldid
        else:
            default = False     #not None so that if old would be a block not in the palette it wouldnt break
        for x in range(pos1[0], pos2[0]+1):
            for y in range(pos1[1], pos2[1]+1):
                for z in range(pos1[2], pos2[2]+1):
                    id = self._blocks.get((x, y, z), default)
                    if type(id) == tuple:   #container
                        id = id[0]
                    if id == oldid:
                        self._blocks[(x, y, z)] = newid

    def open(self, directory:str = None) -> None:
        "Opens an existing schematic which you can then modify. Deletes the schematic you were creating currently!"
        file = NBTFile(directory, "rb")
        if len(file["Palette"]) > 256:
            raise Exception("Too many different blocks in the palette you dumdum")
            #i couldnt find any documentation on how schematics handle palettes with over 256 blocks so i just throw an error :/
        #print(file.pretty_tree())
        self._palette = {}
        self._blocks = {}

        #copy palette
        for i in file["Palette"].items():
            self._palette[i[0].removeprefix("minecraft:")] = i[1].value

        #get offsets
        Metadata = file.get("Metadata")
        OffsetX = Metadata.get("WEOffsetX", 0).value
        OffsetY = Metadata.get("WEOffsetY", 0).value
        OffsetZ = Metadata.get("WEOffsetZ", 0).value

        #get dimensions
        Width = file["Width"].value
        Height = file["Height"].value
        Length = file["Length"].value

        #getting the blocks
        for x in range(Width):
            for y in range(Height):
                for z in range(Length):
                    self._blocks[(x + OffsetX, y + OffsetY, z + OffsetZ)] = file["BlockData"][(y*Length + z)*Width + x]

        #reading block entities (not fun)
        #dict for looking up the max stack size of items
        #anyone wanting to expand this dict is very welcome to do so :)
        maxStack = {"minecraft:heart_of_the_sea": 64,
        "minecraft:redstone": 64,
        "minecraft:redstone_block": 64,
        "minecraft:glass": 64,
        "minecraft:snowball": 16,
        "minecraft:totem_of_undying": 1}
        #go through the blockentity list
        for i in range(len(file["BlockEntities"])):
            block = file["BlockEntities"][i]["Id"].value.removeprefix("minecraft:")
            pos = list(file["BlockEntities"][i]["Pos"].value)
            pos[0] += OffsetX
            pos[1] += OffsetY
            pos[2] += OffsetZ
            pos = tuple(pos)
            #check if its type is container (in our self defined way of storing) or sign
            if "sign" in block:
                text = ""
                for j in range(4):
                    line = file["BlockEntities"][i][f"Text{j+1}"].value.removeprefix('{"text":"').removesuffix('"}')
                    text += f"{line}\n"
                color = file["BlockEntities"][i]["Color"].value
                glowing = bool(file["BlockEntities"][i]["GlowingText"].value)
                self._blocks[pos] = (self._blocks[pos], text, color, glowing)
                continue
            if block == "chest" or block == "barrel" or "shulker_box" in block:
                slots = 27
            elif block == "hopper":
                slots = 5
            elif "furnace" in block or block == "smoker":
                slots = 3
            elif block == "dropper" or block == "dispenser":
                slots = 9
            else: continue     #just skip whatever that might be lol (comparators have an entry in the block entity list)(we just ignnore them lol)
            #this means you will have to update them once you paste the schematic but i couldnt be bothered to add it
            fullness = 0
            for j in range(len(file["BlockEntities"][i].get("Items", []))):     #go trough each slot and count the items
                fullness += file["BlockEntities"][i]["Items"][j]["Count"].value / maxStack.get(file["BlockEntities"][i]["Items"][j]["id"].value, 64)    #default to 64 id the item cant be found
            signalStrength = floor(1 + ((fullness) / (slots)) * 14)
            self._blocks[pos] = (self._blocks[pos], signalStrength)

    def save(self, location:str) -> None:
        "Saves the schematic at the specified location. e.g. C:/some/path/to/schem.schem"
        self._generateSchematic().write_file(location)