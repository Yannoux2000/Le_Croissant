import numpy as np
import math
from LeCommon.Vector import *

def Target_A(vec = [], team = 0):
	return Target(Vec3(vec) * (team*(-2) + 1))

class Target:
	def __init__(self, vec):
		self.loc = vec
		self.local_loc = Vec3()

	def distance(self, other):
		return self.loc.distance(other.loc)
		
	def to(self, t_loc):
		return t_loc - self.loc

class Path():
	def __init__(self, path):
		self.path = path
		self.i = 0
		self.begin = 0
		self.end = len(self.path) - 1

	def flip(self):
		self.path.reverse()

	def next(self):
		self.i += 1
		if self.i >= len(self.path):
			self.i = self.begin

	def go(self):
		return self.path[self.i]

	def then(self):
		if self.i<self.end:
			return self.path[self.i]
		else:
			return None

	def snap(self, loc, near_skip=True):

		for i in range(len(self.path)):
			d = self.path[i].distance(loc)

			if d < self.go().distance(loc):
				self.i = i

		if near_skip: #aim at the next right away
			self.next()

class Obj(Target):
	def __init__(self, vec = Vec3()):
		super(Obj,self).__init__(vec)
		self.vel = Vec3()
		self.rot = Vec3()
		self.ang = Vec3()

		self.matrix = []

	def process(self, physics):
		self.Obj_process(physics)

	def Obj_process(self, physics):
		self.loc.vec = [physics.location.x,physics.location.y,physics.location.z]
		self.vel.vec = [physics.velocity.x,physics.velocity.y,physics.velocity.z]
		self.rot.vec = [physics.rotation.roll,physics.rotation.pitch,physics.rotation.yaw]
		self.ang.vec = [physics.angular_velocity.x,physics.angular_velocity.y,physics.angular_velocity.z]

	def rot_to_mat(self):
		CR = math.cos(self.rot[0])
		SR = math.sin(self.rot[0])
		
		CP = math.cos(self.rot[1])
		SP = math.sin(self.rot[1])

		CY = math.cos(self.rot[2])
		SY = math.sin(self.rot[2])

		self.matrix = []
		self.matrix.append(Vec3([CP*CY, CP*SY, SP]))
		self.matrix.append(Vec3([CY*SP*SR-CR*SY, SY*SP*SR+CR*CY, -CP * SR]))
		self.matrix.append(Vec3([-CR*CY*SP-SR*SY, -CR*SY*SP+SR*CY, CP*CR]))
		return self.matrix

	def to_local(self, other):
		vec = other.loc - self.loc

		x = (vec).dot(self.matrix[0])
		y = (vec).dot(self.matrix[1])
		z = (vec).dot(self.matrix[2])

		return Vec3([x,y,z])

class Ball(Obj):
	def __init__(self, vec = Vec3()):
		super(Ball, self).__init__(vec)

	def process(self, ball):
		self.Obj_process(ball.physics)
		self.matrix = self.rot_to_mat()

class Car(Obj):
	def __init__(self, vec = Vec3()):
		super(Car, self).__init__(vec)
		self.boost = 0

		self.index = 0
		self.team = 0

	def process(self, car):
		self.Obj_process(car.physics)
		self.boost = car.boost
		self.team = car.team
		self.matrix = self.rot_to_mat()

# 	def forward(self):
# 		roll = self.rot[0]
# 		pitch = self.rot[1]
# 		yaw = self.rot[2]

# 		facing_x = np.cos(pitch) *	np.cos(yaw)
# 		facing_y = np.cos(pitch) *	np.sin(yaw)
# 		facing_z = np.sin(pitch)

# 		#double check normilizations of vectors
# 		return Vector3([facing_x, facing_y, facing_z]).normalize()

# 	def left(self):
# 		roll = self.rot[0]
# 		pitch = self.rot[1]
# 		yaw = self.rot[2]# + np.pi/2

# 		facing_x = np.cos(pitch) *(-np.sin(yaw))
# 		facing_y = np.cos(pitch) *	np.cos(yaw)
# 		facing_z = np.sin(pitch)

# 		#double check normilizations of vectors
# 		return Vector3([facing_x, facing_y, facing_z]).normalize()

# 	#retrieve transformation matrix from car info.
# 	def tMat(self):
# 		return Get_TMat(self.Car_Forward(), self.Car_Left(), self.loc)

# def Get_TMat(f, l, t):
# 	#Generate matrix transform
# 	#X Forward, Y = Left, Z = Up

# 	#Y = M . X
# 	#M = Y . X-1
# 	#X = indentity because of f, l, u corresponding to unit vectors

# 	u = f.cross(l)

# 	#the vector t is for translations

# 	#This matrix convert from local to global
# 	return np.concatenate((f.np(0), l.np(0), u.np(0), t.np(1)), axis=1)

