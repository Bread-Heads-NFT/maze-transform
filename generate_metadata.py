#!/usr/bin/env python3

import json
from pathlib import Path
from copy import deepcopy
from PIL import Image
import random

METADATA_TEMPLATE = open("metadata_template.json").read()
MAZES = ["Bagel", "Crossed", "Focaccia", "Sourdough"]
PLAYERS = ["Bread", "Captain Grainbeard", "El Pan Degenerar", "Noot", "Chicken", "Monke", "Reject"]

count = 0

files = list(Path("bread").glob("*.json"))
random.shuffle(files)
index = 0
for file in files:
    print(file)
    print("metadata/" + str(index) + ".json")
    size = file.name.replace("maze_", "").split("_")[0]
    # print(size)
    f = open("metadata/" + str(index) + ".json", 'w')
    maze = random.choice(MAZES)
    player = random.choice(PLAYERS)
    metadata = deepcopy(METADATA_TEMPLATE)
    soln_file = open('bread/' + file.name.replace(".json", ".soln.txt"))
    soln = soln_file.read()
    soln_file.close()
    metadata = metadata.replace("000000", str(count))
    metadata = metadata.replace("###MAZE###", maze)
    metadata = metadata.replace("###PLAYER###", player)
    metadata = metadata.replace("###SIZE###", size)
    metadata = metadata.replace("###MAP###", open(file).read())
    metadata = metadata.replace("###SOLUTION###", soln)
    count += 1
    # print(metadata)
    f.write(metadata)

    image_file = file.name.replace(".json", ".png")
    base = Image.open("bread/" + image_file).convert("RGBA").resize((500, 500), Image.Resampling.BOX)
    if player == "Bread":
        player_layer = Image.open("Bread.png").convert("RGBA").resize((base.width, base.height), Image.Resampling.BOX)
        base.paste(player_layer, (0, 0), player_layer)
    elif player == "Captain Grainbeard":
        player_layer = Image.open("CaptainGrainbeard.png").convert("RGBA").resize((base.width, base.height), Image.Resampling.BOX)
        base.paste(player_layer, (0, 0), player_layer)
    elif player == "El Pan Degenerar":
        player_layer = Image.open("ElPanDegenerar.png").convert("RGBA").resize((base.width, base.height), Image.Resampling.BOX)
        base.paste(player_layer, (0, 0), player_layer)
    elif player == "Noot":
        player_layer = Image.open("Noot.png").convert("RGBA").resize((base.width, base.height), Image.Resampling.BOX)
        base.paste(player_layer, (0, 0), player_layer)
    elif player == "Chicken":
        player_layer = Image.open("Chicken.png").convert("RGBA").resize((base.width, base.height), Image.Resampling.BOX)
        base.paste(player_layer, (0, 0), player_layer)
    elif player == "Monke":
        player_layer = Image.open("Monke.png").convert("RGBA").resize((base.width, base.height), Image.Resampling.BOX)
        base.paste(player_layer, (0, 0), player_layer)
    elif player == "Reject":
        player_layer = Image.open("Reject.png").convert("RGBA").resize((base.width, base.height), Image.Resampling.BOX)
        base.paste(player_layer, (0, 0), player_layer)
    base.save("metadata/" + str(index) + ".png")
    index += 1