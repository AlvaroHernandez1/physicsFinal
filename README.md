Web VPython 3.2
# physicsFinal

## Overview

#This GlowScript VPython simulation models two skaters on frictionless ice colliding with and grabbing onto a pole. After impact, the skaters and pole rotate together as one system.

#The simulation demonstrates conservation of angular momentum. It also shows that kinetic energy is not conserved because the collision is inelastic.

## How to Use

#1. Before starting, use the sliders and dropdown menus to set each skater's mass, starting position, speed, and color. You can also adjust the time until collision. Slide the sliders left and right to change the values. The number next to each slider will update as you move it.
#2. Press "Start Simulation". Two colored balls will appear on screen and move toward the pole in the center. They will both hit the pole at the same time. In however many seconds you decided beforehand.
#3. After the collision, the skaters and pole will start spinning together. The small white circle in the middle shows where the center of mass of the system is.
#4. While the skaters are spinning, look at the bottom of the screen for two sliders labeled "Skater One Position on Pole" and "Skater Two Position on Pole." Slide them to move each skater closer to or farther from the center of the pole. 
#5. When you are done, press "Reset Simulation" to clear the skaters and try again with new settings. Pressing "Factory Reset" will restart everything to its original state.

## Controls

#Each skater has sliders for mass, starting x position, and approach speed, as well as a dropdown to choose their color. The time to collision slider controls how long the skaters travel before hitting the pole. After the collision, the position on pole sliders let you move each skater closer to or farther from the center.

## Graphs

#Three graphs are displayed in real time. The kinetic energy graph shows a drop at the moment of collision since energy is lost in the inelastic impact. The linear momentum graph shows that linear momentum is conserved throughout. The angular momentum graph shows that angular momentum is conserved after the collision.

## Physics Concepts

#Conservation of angular momentum dictates that after the skaters grab the pole, the total angular momentum of the system stays constant. Because angular momentum equals moment of inertia times angular velocity, if one changes the other must change to compensate. Moving the skaters farther from the center increases the moment of inertia and slows the rotation. Moving them inward decreases it and speeds the rotation up.

#When a skater pulls themselves inward along the pole, the pole does not stay still, instead it shifts in the opposite direction. This is Newton's third law: the skater pulls on the pole, and the pole pulls back on the skater with an equal and opposite force. The result is that the center of mass of the whole system stays in the same place, even though both the skater and the pole have moved.

#The collision itself is inelastic, so kinetic energy is lost at the moment of impact, which is visible as a drop on the KE graph. The system rotates around its center of mass, which shifts as the skaters move along the pole.

#Github page: https://github.com/AlvaroHernandez1/physicsFinal.git

scene = canvas(width=1000, height=1000)
originalProblem = "https://i.imgur.com/0YfGbd6.png"
background = box(pos=vector(0, 0, -1), size=vector(1000, 400, 400), texture=originalProblem)
