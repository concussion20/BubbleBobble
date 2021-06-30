# global variables for BubbleBobble game

openingEnd = False
gameWon = False

sizeFactor = 1.5
gameWidth = int(800 * sizeFactor)
gameHeight = int(736 * sizeFactor)

minFrameTicks = 16

# game objects
tileMap = []
minions = []
items = []
bubbles = []
player = None
scores = 0

# key:minionId, value: bubbleId
minionBubbleMap = {}

# game object images
tileImgs = [] 
itemImgs = []
minionImgs = []

minionId = 1
itemId = 1
bubbleId = 1