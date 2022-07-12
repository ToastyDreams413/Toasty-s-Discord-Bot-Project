import Main.Data as Data
from Classes.Dungeon import Dungeon as Dungeon
from Classes.Item import Item as Item
from Classes.Weapon import Weapon as Weapon
from Classes.Armor import Armor as Armor
from Classes.Ability import Ability as Ability
import CreatingStuff.CreatingEnemies as CreatingEnemies
import CreatingStuff.CreatingWeapons as CreatingWeapons
import CreatingStuff.CreatingArmors as CreatingArmors
import CreatingStuff.CreatingAbilities as CreatingAbilities
import CreatingStuff.CreatingGadgets as CreatingGadgets
import CreatingStuff.CreatingItems as CreatingItems

# weapon:
# name, type, dmg, att, defense, wis, hp, mp, speed, luck, perk

# helmet:
# name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, groupBuff, bersAmount, bersTurns, perk

# armor:
# name, type, att, defense, wis, hp, mp, speed, luck, perk

# gadget:
# name, type, att, defense, wis, hp, mp, speed, luck, perk

# dungeon:
# dungeonName, move, moveNumber, enemies, players, xpOnComp, gLoot, rLoot

def createDungeon(dungeonName, party):

  curParty = []
  for member in party:
    curParty.append([member, Data.pOverview[member].name, Data.pOverview[member].selected])
  
  if dungeonName == "Chicken's Den":
    return Dungeon("Chicken's Den", [curParty[0][1], "move"], 1, [CreatingEnemies.createEnemy("Mini Chicken"), CreatingEnemies.createEnemy("Mini Chicken"), CreatingEnemies.createEnemy("Mother Hen")], curParty, 50, [CreatingItems.createItem("Eggs")], [])

  if dungeonName == "Thieves Hideout":
    return Dungeon("Thieves Hideout", [curParty[0][1], "move"], 1, [CreatingEnemies.createEnemy("Thief"), CreatingEnemies.createEnemy("Thief"), CreatingEnemies.createEnemy("Thief")], curParty, 100, [Item("Stone Chunk", "item")], [[CreatingWeapons.createWeapon("Rusty Sword"), 50], [CreatingArmors.createArmor("Rusty Heavy Armor"), 50], [CreatingAbilities.createAbility("Rusty Helmet"), 50]])