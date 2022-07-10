#from keep_alive import keep_alive
# the above line is for later use when I want to host it 24/7

# importing libraries
from random import randint # random library

import os # replit environment
import discord # discord library

# importing data and classes
import Main.Data as Data
import TextStuff.Text as Text
import TextStuff.DungeonText as DungeonText
import TextStuff.ArmorText as ArmorText
import TextStuff.EnemyText as EnemyText
import TextStuff.ItemDescriptions as ItemDescriptions
import TextStuff.WeaponText as WeaponText
import TextStuff.GadgetText as GadgetText
import CreatingStuff.CreatingDungeons as CreatingDungeons
import CreatingStuff.CreatingEnemies as CreatingEnemies
import CreatingStuff.CreatingWeapons as CreatingWeapons
import CreatingStuff.CreatingArmors as CreatingArmors
import CreatingStuff.CreatingAbilities as CreatingAbilities
import CreatingStuff.CreatingGadgets as CreatingGadgets
import CreatingStuff.CreatingItems as CreatingItems
import TextStuff.RaritiesText as RaritiesText
import Main.RarityEmbedColors as RarityEmbedColors
import TextStuff.ItemStatsText as ItemStatsText
import Main.Colors as Colors
import Main.ItemsToTypes as ItemsToTypes
import Main.TypesToTypes as TypesToTypes
import TextStuff.DUnlockReqsText as DUnlockReqsText
import TextStuff.DDifficultiesText as DDifficultiesText
import TextStuff.DDescriptionsText as DDescriptionsText
from Classes.Player import Player as Player
from Classes.Char import Char as Char
from Classes.Dungeon import Dungeon as Dungeon
from Classes.Enemy import Enemy as Enemy
from Classes.Item import Item as Item
from Classes.Weapon import Weapon as Weapon
from Classes.Armor import Armor as Armor
from Classes.Ability import Ability as Ability
from Classes.Gadget import Gadget as Gadget



# setting the Discord client
client = discord.Client()

# Discord event when the bot loads up and is online
@client.event
async def on_ready():
  print("{0.user} is online!".format(client))
  
