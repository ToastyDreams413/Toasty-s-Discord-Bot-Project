# ability class
class Ability:
  def __init__(self, name, type, dmg, att, defense, wis, hp, mp, speed, luck, mpCost, perk):
    self.name = name
    self.type = type
    self.dmg = dmg
    self.att = att
    self.defense = defense
    self.wis = wis
    self.hp = hp
    self.mp = mp
    self.speed = speed
    self.luck = luck
    self.mpCost = mpCost
    self.perk = perk