import game_global
import physics
import game_object_factory
from CPP.system import physics_system

sizeFactor = game_global.sizeFactor
gameWidth = game_global.gameWidth
gameHeight = game_global.gameHeight

bubbleSpeed = 200
maxHorizontalDist = 300
maxVerticalDist = 300

def createBubble(player, musicManager, renderer):
    attrComponent = player.getComponent('player_attributes')
    posComponent = player.getComponent('player_position')
    spriteComponent = player.getComponent('player_sprite')

    if attrComponent.objectState == 'dead' or attrComponent.objectState == 'newborn':
        return

    bubble = game_object_factory.createBubble('bubble' + str(game_global.bubbleId), 'bubble'
        , posComponent.x + (1 if attrComponent.direction else -1) * int(32 * sizeFactor)
        , posComponent.y, (1 if attrComponent.direction else -1) * bubbleSpeed
        , 0, True, 'forwarding', maxHorizontalDist)
    game_global.bubbles.append(bubble)
    game_global.bubbleId += 1

    # update player state accordingly
    if attrComponent.objectState == 'run' or attrComponent.objectState == 'static': 
        attrComponent.objectState = 'bubble'
    elif attrComponent.objectState == 'jumping': 
        attrComponent.objectState = 'jumping_bubble'
    elif attrComponent.objectState == 'falling': 
        attrComponent.objectState = 'falling_bubble'

    spriteComponent.lTimePassed = renderer.getTicks()

    musicManager.PlaySound('bubble')

def drawBubbles(imgManager):
    for bubble in game_global.bubbles:
        posComponent = bubble.getComponent('bubble_position')
        imgComponent = bubble.getComponent('bubble_image')
        imgManager.RenderTile(imgComponent.imgId, posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor), False, False)

def updateBubbles(dt):
    newBubbles = []

    for bubble in game_global.bubbles:
        posComponent = bubble.getComponent('bubble_position')
        velComponent = bubble.getComponent('bubble_velocity')
        attrComponent = bubble.getComponent('bubble_attributes')
        distComponent = bubble.getComponent('bubble_dist')

        if attrComponent.objectState == 'forwarding':
            posComponent.x += int(velComponent.xVel * dt)
            distComponent.currentDistance += abs(int(velComponent.xVel * dt))
            if distComponent.currentDistance >= distComponent.maxDistance:
                attrComponent.objectState = 'floating'

                velComponent.xVel = 0
                velComponent.yVel = -bubbleSpeed

                distComponent.currentDistance = 0
                distComponent.maxDistance = maxVerticalDist
            newBubbles.append(bubble)
        elif attrComponent.objectState == 'floating':
            posComponent.y += int(velComponent.yVel * dt)
            distComponent.currentDistance += abs(int(velComponent.yVel * dt))
            if distComponent.currentDistance < distComponent.maxDistance:
                newBubbles.append(bubble)
        
        _checkCollideMinion(bubble)
    
    game_global.bubbles = newBubbles

def _checkCollideMinion(bubble):
    posComponent = bubble.getComponent('bubble_position')
    velComponent = bubble.getComponent('bubble_velocity')
    attrComponent = bubble.getComponent('bubble_attributes')
    distComponent = bubble.getComponent('bubble_dist')

    if attrComponent.objectState == 'floating':
        return

    for minion in game_global.minions:
        minionPosComponent = minion.getComponent('minion_position')
        minionAttrComponent = minion.getComponent('minion_attributes')
        minionSpriteComponent = minion.getComponent('minion_sprite')

        if minionAttrComponent.isCollidable and minionAttrComponent.objectState != 'floating' \
            and physics_system.PhysicsSystem.AABBCollision(posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor)
            , minionPosComponent.x, minionPosComponent.y, int(32 * sizeFactor), int(32 * sizeFactor)):
                circleMinion(minion.entityId, minionAttrComponent, minionSpriteComponent, bubble.entityId, velComponent, attrComponent, distComponent)
                break

def circleMinion(minionId, minionAttrComponent, minionSpriteComponent, bubbleId, velComponent, attrComponent, distComponent):
    minionAttrComponent.objectState = 'floating'
    minionAttrComponent.isCollidable = False
    minionSpriteComponent.iCurrentFrame = 12

    attrComponent.objectState = 'floating'
    velComponent.xVel = 0
    velComponent.yVel = -bubbleSpeed
    distComponent.currentDistance = 0
    distComponent.maxDistance = maxVerticalDist

    game_global.minionBubbleMap[minionId] = bubbleId
