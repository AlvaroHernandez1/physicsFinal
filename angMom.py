from vpython import *

class Skater:
    def __init__(self, position, velocity, mass, collision_position):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.collision_position = collision_position
        self.ball = sphere(pos=self.position, radius = 15, color = color.cyan)

    def updatePosition(self, time):
        self.position += self.velocity * time
        self.ball.pos = self.position

    def updateL(self, cor):
        r = self.position - cor
        L = mag(cross(r, self.velocity))



class Pole:
    def __init__(self, mass, length):
        self.mass = mass
        self.length = length
        self.I = mass * length * length * (1/12)

        self.velocity = 0

def reset_simulation():
    isRunning = False
    scene.camera.pos = vector(0,0,0)

scene = canvas(width=600, height=600, background=color.white)
scene.ambient = color.white
scene.lights = []
scene.userspin = False
scene.userpan = False
scene.range = 100
button(bind=reset_simulation, text="Reset Simulation")
isRunning = True
skaterList = []
skaterList.append(Skater(vector(-25,100,0), vector(0, -50, 0), 10, 5))
skaterList.append(Skater(vector(25,-100,0), vector(0, 50, 0), 10, 5))

lastTime = 0

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


while isRunning:
    rate(60)
    for skater in skaterList:
        skater.updatePosition(1/60.0)


