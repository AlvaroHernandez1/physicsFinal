from vpython import *

class Skater:
    def __init__(self, position, velocity, mass, col):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.ball = sphere(pos=self.position * 100, radius = 15, color = eval("color." + col))
        self.L = 0
        self.K = 0.5 * mass * (mag(velocity)**2)
        

    def updatePosition(self, time):
        self.position += self.velocity * time
        self.ball.pos = self.position * 100.0
        

    def updateL(self, cor):
        r = self.position - cor
        self.L = self.mass * cross(r, self.velocity)
        return self.L

    def rotateVelocity(self, angVelocity, cor):
        self.velocity = cross(angVelocity, (self.position - cor))
    
    def updateK(self, angVelocity, cor):
        I = self.mass * (mag(self.position - cor)**2)
        KR = 0.5 * I * (mag(angVelocity)**2)
        KT = 0.5 * self.mass * (mag(self.velocity)**2)
        #print('Ball rotational K: ', KR)
        #print('Ball translational K: ', KT)
        self.K = KR + KT

    def LWhileSpinning(self, angVelocity, cor):
        I = self.mass * (mag(self.position - cor)**2)
        return angVelocity * I
        



class Pole:
    def __init__(self, mass, length):
        self.mass = mass
        self.length = length
        self.I_com = mass * length * length * (1/12)
        self.velocity = vector(0,0,0)
        self.position = vector(0,0,0)
        self.body = box(pos=self.position * 100, length = self.length * 100, width = 1, height = 10, color = color.cyan)
        self.K = 0

    def updatePosition(self, time):
        self.position += self.velocity * time
        self.body.pos = self.position * 100.0
    
    def findI(self, cor):
        return self.I_com + self.mass * (mag(self.position - cor)**2)

    def updateK(self, angVelocity, cor):
        I = self.findI(cor)
        KR = 0.5 * I * (mag(angVelocity)**2)
        KT = 0.5 * self.mass * (mag(self.velocity)**2)
        print(angVelocity)
        self.K = KR + KT
    def LWhileSpinning(self, angVelocity, cor):
        I = self.findI(cor)
        return I * angVelocity


scene = canvas(width=600, height=600, background=color.white, align = "left")
scene.ambient = color.white
scene.lights = []
scene.userspin = False
scene.userpan = False
scene.range = 100

# Controller for loop
isRunning = True

# Objects
skaterList = []
pole = Pole(0.00001, 1.0)

# Balls start not collided
ballsCollided = False

# Trials start at 0
trial = 0

com = vector(0, 0, 0)
totMass = 0
sysAngMom = vector(0, 0, 0)
sysMom = vector(0, 0, 0)
sysVelocity = vector(0, 0, 0)
kineticEnergy = 0

comBall = sphere(pos = com*100, radius = 4)

# Graphs
angMomGraph = graph(title = "Angular Momentum Per Trial", xtitle = "Trial", ytitle = "Angular Momentum", align = "left", xmin = 0, ymin = 0, xmax = 10, scroll = True)
angMomCurve = gcurve(graph = angMomGraph)

linMomentumGraph = graph(title = "Linear Momentum Per Trial", xtitle = "Trial", ytitle = "Linear Momentum", align = "left", xmin = 0, ymin = 0)
linMomentumBars = gvbars(graph = linMomentumGraph, delta = 0.25)

kineticEnergyGraph = graph(title = "Kinetic Energy Over Time", xtitle = "Time", ytitle = "Kinetic Energy", align = "left", xmin = 0, xmax = 10, scroll = True, ymin = 0)
kineticEnergyCurve = gcurve(graph = kineticEnergyGraph)

#User Interface ---Would Love to figure out how to put this on the rirght side!
scene.append_to_caption("Skater 1\n")
scene.append_to_caption("Mass: ")
s1MassText = wtext(text="10")
def updateS1Mass(s): 
    s1MassText.text = str(int(s.value))
scene.append_to_caption(" kg")
s1Mass = slider(min=1, max=50, value=10, step=1, bind=updateS1Mass)

scene.append_to_caption("  X position: -")
s1XText = wtext(text="0.25")
def updateS1X(s): 
    s1XText.text = str(s.value)
scene.append_to_caption(" m")

s1X = slider(min=0.01, max=0.5, value=0.25, step=0.01, bind=updateS1X)

scene.append_to_caption("  Speed: ")
s1VText = wtext(text="1")
scene.append_to_caption(" m/s")
def updateS1V(s): 
    s1VText.text = str(s.value)
