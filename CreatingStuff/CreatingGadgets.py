# creating Gadgets

from Classes.Gadget import Gadget as Gadget

def createGadget(name):
  
  if name == "None":
    return Gadget("None", "gadget", 0, 0, 0, 0, 0, 0, 0, None)