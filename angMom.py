from vpython import *

class Skater:
    def __init__(self, position, velocity, mass, collision_position):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.collision_position = collision_position
        self.ball = sphere(pos=self.position * 100, radius = 15, color = color.cyan)
        self.L = 0
        

    def updatePosition(self, time):
        self.position += self.velocity * time
        self.ball.pos = self.position * 100.0
        

    def updateL(self, cor):
        r = self.position - cor
        self.L = self.mass * cross(r, self.velocity)
        return self.L

    def rotateVelocity(self, angVelocity, cor):
        self.velocity = cross(angVelocity, (self.position - cor))
    
        



class Pole:
    def __init__(self, mass, length):
        self.mass = mass
        self.length = length
        self.I = mass * length * length * (1/12)
        self.velocity = vector(0,0,0)
        self.position = vector(0,0,0)
        self.body = box(pos=self.position, length = self.length * 100, width = 1, height = 10, color = color.cyan)


scene = canvas(width=600, height=600, background=color.white)
scene.ambient = color.white
scene.lights = []
scene.userspin = False
scene.userpan = False
scene.range = 100
isRunning = True
skaterList = []
skaterList.append(Skater(vector(-0.25,1.00,0.0), vector(0, -1.00, 0), 10, 5))
skaterList.append(Skater(vector(0.25,-1.00,0), vector(0, 1.00, 0), 10, 5))
pole = Pole(0, 1.0)
ballsCollided = False

def reset_simulation():
    isRunning = False
    scene.camera.pos = vector(0,0,173)
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

com = vector(0, 0, 0)
for skater in skaterList:
    com += skater.mass * skater.position
com += pole.mass * pole.position
totMass = 0
for skater in skaterList:
    totMass += skater.mass
totMass += pole.mass

com /= totMass

sysAngMom = vector(0, 0, 0)
for skater in skaterList:
    sysAngMom += skater.updateL(com)

sysMom = vector(0, 0, 0)
for skater in skaterList:
    sysMom += skater.mass * skater.velocity

prevTime = 0

while isRunning:
    rate(60)

    for skater in skaterList:
        if not ballsCollided and abs(skater.position.y) > 0.15:
            skater.updatePosition(1/60.0)
            
        else:
            ballsCollided = True
    if ballsCollided:
        sysInertia = pole.I
        for skater in skaterList:
            sysInertia += skater.mass * (mag(skater.position - com)**2)

        angVelocity = sysAngMom / sysInertia
        for skater in skaterList:
            skater.ball.rotate(angle=mag(angVelocity)*60.0, axis=com*100.0+vector(0,0.0, 1.0))
            skater.position = skater.ball.pos/100.0
            #skater.rotateVelocity(angVelocity, com)

            #skater.updatePosition(1/60.0)
    


