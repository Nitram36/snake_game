# Import packages
import math, random, pygame
import tkinter as tk
from tkinter import messagebox

# Define a Cube class representing individual segments of the snake and snake snacks
class Cube:

    # Class variables
    width = 700 # width of game window
    rows = 20 # number of rows in game window
    
    # Constructor
    def __init__(self, pos, x_dir=1, y_dir=0, color='red'):
        self.pos = pos # position of cube as a tuple (x,y)
        self.x_dir = x_dir # movement in x direction right = 1, left = -1
        self.y_dir = y_dir # movement in y direction down = 1, up = -1
        self.color = color # colour of cube

    # Function to move snake in a given direction
    def move(self, x_dir, y_dir):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.pos = (self.pos[0] + self.x_dir, self.pos[1] + self.y_dir) # new position of cube

    # Function to draw cube on pygame window
    def draw(self, surface, eyes=False):
        s = self.width // self.rows # size of individual cubes
        x, y = self.pos[0], self.pos[1] # x and y coordinates 
        rect = (x*s+1, y*s+1, s-2, s-2) # define rectangle (x, y, width, height). Make size slightly smaller to fit in grid.
        pygame.draw.rect(surface=surface, color=self.color, rect=rect) # draw cube

        # For drawing eyes on head cube
        if eyes:
            eye1 = (x*s+0.3*s, y*s+8) # centre coordinates of circle (x, y)
            eye2 = (x*s+0.7*s, y*s+8)
            pygame.draw.circle(surface=surface, color='black', center=eye1, radius=4)
            pygame.draw.circle(surface=surface, color='black', center=eye2, radius=4)

# Define a snake class representing the snake in the game
class Snake:

    # Class variables for snake body and turns in the game
    body = []
    turns =  {}

    # Constructor
    def __init__(self, pos, color='red'):
        self.color = color # colour of snake body 
        self.head = Cube(pos) # head of snake is an instance of the Cube class
        self.body.append(self.head) # add snake head to body list
        self.x_dir = 0 
        self.y_dir = 1 # snake initially set to be moving vertically downwards

    # Function to move the snake based on user input.
    def move(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.x_dir = -1
                    self.y_dir = 0
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir] # add current position and new direction to turns dictionary in the format {(x, y): [x_dir, y_dir]}

                elif keys[pygame.K_RIGHT]:
                    self.x_dir = 1
                    self.y_dir = 0
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]

                elif keys[pygame.K_UP]:
                    self.x_dir = 0
                    self.y_dir = -1
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]

                elif keys[pygame.K_DOWN]:
                    self.x_dir = 0
                    self.y_dir = 1
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]

        for i, c in enumerate(self.body): # loop through the body of the snake
            p = c.pos[:] # get the position of each cube
            if p in self.turns: # check if the position is in turns dictionary
                turn = self.turns[p] # if it is, get the turn associated with that position
                c.move(turn[0], turn[1]) # move the cube in the correct direction
                if i == len(self.body)-1:
                    self.turns.pop(p) # once the entire snake has turned, remove the turn from the dictionary
                        
            else: # if the snake reaches the edge of the screen it will appear on the opposite side of the screen
                if c.x_dir == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.x_dir == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0,c.pos[1])
                elif c.y_dir == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.y_dir == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.x_dir,c.y_dir) # ensures body follows head of snake

    # Function to add cube when snake picks up a 'snack'
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.x_dir, tail.y_dir # get current direction of final cube to determine where to append new cube

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1]))) # append new cube to snake body
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))        
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))              

        self.body[-1].x_dir = dx # update direction of appeneded cube
        self.body[-1].y_dir = dy

    # Function to draw body of snake
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface=surface, eyes=True) # draw eyes on first cube (head of snake)
            else:
                c.draw(surface)

    # Function to reset snake to original settings once game is lost.
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x_dir = 0
        self.y_dir = 1

# Function to generate random coordinates for adding 'snacks' to the game
def randomSnack(snake, rows):
    positions = snake.body 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0: # if pos == current position of snake body, generate new coordinates
            continue
        else:
            break
    return (x, y)

# Function to draw a grid on the game window
def drawGrid(surface, width, rows):
    s = width // rows # size of individual cube
    x, y = 0, 0
    for l in range(rows):
        x += s
        y += s
        pygame.draw.line(surface=surface, color='white', start_pos=(x,0), end_pos=(x,width)) # draw gridlines
        pygame.draw.line(surface=surface, color='white', start_pos=(0,y), end_pos=(width,y))

# Function to generate message box when game is lost
def message_box(message):
    root = tk.Tk()
    root.attributes('-topmost', True) # generates a window to appear on top of the game window
    root.withdraw() # hides the window
    messagebox.showinfo(message=message) # displays message
    try:
        root.destroy() # closes window after message box is closed
    except:
        pass

# Main program
def main():

    # Global variables
    global width, rows, snake, snack
    width = 700 # width of game window
    rows = 20 # number of rows in game window
    root = tk.Tk()
    root.withdraw()
    pygame.init() # initialise pygame
    surface = pygame.display.set_mode((width, width)) # generate game window
    snake = Snake(pos=(10,10)) # start snake at position (10,10)
    snack = Cube(randomSnack(snake, rows), color='green') # add a snack to the game
    clock = pygame.time.Clock()

    while True:
        clock.tick(7) # control how fast snake moves, lower = slower
        snake.move() 
        
        if snake.body[0].pos == snack.pos:
            snake.addCube() # add a cube to snake body when it picks up a snack
            snack = Cube(randomSnack(snake, rows), color='green') # add a new snack

        for i in range(len(snake.body)):
            if snake.body[i].pos in list(map(lambda z:z.pos, snake.body[i+1:])): # check if snake hits own body
                print('Score: ', len(snake.body))
                message_box('You Lost!\nPlay Again...')
                snake.reset((10,10))
                break # display message and reset if snake hits own body

        surface.fill(color='dimgrey') # grey background
        drawGrid(surface, width, rows)
        snake.draw(surface)
        snack.draw(surface)
        pygame.display.update()

    pygame.quit()

main() # run program