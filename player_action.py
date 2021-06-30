import game_global
import physics
import game_object_factory
from CPP.system import physics_system

sizeFactor = game_global.sizeFactor
gameWidth = game_global.gameWidth
gameHeight = game_global.gameHeight

runSpeed = 200
deathPeriod = 2000
newBornPeriod = 600
spitBubblePeriod = 300

def createPlayer():
    player = game_object_factory.createPlayer("player", "dragon", [0] * 12, 0, 0, 5, int(3.5 * 32 * sizeFactor)
        , gameHeight - int(32 * 2 * sizeFactor), 0, 0, True, "static")
    return player

def changeRunSpeed(player, direction, isRuning):
    velComponent = player.getComponent('player_velocity')
    attrComponent = player.getComponent('player_attributes')

    if attrComponent.objectState == 'dead' or attrComponent.objectState == 'newborn':
        return 
    elif isRuning:
        # attrComponent.objectState = 'run'
        attrComponent.direction = direction
        velComponent.xVel = (1 if direction else -1) * runSpeed
    else: 
        velComponent.xVel = 0
    
def drawPlayer(player, imgManager, renderer):
    global sizeFactor

    spriteComponent = player.getComponent('player_sprite')
    posComponent = player.getComponent('player_position')
    attrComponent = player.getComponent('player_attributes')

    if attrComponent.objectState == 'newborn':
        curTicks = renderer.getTicks()
        dt = curTicks - spriteComponent.lTimePassed
        if (dt > 0 and dt < 100) or (dt > 200 and dt < 300) or (dt > 400 and dt < 500):
            imgManager.RenderSprite(spriteComponent.spriteId, spriteComponent.iCurrentFrame
                , posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor), not attrComponent.direction, False)
    else:
        imgManager.RenderSprite(spriteComponent.spriteId, spriteComponent.iCurrentFrame
            , posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor), not attrComponent.direction, False)

def updatePlayer(player, dt, renderer, musicManager):
    global sizeFactor

    # update run
    posComponent = player.getComponent('player_position')
    velComponent = player.getComponent('player_velocity')
    attrComponent = player.getComponent('player_attributes')
    spriteComponent = player.getComponent('player_sprite')
    distComponent = player.getComponent('player_jump_dist')

    if attrComponent.objectState == 'dead' and renderer.getTicks() - spriteComponent.lTimePassed < deathPeriod:
        return
    elif attrComponent.objectState == 'dead' and renderer.getTicks() - spriteComponent.lTimePassed >= deathPeriod:
        _makeNewBorn(posComponent, velComponent, attrComponent, spriteComponent, renderer)
        return
    elif attrComponent.objectState == 'newborn' and renderer.getTicks() - spriteComponent.lTimePassed < newBornPeriod:
        return
    elif attrComponent.objectState == 'newborn' and renderer.getTicks() - spriteComponent.lTimePassed >= newBornPeriod:
        velComponent.xVel = velComponent.yVel = 0
        attrComponent.objectState = 'static'
        spriteComponent.iCurrentFrame = 0
        return 

    # when jumping or falling, yVel will never be 0
    if attrComponent.objectState == 'bubble' and renderer.getTicks() - spriteComponent.lTimePassed < spitBubblePeriod:
        spriteComponent.iCurrentFrame = 11
    elif attrComponent.objectState == 'bubble' and renderer.getTicks() - spriteComponent.lTimePassed >= spitBubblePeriod:
        attrComponent.objectState = 'static'
        spriteComponent.iCurrentFrame = 0
    elif velComponent.xVel == 0 and velComponent.yVel == 0:
        attrComponent.objectState = 'static'
        spriteComponent.iCurrentFrame = 0

    if velComponent.xVel != 0 and velComponent.yVel == 0:
        attrComponent.objectState = 'run'

    # update x (possibly in run, jumping, falling state)
    if velComponent.xVel != 0:
        _updatePlayerX(velComponent.xVel * dt, posComponent, attrComponent)
    
    # update jump
    if velComponent.yVel != 0:
        _updatePlayerJump(velComponent, posComponent, distComponent, spriteComponent, attrComponent, renderer) 

    if attrComponent.objectState == 'run' and not physics.checkCollisionBottom(posComponent, int(32 * sizeFactor)):
        attrComponent.objectState = 'falling'
        velComponent.yVel = 2.7
    elif attrComponent.objectState == 'run' and physics.checkCollisionBottom(posComponent, int(32 * sizeFactor)):
        _runAnimation(abs(velComponent.xVel), spriteComponent, renderer)

    _checkCollideItem(posComponent, attrComponent, musicManager)
    _checkCollideMinion(player, musicManager, renderer)


def startJump(player, musicManager):
    global sizeFactor

    velComponent = player.getComponent('player_velocity')
    attrComponent = player.getComponent('player_attributes')
    distComponent = player.getComponent('player_jump_dist')
    spriteComponent = player.getComponent('player_sprite')

    if attrComponent.objectState == 'dead' or attrComponent.objectState == 'newborn' or velComponent.yVel != 0:
        return

    velComponent.yVel = -7.65 * sizeFactor
    attrComponent.objectState = 'jumping'
    distComponent.maxDistance = int(32 * 3 * sizeFactor + 24 * sizeFactor)
    distComponent.currentDistance = 0
    spriteComponent.iCurrentFrame = 12

    musicManager.PlaySound('jump')

