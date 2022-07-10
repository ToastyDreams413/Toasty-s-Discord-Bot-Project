# keeps track of most of the text

import Main.Data as Data

alreadyPlaying = "You're already playing!"
enterName = "Enter your name"

notPlaying = "It doesn't seem like you play yet! Use " + Data.prefix + "start to start playing."
takenName = "Sorry, that name has already been taken, please try again"

classNotUnlocked = "You haven't unlocked that class yet!"
classNoExist = "That class doesn't exist!"
fullCharSlots = "You're full on character slots!"

help = "The command prefix is: **" + str(Data.prefix) + "**\n\n**start** - registers you into the game database so you can start playing\n**create [class]** - creates a character of [class] if you've unlocked that class *and* you have at least one spare character slot\n**run [dungeonName]** - enters you into the dungeon [dungeonName] if you've unlocked that dungeon\n**stats [class]** - if you have a character as [class], shows you its stats overview\n**equipment [class]** - if you have a character as [class], shows you what equipment you have on them\n**overview** - tells you what classes and dungeons you've unlocked, and an overview of your playing\n**help [something]** - specify [something] you want more information or help on, ex: *help stats* or *help weapons*"

helpStats = "[stats help goes here]"

helpWeapons = "[weapons help goes here]"

helpArmors = "[armors help goes here]"

helpAbilities = "[abilities help goes here]"

helpDungeons = "[dungeons help goes here]"

helpClasses = "[classes help goes here]"

helpNotFound = "Sorry, I couldn't find anything for you there."

warriorCreated = "You've successfully created a warrior character! You start off at level 1 with 5 attack, 5 defense, 50 health, 20 MP, 5 speed, and 0 luck. Go out there and conquer some dungeons!"