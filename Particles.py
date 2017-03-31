import pygame
import random
import math
import cv2
class Particle(object):
	def __init__(self, width, height):
		self.size = random.randint(20,30)
		self.x = random.randint(self.size, width - self.size)
		self.y = random.randint(self.size, height - self.size)
		self.color = (0,0,255)
		self.thinkness = 1
		self.speed = 3
		self.angle = 0
	def move(self):
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) *self.speed
	def bounce(self, width, height):
		elasity = 0.8
		if self.x >-self.size + width:
			self.x = 2*(width - self.size) - self.x
			self.angle = -1*self.angle
			self.speed *= elasity
		elif self.x <= self.size:
			self.x = 2*self.size - self.x
			self.angle = -self.angle
			self.speed *= elasity
		if self.y > height - self.size:
			self.y = 2*(height - self.size) - self.y
			self.angle = math.pi - self.angle
			self.speed *= elasity
		elif self.y <= self.size:
			self.y = 2*self.size - self.y
			self.angle = math.pi - self.angle
			self.speed *= elasity
	def collide(self, p1, elasity=0.8):
		dx = p1.x - self.x
		dy = p1.y - self.y
		dist = math.hypot(dx, dy)
		if dist < p1.size + self.size:
			tangent = math.atan2(dy, dx)
			angle = 0.5 * math.pi + tangent
			angle2 = 2*tangent - p1.angle
			angle1 = 2*tangent - self.angle
			speed1 = p1.speed*elasity
			speed2 = self.speed*elasity
			(self.angle, self.speed) = (angle1, speed1)
			(p1.angle, p1.speed) = (angle2, speed2)
			overlap = 0.5*(p1.size + self.size - dist+1)
			p1.x += math.sin(angle)*overlap
			p1.y -= math.cos(angle)*overlap
 			self.x -= math.sin(angle)*overlap
			self.y += math.cos(angle)*overlap
	
class star(Particle):
	def __init__(self, width, height):
		super(star, self).__init__(width, height)
		self.prex = self.x
		self.prey = self.y
		self.t = cv2.getTickCount()
		self.pt = cv2.getTickCount()
	def refresh(self, x, y, radius):
		self.prex = self.x
		self.prey = self.y
		self.pt = self.t
		self.x = x
		self.y = y
		dx=self.x-self.prex
		dy = self.y - self.prey
		self.angle = math.atan2(dy, dx)
		diff = math.hypot(dx, dy)
		self.t = cv2.getTickCount()
		self.speed = diff/((self.pt - self.t)/cv2.getTickFrequency())
	def collide(self, p):
		super(star, self).collide(p, 0.3)

class Environment:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.particles = []
		
# env.addParticles(speed=1.5, angle=0.8, size=4)
	def addParticles(self, n=1, **kargs):
		for i in range(n):
			size = kargs.get('size',40)
			x= random.uniform(size, self.width - size)
			y = random.uniform(size, self.height - size)
			particle = Particle(self.width, self.height)
			particle.speed = kargs.get('speed', 3)
			particle.angle = kargs.get('angle', math.pi*0.5)
			self.particles.append(particle)


	def update(self):
		for i, particle in enumerate(self.particles):
			particle.move()
			particle.bounce(self.width, self.height)
			for particle2 in self.particles[i+1:]:
				particle.collide(particle2)



