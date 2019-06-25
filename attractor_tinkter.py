from tkinter import *
import time, math


canvas_width, canvas_height = 1000, 1000

root = Tk()
root.geometry(f"{canvas_width}x{canvas_height}")

c = Canvas(root, height=canvas_height, width=canvas_width, bg="black")
c.pack()

def step(x, y, z, dt):
    sigma, roe, beta = 10, 28, 8/3

    dx = (sigma * (y - x)) * dt
    dy = (x * (roe - z) - y) * dt
    dz = (x * y - beta * z) * dt

    return dx, dy, dz

def movepoint(canvas, point, dx, dy):
    side = dx * 10 #math.floor(dx * 10)
    vertical = dy * 10 #math.floor(dy * 10)
    print(f"move ({side}, {vertical}).")
    canvas.move(point, side, vertical)

def createline(canvas, point, dx, dy, color):
    side = dx * 10 #math.floor(dx*10)
    vertical = dy * 10#math.floor(dy*10)
    x, y, _, __ = canvas.coords(point)
    canvas.create_line(x, y, x + side, y + vertical, fill=color)

def main():
    size = 10
    t, dt = 0, .01

    point_a = c.create_oval(canvas_width/2, canvas_height/2, canvas_width/2 + size, canvas_height/2 + size, fill="red")
    x_a, y_a, z_a = 1, 1, 1
    dx_a, dy_a, dz_a = 0, 0, 0
    '''
    point_b = c.create_oval(canvas_width/2, canvas_height/2, canvas_width/2 + size, canvas_height/2 + size, fill="green")
    x_b, y_b, z_b = 1, 1, 2
    dx_b, dy_b, dz_b = 0, 0, 0
    '''
    point_c = c.create_oval(canvas_width/2, canvas_height/2, canvas_width/2 + size, canvas_height/2 + size, fill="blue")
    x_c, y_c, z_c = 1, 1, 1.1
    dx_c, dy_c, dz_c = 0, 0, 0


    #print(f"Made a point with x={canvas_width/2} and y = {canvas_height/2}.")

    while True:
        #print(f"({x}, {y}, {z}) with the changes to be ({dx}, {dy}, {dz})")
        createline(c, point_a, dx_a, dy_a, 'red')
        dx_a, dy_a, dz_a, = step(x_a, y_a, z_a, dt)
        x_a += dx_a
        y_a += dy_a
        z_a += dz_a
        movepoint(c, point_a, dx_a, dy_a)
        '''
        createline(c, point_b, dx_b, dy_b, 'green')
        dx_b, dy_b, dz_b, = step(x_b, y_b, z_b, dt)
        x_b += dx_b
        y_b += dy_b
        z_b += dz_b
        movepoint(c, point_b, dx_b, dy_b)
        '''
        createline(c, point_c, dx_c, dy_c, 'blue')
        dx_c, dy_c, dz_c, = step(x_c, y_c, z_c, dt)
        x_c += dx_c
        y_c += dy_c
        z_c += dz_c
        movepoint(c, point_c, dx_c, dy_c)



        root.update_idletasks()
        root.update()
        time.sleep(.01)

main()