def _checkCollideItem(posComponent, attrComponent, musicManager):
    if attrComponent.objectState == 'dead':
        return

    newItems = []
    for item in game_global.items:
        itemPosComponent = item.getComponent('item_position')
        itemAttrComponent = item.getComponent('item_attributes')

        if itemAttrComponent.isCollidable and itemAttrComponent.objectState == 'not eaten' \
            and physics_system.PhysicsSystem.AABBCollision(posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor)
            , itemPosComponent.x, itemPosComponent.y, int(32 * sizeFactor), int(32 * sizeFactor)):
                game_global.scores += 200
                musicManager.PlaySound('eat_item')
        else:
            newItems.append(item)
    
    game_global.items = newItems

def _checkCollideMinion(player, musicManager, renderer):
    posComponent = player.getComponent('player_position')
    velComponent = player.getComponent('player_velocity')
    attrComponent = player.getComponent('player_attributes')
    spriteComponent = player.getComponent('player_sprite')

    if attrComponent.objectState == 'newborn' or attrComponent.objectState == 'dead':
        return

    for minion in game_global.minions:
        minionPosComponent = minion.getComponent('minion_position')
        minionAttrComponent = minion.getComponent('minion_attributes')

        if minionAttrComponent.isCollidable and minionAttrComponent.objectState != 'floating' \
            and physics_system.PhysicsSystem.AABBCollision(posComponent.x, posComponent.y, int(32 * sizeFactor), int(32 * sizeFactor)
            , minionPosComponent.x, minionPosComponent.y, int(32 * sizeFactor), int(32 * sizeFactor)):
                _makeDead(velComponent, attrComponent, spriteComponent, musicManager, renderer)

def _makeDead(velComponent, attrComponent, spriteComponent, musicManager, renderer):
    attrComponent.objectState = 'dead'

    velComponent.xVel = 0
    velComponent.yVel = 0

    spriteComponent.iCurrentFrame = 28
    spriteComponent.lTimePassed = renderer.getTicks()

    musicManager.PlaySound('dead')

def _makeNewBorn(posComponent, velComponent, attrComponent, spriteComponent, renderer):
    attrComponent.objectState = 'newborn'
    attrComponent.direction = True

    posComponent.x = int(3.5 * 32 * sizeFactor)
    posComponent.y = gameHeight - int(32 * 2 * sizeFactor)

    velComponent.xVel = 0
    velComponent.yVel = 0

    spriteComponent.iCurrentFrame = 0
    spriteComponent.lTimePassed = renderer.getTicks()

def _touchGround(velComponent, posComponent, distComponent, spriteComponent, attrComponent, renderer):
    if velComponent.xVel == 0:
        attrComponent.objectState = 'static'
        spriteComponent.iCurrentFrame = 0
    elif velComponent.xVel != 0: 
        attrComponent.objectState = 'run'
        _runAnimation(abs(velComponent.xVel), spriteComponent, renderer)

    distComponent.maxDistance = 0
    distComponent.currentDistance = 0
    velComponent.yVel = 0

    # make player stand on ground
    posComponent.y = posComponent.y // int(32 * sizeFactor) * int(32 * sizeFactor)

def _updatePlayerJump(velComponent, posComponent, distComponent, spriteComponent, attrComponent, renderer):
    global sizeFactor

    if attrComponent.objectState == 'jumping' or attrComponent.objectState == 'jumping_bubble':
        _updatePlayerY(velComponent.yVel, posComponent)
        distComponent.currentDistance -= int(velComponent.yVel)

        if distComponent.currentDistance / distComponent.maxDistance > 0.75:
            velComponent.yVel *=  0.972
        else: 
            velComponent.yVel *=  0.986
        
        if abs(velComponent.yVel) < 2.5 * sizeFactor:
            velComponent.yVel = -2.5 * sizeFactor

        if attrComponent.objectState == 'jumping':
            spriteComponent.iCurrentFrame = 12
        else:
            spriteComponent.iCurrentFrame = 19

        if distComponent.maxDistance <= distComponent.currentDistance:
            attrComponent.objectState = 'falling'
            velComponent.yVel = 2.7

    elif attrComponent.objectState == 'falling' or attrComponent.objectState == 'falling_bubble':
        _updatePlayerY(velComponent.yVel, posComponent)
        if not physics.checkCollisionBottom(posComponent, int(32 * sizeFactor)):
            velComponent.yVel *= 1.05
            if velComponent.yVel > 7.65 * sizeFactor:
                velComponent.yVel = 7.65 * sizeFactor

            if attrComponent.objectState == 'falling':
                spriteComponent.iCurrentFrame = 20
            else:
                spriteComponent.iCurrentFrame = 27
        else:
            _touchGround(velComponent, posComponent, distComponent, spriteComponent, attrComponent, renderer)

def _runAnimation(runSpeed, spriteComponent, renderer):
    curTimeTick = renderer.getTicks()
    if curTimeTick - (260 - runSpeed) > spriteComponent.lTimePassed:
        spriteComponent.lTimePassed = curTimeTick
        if spriteComponent.iCurrentFrame == 0 or spriteComponent.iCurrentFrame >= 5:
            spriteComponent.iCurrentFrame = 1
        else:
            spriteComponent.iCurrentFrame += 1

def _updatePlayerX(dx, posComponent, attrComponent):
    global gameWidth
    global sizeFactor

    if attrComponent.objectState in ['jumping', 'falling', 'jumping_bubble', 'falling_bubble']:
        posComponent.x += int(dx)
    elif attrComponent.objectState == 'run':
        while physics.checkCollisionTileLeftRight(posComponent.x + int(dx), posComponent.y, int(32 * sizeFactor)):
            if dx > 0:
                dx -= 1
            else: 
                dx += 1
        posComponent.x += int(dx)

    # adjust to move out of left bound and right bound
    physics.moveOutOfLeftRightBound(posComponent, int(32 * sizeFactor))


def _updatePlayerY(yVel, posComponent):
    posComponent.y += int(yVel)
