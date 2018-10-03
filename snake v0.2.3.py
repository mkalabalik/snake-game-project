import pygame, random, sys

# Define some variable
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define some direction
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"

# Setup
pygame.init()

# Set the width and height of the screen [width,height]
size = [960, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snake")
 
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(1)


#resources
font_start = pygame.font.Font(None,50)
font_exit = pygame.font.Font(None,50)
font_select = pygame.font.Font(None,50)
font_retry = pygame.font.Font(None,50)
font_score = pygame.font.Font(None,50)
font_wall = pygame.font.Font(None,30)
font_suicide = pygame.font.Font(None,30)
font_author = pygame.font.Font(None, 30)
font_erasmus = pygame.font.Font(None, 30)
font_course = pygame.font.Font(None, 30)
font_size = pygame.font.Font(None, 30)
font_game_over = pygame.font.Font(None,100)

text_start = font_start.render("Start",1,pygame.Color("blue"))
text_exit = font_exit.render("Exit",1,pygame.Color("red"))
text_select = font_select.render(">",1,pygame.Color("blue"))
text_retry = font_retry.render("Retry? Y/N",1,pygame.Color("yellow"))
#text_score = font_retry.render("Score",1,pygame.Color("blue"))
text_wall_on = font_wall.render("(W) Wall     : ON",1,pygame.Color("yellow"))
text_wall_off = font_wall.render("(W) Wall     : OFF",1,pygame.Color("yellow"))
text_suicide_on = font_suicide.render("(S)  Suicide: ON",1,pygame.Color("yellow"))
text_suicide_off = font_suicide.render("(S)  Suicide: OFF",1,pygame.Color("yellow"))
text_game_over = font_game_over.render("GAME OVER!",1,pygame.Color("red"))
text_author = font_author.render("Muhammed KALABALIK", 1, pygame.Color("blue"))
text_erasmus = font_erasmus.render("2017/2018 Erasmus+", 1, pygame.Color("blue"))
text_course = font_course.render("Audiovisual Content Processing in Multimedia Systems Project", 1, pygame.Color("blue"))
text_size_small = font_size.render("(X)  Size     : Small", 1, pygame.Color("yellow"))
text_size_normal = font_size.render("(X)  Size     : Normal", 1, pygame.Color("yellow"))
text_size_big = font_size.render("(X)  Size     : Big", 1, pygame.Color("yellow"))
list_size = [text_size_normal,text_size_small,text_size_big]

background_menu = pygame.image.load("menu.jpg").convert()
background_image = pygame.image.load("backround.jpg").convert()


######################################################++SNAKE++#########################################################
class Snake():
    def __init__(self):
        self.coordinatelist = []
        self.length = 10
        self.direction = RIGHT
        self.temp_direction = RIGHT
        self.speed = 15
        self.new_coordinate=[]
        self.size = 0
        self.snake_size = [15,15]
        self.snake_color = BLUE
        self.snake_head_color = BLACK
        self.create_snake()
        self.tail = None
        self.head = None
        self.backup_tail()
        self.backup_head()
        self.wall = True
        self.suicide = True
        self.score = 0
        
    def create_snake(self):
        self.coordinatelist = self.length*[[0,0]]

    def draw_snake(self):
        for i in self.coordinatelist:
            pygame.draw.rect(screen,WHITE,[i[0], i[1], self.snake_size[0],self.snake_size[1]], 0)
            pygame.draw.rect(screen,self.snake_color,[i[0]+1, i[1]+1, self.snake_size[0]-2,self.snake_size[1]-2], 0)
        pygame.draw.rect(screen,self.snake_head_color,[self.head[0]+1, self.head[1]+1, self.snake_size[0]-2,self.snake_size[1]-2], 0)

    def backup_tail(self):
        self.tail = self.coordinatelist[0]
    
    def backup_head(self):
        self.head = self.coordinatelist[-1]

    def remove_tail(self):
        self.backup_tail()
        self.coordinatelist.remove(self.tail)

    def add_tail(self):
        self.coordinatelist.insert(0,self.tail)

    def next_coordinate(self):
        if self.wall:
            if self.direction == RIGHT:
                self.new_coordinate=[self.coordinatelist[-1][0]+self.speed,self.coordinatelist[-1][1]]
            if self.direction == LEFT:
                self.new_coordinate=[self.coordinatelist[-1][0]-self.speed,self.coordinatelist[-1][1]]
                if self.new_coordinate[0]<0 and not self.wall:
                    self.new_coordinate=[self.new_coordinate[0]+size[0],self.new_coordinate[1]]
            if self.direction == UP:
                self.new_coordinate=[self.coordinatelist[-1][0],self.coordinatelist[-1][1]-self.speed]
                if self.new_coordinate[1]<0 and not self.wall:
                    self.new_coordinate=[self.new_coordinate[0],self.new_coordinate[1]+size[1]]
            if self.direction == DOWN:
                self.new_coordinate=[self.coordinatelist[-1][0],self.coordinatelist[-1][1]+self.speed]
        else:
            if self.direction == RIGHT:
                self.new_coordinate=[(self.coordinatelist[-1][0]+self.speed)%size[0],self.coordinatelist[-1][1]]
            if self.direction == LEFT:
                self.new_coordinate=[self.coordinatelist[-1][0]-self.speed,self.coordinatelist[-1][1]]
                if self.new_coordinate[0]<0 and not self.wall:
                    self.new_coordinate=[self.new_coordinate[0]+size[0],self.new_coordinate[1]]
            if self.direction == UP:
                self.new_coordinate=[self.coordinatelist[-1][0],self.coordinatelist[-1][1]-self.speed]
                if self.new_coordinate[1]<0 and not self.wall:
                    self.new_coordinate=[self.new_coordinate[0],self.new_coordinate[1]+size[1]]
            if self.direction == DOWN:
                self.new_coordinate=[self.coordinatelist[-1][0],(self.coordinatelist[-1][1]+self.speed)%size[1]]


    def add_coordinate(self):
        self.coordinatelist.append(self.new_coordinate)
        
    def respawn(self):
        self.coordinatelist = []
        self.length = 10
        self.direction = RIGHT
        self.temp_direction = RIGHT
        
        if self.size == 0:
            self.new_coordinate = [15, 0]
        elif self.size == 1:
            self.new_coordinate = [10, 0]
        else:
            self.new_coordinate = [20, 0]
        
        self.create_snake()
        self.backup_tail()
        self.backup_head()
        self.score = 0
        fps = 10.0


    def backup_score(self):
        self.score = len(self.coordinatelist)-self.length
    
    def crash(self):
        if self.wall:
            if self.new_coordinate[0] >= size[0] or self.new_coordinate[1] >= size[1] or self.new_coordinate[0] < 0 or self.new_coordinate[1] < 0:
                self.backup_score()
                if end_menu(self.score):  
                    self.respawn()
                else:
                    menu(self, bait)
                    self.respawn()
        if self.suicide:
            if self.new_coordinate in self.coordinatelist:
                self.backup_score()
                if end_menu(self.score):
                    self.respawn()
                else:
                    menu(self, bait)
                    self.respawn()


####################################################++BAIT++############################################################
class Bait():
    def __init__(self):
        self.size=[15,15]
        self.border=[size[0]-self.size[0],size[1]-self.size[1]]
        self.counter=0
        self.color = RED
        self.coordinates = [0, 0]

    def create_bait(self):
        self.coordinates = [random.randrange(0,self.border[0],step=self.size[0]), random.randrange(0,self.border[1],step=self.size[1])]        

    def draw_bait(self):
        pygame.draw.ellipse(screen, self.color, [self.coordinates[0],self.coordinates[1],self.size[0], self.size[1]], 0)

########################################################################################################################

def end_menu(score):
    text_score = font_score.render("Score: "+str(score),1,pygame.Color("blue"))
    screen.blit(background_menu, [0,0])
    screen.blit(text_game_over, [100,200])
    screen.blit(text_score,(250,300))
    screen.blit(text_retry,(235,350))
    pygame.display.flip()
    retry = False
    while retry == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    retry = True
                elif event.key == pygame.K_n:
                    retry = None

    return retry

def menu(snake, bait):
    selected = "Start"
    end = False

    while end == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = "Exit"
                if event.key == pygame.K_UP:
                    selected = "Start"
                if event.key == pygame.K_s:
                    snake.suicide = not snake.suicide
                if event.key == pygame.K_w:
                    snake.wall = not snake.wall
                if event.key == pygame.K_x:
                    snake.size = (snake.size+1)%3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    end = True
                    if snake.size == 0:
                        snake.speed = 15
                        snake.snake_size = [15, 15]
                        bait.size = [15, 15]
                    elif snake.size == 1:
                        snake.speed = 10
                        snake.snake_size = [10, 10]
                        bait.size = [10, 10]
                    else:
                        snake.speed = 20
                        snake.snake_size = [20, 20]
                        bait.size = [20, 20]

                    bait.create_bait()
                    if selected == "Exit":
                        sys.exit()


        if selected == "Start":
            selected_y = 450
        elif selected == "Exit":
            selected_y = 500

        if snake.size == 0:
            text_size = text_size_normal
        elif snake.size == 1:
            text_size = text_size_small
        else:
            text_size = text_size_big


        # --- Drawing Code
        # First, clear the screen to WHITE. Don't put other drawing commands
        # above this, or they will be erased with this command.

        screen.blit(background_menu, [0,0])        
        screen.blit(text_author,(150,50))
        screen.blit(text_erasmus,(168,75))
        screen.blit(text_course,(10,100))
        screen.blit(text_size,(180,350))
        screen.blit(text_start,(220,450))
        screen.blit(text_exit,(220,500))

        if snake.wall:
            screen.blit(text_wall_on,(180,250))
        else:
            screen.blit(text_wall_off,(180,250))
        
        if snake.suicide:
            screen.blit(text_suicide_on,(180,300))
        else:
            screen.blit(text_suicide_off,(180,300))


        screen.blit(text_select,(190,selected_y))

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     

def main(size, snake, bait, fps=25.0):
    menu(snake, bait)

    # -------- Main Program Loop -----------
    while True:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LSHIFT:
                    fps*=2
                
                if event.key == pygame.K_LEFT:
                    if snake.direction != RIGHT:
                        snake.temp_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    if snake.direction != LEFT:
                        snake.temp_direction = RIGHT
                elif event.key == pygame.K_UP:
                    if snake.direction != DOWN:
                        snake.temp_direction = UP
                elif event.key == pygame.K_DOWN:
                    if snake.direction != UP:
                        snake.temp_direction = DOWN
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    fps /= 2

        snake.direction = snake.temp_direction


        # --- Game Logic
        snake.next_coordinate()
        snake.crash()
        snake.add_coordinate()
        snake.remove_tail()
        snake.backup_head()
        snake.backup_tail()
        
        if bait.coordinates in snake.coordinatelist:
            if bait.coordinates == snake.head:
                snake.add_tail()
            bait.create_bait()


        # --- Drawing Code
        # First, clear the screen to WHITE. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        screen.blit(background_image, [0,0])

        bait.draw_bait()
        snake.draw_snake()
        
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
        # Limit frames per second
        clock.tick(fps)

snake = Snake()
bait = Bait()
main(size, snake, bait, fps=10.0)
