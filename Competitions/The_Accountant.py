import sys
import math

# Shoot enemies before they collect all the incriminating data!
# The closer you are to an enemy, the more damage you do but don't get too close or you'll get killed.

#Score is 100 per remaining data point + 10 per kill + bonus
#Bonus = Data Points Left * max(0, (Starting Enemy LifePoints - 3 * Shots Fired)) * 3
class DataLink(object):
	def __init__(self, id, x, y):
		super(DataLink, self).__init__()
		self.id = id
		self.x = x
		self.y = y
		
class Wolff(object):
	def __init__(self, x, y):
		super(Wolff, self).__init__()
		self.x = x
		self.y = y

class Enemy(object):
	def __init__(self, id, x, y, life):
		super(Enemy, self).__init__()
		self.id = id
		self.x = x
		self.y = y
		self.life = life
		self.distFromWolff = abs(math.hypot(self.x - wolff.x, self.y - wolff.y))
		self.closestLink = self.detClosestLink()
		#Mentions Euclidean distance for something, may be used here too
		self.closestLinkDist = abs(math.hypot(self.x - self.closestLink.x, self.y - self.closestLink.y))
		self.potDamageFromWolff = self.detPotDamage()

	def detPotDamage(self):
		return 125000 / (math.pow(abs(math.hypot(self.x - wolff.x, self.y - wolff.y)),1.2))

	def detClosestLink(self):
		rtn = ""
		shortestDist = 999999
		for dl in dataLinks:
			#If dist equals, smaller ID is used, hence the reverse
			if abs(math.hypot(self.x - dl.x, self.y - dl.y)) <= shortestDist:
				rtn = dl
				shortestDist = abs(math.hypot(self.x - dl.x, self.y - dl.y))

		return rtn

# game loop
while True:
	dataLinks = []
	enemyList = []

	x, y = [int(i) for i in input().split()]
	wolff = Wolff(x, y)

	data_count = int(input())
	for i in range(data_count):
		data_id, data_x, data_y = [int(j) for j in input().split()]
		dataLinks.append(DataLink(data_id, data_x, data_y))

	#Reversing because enemies choose smallest id if dist equals
	dataLinks.reverse()
	
	enemy_count = int(input())
	for i in range(enemy_count):
		enemy_id, enemy_x, enemy_y, enemy_life = [int(j) for j in input().split()]
		enemyList.append(Enemy(enemy_id, enemy_x, enemy_y, enemy_life))

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)

	# MOVE x y or SHOOT id
	action = "MOVE"
	x = -1
	y = -1
	shootId = -1

	if len(dataLinks) == 1:
		action = "MOVE"
		x = dataLinks[0].x
		y = dataLinks[0].y

	if len(enemyList) == 1:
		action = "SHOOT"
		shootId = enemyList[0].id

	if action == "SHOOT":
		print("%s %i" % (action, shootId))
	else:
		print("%s %i %i" % (action, x, y))
