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

		return agent.controller(target_location, target_speed)
