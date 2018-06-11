##
##~~~~~~~~SPRITES.PY~~~~~~~~
##
## Author: SamanthaHowze
##
##
##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from bge import logic, events

import mathutils, math

import Sprites

def KeyDown(keycode):
	
	keyboard = logic.keyboard.events

	if keyboard[keycode] == logic.KX_INPUT_ACTIVE:
		return 1
	
	return 0



def PlayerInit(cont):

	obj = cont.owner
	
	if not 'init' in obj:
		
		obj['init'] = 1
		
		obj['sprite'] = [c for c in obj.children if 'sprite' in c][0]

		obj['animdict'] = {
			'walk':['PlayerWalkR', 0, 1, 0, 2],
			'stand':['PlayerStandR', 0, 0, 0, 0, 0, 0, 
			0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3,
			3, 3, 3, 3, 3, 3, 3, 2],
		}
		
		obj['kb'] = {
		'left':events.LEFTARROWKEY,
		'right':events.RIGHTARROWKEY,
		'jump':events.XKEY,
		'action':events.CKEY,
		}

		obj['anim'] = 'walk'
		
		obj['friction'] = 0.5
		obj['accel'] = 0.5 + obj['friction']
		obj['maxspd'] = 5.0 + obj['friction']
		
		obj['facing'] = 1

	else:
		
		return 1

def PlayerUpdate(cont):
	
	obj = cont.owner
		
	mv = obj.worldLinearVelocity.copy()
	
	mv.y, mv.z = 0, 0
	
	mv.magnitude -= obj['friction'] if mv.magnitude - obj['friction'] > 0 else mv.magnitude
	
	if KeyDown(obj['kb']['left']) and mv.x - obj['accel'] > -obj['maxspd']:
		mv.x -= obj['accel']
	elif KeyDown(obj['kb']['right']) and mv.x + obj['accel'] < obj['maxspd']:
		mv.x += obj['accel']
		
	mv.z = obj.worldLinearVelocity.z
	
	obj.worldLinearVelocity = mv
	
	obj.worldPosition.y = 0
	
def PlayerAnimate(cont):

	obj = cont.owner
	
	mv = obj.getVelocity()

	if abs(mv.x) > 0.1:
		obj['anim'] = 'walk'
		sprfps = 6
	else:
		obj['anim'] = 'stand'
		sprfps = 12
		
	if mv.x > 0.1:
		obj['facing'] = 1
	elif mv.x < -0.1:
		obj['facing'] = -1
		
	e = obj['sprite'].worldOrientation.to_euler()
	
	if obj['facing'] == 1:
		e.z = 0
	elif obj['facing'] == -1:
		e.z = math.pi
	
	obj['sprite'].worldOrientation = e

	anim = obj['animdict'][obj['anim']]

	obj['sprite']['spranim'] = anim
	obj['sprite']['sprfps'] = sprfps

	Sprites.SpriteMesh(obj['sprite'])



def PlayerMain(cont):

	obj = cont.owner
		
	if PlayerInit(cont):
		PlayerUpdate(cont)
		PlayerAnimate(cont)
		