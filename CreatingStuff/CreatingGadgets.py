# creating Gadgets

from Classes.Gadget import Gadget as Gadget

# name, type, att, defense, wis, hp, mp, speed, luck, perk

def createGadget(name):
  
  if name == "None":
    return Gadget("None", "gadget", 0, 0, 0, 0, 0, 0, 0, None)

  if name == "Toasty's Amulet":
    return Gadget("Toasty's Amulet", "gadget", 5000, 5000, 5000, 100000, 100000, 0, 0, None)