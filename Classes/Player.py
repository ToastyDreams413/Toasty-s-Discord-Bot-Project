# Player class
class Player:
  def __init__(self, name):
    self.name = name # player's name
    self.chars = [] # characters of this player
    self.charSlots = 2 # max number of characters this player can have
    self.gold = 0 # the amount of gold this player has
    self.cUnlocked = ["warrior"] # classes unlocked by this player
    self.dUnlocked = ["chicken's den"] # dungeons unlocked by this player
    self.details = [] # other details/things to track
    self.dCompleted = {} # dungeons done
    self.cuties = 0 # special currency
    self.inventory = []
    self.selected = "None"