#Web VPython 3.2
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

    def updateK(self, angVelocity, cor, ):
        I = self.findI(cor)
        KR = 0.5 * I * (mag(angVelocity)**2)
        KT = 0.5 * self.mass * (mag(self.velocity)**2)
        #print(angVelocity)
        self.K = KR + KT
    def LWhileSpinning(self, angVelocity, cor):
        I = self.findI(cor)
        return I * angVelocity
    
    def setMass(self, mass):
        self.mass = mass
        self.I_com = self.mass * self.length * self.length * (1/12)
        self.K = 0


scene = canvas(width=600, height=600, background=color.white, align = "left")
scene.ambient = color.white
scene.lights = []
scene.userspin = False
scene.userpan = False
scene.range = 100
scene.userzoom = False
scene.resizable = False

# Controller for loop
isRunning = True

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
angMomGraph = graph(title = "Angular Momentum Over Time", xtitle = "Time (s)", ytitle = "Angular Momentum (kg·m²/s)", align = "left", xmin = 0, ymin = 0, xmax = 10, scroll = True)
angMomCurve = gcurve(graph = angMomGraph)

linMomentumGraph = graph(title = "Linear Momentum Over Time", xtitle = "Time (s)", ytitle = "Linear Momentum (kg·m/s)", align = "left", xmin = 0, xmax = 10, scroll = True, ymin = 0)
linMomentumCurve = gcurve(graph = linMomentumGraph)

kineticEnergyGraph = graph(title = "Kinetic Energy Over Time", xtitle = "Time (s)", ytitle = "Kinetic Energy (J)", align = "left", xmin = 0, xmax = 10, scroll = True, ymin = 0)
kineticEnergyCurve = gcurve(graph = kineticEnergyGraph)

#ensures all three graphs are plotted at same time
kineticEnergyCurve.plot(0, 0)
angMomCurve.plot(0, 0)
linMomentumCurve.plot(0, 0)

#User Interface ---Would Love to figure out how to put this on the rirght side!

scene.append_to_caption(" Basic Instructions:\n")
scene.append_to_caption(" 1. Play with the presets below to adjust the skaters, pole, and collision timing.\n\n 2. Press Start to run the simulation. \n\n 3. After collision, move the skaters along the pole using the position sliders.\n\n 4. Press Reset to restart with the same settings.\n\n 5. Press Factory Reset to return everything to default. \n\n Note: The smaller white circle represents the system's center of mass.\n\n\n")
scene.append_to_caption(" Skater One\n")
scene.append_to_caption(" Mass: ")
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

scene.append_to_caption("\n Skater One Color: ")

colOne = 'cyan'
colTwo = colOne

def skaterOneColor(m):
    global colOne
    if m.selected != "Choose a Color":
        val = m.selected
        colOne = val


skaterOneMenu = menu(choices=['Choose a Color', 'blue', 'green', 'red', 'yellow'], index=0, bind=skaterOneColor)

scene.append_to_caption("\n\n Skater Two\n")
scene.append_to_caption(" Mass: ")
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

scene.append_to_caption("\n Skater Two Color: ")

def skaterTwoColor(m):
    global colTwo
    if m.selected != "Choose a Color":
        val = m.selected
        colTwo = val


skaterTwoMenu = menu(choices=['Choose a Color', 'blue', 'green', 'red', 'yellow'], index=0, bind=skaterTwoColor)



scene.append_to_caption('\n\n\n\n\n')

scene.append_to_caption(" Pole\n Mass: ")
poleMassText = wtext(text="10")
scene.append_to_caption(" kg")
def updatePoleMass(s): 
    poleMassText.text = str(int(s.value))
poleMass = slider(min=1, max=50, value=10, step=1, bind=updatePoleMass)

scene.append_to_caption("\n\n\n\n")
scene.append_to_caption(" Time to Collision: ")
timeText = wtext(text="1")
scene.append_to_caption(" s")
def updateTimeToCollision(s): 
    timeText.text = str(s.value)
timeToCollision = slider(min=1, max=5, value=1, step=1, bind=updateTimeToCollision)


scene.append_to_caption("\n\n\n\n\n")

# Objects
skaterList = []
#Where I can set custom mass and lengths
pole = Pole(poleMass.value, 1.0)

