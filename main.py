from CPP import resource_manager
from CPP.resource_manager import img_manager, music_manager, font_manager, level_manager
from CPP.system import renderer_system, input_system
import time
from threading import Thread
import player_action
import minion_action
import bubble_action
import game_object_factory
import game_global


# in module refs to global variables
sizeFactor = game_global.sizeFactor


# for editor use
class Editor:
    def __init__(self):
        self.tileId = None
        self.tileMap = None

tileEditor = Editor()



# helper functions
# 
def createItem(tileId, x, y):
    item = game_object_factory.createItem('item' + str(game_global.itemId), tileId, x, y, 0, 0, True, 'not eaten')
    game_global.items.append(item)
    game_global.itemId += 1

def createItems():
    for i, row in enumerate(game_global.tileMap):
        for j, tile in enumerate(row):
            if tile in game_global.itemImgs:
                item = game_object_factory.createItem('item' + str(game_global.itemId), tile, int(j * 32 * sizeFactor), int((i + 1) * 32 * sizeFactor), 0, 0, True, 'not eaten')
                game_global.items.append(item)
                game_global.itemId += 1

def removeItemByPos(x, y, oldTileId):
    for i, item in enumerate(game_global.items):
        posComponent = item.getComponent('item_position')
        imgComponent = item.getComponent('item_image')

        if posComponent.x == x and posComponent.y == y:
            # and imgComponent.imgId == oldTileId:
            game_global.items.pop(i)
            return 

def drawItems(imgManager):
    for item in game_global.items:
        posComponent = item.getComponent('item_position')
        imgComponent = item.getComponent('item_image')
        imgManager.RenderTile(imgComponent.imgId, posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor), False, False)

def drawMap(imgManager):
    for i, row in enumerate(game_global.tileMap):
        for j, tile in enumerate(row):
            if tile in game_global.tileImgs:
                imgManager.RenderTile(tile, int(j * 32 * sizeFactor), int((i + 1) * 32 * sizeFactor), int(32 * sizeFactor), int(32 * sizeFactor), False, False)

def drawScores(fontManager):
    fontManager.RenderText(str(game_global.scores) if game_global.scores >= 10 else '0' + str(game_global.scores), int(100 * sizeFactor), int(5 * sizeFactor), int(28 * sizeFactor), 255, 255, 255)
    fontManager.RenderText("00", int((800 - 100) * sizeFactor), int(5 * sizeFactor), int(28 * sizeFactor), 255, 255, 255)

def drawLogo(imgManager):
    imgManager.RenderTexture("logo", int(100 * sizeFactor), int(100 * sizeFactor), int(600 * sizeFactor), int(422 * sizeFactor), False, False)

def drawWin(fontManager):
    fontManager.RenderText('You', int(100 * sizeFactor), int(150 * sizeFactor), int(180 * sizeFactor), 17, 85, 204)
    fontManager.RenderText('Win', int(100 * sizeFactor), int(350 * sizeFactor), int(180 * sizeFactor), 17, 85, 204)

def opening():
    time.sleep(3)
    game_global.openingEnd = True
    print('Opening end now!')

def checkGameEnd():
    return len(game_global.items) == 0 and len(game_global.minions) == 0

# game win
def gameEnd():
    print('You have won!')
    time.sleep(3)
    game_global.gameWon = False
    game_global.scores = 0
    

def resetGame(levelManager):
    # load new level
    game_global.tileMap.clear()
    game_global.tileMap.extend(levelManager.getLevelLayout('level1'))
    tileEditor.tileMap = game_global.tileMap

    # game objects
    game_global.player = player_action.createPlayer()
    minion_action.createMinions()
    createItems()

