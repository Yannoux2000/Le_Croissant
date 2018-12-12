from LeFramework.common.Vector import *
from LeFramework.common.Objs import *

def sign(val):
	return (1) if (val>0) else (-1)

def cap(_val, _min, _max):
	return max(_min, min(_val, _max))

def steer(angle):
	final = ((10 * angle+sign(angle))**3) / 20
	return cap(final,-1,1)

def simpleController(agent, t_obj, t_vel, boost, dodge):
	controller_state = SimpleControllerState()

	t_loc = agent.me.to_local(t_obj)
	me_vel = agent.me.vel.magnitude()
	t_agl = math.atan2(t_loc[1], t_loc[0])

	if t_vel > me_vel:
		controller_state.throttle = 1.0
		if t_vel > 1400 and delta_t > 2.2 and me_vel < 2250 and boost and abs(t_agl) < 1.3:
			controller_state.boost = True
	elif t_vel < me_vel:
		controller_state.throttle = 0

	controller_state.steer = controller_state.yaw = steer(t_agl)

	return controller_state

def controller(agent, t_obj, t_vel, boost, dodge):
		controller_state = SimpleControllerState()

		t_loc = agent.me.to_local(t_obj)
		me_vel = agent.me.vel.magnitude()
		t_agl = math.atan2(t_loc[1], t_loc[0])
		
		delta_t = agent.time - agent.start

		#steer
		controller_state.steer = controller_state.yaw = steer(t_agl)

		#throttle
		if t_vel > me_vel:
			controller_state.throttle = 1.0
			if t_vel > 1400 and delta_t > 2.2 and me_vel < 2250 and boost and abs(t_agl) < 1.3:
				controller_state.boost = True
		elif t_vel < me_vel:
			controller_state.throttle = 0

		#handbrake
		if abs(t_agl) > 1.3:
			controller_state.handbrake = True
			controller_state.boost = False
		else:
			controller_state.handbrake = False

		# dodging
		if delta_t > 2.2 and (t_obj.distance(agent.me)) > me_vel and abs(t_agl) < 0.6 and dodge:
			agent.start = agent.time
		elif delta_t <= 0.1:
			controller_state.jump = True
			controller_state.pitch = -1
		elif delta_t >= 0.1 and delta_t <= 0.15:
			controller_state.jump = False
			controller_state.pitch = -1
		elif delta_t > 0.15 and delta_t < 1:
			controller_state.jump = True
			controller_state.pitch = -1
			# controller_state.yaw = controller_state.steer

		return controller_state
