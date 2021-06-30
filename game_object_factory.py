from CPP.component import sprite_component, attributes_component, img_component, velocity_component, position_component, dist_component
from CPP.entity import game_object
import game_global

sizeFactor = game_global.sizeFactor

def createPlayer(entityId, spriteId, iDelays, iCurrentFrame, iStartFrame, iEndFrame, xPos, yPos, xVel, yVel, isCollidable, objectState):
    global sizeFactor

    player = game_object.GameObject(entityId)

    spriteComponent = sprite_component.SpriteComponent(spriteId, iDelays, iCurrentFrame, iStartFrame, iEndFrame)
    posComponent = position_component.PositionComponent(xPos, yPos)
    velComponent = velocity_component.VelocityComponent(xVel, yVel)
    attrComponent = attributes_component.AttributesComponent(isCollidable, objectState, True)
    distComponent = dist_component.DistComponent(0, int(3 * 32 * sizeFactor + 24 * sizeFactor))

    player.addComponent('player_sprite', spriteComponent)
    player.addComponent('player_position', posComponent)
    player.addComponent('player_velocity', velComponent)
    player.addComponent('player_attributes', attrComponent)
    player.addComponent('player_jump_dist', distComponent)

    return player

def createMinion(entityId, spriteId, iDelays, iCurrentFrame, iStartFrame, iEndFrame, xPos, yPos, xVel, yVel, isCollidable, objectState, maxRunDist):
    minion = game_object.GameObject(entityId)

    spriteComponent = sprite_component.SpriteComponent(spriteId, iDelays, iCurrentFrame, iStartFrame, iEndFrame)
    posComponent = position_component.PositionComponent(xPos, yPos)
    velComponent = velocity_component.VelocityComponent(xVel, yVel)
    attrComponent = attributes_component.AttributesComponent(isCollidable, objectState, True)
    distComponent = dist_component.DistComponent(0, maxRunDist)

    minion.addComponent('minion_sprite', spriteComponent)
    minion.addComponent('minion_position', posComponent)
    minion.addComponent('minion_velocity', velComponent)
    minion.addComponent('minion_attributes', attrComponent)
    minion.addComponent('minion_run_dist', distComponent)

    return minion

def createItem(entityId, imgId, xPos, yPos, xVel, yVel, isCollidable, objectState):
    item = game_object.GameObject(entityId)

    imgComponent = img_component.ImgComponent(imgId)
    posComponent = position_component.PositionComponent(xPos, yPos)
    velComponent = velocity_component.VelocityComponent(xVel, yVel)
    attrComponent = attributes_component.AttributesComponent(isCollidable, objectState, True)

    item.addComponent('item_image', imgComponent)
    item.addComponent('item_position', posComponent)
    item.addComponent('item_velocity', velComponent)
    item.addComponent('item_attributes', attrComponent)

    return item

def createBubble(entityId, imgId, xPos, yPos, xVel, yVel, isCollidable, objectState, maxRunDist):
    bubble = game_object.GameObject(entityId)

    imgComponent = img_component.ImgComponent(imgId)
    posComponent = position_component.PositionComponent(xPos, yPos)
    velComponent = velocity_component.VelocityComponent(xVel, yVel)
    attrComponent = attributes_component.AttributesComponent(isCollidable, objectState, True)
    distComponent = dist_component.DistComponent(0, maxRunDist)

    bubble.addComponent('bubble_image', imgComponent)
    bubble.addComponent('bubble_position', posComponent)
    bubble.addComponent('bubble_velocity', velComponent)
    bubble.addComponent('bubble_attributes', attrComponent)
    bubble.addComponent('bubble_dist', distComponent)

    return bubble