from Classes.Char import Char as Char
from Classes.Player import Player as Player
from Classes.Dungeon import Dungeon as Dungeon
import CreatingStuff.CreatingEnemies as CreatingEnemies
import CreatingStuff.CreatingWeapons as CreatingWeapons
import CreatingStuff.CreatingArmors as CreatingArmors
import CreatingStuff.CreatingAbilities as CreatingAbilities
import CreatingStuff.CreatingGadgets as CreatingGadgets
import CreatingStuff.CreatingItems as CreatingItems
import Main.ItemsToTypes as ItemsToTypes

# keeps track of all data

prefix = "!" # the command prefix, will be customizable later on

playing = [] # discord tags of ppl playing
playingNames = [] # in-game names of ppl playing
namesToTags = {} # {IGN, discord tag}
commandQueue = {} # dictionary of queues for things to respond to, ex: asking for name
pOverview = {} # dictionary of current playing players
inDungeon = {} # dictionary of players currently in dungeons
parties = {} # parties, where [key] is the leader and [value] are the other members
partyMembers = {} # {member, leader}
messageAuthors = {} # message authors
friends = {} # in game friends
admins = ["ToastyDreams#9785", "Toasty Dreams#9785"] # admins



def getPlayerData(player):

  curString = ""
  curPlayer = pOverview[player]

  # name
  curString += curPlayer.name + "\n"

  # chars
  curString += str(len(curPlayer.chars)) + "\n"
  for char in curPlayer.chars:
    curString += char.className + " " + str(char.att) + " " + str(char.defense) + " " + str(char.hp) + " " + str(char.maxHp) + " " + str(char.wis) + " " + str(char.mp) + " " + str(char.maxMp) + " " + str(char.speed) + " " + str(char.luck) + " " + str(char.level) + " " + str(char.xp) + " " + str(len(char.statusEffects)) + "\n"
    for statusEffect in char.statusEffects:
      curString += statusEffect[0] + " " + str(statusEffect[1]) + " " + str(statusEffect[2]) + "\n"
    curString += char.weapon.name + "\n" + char.armor.name + "\n" + char.ability.name + "\n" + char.gadget.name + "\n"

  # gold
  curString += str(curPlayer.gold) + "\n"

  # cUnlocked
  curString += " ".join(curPlayer.cUnlocked) + "\n"

  # dUnlocked
  curString += str(len(curPlayer.dUnlocked)) + "\n"
  for dungeon in curPlayer.dUnlocked:
    curString += dungeon + "\n"

  # inventory
  curString += str(len(curPlayer.inventory)) + "\n"
  for item in curPlayer.inventory:
    curString += item.name + "\n"

  # selected
  curString += curPlayer.selected + "\n"

  # dCompleted
  curString += str(len(curPlayer.dCompleted)) + "\n"
  for dungeon in curPlayer.dCompleted:
    curString += dungeon + "\n" + str(curPlayer.dCompleted[dungeon]) + "\n"

  return curString