s1V = slider(min=0.5, max=3.0, value=1.0, step=0.1, bind=updateS1V)

scene.append_to_caption("\n\nSkater 2\n")
scene.append_to_caption("Mass: ")
s2MassText = wtext(text="10")
scene.append_to_caption(" kg")
def updateS2Mass(s): 
    s2MassText.text = str(int(s.value))
s2Mass = slider(min=1, max=50, value=10, step=1, bind=updateS2Mass)

scene.append_to_caption("  X position: ")
s2XText = wtext(text="0.25")
scene.append_to_caption(" m")
def updateS2X(s): 
    s2XText.text = str(s.value)
s2X = slider(min=0.01, max=0.5, value=0.25, step=0.01, bind=updateS2X)

scene.append_to_caption("  Speed: ")
s2VText = wtext(text="1")
scene.append_to_caption(" m/s")
def updateS2V(s): 
    s2VText.text = str(s.value)
s2V = slider(min=0.5, max=3.0, value=1.0, step=0.1, bind=updateS2V)

scene.append_to_caption("\n\n")
scene.append_to_caption("Time to Collision: ")
timeText = wtext(text="1")
scene.append_to_caption(" s")
def updateTimeToCollission(s): 
    timeText.text = str(s.value)
timeToCollision = slider(min=1, max=5.0, value=1.0, step=1, bind=updateTimeToCollission)


scene.append_to_caption("\n\n Skater One Color:")

colOne = 'cyan'
colTwo = colOne

def skaterOneColor(m):
    global colOne
    val = m.selected
    colOne = val


menu(choices=['Choose a Color', 'blue', 'green', 'red', 'yellow'], index=0, bind=skaterOneColor)

scene.append_to_caption("Skater Two Color:")

def skaterTwoColor(m):
    global colTwo
    val = m.selected
    colTwo = val


menu(choices=['Choose a Color', 'blue', 'green', 'red', 'yellow'], index=0, bind=skaterTwoColor)

scene.append_to_caption('\n')


