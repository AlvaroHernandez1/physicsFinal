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
        self.body = box(pos=self.position * 100, length = self.length * 100, width = 1, height = 10, color = color.cyan)
    def updatePosition(self, time):
        self.position += self.velocity * time
        self.body.pos = self.position * 100.0


scene = canvas(width=600, height=600, background=color.white)
scene.ambient = color.white
scene.lights = []
scene.userspin = False
scene.userpan = False
scene.range = 100

# Controller for loop
isRunning = True

# Objects
skaterList = []
pole = Pole(1, 1.0)

# Balls start not collided
ballsCollided = False

# Trials start at 0
trial = 0

com = vector(0, 0, 0)
totMass = 0
sysAngMom = vector(0, 0, 0)
sysMom = vector(0, 0, 0)
sysVelocity = vector(0, 0, 0)

comBall = sphere(pos = com*100, radius = 4)

# Graphs
angMomGraph = graph(title = "Angular Momentum Per Trial", xtitle = "Trial", ytitle = "Angular Momentum")
angMomBars = gvbars(graph = angMomGraph)

linMomentumGraph = graph(title = "Linear Momentum Per Trial", xtitle = "Trial", ytitle = "Linear Momentum")
linMomentumGraph = gvbars(graph = linMomentumGraph)

kineticEnergyGraph = graph(title = "Kinetic Energy Over Time", xtitle = "Time", ytitle = "Kinetic Energy")
kineticEnergyCurve = gcurve(graph = kineticEnergyGraph)

def start_simulation(evt):
    evt.disabled = True

    evt.current_skaters.append(Skater(vector(0.25,1.00,0.0), vector(0, -1.00, 0), 20, 5))
    evt.current_skaters.append(Skater(vector(-0.25,-1.00,0), vector(0, 1.00, 0), 10, 5))

    # Globals for calculating movement
    global com
    global totMass
    global sysAngMom
    global sysMom
    global ballsCollided
    global sysVelocity

    # Globals for creating graphs
    global angMomGraph
    global angMomBars

    # Balls stop being collided
    ballsCollided = False

    # Recalculate movement values
    com = vector(0, 0, 0)
    totMass = 0
    sysAngMom = vector(0, 0, 0)
    sysMom = vector(0, 0, 0)
    sysVelocity = vector(0, 0, 0)

    for skater in skaterList:
        com += skater.mass * skater.position
    com += pole.mass * pole.position

    for skater in skaterList:
        totMass += skater.mass
    totMass += pole.mass

    com /= totMass

    for skater in skaterList:
        sysAngMom += skater.updateL(com)

    for skater in skaterList:
        sysMom += skater.mass * skater.velocity 
    sysVelocity = sysMom / totMass

    # Update trial number
    trial += 1

    # Plot graphs
    angMomBars.plot(trial, sysAngMom)
    


def reset_simulation(evt):

    #global isRunning
    #isRunning = False
    global com
    global sysVelocity
    
    scene.camera.pos = vector(0,0,173)
    for skater in skaterList:
        skater.ball.visible = False
        #del skater
        #skaterList.remove(0)
    skaterList.clear()

    global ballsCollided
    ballsCollided = False
    #evt.current_pole.body.visible = False
    evt.current_pole.body.axis = vector(evt.current_pole.length * 100, 0.0, 0.0)
    evt.current_pole.velocity = vector(0, 0, 0)
    evt.current_pole.position = vector(0, 0, 0)
    evt.current_pole.body.pos = vector(0, 0, 0)

    com = vector(0, 0, 0)
    sysVelocity = vector(0, 0, 0)

    evt.start_button.disabled = False


startButton = button(bind=start_simulation, text="Start Simulation", current_skaters = skaterList)
resetButon = button(bind=reset_simulation, text="Reset Simulation", current_pole = pole, start_button = startButton)

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
    if ballsCollided:
        sysInertia = pole.I
        for skater in skaterList:
            sysInertia += skater.mass * (mag(skater.position - com)**2)

        angVelocity = sysAngMom / sysInertia
        for skater in skaterList:
            skater.ball.rotate(angle=mag(angVelocity)/60.0, axis = angVelocity, origin=com*100.0)
            skater.position = skater.ball.pos/100.0
            
        pole.body.rotate(angle=mag(angVelocity)/60.0, axis = angVelocity, origin = com*100.0)
        pole.position = pole.body.pos/100.0

        com += sysVelocity/60.0
        comBall.pos = com*100
        for skater in skaterList:
            skater.updatePosition(1/60.0)
        pole.updatePosition(1/60.0)

    else:
        com += sysVelocity/60.0
        comBall.pos = com*100
        for skater in skaterList:
            if not ballsCollided and abs(skater.position.y) > 0.15:
                skater.updatePosition(1/60.0)
            
            else:
                ballsCollided = True
                pole.velocity = sysVelocity
                for skater in skaterList:
                    skater.velocity = sysVelocity
    


