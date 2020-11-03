
import turtle
pen = turtle.Turtle()

def branch(turt):
    pass
    #put in your code here to make the branch look fantastic!
    #the funtion is called while the turtle is facing directly out in the direction of the branch.

def snowflake():
    pen.up()    #pen going to move without drawing
    pen.seth(240)   #faces the bottom left
    pen.forward(50) #moves to the outside of the hexagon
    pen.seth(0)  #pen faces directly right
    pen.down()  #pen is ready to draw
    for i in range(6):  #makes 6 sides of the hexagon
        pen.forward(50) #makes the side of the hexagon 50 pixels long
        pen.right(60) #faces towards the outside of the hexagon
        branch(pen)  #this calls the branch function.
        pen.left(120) #turns to continue the next side of the hexagon

def from_start():
    #this function resets the pen to be directly in middle facing right
    pen.up()
    pen.seth(0)
    pen.goto(0,0)
    pen.down()

def main():
    #this is the main function that controls the program.
    turtle.bgcolor('black')
    pen.color('lightblue')
    pen.width(2)
    snowflake()
    turtle.exitonclick()

main()
