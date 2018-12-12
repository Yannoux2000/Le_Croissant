from rlbot.agents.base_agent import SimpleControllerState

from LeFramework.common.Objs import *
from LeFramework.common.Areas import *
from LeFramework.common.Vector import *
from LeFramework.common.ConstVec import *
from LeFramework.common.Paths import *

 
class ATBA:
	def __init__(self):
		self.expired = False

	def execute(self, agent):
		t_loc = agent.ball
		t_vel = agent.ball.vel.magnitude() + (agent.ball.distance(agent.me)/1.5)

		return agent.controller(t_loc, t_vel, True, True)

class Patrol:
	def __init__(self):
		self.expired = False
		self.path = Path(PATHS.LS())
		self.mid = Path(PATHS.RS())

		self.path.flip()

	def execute(self, agent):
		if self.path.go().distance(agent.me) <= 500 or self.path.overtaked(agent.me):
			self.path.next()
			print(self.path.i)
		
		self.mid.snap(agent.me,near_skip=True)
		if self.path.i == self.path.end:
			self.mid , self.path = self.path, self.mid
			self.path.i = self.path.begin + 1
			print("SWAP PATH")

		t_loc = self.path.go()
		t_vel = 50000
		boost = True
		dodge = False

		return agent.controller(t_loc, t_vel, boost, dodge)

class RandPatrol:
	def __init__(self):
		self.expired = False
		self.pf = PathFinder()
		self.path = Path([Node(BOOSTPAD.b0),Node(BOOSTPAD.b1),Node(BOOSTPAD.b2)])

	def execute(self, agent):
		if self.path.go().distance(agent.me) <= 500:

			if self.path.ended():
				self.path = self.pf.genPath(BOOSTPAD.all(), agent.me.loc, ConstVec.randomVec())
				print(self.path)
			else:
				self.path.next()
				print(self.path.i)

		t_loc = self.path.go()
		t_vel = 2200
		boost = False
		dodge = False

		return agent.controller(t_loc, t_vel, boost, dodge)

class Shoot:
	def __init__(self):
		self.expired = False

	def execute(self, agent):
		dodge = False
		if(agent.bma.inFrontZone(agent.me.loc)):
			print("    InShotZone")
			t_loc = agent.ball
			t_vel = agent.ball.vel.magnitude() + (agent.ball.distance(agent.me)/1.5)
			boost = True

		else:
			print("not InShotZone")
			t_loc = ConstVec.t_get("Goal", agent.team)
			t_vel = (t_loc.distance(agent.me)/1.5)
			boost = False

			if t_loc.distance(agent.me) < 1000:
				t_vel = 22000
				dodge = True
				boost = True


		return agent.controller(t_loc, t_vel, boost, dodge)
