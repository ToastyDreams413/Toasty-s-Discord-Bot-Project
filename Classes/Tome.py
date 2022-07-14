from Classes.Ability import Ability as Ability

# Tome class, child of the Ability class

class Tome(Ability):
  def __init__(self, name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, groupHeal, healAmount, perk):
    super().__init__(name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk)
    self.groupHeal = groupHeal
    self.healAmount = healAmount