import game_global

tileMap = game_global.tileMap
tileImgs = game_global.tileImgs
gameHeight = game_global.gameHeight
gameWidth = game_global.gameWidth

def checkCollisionBottom(posComponent, size):
    global tileImgs
    global gameHeight
    global tileMap

    x = posComponent.x
    y = posComponent.y

    if y < size:
        return False

    row, col = getPosInTileMap(x, y, size)

    # fall out of screen
    if y >= gameHeight and (tileMap[len(tileMap) - 1][col] == 'empty' or tileMap[len(tileMap) - 1][col] not in tileImgs):
        posComponent.y = -size
        return False

    if y > gameHeight - 2 * size:
        if x % size == 0 and (tileMap[len(tileMap) - 1][col] == 'empty' or tileMap[len(tileMap) - 1][col] not in tileImgs):
            return False
        elif x % size != 0 and (tileMap[len(tileMap) - 1][col] == 'empty' or tileMap[len(tileMap) - 1][col] not in tileImgs) \
            and (tileMap[len(tileMap) - 1][col + 1] == 'empty' or tileMap[len(tileMap) - 1][col + 1] not in tileImgs):
            return False

    # to avoid list index out of range
    if row >= len(tileMap) - 1:
        return False

    if x % size == 0:
        return (tileMap[row + 1][col] != 'empty' and tileMap[row + 1][col] in tileImgs) and (tileMap[row][col] == 'empty' or tileMap[row][col] not in tileImgs)
    else:
        return (tileMap[row][col] == 'empty' or tileMap[row][col] not in tileImgs) and (tileMap[row][col + 1] == 'empty' or tileMap[row][col + 1] not in tileImgs) \
            and ((tileMap[row + 1][col] != 'empty' and tileMap[row + 1][col] in tileImgs) or (tileMap[row + 1][col + 1] != 'empty' and tileMap[row + 1][col + 1] in tileImgs))

def checkCollisionTileLeftRight(x, y, size):
    global tileImgs
    global tileMap
    global gameWidth

    if x < 0 or x > gameWidth - size:
        return True

    row, col = getPosInTileMap(x, y, size)
    if x % size == 0:
        return tileMap[row][col] != 'empty' and tileMap[row][col] in tileImgs
    else:
        return (tileMap[row][col] != 'empty' and tileMap[row][col] in tileImgs) or (tileMap[row][col + 1] != 'empty' and tileMap[row][col + 1] in tileImgs)
    
def getPosInTileMap(x, y, size):
    return (y // size - 1, x // size)

# Assumption: left bound and right bound should have exact width as 1
def moveOutOfLeftRightBound(posComponent, size):
    global tileMap

    row, col = getPosInTileMap(posComponent.x, posComponent.y, size)

    leftBound = 1
    rightBound = len(tileMap[0]) - 2
    # while leftBound < len(tileMap[0]):
    #     if tileMap[row][leftBound] != 'empty' and tileMap[row][leftBound] in tileImgs:
    #         leftBound += 1
    #     else:
    #         break
    
    # while rightBound >= 0:
    #     if tileMap[row][rightBound] != 'empty' and tileMap[row][rightBound] in tileImgs:
    #         rightBound -= 1
    #     else:
    #         break
    
    # assert leftBound <= rightBound
    
    if col < leftBound:
        posComponent.x = size * leftBound
    elif col >= rightBound: 
        posComponent.x = size * rightBound
