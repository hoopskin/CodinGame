import sys
import math

class Entity(object):
	def __init__(self, entity_type, owner, x, y, param_1, param_2):
    	#entity_type = id of the player (0 for player or 1 for bomb)
    	#owner = id of the bomb owner
    	#x = x
    	#y = y
    	#param_1 = Players: Numbers of bombs a player can still place. Bombs: Rounds left until explosion
    	#param_2 = Players: Explosion range of player's bombs. Bombs: Explosion range.
		super(Entity, self).__init__()
		self.entity_type = entity_type
		self.owner = owner
		self.x = x
		self.y = y
		self.param_1 = param_1
		self.param_2 = param_2
		

width, height, my_id = [int(i) for i in input().split()]
gameMap = []
floor = '.'
box = '0'
roundsRemaining = 200

#Bomb Range = 3
#Bomb hitting bomb means bomb explodes (bomb)

# game loop
while True:
	entityObjects = []
    for i in range(height):
        row = input()
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        entityObjects.append(Entity(entity_type, owner, x, y, param_1, param_2))


    print("BOMB 6 5")
