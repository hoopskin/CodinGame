import sys, math


class Entity(object):
	def __init__(self, entity_id, entity_type, cyborgCount=0, factoryProduction=0, fromFactory=-1, toFactory=-1, troopSize=-1, distanceToTarget=-1):
		super(Entity, self).__init__()
		self.arg = arg
		self.entity_id = entity_id
		self.entity_type = entity_type
		self.cyborgCount = cyborgCount
		self.factoryProduction = factoryProduction
		self.fromFactory = fromFactory
		self.toFactory = toFactory
		self.troopSize = troopSize
		self.distanceToTarget = distanceToTarget
		
entityObjects = []
factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
linkList = []
for i in range(link_count):
	factory_1, factory_2, distance = [int(j) for j in input().split()]
	linkList.append([factory_1, factory_2, distance])

# game loop
while True:
	entity_count = int(input())  # the number of entities (e.g. factories and troops)
	for i in range(entity_count):
		entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
		entity_id = int(entity_id)
		owner = int(arg_1)
		if entity_type == "FACTORY":
			cyborgCount = int(arg_2)
			factoryProduction = int(arg_3)
			arg_4 = int(arg_4)
			arg_5 = int(arg_5)
			entityObjects.append(Entity(entity_id, entity_type, cyborgCount, factoryProduction))
		else:
			fromFactory = int(arg_2)
			toFactory = int(arg_3)
			troopSize = int(arg_4)
			distanceToTarget = int(arg_5)
			entityObjects.append(Entity(entity_id, entity_type, fromFactory=fromFactory, toFactory=toFactory, troopSize=troopSize, distanceToTarget=distanceToTarget))


	#Per factory you own
		#If any factories are neutral
			#Have closest of your factories send 120% of minimum to that factory
		#Else
			#Attack: Find weakest/closest enemy factory
				#Send 120% of minimum to that factory
			#Defend: Find weakest friendly factory (or one being targeted)
				#Send 120% of minimum to that factory
			#Neutral: Wait...

	# Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
	print("WAIT")
