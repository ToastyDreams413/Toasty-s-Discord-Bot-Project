# creating weapons

from Classes.Weapon import Weapon as Weapon

# name, type, dmg, att, defense, wis, hp, mp, speed, luck, perk

def createWeapon(name):

  if name == "None":
    return Weapon("None", "sword", 0, 0, 0, 0, 0, 0, 0, 0, None)
    
  if name == "Starter Sword":
    return Weapon("Starter Sword", "sword", 5, 0, 0, 0, 0, 0, 0, 0, None)

  if name == "Starter Wand":
    return Weapon("Starter Wand", "wand", 2, 0, 0, 0, 0, 0, 0, 0, None)

  if name == "Rusty Sword":
    return Weapon("Rusty Sword", "sword", 7, 0, 0, 0, 0, 0, 0, 0, None)
  
  if name == "Toasty's Sword":
    return Weapon("Toasty's Sword", "sword", 999999, 0, 0, 0, 0, 0, 0, 0, None)