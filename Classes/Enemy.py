import TextStuff.EnemyText as EnemyText

# Enemy class
class Enemy:
  def __init__(self, name, att, defense, hp, maxHp, mp, maxMp, speed):
    self.name = name
    self.att = att
    self.defense = defense
    self.hp = hp
    self.maxHp = maxHp
    self.mp = mp
    self.maxMp = maxMp
    self.speed = speed
    self.description = ""

  def getEnemyStats(self):
    curString = "**" + self.name + "**\n"
    curString += "\nAttack: " + str(self.att)
    curString += "\nDefense: " + str(self.defense)
    curString += "\nHP: " + str(self.hp) + "/" + str(self.maxHp)
    curString += "\nSpeed: " + str(self.speed)
    curString += "\n\n" + EnemyText.enemyDescriptions[self.name]
    return curString