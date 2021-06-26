import pygame ,sys,random

#general setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1920
screen_height = 1000
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Game rects
ball = pygame.Rect(screen_width/2-10,screen_height/2-10,20,20)
player = pygame.Rect(10,screen_height/2-75,10,150)
player2 = pygame.Rect(screen_width-20,screen_height/2-75,10,150)

# colors
bg_color= pygame.Color(12,12,12)
obj_color= pygame.Color(0,206,0)

#animation
ball_speed=[7,7]
player_speed=0

# mode 0
player2_speed=0
def ball_animation():
    global player2_score,player_score,score_time
    #move
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # test collicion
    if ball.top <= 0 or  ball.bottom >= screen_height:
        ball_speed[1] *= -1
    if ball.left <= 0 :
        player2_score+=1
        score_time = pygame.time.get_ticks()
        reset_ball()
    if ball.right >= screen_width:
        player_score+=1
        score_time = pygame.time.get_ticks()
        reset_ball()
    
    # we can use ball.colliderect(player)  
    if (ball.colliderect(player)) or  (ball.colliderect(player2)):
        ball_speed[0] *= -1
def  reset_ball():
    global score_time
    ball.x=screen_width/2-10
    ball.y=screen_height/2-10
    time_now = pygame.time.get_ticks()
    if time_now - score_time < 2100:
        ball_speed[0]=0
        ball_speed[1]=0
    else:
        score_time = None
        ball_speed[0] = 7*random.choice((1,-1))
        ball_speed[1] = 7*random.choice((1,-1))
def player_animation(player,player_speed):
    player.y+= player_speed
    if player.top <0:
        player.top=0
    if player.bottom >screen_height:
        player.bottom=screen_height  

# mode 1  
mode = 1
mode_text = "single player"
player2_speed_value=4

#score
#init
player_score=0
player2_score=0

#text font
font = pygame.font.Font("freesansbold.ttf",72)
font_of_help = pygame.font.Font("freesansbold.ttf",16)
#timer
score_time = 1
help_timer = pygame.time.get_ticks()
mode_timer = None
def help_show():
    global help_timer
    time_now = pygame.time.get_ticks()
    if time_now - help_timer < 10100:
        help1_text = font_of_help.render(f"control [z] , [s] (player 2 upkey , downkey)",False,obj_color)
        help2_text = font_of_help.render(f"switch mode [m] (single player tow players)",False,obj_color)
        help3_text = font_of_help.render(f"help [h]",False,obj_color)
        screen.blit(help1_text,(10,screen_height-120))
        screen.blit(help2_text,(10,screen_height-80))
        screen.blit(help3_text,(10,screen_height-40))
    else:
        help_timer=None
def mode_show():
    global mode_timer,mode_text
    time_now = pygame.time.get_ticks()
    if time_now - mode_timer < 3100:
        modes_text = font_of_help.render(f"{mode_text}",False,obj_color)
        screen.blit(modes_text,(10,10))
#loop
while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if mode == -1:
                if event.key == pygame.K_DOWN:
                    player2_speed+=6 
                elif event.key == pygame.K_UP:
                    player2_speed-=6
            
            if event.key == pygame.K_s:
                player_speed+=6 
            elif event.key == pygame.K_z:
                player_speed-=6
            
            if event.key == pygame.K_m:
                mode*=-1
                player2_speed=0
                mode_timer=pygame.time.get_ticks()
                if mode == 1:
                    mode_text = "single player"
                else:
                    mode_text = "tow players"
            elif event.key == pygame.K_h:
                help_timer=pygame.time.get_ticks()

            
        if event.type == pygame.KEYUP:
            if mode == -1:
                if event.key == pygame.K_DOWN:
                    player2_speed-=6
                elif event.key == pygame.K_UP:
                    player2_speed+=6
            
            if event.key == pygame.K_s:
                player_speed-=6 
            elif event.key == pygame.K_z:
                player_speed+=6
    if mode == 1 :
        if ball.centery<player2.centery:
            player2_speed=-player2_speed_value
        else:
            player2_speed=player2_speed_value

    ball_animation()
    player_animation(player,player_speed)
    player_animation(player2,player2_speed)
    
    # Draw
    screen.fill(bg_color)
    pygame.draw.rect(screen,obj_color,player)
    pygame.draw.rect(screen,obj_color,player2)
    pygame.draw.ellipse(screen,obj_color,ball)
    pygame.draw.aaline(screen,obj_color,(screen_width/2,0),(screen_width/2,screen_height))

    #text
    player_text = font.render(f"{player_score}",False,obj_color)
    player2_text = font.render(f"{player2_score}",False,obj_color)
    screen.blit(player_text,(screen_width/2-80,5))
    screen.blit(player2_text,(screen_width/2+40,5))

    if score_time:
        reset_ball()
    if help_timer:
        help_show()
    if mode_timer:
        mode_show()
    # Updating the window
    pygame.display.flip()
    clock.tick(60)