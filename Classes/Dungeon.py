from random import randint
import Main.Data as Data

# move is in format of [IGN, "action"]
# players are in format [tag, IGN, class]

# Dungeon class
class Dungeon:
  def __init__(self, dungeonName, move, moveNumber, enemies, players, xpOnComp, gLoot, rLoot):
    self.dungeonName = dungeonName
    self.move = move
    self.moveNumber = moveNumber
    self.enemies = enemies
    self.players = players
    self.xpOnComp = xpOnComp
    self.gLoot = gLoot
    self.rLoot = rLoot

    self.enemiesNameList = []
    self.enemiesDict = {}
    enemyTempNameList = []
    for enemy in self.enemies:
      enemyTempNameList.append(enemy.name)
      
    for enemy in self.enemies:
      if enemy.name in self.enemiesDict:
        self.enemiesDict[enemy.name] += 1
      else:
        self.enemiesDict[enemy.name] = 1
      if enemyTempNameList.count(enemy.name) > 1:
        self.enemiesNameList.append(enemy.name + " " + str(self.enemiesDict[enemy.name]))
      else:
        self.enemiesNameList.append(enemy.name)
      

  def getEnemyString(self):
    curString = ""
    c = 0
    for enemy in self.enemies:
      if enemy.hp <= 0:
        curString += "~~" + self.enemiesNameList[c] + "~~\n"
      else:
        curString += self.enemiesNameList[c] + "\t" + str(enemy.hp) + "/" + str(enemy.maxHp) + " HP\n"
      c += 1
    return curString

  def getMoveString(self):
    curString = "**" + str(self.move[0]) + "** it's your turn! What do you do?"
    return curString

  def getPartyStats(self):
    curString = ""
    for player in self.players:
      curString += "**" + str(player[1]) + "**"
      for char in Data.pOverview[player[0]].chars:
        if char.className == Data.pOverview[player[0]].selected:
          curString += char.getBasicInfo()
          curString += "\n\n"
          break
    return curString

  def inParty(self, playerName):
    for player in self.players:
      if player[1] == playerName:
        return True
    return False

  def getPlayerStats(self, playerName):
    curString = "**__" + playerName + "__**\n\n"
    for player in self.players:
      if player[1] == playerName:
        for char in Data.pOverview[player[0]].chars:
          if char.className == player[2]:
            curString += char.getStats() + "\n\n" + char.getEquipment()
            return curString

  def makeEnemyMoves(self):
    enemyMoves = []
    c = 0
    for enemy in self.enemies:
      if enemy.hp <= 0:
        c += 1
        continue
      playerToAttack = self.players[randint(0, len(self.players) - 1)]
      dmg = enemy.att
      for char in Data.pOverview[playerToAttack[0]].chars:
        if char.className == Data.pOverview[playerToAttack[0]].selected:
          dmg -= char.getTotalDef()
          break
      if dmg <= 0:
        dmg = 1
      enemyMoves.append([self.enemiesNameList[c], playerToAttack, dmg])
      c += 1
    for player in self.players:
      for char in Data.pOverview[player[0]].chars:
        if char.className == player[2]:
          char.mp = min(char.mp + char.wis, char.getTotalMaxMp())
    return enemyMoves

  def checkForWin(self):
    for enemy in self.enemies:
      if enemy.hp > 0:
        return False
        break
    return True

  def checkForLoss(self):
    for player in self.players:
      for char in Data.pOverview[player[0]]:
        if char.className == Data.pOverview[player[0]].selected:
          return False
    return True