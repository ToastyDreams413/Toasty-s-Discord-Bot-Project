# keeps track of most of the text

import Main.Data as Data

alreadyPlaying = "You're already playing!"
enterName = "Enter your name"

notPlaying = "It doesn't seem like you play yet! Use " + Data.prefix + "start to start playing."
takenName = "Sorry, that name has already been taken, please try again"

classNotUnlocked = "You haven't unlocked that class yet!"
classNoExist = "That class doesn't exist!"
fullCharSlots = "You're full on character slots!"

help = "The command prefix is: **" + str(Data.prefix) + "**\n\n**start** - registers you into the game database so you can start playing\n**create [class]** - creates a character of [class] if you've unlocked that class *and* you have at least one spare character slot\n**run [dungeon name]** - enters you into the dungeon [dungeon name] if you've unlocked that dungeon\n**stats** - shows you the stats for your selected class\n**equipment** - shows you what equipment you have on your selected class\n**overview** - tells you what classes and dungeons you've unlocked, and an overview of your playing\n**equip [item name]** - equip an item\n**unequip [item name]** - unequip an item\n**inv** - view your inventory\n**party [name]** - invite [name] to your party, if they play (use !help party for more party commands)\n**help [something]** - specify [something] you want more information or help on, such as: *stats*, *dungeons*, or *party*\n**report [message]** - report a bug by typing a message, the developer will be notified and see [message]"

helpStats = "**HP** - your health points; the more health you have, the more damage you can tank before dying\n**MP** - your magic points, for using abilities\n**attack** - your attack; the more attack you have, the more damage you deal\n**defense** - your defense; the more defense you have, the less damage you take per hit on non armor-piercing attack\n**speed** - your speed; higher speed means higher chance for enemy attacks to completely miss you\n**luck** - your luck; higher luck means better loot from dungeons"

helpWeapons = "[weapons help goes here]"

helpArmors = "[armors help goes here]"

helpAbilities = "[abilities help goes here]"

helpDungeons = "In dungeons, you don't need to use the prefix " + str(Data.prefix) + " to run commands.\n\n**attack** - attack an enemy (you will be asked who you want to attack)\n**ability** - use your ability, if you have enough MP\n**pstats** - view the overview stats for your party (if you are alone, it'll just show yourself\n**pstats [name]** - shows you a more detailed stats overview for player [name], if they are in the dungeon with you\n**estats** - view the overview stats for the enemies in the dungeon\n**estats [name]** - view a more detailed stats overview for the enemy [name], if they are an enemy in the dungeon"

helpClasses = "[classes help goes here]"

helpParty = "**party** - see the members of your current party\n**party [name]** - invite [name] to your party\n**pdisband** - disband the party\n**pleave** - leave the party\n**pkick [name]** - kick [name] from the party"

helpNotFound = "Sorry, I couldn't find anything for you there."

warriorCreated = "You've successfully created a warrior character! You start off at level 1 with 5 attack, 5 defense, 50 health, 20 MP, 5 speed, and 0 luck. Go out there and conquer some dungeons!"