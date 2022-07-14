from Classes.Ability import Ability as Ability

# Spell class, child of the Ability class

class Spell(Ability):
  def __init__(self, name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk):
    super().__init__(name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk)