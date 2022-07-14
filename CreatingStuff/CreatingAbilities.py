# creating abilities

from Classes.Ability import Ability as Ability
from Classes.Helmet import Helmet as Helmet
from Classes.Spell import Spell as Spell
from Classes.Shield import Shield as Shield
from Classes.Tome import Tome as Tome

# ABILITY: name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk

# HELMET: name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, groupBuff, bersAmount, bersTurns, perk

# SPELL: name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk

# SHIELD: name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, stunTurns, perk

# TOME: name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, groupHeal, healAmount, perk

def createAbility(name):

  if name == "None":
    return Ability("None", "ability", 0, 0, 0, 0, 0, 0, 0, 0, 0, None)

  if name == "Starter Helmet":
    return Helmet("Starter Helmet", "helmet", 0, 0, 2, 0, 0, 0, 0, 0, 50, False, 2, 1, None)

  if name == "Starter Spell":
    return Spell("Starter Spell", "spell", 3, 1, 0, 1, 0, 5, 0, 0, 25, None)

  if name == "Starter Shield":
    return Shield("Starter Shield", "shield", 0, 0, 2, 0, 0, 0, 0, 0, 50, 1, None)

  if name == "Starter Tome":
    return Tome("Starter Tome", "tome", 0, 0, 0, 1, 5, 5, 0, 0, 25, False, 10, None)
    
  if name == "Rusty Helmet":
    return Helmet("Rusty Helmet", "helmet", 0, 0, 3, 0, 0, 0, 0, 0, 60, True, 2, 1, None)

  if name == "Toasty's Helmet":
    return Helmet("Toasty's Helmet", "helmet", 0, 5000, 5000, 0, 100000, 100000, 0, 0, 100, True, 100, 10, None)