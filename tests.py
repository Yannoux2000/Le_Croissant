from quicktracer import trace
import numpy as np
import time

class Motor():
	def __init__(self, p=0, v=0):
		self._nmax = 10
		self.position = [p] * self._nmax
		self.vitesse = [v] * self._nmax

	def process(self, commande = 0, dt = 1):

		newv = commande * 0.4 * dt + self.vitesse[-1] * 0.5 * dt
		newp = Rad_clip(self.vitesse[-1] * dt + self.position[-1] * dt)

		self.update(newp, newv)
		return newp, newv

	def update(self, newp, newv):

		self.vitesse.append(newv)
		self.position.append(newp)

		self.vitesse = self.vitesse[-self._nmax:]
		self.vitesse = self.vitesse[-self._nmax:]

def Rad_clip(val):
		# Make sure we go the 'short way'
		val = val / (180/np.pi)
		if abs(val) > np.pi:
			val += (2 * np.pi) if val < 0 else (- 2 * np.pi)
		return val * (180/np.pi)


m = Motor()

c = 90
pm1 = 0

for i in range(300):
	p,v = m.process(commande=c)
	trace(Rad_clip(p))
	trace(v)
	dp = p - pm1
	pm1 = p
	com = (90 - p - dp)/10
	c = np.clip(com,-1,1)
	time.sleep(0.02)