# main function
def main():
    # game window
    gameWindow = renderer_system.RendererSystem.getInstance("BubbleBobble", int(100 * sizeFactor)
        , int(100 * sizeFactor), game_global.gameWidth, game_global.gameHeight)

    resourceManager = resource_manager.ResourceManager.getInstance()
    resourceManager.startUp(gameWindow)
    
    # load images
    imgManager = resourceManager.getImgManager()
    imgManager.loadTexture("logo", "Assets/image/BubbleBobbleLogo.png")
    imgManager.loadTexture("dragon", "Assets/image/dragon.png")
    imgManager.loadTexture("dragon_blue", "Assets/image/Bubble Dragons.png")
    imgManager.loadTexture("monster", "Assets/image/mon_zen-chan.png")
    imgManager.loadTexture("tile_pink", "Assets/image/Wall1.png")
    imgManager.loadTexture("apple", "Assets/image/apple.png")
    imgManager.loadTexture("banana", "Assets/image/banana.png")
    imgManager.loadTexture("bubble", "Assets/image/Bubble_sprites.png")
    imgManager.loadTexture("tiles", "Assets/image/post-26314-0-12461100-1341952532.png")
    
    imgManager.loadTile("tile_pink", "Tile", 0, 0, 16, 16, "tile_pink")
    imgManager.loadTile("tile_blue", "Tile", 138, 209, 16, 16, "tiles")
    imgManager.loadTile("item_banana", "Item", 0, 0, 64, 64, "banana")
    imgManager.loadTile("item_apple", "Item", 0, 0, 64, 64, "apple")
    imgManager.loadTile("bubble", "Custom", 144, 0, 24, 24, "bubble")

    imgManager.loadSprite("dragon", "Player", ["dragon"] * 29
        , [0, 25, 50, 75, 100, 125,  0, 25, 100, 125, 150, 175,  0, 25, 50, 75, 100, 125, 150, 175,  0, 25, 50, 75, 100, 125, 150, 175, 200]
        , [100, 100, 100, 100, 100, 100,  125, 125, 125, 125, 125, 125,  75, 75, 75, 75, 75, 75, 75, 75,  50, 50, 50, 50, 50, 50, 50, 50, 25]
        , [25] * 29, [25] * 29)
    # imgManager.loadSprite("dragon_blue", "Player", ["dragon_blue"] * 6
    #     , [90, 120, 150, 180, 210, 240]
    #     , [120] * 6
    #     , [30] * 6, [30] * 6)
    imgManager.loadSprite("monster", "Minion", ["monster"] * 13
        , [0, 32, 64, 96, 0, 32, 64, 96, 0, 32, 64, 96, 128], [436, 436, 436, 436, 404, 404, 404, 404, 372, 372, 372, 372, 372]
        , [32] * 13, [32] * 13)

    game_global.tileImgs.extend(['empty', 'tile_pink', 'tile_blue'])
    game_global.itemImgs.extend(['item_banana', 'item_apple'])
    game_global.minionImgs.extend(['monster'])

    # load musics
    musicManager = resourceManager.getMusicManager()
    musicManager.loadMusic("themesong", "Assets/music/themesong.mp3")
    musicManager.loadMusic("menu", "Assets/music/menu.mp3")
    musicManager.loadSound("bubble", "Assets/sound/bubble.wav")
    musicManager.loadSound("jump", "Assets/sound/jump.wav")
    musicManager.loadSound("eat_item", "Assets/sound/eat_item.wav")
    musicManager.loadSound("dead", "Assets/sound/dead.wav")

    musicManager.PlayMusic("themesong")

    # load font
    fontManager = resourceManager.getFontManager()

    # load levels
    levelManager = resourceManager.getLevelManager()
    levelManager.loadLevel('level1', 'Assets/level/level1.txt')

    # main loop
    inputSystem = input_system.InputSystem.getInstance()


    # start "opening" sub-thread
    Thread(target=opening, args=[]).start()

    resetGame(levelManager)

    running = True
    buttons = [False, False, False, False]
    lastTimeTick = gameWindow.getTicks()

    while (running):
        key = inputSystem.getPressedKey()

        if not game_global.openingEnd:
            pass
        elif game_global.gameWon:
            pass
        elif key == 'Quit':
            running = False
        elif key == 'SDL_BUTTON_LEFT':
            # handle editor events
            # 
            x, y = inputSystem.getMousePosition()
            x, y = x // int(32 * sizeFactor), y // int(32 * sizeFactor) - 1
            # if tile, item, minion, add them
            # can only add minion, not remove
            if tileEditor.tileId is not None \
                and (tileEditor.tileId in game_global.tileImgs or tileEditor.tileId in game_global.itemImgs or tileEditor.tileId in game_global.minionImgs) \
                and y >= 0 \
                and game_global.tileMap[y][x] not in game_global.minionImgs: 

                oldTileId = game_global.tileMap[y][x]
                game_global.tileMap[y][x] = tileEditor.tileId

                # if add minion, new an object
                if tileEditor.tileId in game_global.minionImgs:
                    minion_action.createMinion(int(x * 32 * sizeFactor), int((y + 1) * 32 * sizeFactor))
                # if add item, new an object
                if tileEditor.tileId in game_global.itemImgs and tileEditor.tileId != oldTileId:
                    createItem(tileEditor.tileId, int(x * 32 * sizeFactor), int((y + 1) * 32 * sizeFactor))
                # if clear item, remove it from global item list too
                if oldTileId in game_global.itemImgs and tileEditor.tileId != oldTileId:
                    removeItemByPos(int(x * 32 * sizeFactor), int((y + 1) * 32 * sizeFactor), oldTileId)

        elif key == 'SDLK_LEFT_down':
            buttons[0] = True
        elif key == 'SDLK_RIGHT_down':
            buttons[1] = True
        elif key == 'SDLK_LEFT_up':
            buttons[0] = False
        elif key == 'SDLK_RIGHT_up':
            buttons[1] = False
        elif key == 'SDLK_UP_down':
            buttons[2] = True
        elif key == 'SDLK_SPACE_down':
            buttons[3] = True

        if buttons[0]:
            player_action.changeRunSpeed(game_global.player, False, True)
        elif buttons[1]:
            player_action.changeRunSpeed(game_global.player, True, True)
        else:
            # the second arg will be ignored
            player_action.changeRunSpeed(game_global.player, True, False)

        if buttons[2]:
            player_action.startJump(game_global.player, musicManager)
            buttons[2] = False
        if buttons[3]:
            bubble_action.createBubble(game_global.player, musicManager, gameWindow)
            buttons[3] = False

        # cap FPS to 60
        curTimeTick = gameWindow.getTicks()
        dt = curTimeTick - lastTimeTick
        if dt < game_global.minFrameTicks:
            gameWindow.delay(game_global.minFrameTicks - dt)
        dt = game_global.minFrameTicks / 1000
        lastTimeTick = gameWindow.getTicks()

        if game_global.openingEnd and not game_global.gameWon:
            bubble_action.updateBubbles(dt)
            minion_action.updateMinions(dt)
            player_action.updatePlayer(game_global.player, dt, gameWindow, musicManager)

        # draw
        gameWindow.clear()
        
        drawMap(imgManager)
        drawScores(fontManager)

        player_action.drawPlayer(game_global.player, imgManager, gameWindow)
        bubble_action.drawBubbles(imgManager)
        minion_action.drawMinions(imgManager)
        drawItems(imgManager)

        if not game_global.openingEnd:
            drawLogo(imgManager)
        if game_global.gameWon:
            drawWin(fontManager)

        gameWindow.flip()

        if checkGameEnd():
            game_global.gameWon = True
            Thread(target=gameEnd, args=[]).start()
            resetGame(levelManager)
            buttons = [False, False, False, False]
            lastTimeTick = gameWindow.getTicks()


if __name__ == "__main__":
    main()