# Discord event for when a message is sent
@client.event
async def on_message(message):
  curAuthor = str(message.author)
  if message.author == client.user:
    return

  words = list(map(str, message.content.strip().split(" ")))

  # DMs
  if not message.guild:
    try:
      if len(Data.commandQueue[curAuthor]) > 0 and Data.commandQueue[curAuthor][0] == "party invite":
        if words[0] == "accept":
          em = discord.Embed(title = "Joining Party", description = "You have successfully joined **" + Data.pOverview[Data.commandQueue[curAuthor][1]].name + "**'s party!", color = Colors.pink)
          await message.channel.send(embed = em)
          Data.parties[Data.commandQueue[curAuthor][1]] = [curAuthor]
          Data.partyMembers[curAuthor] = Data.commandQueue[curAuthor][1]
          em = discord.Embed(title = "Party Invite Accepted", description = "**" + Data.pOverview[curAuthor].name + "** accepted the party invite!", color = Colors.pink)
          await Data.commandQueue[curAuthor][2].send(embed = em)
          Data.commandQueue[curAuthor] = []
          return
        elif words[0] == "decline":
          em = discord.Embed(title = "Party Invite Declined", description = "**" + Data.pOverview[curAuthor].name + "** declined the party invite!", color = Colors.pink)
          await Data.commandQueue[curAuthor][2].send(embed = em)
          Data.commandQueue[curAuthor] = []
    except discord.errors.Forbidden:
      pass
    return

  # checking if the player plays
  plays = True
  curPlayer = ""
  if curAuthor not in Data.playing:
    plays = False


  
  # if this message author is in queue; are they responding to something
  if plays and len(Data.commandQueue[curAuthor]) != 0:

    # if they are responding to asking for their name
    if Data.commandQueue[curAuthor][0] == "name":
      
      if words[0] in Data.playingNames:
        await message.channel.send(Text.takenName)
        return
        
      Data.pOverview[curAuthor] = Player(words[0])
      Data.messageAuthors[words[0]] = message.author
      em = discord.Embed(title = "Welcome", description = "Welcome **" + words[0] + "**!\nUse " + Data.prefix + "create [class] to create your first character, or " + Data.prefix + "help for help!", color = Colors.green)
      await message.channel.send(embed = em)
      del Data.commandQueue[curAuthor][0]
      Data.playingNames.append(words[0])
      Data.namesToTags[words[0]] = curAuthor
      return
  # end command queue check



  # if the player is in a dungeon; are they doing dungeon stuff
  if plays and (curAuthor in Data.inDungeon or (curAuthor in Data.partyMembers and Data.partyMembers[curAuthor] in Data.inDungeon)):

    curLeader = curAuthor
    if curAuthor in Data.partyMembers:
      curLeader = Data.partyMembers[curAuthor]

    if Data.pOverview[curAuthor].name == Data.inDungeon[curLeader].move[0] and Data.inDungeon[curLeader].move[1] == "attack":

      attacking = " ".join(words)

      if attacking == "exit" or attacking == "stop":

        Data.inDungeon[curLeader].move[1] = "move"
        em = discord.Embed(title = "Stop Attacking", description = "You have successfully stopped attacking.\nWhat would you like to do?", color = Colors.navy)
        await message.channel.send(embed = em)
        return
      
      if attacking not in Data.inDungeon[curLeader].enemiesNameList:

        em = discord.Embed(title = "Error", description = "No such enemy exists in this dungeon!", color = Colors.red)
        await message.channel.send(embed = em)
        return

      curDmg = 0
      for char in Data.pOverview[curAuthor].chars:
        if char.className == Data.pOverview[curAuthor].selected:
          curDmg = char.getTotalDmg()
          break

      curEnemy = Data.inDungeon[curLeader].enemies[Data.inDungeon[curLeader].enemiesNameList.index(attacking)]
      curDmg -= curEnemy.defense
      if curDmg <= 0:
        curDmg = 1
      curDmg = min(curDmg, curEnemy.hp)
      em = discord.Embed(title = "Enemy Hit", description = "You hit " + attacking + " for " + str(curDmg) + " damage!", color = Colors.maroon)
      await message.channel.send(embed = em)
      dead = False
      if curDmg == curEnemy.hp:
        dead = True
        em = discord.Embed(title = "Enemy Killed", description = "You've taken down " + attacking + "!", color = Colors.maroon)
        await message.channel.send(embed = em)

      Data.inDungeon[curLeader].enemies[Data.inDungeon[curLeader].enemiesNameList.index(attacking)].hp -= curDmg

      # if an enemy just died
      if dead:
        # checking if all enemies are dead
        if Data.inDungeon[curLeader].checkForWin():
          em = discord.Embed(title = "Dungeon Completed", description = "You won!\nYou've conquerued " + Data.inDungeon[curLeader].dungeonName + "\n\n", color = Colors.green)
          await message.channel.send(embed = em)
          for player in Data.inDungeon[curLeader].players:
            lootString = "\n\n__You obtained the following items:__"
            for item in Data.inDungeon[curLeader].gLoot:
              Data.pOverview[player[0]].inventory.append(item)
              lootString += "\n" + item.name
            for item in Data.inDungeon[curLeader].rLoot:
              curNum = randint(1, 100)
              if curNum <= item[1]:
                Data.pOverview[player[0]].inventory.append(item)
                lootString += "\n" + item.name
            em = discord.Embed(title = "Dungeon Rewards", description = "You earned " + str(Data.inDungeon[curLeader].xpOnComp) + " xp" + lootString, color = Colors.green)
            await Data.messageAuthors[player[1]].send(embed = em)
            for char in Data.pOverview[player[0]].chars:
              if char.className == Data.pOverview[player[0]].selected:
                char.hp = char.getTotalMaxHp()
                char.mp = char.getTotalMaxMp()
                char.xp += Data.inDungeon[curLeader].xpOnComp

                # if they have enough xp to level up now
                if char.xp >= Data.xpToNextLevel[char.level - 1]:
                  char.xp -= Data.xpToNextLevel[char.level - 1]
                  char.level += 1
                  em = discord.Embed(title = "Level up", description = "Your " + char.className + " leveled up to level " + str(char.level) + "!", color = Colors.green)
                  await Data.messageAuthors[player[1]].send(embed = em)

          del Data.inDungeon[curLeader]
          
          return

          

      Data.inDungeon[curLeader].move[1] = "move"
      if Data.inDungeon[curLeader].move[0] == Data.inDungeon[curLeader].players[-1][1]:
        Data.inDungeon[curLeader].move[0] = Data.inDungeon[curLeader].enemiesNameList[0]
        curString = "It's now the enemy's turn!"

        enemyMoves = Data.inDungeon[curLeader].makeEnemyMoves()

        needCheck = False
        for enemyMove in enemyMoves:
          for char in Data.pOverview[enemyMove[1][0]].chars:
            if char.className == enemyMove[1][2]:
              char.hp -= enemyMove[2]
              curString += "\n" + enemyMove[0] + " hit **" + enemyMove[1][1] + "** for " + str(enemyMove[2]) + " damage!"
              if char.hp == 0:
                needCheck = True
              break

        em = discord.Embed(title = "Enemy Turn", description = curString, color = Colors.maroon)
        await message.channel.send(embed = em)
        
        if needCheck:
          if Data.inDungeon[curLeader].checkForLoss():
            em = discord.Embed(title = "Dungeon Failed", description = "You failed to conquer the dungeon! You were kicked out for your unsuccessful attempt. Try again sometime!", color = Colors.red)
            await message.channel.send(embed = em)
            del Data.inDungeon[curLeader]
            return

        Data.inDungeon[curLeader].move = [Data.inDungeon[curLeader].players[0][1], "move"]
        em = discord.Embed(title = "Player Move", description = Data.inDungeon[curLeader].getMoveString(), color = Colors.navy)
        await message.channel.send(embed = em)
        
      else:
        c = 0
        for player in Data.inDungeon[curLeader].players:
          if player[1] == Data.inDungeon[curLeader].move[0]:
            c += 1
            Data.inDungeon[curLeader].move[0] = Data.inDungeon[curLeader].players[c][1]
            em = discord.Embed(title = "Player Move", description = Data.inDungeon[curLeader].getMoveString(), color = Colors.navy)
            await message.channel.send(embed = em)
            return
          c += 1
      return
      

      
    
    if words[0] == "!pStats" or words[0] == "!pstats" or words[0] == "pstats" or words[0] == "pStats" or words[0] == "!partystats" or words[0] == "!partyStats" or words[0] == "partystats" or words[0] == "partyStats":

      if len(words) == 1:
        em = discord.Embed(title = "Party Stats", description = Data.inDungeon[curLeader].getPartyStats(), color = Colors.pink)
        await message.channel.send(embed = em)
        
      else:
        
        curPlayer = " ".join(words[1:])
        
        if not Data.inDungeon[curLeader].inParty(curPlayer):        
          if curPlayer in Data.playing:
            em = discord.Embed(title = "Error", description = "That player isn't in this dungeon with you!", color = Colors.red)
            await message.channel.send(embed = em)
          else:
            em = discord.Embed(title = "Error", description = "That player doesn't exist!", color = Colors.red)
            await message.channel.send(embed = em)
          return

        em = discord.Embed(title = "Player Stats", description = Data.inDungeon[curLeader].getPlayerStats(curPlayer), color = Colors.pink)
        await message.channel.send(embed = em)
        
      return

    if words[0] == "!estats" or words[0] == "!eStats" or words[0] == "estats" or words[0] == "eStats" or words[0] == "!enemyStats" or words[0] == "!enemystats" or words[0] == "enemystats" or words[0] == "enemyStats":

      if len(words) == 1:
        em = discord.Embed(title = "Enemies", description = Data.inDungeon[curLeader].getEnemyString(), color = Colors.navy)
        await message.channel.send(embed = em)

      else:

        curEnemy = " ".join(words[1:])

        if curEnemy not in Data.inDungeon[curLeader].enemiesNameList:
          em = discord.Embed(title = "Error", description = "No such enemy exists in this dungeon!", color = Colors.red)
          await message.channel.send(embed = em)
          return

        em = discord.Embed(title = "Enemy Info", description = Data.inDungeon[curLeader].enemies[Data.inDungeon[curLeader].enemiesNameList.index(curEnemy)].getEnemyStats(), color = Colors.navy)
        await message.channel.send(embed = em)
        return


    
    if words[0] == "attack" and Data.pOverview[curAuthor].name == Data.inDungeon[curLeader].move[0] and Data.inDungeon[curLeader].move[1] == "move":

      em = discord.Embed(title = "Attack", description = "Who would you like to attack?\n" + Data.inDungeon[curLeader].getEnemyString(), color = Colors.maroon)
      await message.channel.send(embed = em)
      Data.inDungeon[curLeader].move[1] = "attack"
      return



    if words[0] == "ability" and Data.pOverview[curAuthor].name == Data.inDungeon[curLeader].move[0] and Data.inDungeon[curLeader].move[1] == "move":

      for char in Data.pOverview[curAuthor].chars:
        
        if char.className == Data.pOverview[curAuthor].selected:
          
          if char.mp < char.ability.mpCost:
            em = discord.Embed(title = "Error", description = "You don't have enough MP!", color = Colors.red)
            await message.channel.send(embed = em)
            return

          em = discord.Embed(title = "Ability", description = char.useAbility(), color = Colors.navy)
          await message.channel.send(embed = em)

          Data.inDungeon[curLeader].move[1] = "move"
          if Data.inDungeon[curLeader].move[0] == Data.inDungeon[curLeader].players[-1][1]:
            Data.inDungeon[curLeader].move[0] = Data.inDungeon[curLeader].enemiesNameList[0]
            curString = "It's now the enemy's turn!"

            enemyMoves = Data.inDungeon[curLeader].makeEnemyMoves()

            needCheck = False
            for enemyMove in enemyMoves:
              for char in Data.pOverview[enemyMove[1][0]].chars:
                if char.className == enemyMove[1][2]:
                  char.hp -= enemyMove[2]
                  curString += "\n" + enemyMove[0] + " hit **" + enemyMove[1][1] + "** for " + str(enemyMove[2]) + " damage!"
                  if char.hp == 0:
                    needCheck = True
                  break

            em = discord.Embed(title = "Enemy Turn", description = curString, color = Colors.maroon)
            await message.channel.send(embed = em)
        
            if needCheck:
              if Data.inDungeon[curLeader].checkForLoss():
                em = discord.Embed(title = "Dungeon Failed", description = "You failed to conquer the dungeon! You were kicked out for your unsuccessful attempt. Try again sometime!", color = Colors.red)
                await message.channel.send(embed = em)
                del Data.inDungeon[curLeader]
                return

            Data.inDungeon[curLeader].move = [Data.inDungeon[curLeader].players[0][1], "move"]
            em = discord.Embed(title = "Player Move", description = Data.inDungeon[curLeader].getMoveString(), color = Colors.navy)
            await message.channel.send(embed = em)
        
          else:
            c = 0
            for player in Data.inDungeon[curLeader].players:
              if player[1] == Data.inDungeon[curLeader].move[0]:
                c += 1
                Data.inDungeon[curLeader].move[0] = Data.inDungeon[curLeader].players[c][1]
                em = discord.Embed(title = "Player Move", description = Data.inDungeon[curLeader].getMoveString(), color = Colors.navy)
                await message.channel.send(embed = em)
                return
              c += 1
            
          return
      
      return

  # end in dungeon check
      
      
  
  if plays:
    curPlayer = Data.pOverview[curAuthor]
      
  # only check for a command if the prefix is right
  if words[0][0] != Data.prefix:
    return
  words[0] = words[0][1:] # remove prefix from text string


  
  if words[0] == "help":
    if len(words) == 1:
      em = discord.Embed(title = "Help", description = Text.help, color = Colors.navy)
      await message.channel.send(embed = em)
      return
    if len(words) == 2:
      if words[1] == "stats":
        em = discord.Embed(title = "Help", description = Text.helpStats, color = Colors.navy)
        await message.channel.send(embed = em)
        return
      
      if words[1] == "weapons":
        em = discord.Embed(title = "Help", description = Text.helpWeapons, color = Colors.navy)
        await message.channel.send(embed = em)
        return
        
      if words[1] == "armors":
        em = discord.Embed(title = "Help", description = Text.helpArmors, color = Colors.navy)
        await message.channel.send(embed = em)
        return
        
      if words[1] == "abilities":
        em = discord.Embed(title = "Help", description = Text.helpAbilities, color = Colors.navy)
        await message.channel.send(embed = em)
        return
      
      if words[1] == "classes":
        em = discord.Embed(title = "Help", description = Text.helpClasses, color = Colors.navy)
        await message.channel.send(embed = em)
        return
      
      if words[1] == "dungeons":
        em = discord.Embed(title = "Help", description = Text.helpDungeons, color = Colors.navy)
        await message.channel.send(embed = em)
        return
        
    em = discord.Embed(title = "Error", description = Text.helpNotFound, color = Colors.red)
    await message.channel.send(embed = em)
    return
      

      
  # create a new character/class
  if words[0] == "create":
    
    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return

    if len(words) == 1:
      return

    # if they've unlocked the class and they have a spare character slot
    if words[1] in curPlayer.cUnlocked and len(curPlayer.chars) < curPlayer.charSlots:
      for char in curPlayer.chars:
        if char.className == words[1]:
          em = discord.Embed(title = "Error", description = "You already have a " + words[1] + "! You cannot have multiple characters of the same class", color = Colors.red)
          await message.channel.send(embed = em)
          return
      if words[1] == "warrior" or words[1] == "warr":
        curChar = Char("warrior", 5, 5, 50, 50, 5, 50, 50, 5, 0, 1, 0)
        Data.pOverview[curAuthor].chars.append(curChar)
        em = discord.Embed(title = "Creating Character", description = Text.warriorCreated, color = Colors.navy)
        await message.channel.send(embed = em)
        
    elif words[1] not in curPlayer.cUnlocked:
      if words[1] in Data.classes:
        em = discord.Embed(title = "Error", description = Text.classNotUnlocked, color = Colors.red)
        await message.channel.send(embed = em)
      else:
        em = discord.Embed(title = "Error", description = Text.classNoExist, color = Colors.red)
        await message.channel.send(embed = em)
        
    elif len(curPlayer.chars) == curPlayer.charSlots:
      em = discord.Embed(title = "Error", description = Text.fullCharSLots, color = Colors.red)
      await message.channel.send(embed = em)
    return


  
  # run a dungeon
  if words[0] == "run":

    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return

    if curAuthor in Data.partyMembers:
      em = discord.Embed(title = "Error", description = "You can't queue for dungeons since you are not your party's leader!", color = Colors.red)
      await message.channel.send(embed = em)
      return
    
    for i in range (1, len(words)):
      words[i] = words[i].lower()
    dungeonName = " ".join(words[1:])
    dungeonName.lower()
    
    if dungeonName not in curPlayer.dUnlocked:
      if dungeonName in Data.dungeons:
        em = discord.Embed(title = "Error", description = "You haven't unlocked that dungeon yet!", color = Colors.red)
        await message.channel.send(embed = em)
      else:
        em = discord.Embed(title = "Error", description = "That dungeon doesn't exist!", color = Colors.red)
        await message.channel.send(embed = em)
      return
      
    allUnlocked = True
    if curAuthor in Data.parties:
      for member in Data.parties[curAuthor]:
        if dungeonName not in Data.pOverview[member].dUnlocked:
          allUnlocked = False
          break
          
    if not allUnlocked:
      em = discord.Embed(title = "Error", description = "Someone in your party hasn't unlocked that dungeon!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    allSelected = True
    if Data.pOverview[curAuthor].selected == None:
      allSelected = False
      
    if curAuthor in Data.parties:
      for member in Data.parties[curAuthor]:
        if Data.pOverview[member].selected == None:
          allSelected = False
          break
          
    if not allSelected:
      em = discord.Embed(title = "Error", description = "Either you or someone in your party doesn't have a class selected!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    curString = "**" + Data.pOverview[curAuthor].name + "**"
    if curAuthor in Data.parties:
      for member in Data.parties[curAuthor]:
        curString += ", **" + Data.pOverview[member].name + "**"

    for i in range (1, len(words)):
      words[i] = words[i][0].upper() + words[i][1:]
    rDungeonName = " ".join(words[1:])

    curParty = [curAuthor]
    if curAuthor in Data.parties:
      for member in Data.parties[curAuthor]:
        curParty.append(member)
    if len(curParty) > Data.playerLimits[rDungeonName]:
      em = discord.Embed(title = "Error", description = "Your party exceeds the max number of members (" + str(Data.playerLimits[rDungeonName]) + ") for this dungeon!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    em = discord.Embed(title = "Successfully Entered Dungeon", description = curString + " successfully entered " + rDungeonName + ".", color = Colors.navy)    
    await message.channel.send(embed = em)
      
    Data.inDungeon[curAuthor] = CreatingDungeons.createDungeon(rDungeonName, curParty)

    em = discord.Embed(title = "Entering Dungeon", description = DungeonText.enterDungeonText(rDungeonName), color = Colors.navy)
    await message.channel.send(embed = em)
    em = discord.Embed(title = "Enemies", description = Data.inDungeon[curAuthor].getEnemyString(), color = Colors.navy)
    await message.channel.send(embed = em)
    em = discord.Embed(title = "Player Move", description = Data.inDungeon[curAuthor].getMoveString(), color = Colors.navy)
    await message.channel.send(embed = em)

    return


  
  if words[0] == "overview":
    
    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return
      
    curString = "**Overview for " + Data.pOverview[curAuthor].name + "**\n\n__Characters:__\n"
    if len(curPlayer.chars) == 0:
      curString += "You don't have any characters right now\n"
    else:
      for char in curPlayer.chars:
        curString += char.className + " [lvl " + str(char.level) + "]\n"
    curString += "\n__Dungeons:__\n"
    if len(curPlayer.dungeonsCompleted) == 0:
      curString += "You haven't completed any dungeons yet\n"
    else:
      for dungeon in curPlayer.dungeonsCompleted:
        curString += dungeon + " - " + str(curPlayer.dungeonsCompleted[dungeon]) + "\n"
    curString += "\n__Classes Unlocked:__\n"
    curString += "\n".join(curPlayer.cUnlocked)
    curString += "\n\n__Dungeons Unlocked:__\n"
    curString += "\n".join(curPlayer.dUnlocked)
    em = discord.Embed(title = "Player Overview", description = curString, color = Colors.teal)
    await message.channel.send(embed = em)
    return


  
  if words[0] == "stats":
    
    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return

    if Data.pOverview[curAuthor].selected == None:
      em = discord.Embed(title = "Error", description = "You don't have a class selected!", color = Colors.red)
      await message.channel.send(embed = em)
      return
    
    for char in Data.pOverview[curAuthor].chars:
      if char.className == Data.pOverview[curAuthor].selected:
        em = discord.Embed(title = "Stats", description = char.getStats(), color = Colors.navy)
        await message.channel.send(embed = em)
        return


  
  if words[0] == "equipment":

    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return

    if Data.pOverview[curAuthor].selected == None:
      em = discord.Embed(title = "Error", description = "You don't have a class selected!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    for char in Data.pOverview[curAuthor].chars:
      if char.className == Data.pOverview[curAuthor].selected:
        em = discord.Embed(title = "Equipment", description = char.getEquipment(), color = Colors.gold)
        await message.channel.send(embed = em)
        return


  
  if words[0] == "inv" or words[0] == "inventory" or words[0] == "storage" or words[0] == "backpack":

    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return

    if len(Data.pOverview[curAuthor].inventory) == 0:
      em = discord.Embed(title = "Inventory", description = "Your inventory is empty!", color = Colors.brown)
      await message.channel.send(embed = em)
    else:
      invString = ""
      for item in Data.pOverview[curAuthor].inventory:
        invString += item.name + "\n"
      em = discord.Embed(title = "Inventory", description = invString, color = Colors.brown)
      await message.channel.send(embed = em)
    return


  
  if words[0] == "party" or words[0] == "p":
    
    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return

    if len(words) == 1:
      if curAuthor in Data.parties:
        curPartyMembers = ""
        for member in Data.parties[curAuthor]:
          curPartyMembers += "\n**" + Data.pOverview[member].name + "**"
        em = discord.Embed(title = "Party", description = "Party Leader: **" + Data.pOverview[curAuthor].name + "**\n\nParty Members:" + curPartyMembers, color = Colors.pink)
        await message.channel.send(embed = em)
        
      elif curAuthor in Data.partyMembers:
        pLeader = Data.partyMembers[curAuthor]
        curPartyMembers = ""
        for member in Data.parties[pLeader]:
          curPartyMembers += "\n**" + Data.pOverview[member].name + "**"
        em = discord.Embed(title = "Party", description = "Party Leader: **" + Data.pOverview[pLeader].name + "**\n\nParty Members:" + curPartyMembers, color = Colors.pink)
        await message.channel.send(embed = em)
      return

    curPlayer = " ".join(words[1:])
    
    if curPlayer not in Data.playingNames:
      em = discord.Embed(title = "Error", description = "That person doesn't play!", color = Colors.red)
      await message.channel.send(embed = em)
    else:
      if curPlayer == Data.pOverview[curAuthor].name:
        em = discord.Embed(title = "Error", description = "You can't invite yourself to your own party!", color = Colors.red)
        await message.channel.send(embed = em)
        return
        
      try:
        em = discord.Embed(title = "Party Invitation", description = "You've been invited to " + Data.pOverview[curAuthor].name + "'s party! Respond with \"accept\" or \"decline\".", color = Colors.pink)
        await Data.messageAuthors[curPlayer].send(embed = em)
        em = discord.Embed(title = "Party Invitation", description = "You have sucessfully invited " + curPlayer + " to your party!", color = Colors.pink)
        await message.channel.send(embed = em)
        Data.commandQueue[Data.namesToTags[curPlayer]] = ["party invite", curAuthor, message.channel]
        
      except discord.errors.Forbidden:
        em = discord.Embed(title = "Error", description = "They don't have their DMs open! Have them open their DMs and try again.", color = Colors.red)
        await message.channel.send(embed = em)

    return



  if words[0] == "pdisband" or words[0] == "pDisband" or words[0] == "partydisband" or words[0] == "partyDisband":

    if curAuthor not in Data.parties:
      em = discord.Embed(title = "Error", description = "You are not a party leader!", color = Colors.red)
      await message.channel.send(embed = em)

    else:
      em = discord.Embed(title = "Party Disbanded", description = "You have successfully disbanded your party!", color = Colors.pink)
      await message.channel.send(embed = em)
      for member in Data.parties[curAuthor]:
        em = discord.Embed(title = "Party Disbanded", description = "**" + Data.pOverview[curAuthor].name + "** has disbanded the party!", color = Colors.pink)
        await Data.messageAuthors[Data.pOverview[member].name].send(embed = em)
      del Data.parties[curAuthor]
    return



  if words[0] == "pkick" or words[0] == "pKick" or words[0] == "partykick" or words[0] == "partyKick":

    if curAuthor not in Data.parties:
      em = discord.Embed(title = "Error", description = "You are not a party leader!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    curPlayer = " ".join(words[1:])
    found = False
    memberToKick = ""
    for member in Data.parties[curAuthor]:
      if Data.pOverview[member].name == curPlayer:
        found = True
        memberToKick = member
        break
    if not found:
      em = discord.Embed(title = "Error", description = "That player is not in your party!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    Data.parties[curAuthor].remove(memberToKick)
    em = discord.Embed(title = "Party Kick", description = "You successfully kicked **" + curPlayer + "** from your party!", color = Colors.pink)
    await message.channel.send(embed = em)
    em = discord.Embed(title = "Party Kick", description = "You were kicked from **" + Data.pOverview[curAuthor].name + "**'s party!", color = Colors.pink)
    await Data.messageAuthors[curPlayer].send(embed = em)
    if len(Data.parties[curAuthor]) == 0:
      em = discord.Embed(title = "Party Disbanded", description = "Your party was automatically disbanded because you were the last member in it.", color = Colors.pink)
      await Data.messageAuthors[Data.pOverview[curAuthor].name].send(embed = em)
    return



  if words[0] == "pleave" or words[0] == "pLeave" or words[0] == "partyleave" or words[0] == "partyLeave":

    if curAuthor not in Data.partyMembers:
      em = discord.Embed(title = "Error", description = "You are not a party member! If you are a party leader, try using !pdisband instead.", color = Colors.pink)
      await message.channel.send(embed = em)
      return

    Data.parties[Data.partyMembers[curAuthor]].remove(curAuthor)
    em = discord.Embed(title = "Leave Party", description = "You have successfully left **" + Data.pOverview[Data.partyMembers[curAuthor]].name + "**'s party!", color = Colors.pink)
    await message.channel.send(embed = em)
    em = discord.Embed(title = "Leave Party", description = "**" + Data.pOverview[curAuthor].name + "** has left your party!", color = Colors.pink)
    await Data.messageAuthors[Data.pOverview[Data.partyMembers[curAuthor]].name].send(embed = em)
    if len(Data.parties[Data.partyMembers[curAuthor]]) == 0:
      em = discord.Embed(title = "Party Disbanded", description = "Your party was automatically disbanded because you were the last member in it.", color = Colors.pink)
      await Data.messageAuthors[Data.pOverview[Data.partyMembers[curAuthor]].name].send(embed = em)
    return



  if words[0] == "select":
    
    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return
      
    className = " ".join(words[1:])
    if className in Data.pOverview[curAuthor].cUnlocked:
      Data.pOverview[curAuthor].selected = className
      em = discord.Embed(title = "Class Selected", description = "Successfully selected the " + className + " class!", color = Colors.navy)
      await message.channel.send(embed = em)
    else:
      em = discord.Embed(title = "Error", description = "Either that class doesn't exist or you haven't unlocked it yet!", color = Colors.red)
      await message.channel.send(embed = em)
    return



  if words[0] == "info":
    
    if len(words) == 1:
      return

    curItem = " ".join(words[1:])
    if curItem not in ItemDescriptions.itemDescriptions:
      em = discord.Embed(title = "Error", description = "That item doesn't exist!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    em = discord.Embed(title = "Item Info", description = "**__" + curItem + "__**\n\n" + RaritiesText.itemRarities[curItem] + "\n\n" + ItemStatsText.itemStatsText[curItem] + "\n\n" + ItemDescriptions.itemDescriptions[curItem], color = RarityEmbedColors.rarityEmbedColors[RaritiesText.itemRarities[curItem]])
    await message.channel.send(embed = em)
    return



  if words[0] == "dinfo" or words[0] == "dInfo" or words[0] == "dungeoninfo" or words[0] == "dungeonInfo":

    if len(words) == 1:
      return

    curDungeon = " ".join(words[1:])
    if curDungeon not in DUnlockReqsText.reqs:
      em = discord.Embed(title = "Error", description = "That dungeon doesn't exist!", color = Colors.red)
      return

    em = discord.Embed(title = "Dungeon Info", description = "**__" + curDungeon + "__**\n\n__Difficulty:__ " + DDifficultiesText.difficulties[curDungeon] + "\n\n__Requirements to unlock:__ " + DUnlockReqsText.reqs[curDungeon] + "\n\n" + DDescriptionsText.description[curDungeon], color = Colors.navy)
    await message.channel.send(embed = em)
    return



  if words[0] == "equip":

    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return
    
    if len(words) == 1:
      return

    if Data.pOverview[curAuthor].selected == None:
      em = discord.Embed(title = "Error", description = "You don't have a class selected!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    curItem = " ".join(words[1:])
    for item in Data.pOverview[curAuthor].inventory:
      
      if item.name == curItem:
        
        for char in Data.pOverview[curAuthor].chars:
          
          if char.className == Data.pOverview[curAuthor].selected:

            addString = ""
            
            if TypesToTypes.typetype[item.type] == "weapon":
              if char.weapon.name != "None":
                Data.pOverview[curAuthor].inventory.append(char.weapon)
                addString = "\nTo do so, you automatically unequipped your " + char.weapon.name + "."
              char.weapon = item
              Data.pOverview[curAuthor].inventory.remove(item)
              
            elif TypesToTypes.typetype[item.type] == "ability":
              if char.ability.name != "None":
                Data.pOverview[curAuthor].inventory.append(char.ability)
                addString = "\nTo do so, you automatically unequipped your " + char.ability.name + "."
              char.ability = item
              Data.pOverview[curAuthor].inventory.remove(item)
              
            elif TypesToTypes.typetype[item.type] == "armor":
              if char.armor.name != "None":
                Data.pOverview[curAuthor].inventory.append(char.armor)
                addString = "\nTo do so, you automatically unequipped your " + char.armor.name + "."
              char.armor = item
              Data.pOverview[curAuthor].inventory.remove(item)
              
            elif TypesToTypes.typetype[item.type] == "gadget":
              if char.gadget.name != "None":
                Data.pOverview[curAuthor].inventory.append(char.gadget)
                addString = "\nTo do so, you automatically unequipped your " + char.gadget.name + "."
              char.gadget = item
              Data.pOverview[curAuthor].inventory.remove(item)
              
            else:
              em = discord.Embed(title = "Error", description = "You cannot equip that item into any of your gear slots!", color = Colors.red)
              await message.channel.send(embed = em)
              return

            char.resetStats()  
              
            em = discord.Embed(title = "Equip", description = "Successfully equipped " + item.name + "!" + addString, color = Colors.green)
            await message.channel.send(embed = em)
            return

    em = discord.Embed(title = "Error", description = "Item not found in your inventory!", color = Colors.red)
    await message.channel.send(embed = em)
    return



  if words[0] == "unequip":

    if not plays:
      em = discord.Embed(title = "Error", description = Text.notPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return
    
    if len(words) == 1:
      return

    if Data.pOverview[curAuthor].selected == None:
      em = discord.Embed(title = "Error", description = "You don't have a class selected!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    curItem = " ".join(words[1:])
    if curItem == "None":
      return

    for char in Data.pOverview[curAuthor].chars:
      if char.className == Data.pOverview[curAuthor].selected:
        
        if char.weapon.name == curItem:
          Data.pOverview[curAuthor].inventory.append(char.weapon)
          char.weapon = CreatingWeapons.createWeapon("None")
      
        elif char.ability.name == curItem:
          Data.pOverview[curAuthor].inventory.append(char.ability)
          char.ability = CreatingAbilities.createAbility("None")
      
        elif char.armor.name == curItem:
          Data.pOverview[curAuthor].inventory.append(char.armor)
          char.armor = CreatingArmors.createArmor("None")
      
        elif char.gadget.name == curItem:
          Data.pOverview[curAuthor].inventory.append(char.gadget)
          char.gadget = CreatingGadgets.createGadget("None")
        else:
          em = discord.Embed(title = "Error", description = "You don't have that item equipped!", color = Colors.red)
          await message.channel.send(embed = em)
          return

        char.resetStats()
        em = discord.Embed(title = "Unequip", description = "You successfully unequipped your " + curItem + "!", color = Colors.green)
        await message.channel.send(embed = em)
        return



  if words[0] == "admin":

    if curAuthor not in Data.admins:
      em = discord.Embed(title = "Error", description = "You must be an admin to run admin commands!", color = Colors.red)
      await message.channel.send(embed = em)
      return

    command = words[1]

    if command == "give":

      player = words[2]
      if player not in Data.playingNames:
        return

      curItem = " ".join(words[3:])
      rCurItem = ""
      if ItemsToTypes.itemType[curItem] == "weapon":
        rCurItem = CreatingWeapons.createWeapon(curItem)
      elif ItemsToTypes.itemType[curItem] == "ability":
        rCurItem = CreatingAbilities.createAbility(curItem)
      elif ItemsToTypes.itemType[curItem] == "armor":
        rCurItem = CreatingArmors.createArmor(curItem)
      elif ItemsToTypes.itemType[curItem] == "gadget":
        rCurItem = CreatingGadgets.createGadget(curItem)
      Data.pOverview[Data.namesToTags[player]].inventory.append(rCurItem)
      em = discord.Embed(title = "Giving Item (Admin)", description = "You successfully gave " + curItem + " to **" + player + "**!", color = Colors.green)
      await message.channel.send(embed = em)
      return
    
    return
    
    
  
  # test command to see if the bot is up and running
  if words[0] == "toasty":
    em = discord.Embed(title = "Toasty", description = "toasty!", color = Colors.black)
    await message.channel.send(embed = em)
    return


    
  # joining for the first time
  if words[0] == "start":
    if curAuthor in Data.playing:
      em = discord.Embed(title = "Error", description = Text.alreadyPlaying, color = Colors.red)
      await message.channel.send(embed = em)
      return

    em = discord.Embed(title = "Enter Name", description = Text.enterName, color = Colors.navy)
    await message.channel.send(embed = em)
    Data.commandQueue[curAuthor] = ["name"]
    Data.playing.append(curAuthor)
    return
    
              

#keep_alive()
# the above line is for later use when I want to host it 24/7


my_secret = os.environ['TOKEN']
client.run(my_secret)