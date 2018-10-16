from LeCommon.Vector import *
from LeCommon.Objs import *
from LeCommon.ConstVec import *

class Line():

	def __init__(self, vecA, vecB):
		self.vecA = vecA
		self.vecB = vecB

	def __str__(self):
		return "[ "+str(self.vecA)+" - "+str(self.vecB)+" ]"

"""
This class is based on a radial area principle.
Subdividing the areas into 6 zones, starting from the ball, should help define weither an agent can be threatening
or in disadvantage.
	  ________________
	 /        |       \
	 |-----___|___----|
	[      ___X___     ]
	 |-----   |   ----|
	 \________|______ /

this drawing is perfect
the map would be subdevided depending on the goal_Pole to ball segments, 
and depending on the ball to side walls segments

from theses segment the bot would define weither an agent is correctly placed (if an agent is in one zone)
or is he a possible threat (alined with the ball)

"""

def inAngle(o_loc, a_loc, t_loc):
	a_agl = o_loc.angle(a_loc)
	t_agl = sign(a_agl) * o_loc.angle(t_loc)

	return (a_agl > t_agl)

class BallMetaArea():
	def __init__(self):
		self.ball = Vec3()

		self.Goal_sideL = Vec3()
		self.Goal_sideR = Vec3()

		self.Home_sideL = Vec3()
		self.Home_sideR = Vec3()

		self.Wall_L = Vec3()
		self.Wall_R = Vec3()

	def update(self, ball, team):
		self.ball = ball

		Pl = ConstVec.get('Goal_L',team)
		Pr = ConstVec.get('Goal_R',team)

		self.Goal_sideL = - self.ball.to(Pl)
		self.Goal_sideR = - self.ball.to(Pr)

		Pl = ConstVec.get('Home_L',team)
		Pr = ConstVec.get('Home_R',team)

		self.Home_sideL = - self.ball.to(Pl)
		self.Home_sideR = - self.ball.to(Pr)

		Wl = ConstVec.get('Wall_L', team)
		Wr = ConstVec.get('Wall_R', team)

		self.Wall_sideL = - self.ball.to(Wl)
		self.Wall_sideR = - self.ball.to(Wr)

	def inFrontZone(self, loc):
		return inAngle(loc, self.Goal_sideL, self.Goal_sideR)

	def inShotZone(self, loc):
		return inAngle(loc, self.Home_sideL, self.Home_sideR)

	# def inShotZone(self, loc):
	# 	return BallMetaArea.inZone(loc, self.Goal_sideL, self.Goal_sideR)

	# def inShotZone(self, loc):
	# 	return BallMetaArea.inZone(loc, self.Goal_sideL, self.Goal_sideR)