def factory_reset(evt):
    global colOne
    global colTwo
    global kineticEnergyCurve
    global angMomCurve
    global linMomentumCurve
    global time

    reset_simulation(evt)

    s1Mass.value = 10
    s1X.value = 0.25
    s1V.value = 1.0

    s2Mass.value = 10
    s2X.value = 0.25
    s2V.value = 1.0

    timeToCollision.value = 1.0
    poleMass.value = 10

    positionOnPole1.value = 0.25
    positionOnPole2.value = 0.25

    #need to update text as well
    s1MassText.text = "10"
    s1XText.text = "0.25"
    s1VText.text = "1.0"
    s2MassText.text = "10"
    s2XText.text = "0.25"
    s2VText.text = "1.0"
    timeText.text = "1.0"
    poleMassText.text = "10"
    positionText1.text = "0.25"
    positionText2.text = "0.25"

    skaterOneMenu.index = 0
    skaterTwoMenu.index = 0

    colOne = "cyan"
    colTwo = "cyan"

    pole.setMass(10)

    time = 0

    kineticEnergyCurve.delete()
    angMomCurve.delete()
    linMomentumCurve.delete()

    kineticEnergyCurve = gcurve(graph = kineticEnergyGraph)
    angMomCurve = gcurve(graph = angMomGraph)
    linMomentumCurve = gcurve(graph = linMomentumGraph)

    kineticEnergyCurve.plot(0, 0)
    angMomCurve.plot(0, 0)
    linMomentumCurve.plot(0, 0)




def start_simulation(evt):
    evt.disabled = True
    positionOnPole1.value = abs(s1X.value)
    positionOnPole2.value = abs(s2X.value)
    positionText1.text = str(abs(s1X.value))
    positionText2.text = str(abs(s2X.value))

    pole.setMass(poleMass.value)
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
    #linMomentumBars.plot(trial, mag(sysMom))
    


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
    sysAngMom = vector(0,0,0)
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

    global sysMom
    global kineticEnergy

    sysMom = vector(0,0,0)
    kineticEnergy = 0

    evt.start_button.disabled = False


startButton = button(bind=start_simulation, text="▶ Start", current_skaters = skaterList, background = vector(144/255, 238/255, 144/255))
scene.append_to_caption("   ")
resetButon = button(bind=reset_simulation, text="↺ Reset", current_pole = pole, start_button = startButton, background = vector(255/255, 127/255, 127/255))
scene.append_to_caption("   ")
factoryResetButton = button(bind=factory_reset, text="⚠ Factory Reset", current_pole=pole, start_button=startButton, background = vector(0,0,0), color = vector(255/255, 255/255, 0))

#Moving Skaters on pole
scene.append_to_caption("\n\nSkater One Position on Pole: ")
positionText1 = wtext(text="0.25")
scene.append_to_caption(" m")
def updatePositionOnPole1(s):
    global ballsCollided
    if ballsCollided:
        positionText1.text = str(s.value)
    else:
        s.value = positionOnPole1.value
positionOnPole1 = slider(min=0.01, max=0.5, value=abs(s1X.value), step=.01, bind=updatePositionOnPole1)

scene.append_to_caption("Skater Two Position on Pole: ")
positionText2 = wtext(text="0.25")
scene.append_to_caption(" m")
def updatePositionOnPole2(s):
    global ballsCollided
    if ballsCollided:
        positionText2.text = str(s.value)
    else:
        s.value = positionOnPole2.value
positionOnPole2 = slider(min=0.01, max=0.5, value=abs(s2X.value), step=.01, bind=updatePositionOnPole2)

scene.append_to_caption("\n\n")

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
        # Updating skater positions
        if len(skaterList) == 2:
            pole_axis = norm(pole.body.axis)

            skater1 = skaterList[0]
            skater1.position = pole.position - pole_axis * positionOnPole1.value
            skater1.ball.pos = skater1.position * 100

            skater2 = skaterList[1]
            skater2.position = pole.position + pole_axis * positionOnPole2.value
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
        linMomentumCurve.plot(time, mag(sysMom))




    else:
        positionOnPole1.value = abs(s1X.value)
        positionOnPole2.value = abs(s2X.value)
        positionText1.text = str(abs(s1X.value))
        positionText2.text = str(abs(s2X.value))

        com += sysVelocity/60.0
        comBall.pos = com*100
        for skater in skaterList:
            skater.updatePosition(1/60.0)
        if len(skaterList) > 0 and skaterList[0].position.y <= 0:
            ballsCollided = True
            pole.velocity = sysVelocity
            for skater in skaterList:
                skater.velocity = sysVelocity
        if len(skaterList) > 0:       
            kineticEnergyCurve.plot(time, kineticEnergy)
        else:
            kineticEnergyCurve.plot(time, 0)
        linMomentumCurve.plot(time, mag(sysMom))
        angMomCurve.plot(time,0)
    time += 1/60.0