def backup():
  global prefix, playing, playingNames, namesToTags, commandQueue, pOverview, inDungeon, parties, partyMembers, messageAuthors, friends, admins

  f = open("backup.txt", "w")
  f.write("")
  f.close()
  
  f = open("backup.txt", "a")
  f.write(prefix + "\n")

  # playing
  f.write(str(len(playing)) + "\n")
  for player in playing:
    f.write(player + "\n")

  # playingNames
  f.write(" ".join(playingNames) + "\n")

  # namesToTags
  f.write(str(len(namesToTags)) + "\n")
  for tag in namesToTags:
    f.write(tag + "\n" + namesToTags[tag] + "\n")

  # commandQueue
  f.write(str(len(commandQueue)) + "\n")
  for queue in commandQueue:
    f.write(queue + "\n" + " ".join(commandQueue[queue]) + "\n")

  # pOverview
  f.write(str(len(pOverview)) + "\n")
  for player in pOverview:
    f.write(player + "\n")
    f.write(getPlayerData(player))

  # inDungeon
  f.write(str(len(inDungeon)) + "\n")
  for dungeon in inDungeon:
    f.write(dungeon.dungeonName + " " + " ".join(dungeon.move) + "\n")
    for i in range (len(dungeon.enemies)):
      f.write(dungeon.enemies[i].name)
      if i != len(dungeon.enemies - 1):
        f.write(" ")
      else:
        f.write("\n")
    f.write(str(len(dungeon.players)) + "\n")
    for p in dungeon.players:
      f.write(" ".join(p) + "\n")
    f.write(str(dungeon.xpOnComp) + "\n")
    f.write(str(len(dungeon.gLoot)) + "\n")
    for loot in dungeon.gLoot:
      f.write(loot.name + "\n")
    f.write(str(len(dungeon.rLoot)) + "\n")
    for loot in dungeon.rLoot:
      f.write(loot.name + "\n")

  # parties
  f.write(str(len(parties)) + "\n")
  for party in parties:
    f.write(party + " " + " ".join(parties[party]) + "\n")

  # partyMembers
  f.write(str(len(partyMembers)) + "\n")
  for partyMember in partyMembers:
    f.write(partyMember + " " + partyMembers[partyMember] + "\n")    
      
  f.close()




