import Main.Data as Data
import Main.LevelUpBuffs as LevelUpBuffs
from Classes.Weapon import Weapon as Weapon
from Classes.Armor import Armor as Armor
from Classes.Ability import Ability as Ability
from Classes.Gadget import Gadget as Gadget
import CreatingStuff.CreatingWeapons as CreatingWeapons
import CreatingStuff.CreatingArmors as CreatingArmors
import CreatingStuff.CreatingAbilities as CreatingAbilities
import CreatingStuff.CreatingGadgets as CreatingGadgets

# Char class
class Char:
  def __init__(self, className, att, defense, hp, maxHp, wis, mp, maxMp, speed, luck, level, xp):
    self.className = className # the selected class
    self.att = att # attack
    self.defense = defense # defense
    self.hp = hp # health
    self.maxHp = maxHp # max health
    self.wis = wis # wisdom
    self.mp = mp # MP
    self.maxMp = maxMp # max MP
    self.speed = speed # speed
    self.luck = luck # luck
    self.level = level # level
    self.xp = xp # xp
    self.weapon = ""
    self.armor = ""
    self.ability = ""
    self.gadget = ""
    self.statusEffects = []
    
    if className == "warrior":
      self.weapon = CreatingWeapons.createWeapon("Starter Sword")
      self.armor = CreatingArmors.createArmor("None")
      self.ability = CreatingAbilities.createAbility("Starter Helmet")
      self.gadget = CreatingGadgets.createGadget("None")


  def getBasicInfo(self):
    return " [lvl " + str(self.level) + " " + self.className + "]:\n" + str(self.hp) + "/" + str(self.getTotalMaxHp()) + " HP\n" + str(self.mp) + "/" + str(self.getTotalMaxMp()) + " MP"

  def getStats(self):
    return "Class: " + str(self.className.title()) + "\n\nLevel: " + str(self.level) + "\n" + str(self.xp) + "/" + str(Data.xpToNextLevel[self.level - 1]) + " XP\n\nAttack: " + str(self.getTotalAtt()) + "\nDefense: " + str(self.getTotalDef()) + "\nWisdom: " + str(self.getTotalWis()) + "\nHP: " + str(self.hp) + "/" + str(self.getTotalMaxHp()) + "\nMP: " + str(self.mp) + "/" + str(self.getTotalMaxMp()) + "\nSpeed: " + str(self.getTotalSpeed()) + "\nLuck: " + str(self.getTotalLuck())

  def getEquipment(self):
    return "Weapon: " + self.weapon.name + "\nArmor: " + self.armor.name + "\nAbility: " + self.ability.name + "\nGadget: " + self.gadget.name

  def getTotalAtt(self):
    return self.att + self.weapon.att + self.armor.att + self.ability.att + self.gadget.att
  
  def getTotalDmg(self):
    baseDmg = self.weapon.dmg + self.getTotalAtt()
    for statusEffect in self.statusEffects:
      if statusEffect[0] == "berserk":
        baseDmg *= statusEffect[1]
        statusEffect[2] -= 1
    for statusEffect in self.statusEffects:
      if statusEffect[2] == 0:
        self.statusEffects.remove(statusEffect)
    return int(baseDmg)

  def getTotalDef(self):
    return self.defense + self.weapon.defense + self.armor.defense + self.ability.defense + self.gadget.defense

  def getTotalWis(self):
    return self.wis + self.weapon.wis + self.armor.wis + self.ability.wis + self.gadget.wis

  def getTotalMaxHp(self):
    return self.maxHp + self.weapon.hp + self.armor.hp + self.ability.hp + self.gadget.hp

  def getTotalMaxMp(self):
    return self.maxMp + self.weapon.mp + self.armor.mp + self.ability.mp + self.gadget.mp

  def getTotalSpeed(self):
    return self.speed + self.weapon.speed + self.armor.speed + self.ability.speed + self.gadget.speed

  def getTotalLuck(self):
    return self.luck + self.weapon.luck + self.armor.luck + self.ability.luck + self.gadget.luck

  def useAbility(self):
    self.mp -= self.ability.mpCost
    curString = ""
    if self.ability.type == "helmet":
      self.statusEffects.append(["berserk", self.ability.bersAmount, self.ability.bersTurns])
      curAdd = ""
      if self.ability.groupBuff:
        curAdd = "everyone's"
      else:
        curAdd = "your"
      curString += "You used your berserker ability, costing " + str(self.ability.mpCost) + " MP, and buffing " + curAdd + " base damage by " + str(self.ability.bersAmount) + "x for " + str(self.ability.bersTurns) + " turn"
      if self.ability.bersTurns > 1:
        curString += "s"
    return curString

  def resetStats(self):
    self.hp = self.getTotalMaxHp()
    self.mp = self.getTotalMaxMp()

  # hp, mp, att, def, wis, speed
  def levelUp(self):
    self.xp -= Data.xpToNextLevel[self.level - 1]
    curLevelUp = LevelUpBuffs.levelUpBuffs[self.className][self.level - 1]
    curString = "You leveled up to level " + str(self.level + 1) + "!\n\nYou gained +" + str(curLevelUp[0]) + " HP, +" + str(curLevelUp[1]) + " MP, +" + str(curLevelUp[2]) + " attack, +" + str(curLevelUp[3]) + " defense, and +" + str(curLevelUp[4]) + " wisdom."
    
    self.maxHp += curLevelUp[0]
    self.maxMp += curLevelUp[1]
    self.att += curLevelUp[2]
    self.defense += curLevelUp[3]
    self.wis += curLevelUp[4]
    self.speed += curLevelUp[5]
    self.level += 1
    self.resetStats()
    return curString