from vpython import *

class Skater
    def __init__(position, velocity, mass, collision_position):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.collision_position = collision_position

    def updatePosition(time):
        self.position += self.velocity * time


class Pole
    def __init__(mass, length):
        self.mass = mass
        self.length = length
        self.I = mass * length * length * (1/12)

        self.velocity = 0



scene = canvas(width=600, height=600, background=color.white)
scene.ambient = color.white
scene.lights = []
scene.userspin = True
scene.userpan = True
scene.range = 100
button(bind=reset_simulation, text="Reset Simulation")

ice_texture = "https://i.imgur.com/SCIkDjk.png"
tiles = 4
tile = 0
y=100
x=100
while (tile < tiles):
    y_temp = y
    y=x * -1
    x = y_temp
    box (pos=vector(x,y,0), size=vector(200,200,0.1), texture=ice_texture)
    tile+=1


def reset_simulation():
    scene.camera.pos = vector(0,0,0)