def loadData():
  global prefix, playing, playingNames, namesToTags, commandQueue, pOverview, inDungeon, parties, partyMembers, messageAuthors, friends, admins

  f = open("backup.txt", "r")

  prefix = f.readline().strip()
  numP = int(f.readline().strip())
  for i in range (numP):
    playing.append(f.readline().strip())
  playingNames = f.readline().strip().split(" ")
  
  namesToTags.clear()
  cNum = int(f.readline().strip())
  for i in range (cNum):
    l1 = f.readline().strip()
    l2 = f.readline().strip()
    namesToTags[l1] = l2

  commandQueue.clear()
  cNum = int(f.readline().strip())
  for i in range (cNum):
    l1 = f.readline().strip()
    l2 = f.readline().strip().split(" ")
    commandQueue[l1] = l2

  pOverview.clear()
  cNum = int(f.readline().strip())
  for i in range (cNum):
    cUser = f.readline().strip()
    cName = f.readline().strip()
    curPlayer = Player(cName)
    numChars = int(f.readline().strip())
    for j in range (numChars):
      cStats = f.readline().strip().split(" ")
      curChar = Char(cStats[0], int(cStats[1]), int(cStats[2]), int(cStats[3]), int(cStats[4]), int(cStats[5]), int(cStats[6]), int(cStats[7]), int(cStats[8]), int(cStats[9]), int(cStats[10]), int(cStats[11]))
      for c in range (int(cStats[12])):
        curStatusEffect = f.readline().strip().split(" ")
        curStatusEffect[1] = int(curStatusEffect[1])
        curStatusEffect[2] = int(curStatusEffect[2])
        curChar.statusEffects.append(curStatusEffect)
      curWeapon = f.readline().strip()
      curArmor = f.readline().strip()
      curAbility = f.readline().strip()
      curGadget = f.readline().strip()
      curChar.weapon = CreatingWeapons.createWeapon(curWeapon)
      curChar.armor = CreatingArmors.createArmor(curArmor)
      curChar.ability = CreatingAbilities.createAbility(curAbility)
      curChar.gadget = CreatingGadgets.createGadget(curGadget)
      curPlayer.chars.append(curChar)
    curPlayer.gold = int(f.readline().strip())
    curPlayer.cUnlocked = f.readline().strip().split(" ")
    curPlayer.dUnlocked = []
    dNum = int(f.readline().strip())
    for x in range (dNum):
      curPlayer.dUnlocked.append(f.readline().strip())
    invSize = int(f.readline().strip())
    for j in range (invSize):
      curItem = f.readline().strip()
      if ItemsToTypes.itemType[curItem] == "weapon":
        curPlayer.inventory.append(CreatingWeapons.createWeapon(curItem))
      elif ItemsToTypes.itemType[curItem] == "ability":
        curPlayer.inventory.append(CreatingAbilities.createAbility(curItem))
      elif ItemsToTypes.itemType[curItem] == "armor":
        curPlayer.inventory.append(CreatingArmors.createArmor(curItem))
      elif ItemsToTypes.itemType[curItem] == "gadget":
        curPlayer.inventory.append(CreatingGadgets.createGadget(curItem))
      elif ItemsToTypes.itemType[curItem] == "item":
        curPlayer.inventory.append(CreatingItems.createItem(curItem))
    curPlayer.selected = f.readline().strip()
    curPlayer.dCompleted = {}
    d = int(f.readline().strip())
    for x in range (d):
      l1 = f.readline().strip()
      l2 = int(f.readline().strip())
      curPlayer.dCompleted[l1] = l2
    pOverview[cUser] = curPlayer

  inDungeon.clear()
  cNum = int(f.readline().strip())
  for i in range (cNum):
    curLine = f.readline().strip().split(" ")
    cName = curLine[0]
    cMove = curLine[1:]
    enemyList = f.readline().strip().split(" ")
    cEnemies = []
    for enemy in enemyList:
      cEnemies.append(CreatingEnemies.createEnemy(enemy))
    numPlayers = int(f.readline().strip())
    cPlayers = []
    for c in range (numPlayers):
      cPlayers.append(f.readline().strip().split(" "))
    cXP = int(f.readline().strip())

    numGLoot = int(f.readline().strip())
    cGLoot = []
    for c in range (numGLoot):
      curLoot = f.readline().strip()
      if ItemsToTypes.itemType[curLoot] == "weapon":
        cGLoot.append(CreatingWeapons.createWeapon(curItem))
      elif ItemsToTypes.itemType[curLoot] == "armor":
        cGLoot.append(CreatingArmors.createArmor(curItem))
      elif ItemsToTypes.itemType[curLoot] == "ability":
        cGLoot.append(CreatingAbilities.createAbility(curItem))
      elif ItemsToTypes.itemType[curLoot] == "gadget":
        cGLoot.append(CreatingGadgets.createGadget(curItem))
      elif ItemsToTypes.itemType[curLoot] == "item":
        cGLoot.append(CreatingItems.createItem(curItem))

    numRLoot = int(f.readline().strip())
    cRLoot = []
    for c in range (numRLoot):
      curLoot = f.readline().strip()
      if ItemsToTypes.itemType[curLoot] == "weapon":
        cRLoot.append(CreatingWeapons.createWeapon(curItem))
      elif ItemsToTypes.itemType[curLoot] == "armor":
        cRLoot.append(CreatingArmors.createArmor(curItem))
      elif ItemsToTypes.itemType[curLoot] == "ability":
        cRLoot.append(CreatingAbilities.createAbility(curItem))
      elif ItemsToTypes.itemType[curLoot] == "gadget":
        cRLoot.append(CreatingGadgets.createGadget(curItem))
      elif ItemsToTypes.itemType[curLoot] == "item":
        cRLoot.append(CreatingItems.createItem(curItem))

  numParties = int(f.readline().strip())
  parties.clear()
  for i in range (numParties):
    curParty = f.readline().strip().split(" ")
    parties[curParty[0]] = curParty[1:]

  numPM = int(f.readline().strip())
  partyMembers.clear()
  for i in range (numPM):
    cPM = f.readline().strip().split(" ")
    partyMembers[cPM[0]] = cPM[1]




playerLimits = {
  "Chicken's Den" : 2,
  "Thieves Hideout" : 5
}

classes = ["warrior", "knight", "priest", "mage", "jester", "assassin"] # classes
dungeons = ["chicken's den", "thieves hideout", "your mom's basement", "the endless void", "toasty's temple", "toasty's castle"] # dungeons



xpToNextLevel = [
  100, # to lvl 2
  200, # to lvl 3
  300, # to lvl 4
  500, # to lvl 5
  800, # to lvl 6
  1000, # to lvl 7
  2500, # to lvl 8
  5000, # to lvl 9
  10000 # to lvl 10
]