import numpy as np
import time
from LeMaths import *

from quicktracer import trace

DODGE_TIME = 0.3
FDASH_ACT_TIME = 0.5
step_forward = 5

#LECROISSANT IS HARDCODED

class Agent:
	def __init__(self, name, team, index, bot_parameters=None):
		self.name = name
		self.team = team  # 0 towards positive goal, 1 towards negative goal.
		self.index = index
		self.config_file = bot_parameters

		self.debug = True if index==0 else False

		#Bot's states, instead of having self.var all around here, it is kept in a dictionnary
		self.state = {'FDashStep' : 0, 'FDashTime' : 0, 'FDashToken' : 0, 'Gradient' : 1, 'PrevAngle' : 0, 'Target' : None}
		self.reset_output()

		self.my_car = None

		self.home = Vector3(0, 5000 * (self.team * 2 - 1),0)
		self.goal = Vector3(0,-5000 * (self.team * 2 - 1),0)

		self.HomeBA = Vector3( 3150, 4000 * (self.team * 2 - 1),1500) # 1500
		self.HomeBB = Vector3(-3150, 4000 * (self.team * 2 - 1),1500) # 1500

		self.MidBA = Vector3( 3500, 0, 0) # 1500
		self.MidBB = Vector3(-3500, 0, 0) # 1500

		self.GoalBA = Vector3( 3150,-4000 * (self.team * 2 - 1),1500) # 1500
		self.GoalBB = Vector3(-3150,-4000 * (self.team * 2 - 1),1500) # 1500

		self.state['Target'] = self.HomeBA

		self.roll_t = [0] * step_forward
		self.yaw_t = [0] * step_forward
		self.pitch_t = [0] * step_forward

		# self.car_dirm1 = Vector3()
		print("Done Loading {},\tReady to Go !".format(self.name))

		#retrieve parameters from the bot_parameters data, editable in LeCroissant.cfg
	def load_config_file(self):
		if self.config_file is None:
			return
		# read file code here

	def reset_output(self):

		self.output = {
			'throttle' : 0,
			'steer' : 0,
			'pitch' : 0,
			'yaw' : 0,
			'roll' : 0,
			'jump' : False,
			'boost' : False,
			'handbrake' : False
		}

	def get_output_vector(self, game_tick_packet):

		self.reset_output()

		self.my_car = Car(Get_car(game_tick_packet,self.index))

		ball_loc = Vectorize_Loc(game_tick_packet.gameball)

		# #vector representing a line
		# car_to_ball = self.my_car.to(ball_loc)
		# car_to_goal = self.goal - car_loc
		# car_to_home = self.home - car_loc

		# self.my_car.steer_to(ball_loc)
		# goal_angle = Rad_clip(car_to_goal.yaw - car_dir.yaw)
		# home_angle = Rad_clip(car_to_home.yaw - car_dir.yaw)

		# self.state['Target'] = ball_loc


		# if self.state['Target'] == self.GoalBA or self.my_car.loc.z > 50:
		# 	self.output['jump'] = True

		# if self.my_car.reached(self.GoalBA.Gnd()):
		# 	self.state['Target'] = self.HomeBA
		# 	print("Reset")

		# if (self.my_car.reached(self.state['Target'])):
		# 	# print("Reached")

		# 	if self.my_car.reached(self.GoalBA):
		# 		self.state['Target'] = self.HomeBA
		# 		print("GOAL !")

		# 	if self.state['Target'] == self.MidBA:
		# 		self.state['Target'] = self.GoalBA
		# 		print("GoalBAMidAir")

		# 	if self.state['Target'] == self.HomeBA:
		# 		self.state['Target'] = self.MidBA
		# 		print("MidBA")

		if self.my_car.reached(self.state['Target'].Gnd()):
			if self.state['Target'].Gnd().distance(self.HomeBA.Gnd()) < 90:
				self.state['Target'] = self.HomeBB
				self.output['jump'] = True
				print("Going HomeBB")
			elif self.state['Target'].Gnd().distance(self.HomeBB.Gnd()) < 90:
				self.state['Target'] = self.MidBB
				self.output['jump'] = True
				print("Going MidBB")
			elif self.state['Target'].Gnd().distance(self.MidBB.Gnd()) < 90:
				self.state['Target'] = self.GoalBB
				self.output['jump'] = True
				print("Going GoalBB")
			elif self.state['Target'].Gnd().distance(self.GoalBB.Gnd()) < 90:
				self.state['Target'] = self.GoalBA
				self.output['jump'] = True
				print("Going GoalBA")
			elif self.state['Target'].Gnd().distance(self.GoalBA.Gnd()) < 90:
				self.state['Target'] = self.MidBA
				self.output['jump'] = True
				print("Going MidBA")
			elif self.state['Target'].Gnd().distance(self.MidBA.Gnd()) < 90:
				self.state['Target'] = self.HomeBA
				self.output['jump'] = True
				print("Going HomeBA")

		# car_to_target = self.state['Target'] - car_loc
		# steer_rad = Rad_clip(car_dir.yaw - car_to_target.yaw) * 1.6

		steer_rad = 0
		t_local = self.my_car.localize(self.state['Target'])
		avl_local = self.my_car.localize_rot(self.my_car.avl)

		#Both Methods works the local one is giving more stability towards steering
		#but it can also have issue when car is pointing down

		steer_rad = self.my_car.steer_to(self.state['Target']) * 1.6
		# steer_rad = Rad_clip(np.pi - t_local.yaw) * 1.2

		yaw_rad = 0
		pitch_rad = 0
		roll_rad = 0


		# PID control to stop overshooting.
		if self.my_car.roll < 0.5:
			roll_rad = 0
		else :
			roll_rad  = 3 * self.my_car.roll  + 0.30 * avl_local.x

		yaw_rad   = 2 * self.my_car.steer_to(self.state['Target']) - 0.70 * avl_local.z
		pitch_rad = 3 * t_local.pitch + 0.90 * avl_local.y

		# roll_rad = - Rad_clip(self.roll_t[-1]) / 5											# + avl_local.x * 0.2
		# yaw_rad = Rad_clip(np.pi - self.yaw_t[-1]) * 0.8	# * 2 * (1/2 - abs(self.roll_t[-1])/np.pi)			# + avl_local.z * 1
		# pitch_rad = Rad_clip(self.pitch_t[-1] - (self.pitch_t[-1] - self.pitch_t[-2])/2) 				# + avl_local.y * 1


		if t_local.pitch < 0 and not self.my_car.ent.bOnGround:
			self.output['boost'] = True

			#Replace this with a Airial Token
		# if self.state['Target']==self.GoalBA:
		# self.output['handbrake'] = True
		self.output['yaw'] = np.clip(yaw_rad, -1.0, 1.0)
		self.output['pitch'] = np.clip(pitch_rad, -1.0, 1.0)
		self.output['roll'] = np.clip(roll_rad, -1.0, 1.0)

		# self.output['yaw'] = 1


		# if(abs(pitch_rad) < 0.2):
		# 	self.output['boost'] = True

			## GROUND PLAYS

			##Drift Turns
		# if abs(steer_rad) > np.pi/2:
		# 	self.PowerTurn()

			##Speeding Up movements
		# if(abs(steer_rad) < 0.2):
		# 	if not self.my_car.reached(self.state['Target'],threshold=1500):

		# 		#Decide which boosting method
		# 		if(self.my_car.ent.Boost>100):
		# 			self.output['boost'] = True
		# 			self.Cancel_FDash_t()
		# 		else:
		# 			self.Set_FDash_t()

		# 	else:
		# 		self.Cancel_FDash_t()

		self.output['throttle'] = 1.0
		# self.output['steer'] = np.clip(yaw_rad,-1.0,1.0)

			##SUBROUTINES
		#SubRoutines are always called even if not used.
		self.FDash()

		if self.debug :
			dbg_msg = ""

			# dbg_msg += "Yaw : {:6.3f}  ".format(yaw_rad)
			# dbg_msg += "T_Pitch : {:6.3f}  ".format(target_pitch)

			# trace(roll_rad)
			# trace(yaw_rad)
			# trace(pitch_rad)

			# print(dbg_msg)

		action = []
		for key in self.output:
			action.append(self.output[key])
		return action

	def PowerTurn(self):
		self.output['handbrake'] = True
		# self.output['throttle'] = -1.0




	# UP = Vector3(0,0,1)
	# def get_pitch_yaw_roll(forward, up=UP):
	# 	car = self.my_car
	# 	forward = normalize(forward)
	# 	desired_facing_angular_vel = -cross(car.forward, forward)
	# 	desired_up_angular_vel = -cross(car.up, up)

	# 	pitch = dot(desired_facing_angular_vel, car.right)
	# 	yaw = -dot(desired_facing_angular_vel, car.up)
	# 	roll = dot(desired_up_angular_vel, car.forward)

	# 	pitch_vel =  dot(car.angular_vel, car.right)
	# 	yaw_vel   = -dot(car.angular_vel, car.up)
	# 	roll_vel  =  dot(car.angular_vel, car.forward)

	# 	# avoid getting stuck in directly-opposite states
	# 	if dot(car.up, up) < -.8 and dot(car.forward, forward) > .8:
	# 		if roll == 0:
	# 			roll = 1
	# 		roll *= 1e10
	# 	if dot(car.forward, forward) < -.8:
	# 		if pitch == 0:
	# 			pitch = 1
	# 		pitch *= 1e10

	# 	trace(dot(car.up, up))
	# 	trace(pitch)
	# 	trace(roll)

	# 	if dot(car.forward, forward) < 0.0:
	# 		pitch_vel *= -1

	# 	# PID control to stop overshooting.
	# 	roll  = 3*roll  + 0.30*roll_vel
	# 	yaw   = 3*yaw   + 0.70*yaw_vel
	# 	pitch = 3*pitch + 0.90*pitch_vel

	# 	# only start adjusting roll once we're roughly facing the right way
	# 	if dot(car.forward, forward) < 0:
	# 		roll = 0

	# 	# To debug a single-axis
	# 	# pitch = 0
	# 	# yaw = 0
	# 	# roll = 0
	# 	return (pitch, yaw, roll)



	def Set_FDash_t(self):
		#State 1 : Check Timer
		if self.state['FDashToken'] == -1:

			if self.state['FDashTime'] + FDASH_ACT_TIME < time.time():
				print("FDash_Set")
				self.state['FDashToken'] = 1

		#State 0 : Start Timer
		if self.state['FDashToken'] == 0:
			
			if self.my_car.ent.bOnGround:
				self.state['FDashTime'] = time.time()
				self.state['FDashToken'] = -1

	def Cancel_FDash_t(self):
		if not self.state['FDashToken'] == 0:
			print("FDash_Canceled") 
		self.state['FDashToken'] = 0
		self.state['FDashStep'] = 0

	def FDash(self):
		if self.state['FDashToken']:
			#State 5
			if self.state['FDashStep'] == 5:
				if self.my_car.ent.bOnGround:
					self.state['FDashStep'] = 0

					self.state['FDashToken'] = 0
					self.state['FDashStep'] = 0
					print("FDash_Ended")
			#State 4
			if self.state['FDashStep'] == 4:
				self.output['pitch'] = -1.0
				self.output['jump'] = True
				if self.my_car.ent.bDoubleJumped:
					self.state['FDashStep'] = 5
				if self.state['FDashTime'] + 2 * DODGE_TIME < time.time():

					self.state['FDashToken'] = 0
					self.state['FDashStep'] = 0
					print("FDash_Failed")

			#State 3
			if self.state['FDashStep'] == 3:
				self.output['pitch'] = -1.0
				self.output['jump'] = False

				if self.state['FDashTime'] + DODGE_TIME < time.time():
					self.state['FDashStep'] = 4

			#State 2
			if self.state['FDashStep'] == 2:
				self.output['jump'] = True
				self.state['FDashTime'] = time.time()
				self.state['FDashStep'] = 3

			#State 1 : Check Timer
			if self.state['FDashStep'] == 1:

				if self.state['FDashTime'] + FDASH_ACT_TIME < time.time():
					self.state['FDashStep'] = 2

			#State 0 : Start Timer
			if self.state['FDashStep'] == 0:
				
				if self.my_car.ent.bOnGround:
					self.state['FDashTime'] = time.time()
					self.state['FDashStep'] = 1