# #using matrix algorithms to find local and global coords
# def to_local(car, vec):
# 	#Inverted from the local to global matrix generated
# 	matM = np.linalg.inv(Car_TMat(car))
# 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 	return outvec

# def to_global(car, vec):

# 	matM = Get_TMat(car)
# 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 	return outvec


	# def reached(self, t_loc, threshold = 500):
	# 	return (self.distance(t_loc) < threshold)

# 	def Forward(self):

# 		facing_x = np.cos(self.rot.) * np.cos(self.yaw)
# 		facing_y = np.cos(self.pitch) * np.sin(self.yaw)
# 		facing_z = np.sin(self.pitch)

# 		#double check normilizations of vectors
# 		return Vector3(facing_x, facing_y, facing_z).normalize()

# 	def Left(self):

# 		left_x = np.cos(self.pitch) * (-np.sin(self.yaw))
# 		left_y = np.cos(self.pitch) * np.cos(self.yaw)
# 		left_z = np.sin(self.pitch)

# 		return Vector3(left_x, left_y, left_z).normalize()

# 	def TMat(self):
# 		return Get_TMat(self.Forward(), self.Left(), self.loc)

# 	def RMat(self):
# 		return Get_TMat(self.Forward(), self.Left(), Vector3())

# 	def localize(self, vec):
# 		#Inverted from the local to global matrix generated
# 		matM = np.linalg.inv(self.TMat())
# 		outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 		return outvec

# 	def localize_rot(self, vec):

# 		matM = np.linalg.inv(self.RMat())
# 		outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 		return outvec

# 	def globalize(self, vec):

# 		matM = self.TMat()
# 		outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 		return outvec

# 	def p_array_to(self, t_loc):
# 		t_local = self.localize(t_loc)

# 		ret = t_local.p_array()
# 		ret[0] = Rad_clip(np.pi - ret[0])
		
# 		return ret

# 	def array_to(self, t_loc):
# 		t_local = self.localize(t_loc)

# 		ret = t_local.array()
# 		ret[0] = Rad_clip(np.pi - ret[0])
		
# 		return ret

# 	def p_array(self):
# 		return self.loc.p_array() + self.dir.p_array() + self.vel.p_array() + self.avl.p_array()

# 	def c_array(self):
# 		return self.loc.c_array() + self.dir.c_array() + self.vel.c_array() + self.avl.c_array()

# 	def array(self):
# 		return self.loc.array() + self.dir.array() + self.vel.array() + self.avl.array()


# def Car_To_Vec(car):
# 	return Vectorize_Loc(car), Car_Forward(car), Vectorize_Vel(car), Vectorize_Avl(car)

# def Rad_clip(val):
# 		# Make sure we go the 'short way'
# 		if abs(val) > np.pi:
# 			val += (2 * np.pi) if val < 0 else (- 2 * np.pi)
# 		return val


# def Car_Forward(car):

# 	pitch = float(car.Rotation.Pitch) * URotationToRadians
# 	yaw = float(car.Rotation.Yaw) * URotationToRadians
# 	roll = float(car.Rotation.Roll) * URotationToRadians

# 	facing_x = np.cos(pitch) *	np.cos(yaw)
# 	facing_y = np.cos(pitch) *	np.sin(yaw)
# 	facing_z = np.sin(pitch)

# 	#double check normilizations of vectors
# 	return Vector3(facing_x, facing_y, facing_z).normalize()

# def Car_Left(car):

# 	pitch = float(car.Rotation.Pitch) * URotationToRadians
# 	yaw = float(car.Rotation.Yaw) * URotationToRadians + np.pi/2
# 	roll = float(car.Rotation.Roll) * URotationToRadians

# 	facing_x = np.cos(pitch) *(-np.sin(yaw))
# 	facing_y = np.cos(pitch) *	np.cos(yaw)
# 	facing_z = np.sin(pitch)

# 	#double check normilizations of vectors
# 	return Vector3(facing_x, facing_y, facing_z).normalize()

# #retrieve transformation matrix from car info.
# def Car_TMat(car):
# 	return Get_TMat(Car_Forward(car), Car_Left(car), Vectorize_Loc(car))

# def Get_TMat(f, l, t):
# 	#Generate matrix transform
# 	#X Forward, Y = Left, Z = Up

# 	#Y = M . X
# 	#M = Y . X-1
# 	#X = indentity because of f, l, u corresponding to unit vectors

# 	u = f.cross(l)

# 	#the vector t is for translations

# 	#This matrix convert from local to global
# 	return np.concatenate((f.np(0), l.np(0), u.np(0), t.np(1)), axis=1)

# # #using matrix algorithms to find local and global coords
# # def to_local(car, vec):
# # 	#Inverted from the local to global matrix generated
# # 	matM = np.linalg.inv(Car_TMat(car))
# # 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# # 	return outvec

# # def to_global(car, vec):

# # 	matM = Get_TMat(car)
# # 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# # 	return outvec
