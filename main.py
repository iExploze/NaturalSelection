import random
import math
import pygame
import time

import csv

generation_length = 3000
delay = 1000

amount_food = 100
amount_creatures = 20

creature_death_percentile = 0.5

mutation_const = 0.05



class Food:
	def __init__(self):
		self.x = random.randint(100, 1820)
		self.y = random.randint(100, 980)
		self.color = (255, 0, 0)

		self.energy = 1

	def draw(self):
		pygame.draw.circle(canvas, self.color, (self.x, self.y), 3)


class Creature:
	def __init__(self, genes=(1, 1)):
		self.name = ""
		self.x = random.randint(100, 1820)
		self.y = random.randint(100, 980)
		self.dx, self.dy = normalize((random_signed(), random_signed()))


		self.energy = 0.99

		# self.base_speed, self.base_sense = [random.randrange(1,2), random.randrange(6, 60)]
		self.base_speed, self.base_sense = [1, 30]
		self.gene_speed, self.gene_sense = genes #[1, 1]

		self.color = (0, 255, 255)

		self.base_energy_loss = 1/72
		self.time_energy_sync = 1/72/2 # trys to make base creature lose 1 energy per second


		self.new_direction_timer = 0

	def get_speed(self):
		return self.base_speed * self.gene_speed

	def get_sense(self):
		return self.base_sense * self.gene_sense

	def move(self):
		# if self.energy <= 0:
		# 	creatures.remove(self)



		# self.x += self.dx * self.get_speed()
		# self.y += self.dy * self.get_speed()

		self.x += self.dx * self.get_speed() * dtf
		self.y += self.dy * self.get_speed() * dtf

		self.x %= screen_width
		self.y %= screen_height

		# 0.027... base el
		energy_loss = self.base_energy_loss*self.time_energy_sync*(self.gene_speed**2+self.gene_sense)
		# print(f'base energy lost per step: {energy_loss}')
		self.energy -= energy_loss


	def draw(self):
		pygame.draw.rect(canvas, self.color, (self.x - 5, self.y - 5, 10, 10))
		pygame.draw.circle(canvas, (70, 70, 70), (self.x, self.y), self.get_sense(), width=1)

	def sense_food(self):

		# finds food that is closest out of all global foods
		closest_food = None
		shortest_dist = 1000000
		for food in foods:
			eval_dist = distance((self.x, self.y), (food.x, food.y))
			if self.get_sense() >= eval_dist and eval_dist < shortest_dist:
				closest_food = food
				shortest_dist = eval_dist

		# print(closest_food, shortest_dist)

		if closest_food != None:  # turn self to pursue closest food
			self.dx, self.dy = normalize((closest_food.x - self.x, closest_food.y - self.y))


		elif self.new_direction_timer <= time.time():
			smoothness = 0.8
			self.dx, self.dy = normalize((self.dx + smoothness*random_signed(), self.dy + smoothness*random_signed()))
			self.new_direction_timer = time.time() + 0.3


	def eat_food(self):
		for food in foods:
			if distance((self.x, self.y), (food.x, food.y)) <= 14:
				self.energy += food.energy
				foods.remove(food)

	def __repr__(self):
		return f'{self.name}: genes: {self.gene_speed, self.gene_sense}'


# utility functions
def normalize(velo):
	dx, dy = velo
	mag = math.sqrt(dx ** 2 + dy ** 2)

	if mag == 0:
		return 0,0

	return [dx / mag, dy / mag]


def distance(a, b):
	x1, y1 = a
	x2, y2 = b

	return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def random_signed():
	"""
	Returns a random number from [-1 to 1)
	:return:
	"""
	return 2*(random.random() - 0.5)

def genes_to_color():
	pass


creatures = []
foods = []
age = 0
generation = 0



def start_simulation():
	global foods, creatures, age



	creatures = []
	foods = []



	for i in range(amount_food):
		foods.append(Food())

	for i in range(amount_creatures):
		creatures.append(Creature())

	# creatures.append(Creature((545.1610324170359,633.7939459012329)))

def averages():
	energy = 0
	speed = 0
	sense = 0
	for creature in creatures:
		energy += creature.energy
		speed += creature.gene_speed
		sense += creature.gene_sense

	amount_creatures = len(creatures)
	energy /= amount_creatures
	speed /= amount_creatures
	sense /= amount_creatures



	with open('logs/conformity.csv', 'a', newline='') as file:

		writer = csv.writer(file)
		writer.writerow([generation, amount_creatures, energy, speed, sense])



	print(f'average energy: {energy}')
	print(f'average speed: {speed}')
	print(f'average sense: {sense}')

def reproduce_top_half():

	min_value = 0.2

	global foods, creatures, age

	foods = []
	for i in range(amount_food):
		foods.append(Food())

	creatures.sort(key=lambda obj: obj.energy, reverse=True)



	new_creatures = []
	for i, creature in enumerate(creatures[:amount_creatures//2]):
		parent_speed, parent_sense = creature.gene_speed, creature.gene_sense
		child_speed, child_sense = max(parent_speed+mutation_const*random_signed(), min_value), max(parent_sense+mutation_const*random_signed(), min_value)

		print(f'{i} speed{parent_speed} => {child_speed}, sense{parent_sense} => {child_sense}')

		new_creatures.append(
			Creature((child_speed, child_sense))
		)

		new_creatures.append(
			Creature((parent_speed, parent_sense))
		)


	creatures = new_creatures

def reproduce_by_food():

	min_value = 0.2

	global foods, creatures, age, amount_food

	foods = []
	for i in range(amount_food):
		foods.append(Food())

	creatures.sort(key=lambda obj: obj.energy, reverse=True)


	reproduced, survived, died = 0,0,0 # statistics
	new_creatures = []
	for i, creature in enumerate(creatures):
		parent_speed = creature.gene_speed
		parent_sense = creature.gene_sense
		if creature.energy >= 2:
			reproduced += 1

			kids = max(int(math.log2(creature.energy)), 1)

			for j in range(kids):

				child_speed = max(parent_speed + mutation_const * random_signed(), min_value)
				child_sense =  max(parent_sense + mutation_const * random_signed(), min_value)

				new_creatures.append(
					Creature((child_speed, child_sense))
				)

			new_creatures.append(
				Creature((parent_speed, parent_sense))
			)

		elif 1 <= creature.energy < 2:
			survived += 1
			new_creatures.append(
				Creature((parent_speed, parent_sense))
			)
		else:
			died += 1

	print(f'reproduced: {reproduced}\tsurvived: {survived}\tdied: {died}')
	# amount_food -= 1
	creatures = new_creatures




with open('logs/conformity.csv', 'w', newline='') as file:

	writer = csv.writer(file)
	writer.writerow(['generation', 'amount_creatures', 'average_energy', 'average_speed', 'average_sense'])




# print(normalize((random.random() - 0.5, random.random() - 0.5)))

pygame.init()
canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

clock = pygame.time.Clock()
dt = clock.tick(delay)
dtfc = 1

start_simulation()


running = True
while running:



	canvas.fill((0, 0, 0))

	dt = clock.tick(delay)
	dtf = dt / dtfc


	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				start_simulation()



	for creature in creatures:
		creature.sense_food()
		creature.move()
		creature.eat_food()
		creature.draw()

	for food in foods:
		food.draw()

	pygame.display.update()

	# print(f'mod {creatures[-1].energy} vs. {creatures[0].energy}')


	if age % generation_length == generation_length-1 or len(foods) == 0:
		age = 0
		averages()
		reproduce_by_food()
		generation += 1
		print(f'\n GENERATION {generation}')


	age += 1

