from vpython import *
scene = canvas(width=600, height=600, background=color.white)
scene.ambient = color.black

scene.userspin = False
scene.userpan = False
tiles = 4
tile = 0
y=100
x=100
while (tile < tiles):
    y_temp = y
    y=x * -1
    x = y_temp
    box (pos=vector(x,y,0), size=vector(200,200,200), texture="ice_tile.png")
    tile+=1

#sphere(pos=vec(0,0,0), texture=textures.wood, color=color.cyan)
