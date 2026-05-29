from vpython import *

class Skater:
    def __init__(self, position, velocity, mass, collision_position):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.collision_position = collision_position
        self.ball = sphere(pos=self.position, radius = 15, color = color.cyan)
        self.L = 0

    def updatePosition(self, time):
        self.position += self.velocity * time
        self.ball.pos = self.position

    def updateL(self, cor):
        r = self.position - cor
        self.L = cross(r, self.velocity)
        return self.L

        



class Pole:
    def __init__(self, mass, length):
        self.mass = mass
        self.length = length
        self.I = mass * length * length * (1/12)
        self.velocity = vector(0,0,0)
        self.position = vector(0,0,0)
        self.body = box(pos=self.position, length = self.length, width = 1, height = 10, color = color.cyan)


scene = canvas(width=600, height=600, background=color.white)
scene.ambient = color.white
scene.lights = []
scene.userspin = False
scene.userpan = False
scene.range = 100
isRunning = True
skaterList = []
skaterList.append(Skater(vector(-25,100,0), vector(0, -50, 0), 10, 5))
skaterList.append(Skater(vector(25,-100,0), vector(0, 50, 0), 10, 5))
pole = Pole(10, 92)

lastTime = 0

def reset_simulation():
    isRunning = False
    scene.camera.pos = vector(0,0,0)
    for skater in skaterList:
        skater.ball.visible = False
        del skater
    isRunning = True

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

ballsCollided = False

com = vector(0, 0, 0)
for skater in skaterList:
    com += skater.mass * skater.position
com += pole.mass * pole.position
totMass = 0
for skater in skaterList:
    totMass += skater.mass
totMass += pole.mass

com /= totMass

print (com)
sysAngMom = vector(0, 0, 0)
for skater in skaterList:
    sysAngMom += skater.updateL(com)

sysMom = vector(0, 0, 0)
for skater in skaterList:
    sysMom += skater.mass * skater.velocity

while isRunning:
    rate(60)

    for skater in skaterList:
        if abs(skater.position.y) > 15 and not ballsCollided:
            skater.updatePosition(1/60.0)
        else:
            ballsCollided = True
    #if ballsCollided:
        #for skater in skaterList
    