scene.append_to_caption("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def start_simulation(evt):
    evt.disabled = True
    positionOnPole1.value = abs(s1X.value)
    positionOnPole2.value = abs(s2X.value)
    positionText1.text = str(abs(s1X.value))
    positionText2.text = str(abs(s2X.value))

    # Y position is equal to Time * Velocity, to make the both balls collide at same time
    evt.current_skaters.append(Skater(vector(-1*s1X.value, timeToCollision.value * s1V.value, 0), vector(0, -s1V.value, 0), s1Mass.value, colOne))
    evt.current_skaters.append(Skater(vector(s2X.value, -timeToCollision.value * s2V.value, 0), vector(0, s2V.value, 0), s2Mass.value, colTwo))

    # Globals for calculating movement
    global com
    global totMass
    global sysAngMom
    global sysMom
    global ballsCollided
    global sysVelocity
    global kineticEnergy

    # Globals for creating graphs
    global angMomGraph
    global angMomBars

    global linMomentumGraph
    global linMomentumBars

    global trial

    # Balls stop being collided
    ballsCollided = False

    # Recalculate movement values
    com = vector(0, 0, 0)
    totMass = 0
    sysAngMom = vector(0, 0, 0)
    sysMom = vector(0, 0, 0)
    sysVelocity = vector(0, 0, 0)

    kineticEnergy = 0
    for skater in evt.current_skaters:
        kineticEnergy += skater.K

    for skater in skaterList:
        com += skater.mass * skater.position
    com += pole.mass * pole.position

    for skater in skaterList:
        totMass += skater.mass
    totMass += pole.mass

    com /= totMass

    for skater in skaterList:
        sysAngMom += skater.updateL(com)
    #print(sysAngMom)
    for skater in skaterList:
        sysMom += skater.mass * skater.velocity 
    sysVelocity = sysMom / totMass

    # Update trial number
    trial += 1

    # Plot graphs
    #angMomBars.plot(trial, mag(sysAngMom))
    linMomentumBars.plot(trial, mag(sysMom))
    


def reset_simulation(evt):

    #global isRunning
    #isRunning = False
    global com
    global sysVelocity

    global graphAngMom
    #graphAngMom = 0
    
    #global angVelocity
    #angVelocity = 0

    global sysAngMom
    sysAngMom = 0
    scene.camera.pos = vector(0,0,173)
    for skater in skaterList:
        skater.ball.visible = False
        #del skater
        #skaterList.remove(0)
    skaterList.clear()
    global ballsCollided
    ballsCollided = False
    #evt.current_pole.body.visible = False
    evt.current_pole.velocity = vector(0, 0, 0)
    evt.current_pole.body.axis = vector(evt.current_pole.length * 100, 0.0, 0.0)
    evt.current_pole.position = vector(0, 0, 0)
    evt.current_pole.body.pos = vector(0, 0, 0)

    com = vector(0, 0, 0)
    sysVelocity = vector(0, 0, 0)

    evt.start_button.disabled = False


startButton = button(bind=start_simulation, text="Start Simulation", current_skaters = skaterList)
resetButon = button(bind=reset_simulation, text="Reset Simulation", current_pole = pole, start_button = startButton)

#Moving Skaters on pole
scene.append_to_caption("\n\nSkater One Position on Pole ")
positionText1 = wtext(text="0.25")
scene.append_to_caption(" m")
def updatePositionOnPole1(s):
    global ballsCollided
    if ballsCollided:
        positionText1.text = str(s.value)
    else:
        s.value = positionOnPole1.value
positionOnPole1 = slider(min=0.1, max=0.5, value=abs(s1X.value), step=.1, bind=updatePositionOnPole1) # max should be pole length

scene.append_to_caption("Skater One Position on Pole ")
positionText2 = wtext(text="0.25")
scene.append_to_caption(" m")
def updatePositionOnPole2(s):
    global ballsCollided
    if ballsCollided:
        positionText2.text = str(s.value)
    else:
        s.value = positionOnPole2.value
positionOnPole2 = slider(min=0.1, max=0.5, value=abs(s1X.value), step=.1, bind=updatePositionOnPole2)

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


time = 0
while isRunning:
    rate(60)
    if ballsCollided:
        # Updating Ball Position
        if len(skaterList) == 2:
            skater1 = skaterList[0]
            distance_vector = skater1.position - pole.position
            distance_vector *= positionOnPole1.value/(mag(distance_vector))
            skater1.position = distance_vector + pole.position
            skater1.ball.pos = skater1.position * 100
        # Update other skater
        if len(skaterList) == 2:
            skater2 = skaterList[1]
            distance_vector = skater2.position - pole.position
            distance_vector *= positionOnPole2.value/(mag(distance_vector))
            skater2.position = distance_vector + pole.position
            skater2.ball.pos = skater2.position * 100

        # Update COM
        
        temp_com = vector(0, 0, 0)
        totMass = 0
        for skater in skaterList:
            temp_com += skater.mass * skater.position
        temp_com += pole.mass * pole.position

        for skater in skaterList:
            totMass += skater.mass
        totMass += pole.mass

        temp_com /= totMass

        com_change = com - temp_com

        pole.position += com_change
        pole.body.pos = pole.position*100
        for skater in skaterList:
            skater.position += com_change
            skater.ball.pos = skater.position * 100

        sysInertia = pole.findI(com)
        for skater in skaterList:
            sysInertia += skater.mass * (mag(skater.position - com)**2)
            #print(mag(skater.position - com))
        #print(sysInertia)

        angVelocity = sysAngMom / sysInertia
        #print(angVelocity)
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

        # Calculate kinetic energy
        kineticEnergy = 0
        for skater in skaterList:
            skater.updateK(angVelocity, com)
            kineticEnergy += skater.K
        pole.updateK(angVelocity, com)
        kineticEnergy += pole.K
        #print(kineticEnergy)

        # Graph new kinetic energy
        kineticEnergyCurve.plot(time, kineticEnergy)

        # Calculate angular momentum
        global graphAngMom
        graphAngMom = vector(0, 0, 0)
        for skater in skaterList:
            graphAngMom += skater.LWhileSpinning(angVelocity, com)
        graphAngMom += pole.LWhileSpinning(angVelocity, com)

        angMomCurve.plot(time, mag(graphAngMom))



    else:
        com += sysVelocity/60.0
        comBall.pos = com*100
        for skater in skaterList:
            skater.updatePosition(1/60.0)

        if skaterList and skaterList[0].position.y <= 0:
            ballsCollided = True
            pole.velocity = sysVelocity
            for skater in skaterList:
                skater.velocity = sysVelocity
        if skaterList:       
            kineticEnergyCurve.plot(time, kineticEnergy)
        else:
            kineticEnergyCurve.plot(time, 0)
    time += 1/60.0


