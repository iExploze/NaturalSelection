import random
import math
import pygame
import time


class Food:
	def __init__(self):
		self.x = random.randint(100, 1820);
		self.y = random.randint(100, 980)
		self.color = (255, 0, 0)

		self.energy = 1

	def draw(self):
		pygame.draw.circle(canvas, self.color, (self.x, self.y), 3)


class Creature:
	def __init__(self):
		self.x = random.randint(100, 1820)
		self.y = random.randint(100, 980)
		self.dx, self.dy = normalize((random.random() - 0.5, random.random() - 0.5))
		self.color = (255, 255, 255)

		self.energy = 100

		self.base_speed, self.base_sense = [1, 300]
		self.gene_speed, self.gene_sense = [1, 1]

		self.new_direction_timer = 0

	def get_speed(self):
		return self.base_speed * self.gene_speed

	def get_sense(self):
		return self.base_sense * self.gene_sense

	def move(self):
		self.x += self.dx
		self.y += self.dy

	def draw(self):
		pygame.draw.rect(canvas, self.color, (self.x - 5, self.y - 5, 10, 10))

	def sense_food(self):

		# finds food that is closest out of all global foods
		closest_food = None;
		shortest_dist = 1000000
		for food in foods:
			eval_dist = distance((self.x, self.y), (food.x, food.y))
			if self.get_sense() >= eval_dist and eval_dist < shortest_dist:
				closest_food = food
				shortest_dist = eval_dist

		print(closest_food, shortest_dist)

		if closest_food != None:  # turn self to pursue closest food
			self.dx, self.dy = normalize((closest_food.x - self.x, closest_food.y - self.y))


		elif self.new_direction_timer <= time.time():
			self.dx, self.dy = normalize((random.random() - 0.5, random.random() - 0.5))
			self.new_direction_timer = time.time() + 0.3


def normalize(velo):
	dx, dy = velo
	mag = math.sqrt(dx ** 2 + dy ** 2)
	return [dx / mag, dy / mag]


def distance(a, b):
	x1, y1 = a
	x2, y2 = b

	return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


creatures = []
foods = []


def start_simulation():
	global foods, creatures

	creatures = []
	foods = []

	amount_food = 50;
	amount_creatures = 25

	for i in range(amount_food):
		foods.append(Food())

	for i in range(amount_creatures):
		creatures.append(Creature())


print(normalize((random.random() - 0.5, random.random() - 0.5)))

pygame.init()
canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

delay = 72
clock = pygame.time.Clock()

start_simulation()

running = True
while running:

	canvas.fill((0, 0, 0))

	clock.tick(delay)

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				start_simulation()

	for food in foods:
		food.draw()

	for creature in creatures:
		creature.sense_food()
		creature.move()
		creature.draw()

	pygame.display.update()





# TODO: smooth motion?
# TODO: destroy food on collide
# TODO: genes + reproduction
# TODO: energy costs




