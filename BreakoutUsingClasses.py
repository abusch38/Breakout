#Breakout using Classes and Tkinter
#By Andrew Busch

#To Do List: 
#-Have the ball hit bricks when it hits on the side

from tkinter import *
import random
import time

#setup Ball
class Ball(object):
    global brick_object_wrapper
    def __init__(self, canvas, brick, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.brick = brick
        self.score = score
        #names the ball on the canvas
        self.id = canvas.create_oval(10, 10, 24, 24, fill=color)
        #positions the ball at this location
        self.pos = self.canvas.move(self.id, 245, 200)

        #sets up the inital movement variables of the ball with a random horizontal start value
        self.starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(self.starts)
        #use startsd this to debug brick rows
        self.startsd = [0]
        self.x = self.starts[0]
        self.y = -3

        #Lets the Ball class know the dimensions of the canvas.
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        
        #a boolean variable we will change if the ball hits the bottom
        self.hit_bottom = False

    def reset(self):
        #resets the ball's position on the screen
        bx1, by1, bx2, by2 = self.canvas.coords(self.id)
        move_x = 250-bx1
        move_y = -280
        self.canvas.move(self.id, move_x, move_y)
        self.x = self.starts[0]
        #resets whether the ball has hit the bottom of the screen. 
        self.hit_bottom = False

    #check to see if the ball hits the paddle
    def hit_paddle(self, pos):
        #position variable contains two coordinate pairs: (x1,y1,x2,y2)
        #coordinates of paddle rectangle: top left then bottom right
        bx1, by1, bx2, by2 = pos
        paddle_pos = self.canvas.coords(self.paddle.id)
        px1, py1, px2, py2 = paddle_pos

        #splits the paddle into 3rds
        paddle_3rd = (px2-px1)/3
        
        #ball's position (pos) compared to the paddle's position (paddle_pos)
        #hit the left 3rd of the paddle
        if bx2 >= px1 and bx1 <= (px1+paddle_3rd):
            if by2 >= py1 and by2 <= py2:
                if self.x <0:
                    #if the ball is going left, self.x is negative. 
                    self.x = self.x-2
                elif self.x>= 0:
                    self.x = self.x-2
                return True
            return False
        
        #hit the middle 3rd of the paddle
        if bx2 >= (px1+paddle_3rd) and bx1 <= (px2-paddle_3rd):
            if by2 >= py1 and by2 <= py2:
                #no change to self.x
                pass
                return True
            return False

        #hit the right 3rd of the paddle
        if bx2 >= (px2-paddle_3rd) and bx1 <= px2:
            if by2 >= py1 and by2 <= py2:
                if self.x <0:
                    self.x = self.x+2
                elif self.x>= 0:
                    self.x = self.x+2
                return True
            return False

    #see which row of bricks the ball will hit and then pass to a logic function
    def check_hit_brick(self, brick):

        global brick_object_wrapper, brick_object_list1, brick_object_list2, brick_object_list3

        #getting the coordinates of the ball. (this probably could be it's own function)
        self.pos = self.canvas.coords(self.id)
        b_x1, b_y1, b_x2, b_y2 = self.canvas.coords(self.id)
        
        #Checks the y-coordinates of the bricks to see which row the ball will hit
        #y1 is closest to the top of the screen.
        #y4 is closes to the bottom of hte screen.
        sorted_brick_y_values = sorted(brick.brick_y_list)
        y1_brick_value = sorted_brick_y_values[0]
        len_brick_values = len(brick.brick_y_list)
        y4_brick_value = sorted_brick_y_values[len_brick_values-1]
        y_brick_fourths = len_brick_values/4
        y2 = int(y_brick_fourths)
        y3 = int(2*y_brick_fourths)
        y2_brick_value = sorted_brick_y_values[y2]
        y3_brick_value = sorted_brick_y_values[y3]
        
        #checking the ball against row1 bricks (top row)
        if b_y1 <= y2_brick_value and b_y2 >= y1_brick_value:
            brick_array = brick_object_wrapper[0]
            self.check_hit_brick_logic(brick_array)

        #checking the ball against row2 bricks (middle row)
        if b_y1 <= y3_brick_value and b_y2 >= y2_brick_value:
            brick_array = brick_object_wrapper[1]
            self.check_hit_brick_logic(brick_array)

        #checking the ball against row3 bricks (bottom row)
        if b_y1 <= y4_brick_value and b_y2 >= y3_brick_value:
            brick_array = brick_object_wrapper[2]
            self.check_hit_brick_logic(brick_array)

    #Once the brick row is established, 
    #this is the logic behind seeing which brick is hit by the ball. 
    def check_hit_brick_logic(self, brick_array):
        
        #sets the initializes the row to zero in a multidimensional array
        row = 0

        #whatever array was passed in as an argument is now brick_object_list
        brick_object_list = brick_array

        halfball = (self.pos[0]-self.pos[2])/2
        #cycles through all 10 bricks/rows of the brick_object_list
        for i in range(0, len(brick_object_list)):

            #pulling out information from the brick_array
            brick_id = brick_object_list[row][0]
            brick_state = brick_object_list[row][1]
            brick_number = brick_object_list[row][2]
            brick_rect_id = brick_object_list[row][3]
            brick_pos= brick_object_list[row][4]

            #check to see if the ball's x positions are between the brick's x positions

            #The ball hits the brick square on:
            if self.pos[0] >= brick_pos[0] and self.pos[2] <= brick_pos[2]:
                #calls the delete_bricks function
                self.delete_bricks(brick_array, brick_object_list, row)

            elif self.pos[0] >= brick_pos[0] and self.pos[2]+halfball <=brick_pos[2]:
                #calls the delete_bricks function
                self.delete_bricks(brick_array, brick_object_list, row)

            elif self.pos[0]-halfball >= brick_pos[0] and self.pos[2] <=brick_pos[2]:
                #calls the delete_bricks function
                self.delete_bricks(brick_array, brick_object_list, row)
                
            '''
            If the ball hits the sides of the brick, it should also hit the brick
            '''

            #increase the row value by 1 to cycle through each of the bricks in the array    
            row = row + 1
            
    def delete_bricks(self, brick_array, brick_object_list, row):
        #global brick_object_wrapper, brick_object_list1, brick_object_list2, brick_object_list3

        #pulling out information from the brick_array
        brick_id = brick_object_list[row][0]
        brick_state = brick_object_list[row][1]
        brick_number = brick_object_list[row][2]
        brick_rect_id = brick_object_list[row][3]
        brick_pos= brick_object_list[row][4]

        #If the brick is not broken
        if brick_state >= 1:
            #changing the state of the brick object
            #print("brick state before hit: ", brick_rect_id, brick_object_list[row][1])
            brick_object_list[row][1] = brick_object_list[row][1] - 1
            #change the color of the brick object after a hit
            canvas.itemconfig(brick_rect_id, fill = 'red')
            #print("brick state after hit: ", brick_object_list[row][1])
            self.hit_brick = True
            self.y = -self.y

            #trying to change the brick color based on the
            #number of times the brick has been hit (state number)
            if brick_object_list[row][1]==0:
                #increase the score by one
                self.score.hit()
                #see if the score equals the number of bricks
                score.check_score()
                #delete the brick
                canvas.delete(brick_rect_id)

        #if the brick is broken
        if brick_state ==0:
            pass

    #creating the ball on the screen.
    def draw(self, brick):
        #Move: id of variable, horizontal movement added to intial position, vertical movement
        self.canvas.move(self.id, self.x, self.y)

        #creating a variable called "pos" for the position of the ball
        #pos contains 4 numbers or two coordinate pairs: (x1,y1,x2,y2)
        #coordinates of rectangle enclosing the ball: top left then bottom right
        pos = self.canvas.coords(self.id)

        #checks the y1 value on the top of the ball to see if
        #we hit the top of the canvas
        if pos[1] <= 0:
            self.y = 3

        #checks the y2 value on the bottom of the ball to see if
        #we hit the bottom of the canvas
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True

        #what happens when you hit the paddle (i.e. self.hit_paddle() == True)
        if self.hit_paddle(pos) == True:
            self.y = -3

        #check to see if the left-side of the ball hits the edge of the canvas
        if pos[0] <= 0:
            self.x = -self.x
            
        #check to see if the right-side of the ball hits the edge of the canvas
        if pos[2] >= self.canvas_width:
            self.x = -self.x

        #check to see if the ball hits a brick. 
        self.check_hit_brick(brick)


class Paddle(object):
    def __init__(self, canvas, color):
        self.canvas = canvas
        #names the paddle on the canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        #moves the paddle to this location.
        self.canvas.move(self.id, 225, 450)
        self.x = 0
        #makes sure the paddle knows the edges of the canvas
        self.canvas_width = self.canvas.winfo_width()
        self.mouse_x = self.canvas_width/2
        self.mouse_y = 450
        #binds the movement of the paddle to the left and right arrows.
        self.canvas.bind_all('<Motion>', self.mouse_position)
        #the game will start once the left-mouse button is pushed.
        self.started = False
        self.canvas.bind_all('<Button-1>', self.start_game)

    def reset(self):
        #resets the Paddle on the screen
        px1, py1, px2, py2 = self.canvas.coords(self.id)
        move_x = 225-px1
        move_y = 0
        self.canvas.move(self.id, move_x, move_y)
        self.started = False
        
    def draw(self):
        #position variable for the paddle
        pos = self.canvas.coords(self.id)
        x1 = pos[0]
        x2 = pos[2]
        paddle_3rd = (x2-x1)/3

        #sets direction of the paddle if the mouse is left of the middle 3rd
        if self.mouse_x < (x1+paddle_3rd):
            self.x = -3
        #sets direction of the paddle if the mouse is right of the middle 3rd
        elif self.mouse_x > (x2-paddle_3rd):
            self.x = 3
        #does not move the paddle if the mouse is in the middle 3rd of the paddle
        else:
            self.x = 0

        #moves the paddle based on previous if statements
        self.canvas.move(self.id, self.x, 0)
        
    
    def mouse_position(self, event):
        #based on mouse movement
        pos = self.canvas.coords(self.id)
        x1 = pos[0]
        x2 = pos[2]
        self.canvas.focus_set()
        #print("Moved mouse to: ", event.x, event.y)

        #captures the x and y coordinates of the mouse pointer on the screen
        self.mouse_x = float(event.x)
        self.mouse_y = float(event.y)

        #If the self.mouse_x is too far left, reset it. 
        if self.mouse_x<=30:
            self.mouse_x = 30
            
        #If the self.mouse_x is too far right, reset it.
        elif self.mouse_x>=self.canvas_width-30:
            self.mouse_x = self.canvas_width-30

        else:
            pass

    #function starts the game
    def start_game(self, evt):
        self.started = True    


#setup Brick class where each brick will be an object.
class Brick(object):
    global brick_object_wrapper, brick_object_list1, brick_object_list2, brick_object_list3
    
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        #Lets the Brick class know the dimensions of the canvas.
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        #whether the brick is hit or not hit
        self.state = 2
        self.brick_number = 0
        self.brick_y_list = []
        self.brick_position = []
        self.rect_id = ''
        self.brick_height = 15
        self.y1_brick_val = 45
        self.y2_brick_val = self.y1_brick_val+self.brick_height

    def set_up_bricks(self, canvas, color):
        #Set up each row of bricks
        self.set_up_bricks_row1(canvas, color)
        self.set_up_bricks_row2(canvas, color)
        self.set_up_bricks_row3(canvas, color)

    def set_up_bricks_row1(self, canvas, color):
        #call the brick setup loop with row 1 values. 
        global brick_object_wrapper
        #sets the initial brick number to 1
        n=1
        
        self.brick_setup_loop(canvas, color, 1, brick_object_list1)
        #add array of row 1 bricks to brick_object_wrapper
        brick_object_wrapper.append(brick_object_list1)

    def set_up_bricks_row2(self, canvas, color):
        #call the brick setup loop with row 2 values. 
        global brick_object_wrapper
        #sets the initial brick number to 11
        n=11

        #change the y-values of row 2 bricks
        self.y1_brick_val = self.y1_brick_val + self.brick_height
        self.y2_brick_val = self.y2_brick_val + self.brick_height
        self.brick_setup_loop(canvas, color, 11, brick_object_list2)
        #add array of row 2 bricks to brick_object_wrapper
        brick_object_wrapper.append(brick_object_list2)

    def set_up_bricks_row3(self, canvas, color):
        #call the brick setup loop with row 3 values. 
        global brick_object_wrapper
        #sets the initial brick number to 21
        n=21
        #print("Row3 setup starting: ")

        #change the y-values of row 3 bricks
        self.y1_brick_val = self.y1_brick_val + self.brick_height
        self.y2_brick_val = self.y2_brick_val + self.brick_height
        self.brick_setup_loop(canvas, color, 21, brick_object_list3)
        #add array of row 3 bricks to brick_object_wrapper
        brick_object_wrapper.append(brick_object_list3)


    def brick_setup_loop(self, canvas, color, n, brick_object_list_num):
        #This is the loop that creates each of the bricks on the screen in 1 row. 
        n = n
        color = color
        brick_object_list = brick_object_list_num
        for i in range(0,10):
            sub_brick_array = []
            #creating the brick object
            self.id = Brick(canvas, color)
            #adding the object to the brick array
            sub_brick_array.append(self.id)
            sub_brick_array.append(self.id.state)
            #trying to access the 'state' of the objects in the list.
            #giving the individual brick a number and adding it to the array
            self.brick_number = n
            sub_brick_array.append(self.brick_number)

            #setting the individual brick width
            brick_width = self.canvas_width/10

            #I had ot divide by mod10 to get the 2nd and 3rd row of bricks on the screen
            #that meant brick 10, 20, 30 were off the screen. I added an extra brick_width
            x1 = brick_width*((self.brick_number%10)-1)+brick_width
            x2 = brick_width*(self.brick_number%10)-1+brick_width
            self.rect_id = canvas.create_rectangle(x1, self.y1_brick_val, x2, self.y2_brick_val, fill=self.color)
            brick_pos = self.canvas.coords(self.rect_id)
            #creating a list of y-values for the bricks in order to check the lowest value.
            self.brick_y_list.append(brick_pos[1])
            self.brick_y_list.append(brick_pos[3])
            
            #adding the drawn object to the dictionary of drawn bricks where id: position
            sub_brick_array.append(self.rect_id)
            sub_brick_array.append(brick_pos)
            brick_object_list.append(sub_brick_array)
            self.brick_position.append(self.id)
            self.brick_position.append(brick_pos)

            #increases the brick number by 1
            n+=1           

        
class Score(object):
    def __init__(self, canvas, color):
        self.score = 0
        self.lives = 3
        self.canvas = canvas
        self.win = False
        self.id = canvas.create_text(440, 10, text = "Score: ", \
                                     fill = color)
        self.score_id = canvas.create_text(470, 10, text=self.score, \
                                     fill=color)
        self.id = canvas.create_text(30, 10, text = "Lives: ", \
                                     fill = color)
        self.lives_id = canvas.create_text(60, 10, text = self.lives, \
                                     fill = color)
        
    #if the ball hits a brick, increase the score by 1
    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.score_id, text=self.score)

    #if the ball goes past the paddle, decrease the number of lives by 1
    def lose_life(self):
        self.lives -=1
        self.canvas.itemconfig(self.lives_id, text=self.lives)

    #check to see if the player's score matches the number of bricks
    def check_score(self):
        if self.score == 30:
            game_win_text = canvas.create_text(250, 200, fill = 'blue', font = 'Arial 36', text='YOU WIN!')
            print("You Win!")
            self.win = True
        else:
            pass


