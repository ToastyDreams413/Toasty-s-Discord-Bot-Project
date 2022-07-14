from Classes.Ability import Ability as Ability

# Shield class, child of the Ability class

class Shield(Ability):
  def __init__(self, name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, stunTurns, perk):
    super().__init__(name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk)
    self.stunTurns = sturnTurns