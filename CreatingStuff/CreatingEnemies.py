from Classes.Enemy import Enemy as Enemy

# name, att, defense, hp, maxHp, mp, maxMp, speed

def miniChicken():
  return Enemy("Mini Chicken", 1, 1, 10, 10, 0, 0, 0)

def motherHen():
  return Enemy("Mother Hen", 5, 5, 25, 25, 0, 0, 0)

def thief():
  return Enemy("Thief", 15, 15, 30, 30, 0, 0, 0)