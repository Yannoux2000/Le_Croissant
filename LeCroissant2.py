import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from LeCommon.Objs import *
from LeCommon.Areas import *
from LeCommon.Vector import *
from LeCommon.ConstVec import *
from States import *

class LeCroissant2(BaseAgent):

	def initialize_agent(self):

		self.me = Car()
		self.ball = Ball()
		#This runs once before the bot starts up
		self.controller_state = SimpleControllerState()
		self.bma = BallMetaArea()

		self.start = 0.0

		self.state = ATBA()

	def preprocess(self,game):
		self.time = game.game_info.seconds_elapsed
		self.me.process(game.game_cars[self.index])
		self.ball.process(game.game_ball)
		self.bma.update(self.ball.loc, self.team)

	def print_out(self):
		# print(self.bma.inShotZone(self.me.loc))
		pass

	def get_output(self, packet: GameTickPacket) -> SimpleControllerState:		
		self.preprocess(packet)
		self.render()
		self.print_out()
		return self.state.execute(self)

	def controller(self, t_obj,t_vel):
		controller_state = SimpleControllerState()

		t_loc = self.me.to_local(t_obj)
		t_agl = math.atan2(t_loc[1], t_loc[0])
		current_speed = self.me.vel.magnitude()

		#steering
		if t_agl > 0.1:
			controller_state.steer = controller_state.yaw = 1
		elif t_agl < -0.1:
			controller_state.steer = controller_state.yaw = -1
		else:
			controller_state.steer = controller_state.yaw = 0
		
		#throttle
		if t_vel > current_speed:
			controller_state.throttle = 1.0
			if t_vel > 1400 and self.start > 2.2 and current_speed < 2250:
				controller_state.boost = True
		elif t_vel < current_speed:
			controller_state.throttle = 0

		#dodging
		delta_t = self.time - self.start
		if delta_t > 2.2 and (t_obj.distance(self.me)) > 1000 and abs(t_agl) < 1.3:
			self.start = self.time
		elif delta_t <= 0.1:
			controller_state.jump = True
			controller_state.pitch = -1
		elif delta_t >= 0.1 and delta_t <= 0.15:
			controller_state.jump = False
			controller_state.pitch = -1
		elif delta_t > 0.15 and delta_t < 1:
			controller_state.jump = True
			controller_state.yaw = controller_state.steer
			controller_state.pitch = -1

		return controller_state

	def render(self):
		self.renderer.clear_screen()
		self.renderer.begin_rendering()
		self.renderer.draw_line_3d(self.ball.loc.vec,ConstVec.Pole_L.vec, self.renderer.red())
		self.renderer.draw_line_3d(self.ball.loc.vec,self.me.loc.vec, self.renderer.blue())
		self.renderer.draw_line_3d(self.ball.loc.vec,ConstVec.Pole_R.vec, self.renderer.red())
		self.renderer.end_rendering()

# class Vector2:
# 	def __init__(self, x=0, y=0):
# 		self.x = float(x)
# 		self.y = float(y)

# 	def __add__(self, val):
# 		return Vector2(self.x + val.x, self.y + val.y)

# 	def __sub__(self, val):
# 		return Vector2(self.x - val.x, self.y - val.y)

# 	def correction_to(self, ideal):
# 		# The in-game axes are left handed, so use -x
# 		current_in_radians = math.atan2(self.y, -self.x)
# 		ideal_in_radians = math.atan2(ideal.y, -ideal.x)

# 		correction = ideal_in_radians - current_in_radians

# 		# Make sure we go the 'short way'
# 		if abs(correction) > math.pi:
# 			if correction < 0:
# 				correction += 2 * math.pi
# 			else:
# 				correction -= 2 * math.pi

# 		return correction

# def get_car_facing_vector(car):
# 	pitch = float(car.physics.rotation.pitch)
# 	yaw = float(car.physics.rotation.yaw)

# 	facing_x = math.cos(pitch) * math.cos(yaw)
# 	facing_y = math.cos(pitch) * math.sin(yaw)

# 	return Vector2(facing_x, facing_y)