import Main.Data as Data
from Classes.Dungeon import Dungeon as Dungeon
from Classes.Item import Item as Item
from Classes.Weapon import Weapon as Weapon
from Classes.Armor import Armor as Armor
from Classes.Ability import Ability as Ability
import CreatingStuff.CreatingEnemies as CreatingEnemies

def createDungeon(dungeonName, party):

  curParty = []
  for member in party:
    curParty.append([member, Data.pOverview[member].name, Data.pOverview[member].selected])
  
  if dungeonName == "Chicken's Den":
    return Dungeon("Chicken's Den", [curParty[0][1], "move"], 1, [CreatingEnemies.miniChicken(), CreatingEnemies.miniChicken(), CreatingEnemies.motherHen()], curParty, 50, [Item("Eggs", "item")], [])