import game_global
import physics
import game_object_factory

tileMap = game_global.tileMap
minionImgs = game_global.minionImgs

sizeFactor = game_global.sizeFactor
gameHeight = game_global.gameHeight
gameWidth = game_global.gameWidth

runSpeed = 150
maxRunDist = 200

def drawMinions(imgManager):
    global sizeFactor

    for minion in game_global.minions:
        spriteComponent = minion.getComponent('minion_sprite')
        posComponent = minion.getComponent('minion_position')
        attrComponent = minion.getComponent('minion_attributes')

        imgManager.RenderSprite(spriteComponent.spriteId, spriteComponent.iCurrentFrame
            , posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor), not attrComponent.direction, False)

def createMinion(x, y):
    minion = game_object_factory.createMinion('minion' + str(game_global.minionId), 'monster', [200] * 12, 0, 0
        , 3, x, y, runSpeed, 0, True, 'run', maxRunDist)
    game_global.minions.append(minion)
    game_global.minionId += 1

def createMinions():
    global sizeFactor
    global tileMap

    for i, row in enumerate(tileMap):
        for j, tile in enumerate(row):
            if tile in minionImgs:
                minion = game_object_factory.createMinion('minion' + str(game_global.minionId), 'monster', [200] * 12, 0, 0
                    , 3, int(j * 32 * sizeFactor), int((i + 1) * 32 * sizeFactor), runSpeed, 0, True, 'run', maxRunDist)
                game_global.minions.append(minion)
                game_global.minionId += 1

def updateMinions(dt):
    newMinions = []

    for minion in game_global.minions:
        posComponent = minion.getComponent('minion_position')
        velComponent = minion.getComponent('minion_velocity')
        attrComponent = minion.getComponent('minion_attributes')
        spriteComponent = minion.getComponent('minion_sprite')
        runDistComponent = minion.getComponent('minion_run_dist')

        if attrComponent.objectState == 'floating' and minion.entityId in game_global.minionBubbleMap:
            bubbleId = game_global.minionBubbleMap[minion.entityId]

            bubble = _findBubbleById(bubbleId)

            # if bubble disappear, so does minion
            if bubble is None:
                del game_global.minionBubbleMap[minion.entityId]
                game_global.scores += 500
                continue
            # else
            else:
                bubblePosComponent = bubble.getComponent('bubble_position')

                posComponent.x = bubblePosComponent.x
                posComponent.y = bubblePosComponent.y
            
        if attrComponent.objectState == 'run':
            _updateMinionX(dt, velComponent, posComponent, attrComponent, runDistComponent)

        if attrComponent.objectState == 'falling' and velComponent.yVel != 0:
            _updateMinionFalling(velComponent, posComponent, spriteComponent, attrComponent) 

        if attrComponent.objectState == 'run' and not physics.checkCollisionBottom(posComponent, int(32 * sizeFactor)):
            attrComponent.objectState = 'falling'
            velComponent.yVel = 2.7
        elif attrComponent.objectState == 'run' and physics.checkCollisionBottom(posComponent, int(32 * sizeFactor)):
            _runAnimation(spriteComponent)
        
        newMinions.append(minion)
    
    game_global.minions = newMinions

def _findBubbleById(bubbleId):
    for bubble in game_global.bubbles:
        if bubble.entityId == bubbleId:
            return bubble
    return None

def _updateMinionX(dt, velComponent, posComponent, attrComponent, runDistComponent):
    global gameWidth
    global sizeFactor

    dx = dt * velComponent.xVel

    if attrComponent.objectState == 'run':
        while physics.checkCollisionTileLeftRight(posComponent.x + int(dx), posComponent.y, int(32 * sizeFactor)):
            if dx > 0:
                dx -= 1
            else: 
                dx += 1

        posComponent.x += int(dx)
        runDistComponent.currentDistance += abs(int(dx))
        if runDistComponent.currentDistance >= runDistComponent.maxDistance or int(dx) == 0:
            attrComponent.direction = not attrComponent.direction
            velComponent.xVel = -velComponent.xVel
            runDistComponent.currentDistance = 0

        # adjust to move out of left bound and right bound
        physics.moveOutOfLeftRightBound(posComponent, int(32 * sizeFactor))


def _runAnimation(spriteComponent):
    spriteComponent.update()

def _updateMinionFalling(velComponent, posComponent, spriteComponent, attrComponent):
    global sizeFactor

    if attrComponent.objectState == 'falling':
        _updateMinionY(velComponent.yVel, posComponent)
        if not physics.checkCollisionBottom(posComponent, int(32 * sizeFactor)):
            velComponent.yVel *= 1.05
            if velComponent.yVel > 7.65 * sizeFactor:
                velComponent.yVel = 7.65 * sizeFactor

            spriteComponent.iCurrentFrame = 8
        else:
            _touchGround(velComponent, posComponent, spriteComponent, attrComponent)

def _updateMinionY(yVel, posComponent):
    posComponent.y += int(yVel)

def _touchGround(velComponent, posComponent, spriteComponent, attrComponent):
    global sizeFactor

    attrComponent.objectState = 'run'
    spriteComponent.iCurrentFrame = 0
    _runAnimation(spriteComponent)
    velComponent.yVel = 0

    # make player stand on ground
    posComponent.y = posComponent.y // int(32 * sizeFactor) * int(32 * sizeFactor)