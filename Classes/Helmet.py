from Classes.Ability import Ability as Ability

# Helmet class, child of the Ability class

class Helmet(Ability):
  def __init__(self, name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, groupBuff, bersAmount, bersTurns, perk):
    super().__init__(name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk)
    self.groupBuff = groupBuff
    self.bersAmount = bersAmount
    self.bersTurns = bersTurns