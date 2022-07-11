# creating armors

from Classes.Armor import Armor as Armor

# name, type, att, defense, wis, hp, mp, speed, luck, perk

def createArmor(name):

  if name == "None":
    return Armor("None", "armor", 0, 0, 0, 0, 0, 0, 0, None)

  if name == "Rusty Heavy Armor":
    return Armor("Rusty Heavy Armor", "heavy armor", 0, 5, 0, 0, 0, 0, 0, None)

  if name == "Toasty's Heavy Armor":
    return Armor("Toasty's Heavy Armor", "heavy armor", 0, 25000, 5000, 50000, 50000, 0, 0, None)