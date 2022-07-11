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
admins = ["ToastyDreams#9785"] # admins

playerLimits = {
  "Chicken's Den" : 2,
  "Thieves Hideout" : 5
}



classes = ["warrior", "knight", "priest", "mage", "jester", "assassin"] # classes
dungeons = ["chicken's den", "your mom's basement", "the endless void", "toasty's temple", "toasty's castle"] # dungeons



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