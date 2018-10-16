from rlbot.agents.base_agent import SimpleControllerState

from LeCommon.Objs import *
from LeCommon.Areas import *
from LeCommon.Vector import *
from LeCommon.ConstVec import *


class ATBA:
	def __init__(self):
		self.expired = False

	def execute(self, agent):
		target_location = agent.ball
		target_speed = agent.ball.vel.magnitude() + (agent.ball.distance(agent.me)/1.5)

		return agent.controller(target_location, target_speed, True, True)

class Patrol:
	def __init__(self):
		self.expired = False
		self.path = Path(PATHS.LS())
		self.mid = Path(PATHS.RS())

		self.mid.flip()

	def execute(self, agent):
		if self.path.go().distance(agent.me) <= 500:
			self.path.next()
			print(self.path.i)
		
		self.mid.snap(agent.me)
		if self.path.i == self.path.end:
			self.mid , self.path = self.path, self.mid
			self.path.i = 0
			print("SWAP PATH")

		target_location = self.path.go()
		target_speed = 50000
		boost = True
		dodge = False

		return agent.controller(target_location, target_speed, boost, dodge)

class Shoot:
	def __init__(self):
		self.expired = False

	def execute(self, agent):
		dodge = False
		if(agent.bma.inFrontZone(agent.me.loc)):
			print("    InShotZone")
			target_location = agent.ball
			target_speed = agent.ball.vel.magnitude() + (agent.ball.distance(agent.me)/1.5)
			boost = True

		else:
			print("not InShotZone")
			target_location = ConstVec.t_get("Goal", agent.team)
			target_speed = (target_location.distance(agent.me)/1.5)
			boost = False

			if target_location.distance(agent.me) < 1000:
				target_speed = 22000
				dodge = True
				boost = True


		return agent.controller(target_location, target_speed, boost, dodge)