#Normal tkinter intro.
tk = Tk()
#Title of the game
tk.title("Game")
tk.resizable(0, 0)
#window appears on top
tk.wm_attributes("-topmost", 1)
#dimensions of the canvas
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
#tkinter redraws the canvas--just in case
tk.update()



#creating an object instance of our Score Class
score = Score(canvas, 'dark green')
#creating an object instance of our Paddle Class
paddle = Paddle(canvas, 'blue')

#setting up the empty lists
brick_object_wrapper = []
brick_object_list1 = []
brick_object_list2 = []
brick_object_list3 = []

#sets up the bricks on the screen
brick = Brick(canvas, 'orange')
brick.set_up_bricks(canvas, 'orange')

#creating an object instance of our Ball Class
ball = Ball(canvas, brick, paddle, score, 'red')


#This is our animation loop. It will run until the ball hits the bottom.
def mainloop():
    condition = 1
    while condition:
        if ball.hit_bottom == False and paddle.started == True:
            #draws the ball
            ball.draw(brick)
            #draws the paddle
            paddle.draw()

            if score.win == True:
                condition = 0
                tk.update_idletasks()
                tk.update()
                quit
                
        #if the ball hits the bottom
        if ball.hit_bottom == True:
            time.sleep(1)

            #lose one life
            score.lose_life()
            
            if score.lives > 0:
                #call reset of ball
                ball.reset()
                #call reset of paddle
                paddle.reset()
                
            elif score.lives ==0:
                #stop the animation by no longer calling ball.draw() and paddle.draw()
                #wait 1 second and then display the text "Game Over"
                game_over_text = canvas.create_text(250, 200, fill = 'blue', font = 'Arial 36', text='GAME OVER')
                print("Game Over.")
                condition = 0
                quit

        #force tkinter to redraw the canvas.
        tk.update_idletasks()
        tk.update()
        #Pause between loop cycles to slow the animation down.
        time.sleep(0.01)

#Call the mainloop
mainloop()
