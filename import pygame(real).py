import pygame
import os
import random

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 900, 500
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ROBO_SPACE")
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game constants
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Event definitions
BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load images and transform them
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'tank blue.webp'))
BLUE_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'tank red.webp'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'desert.webp')), (WIDTH, HEIGHT))
HEALTH_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'health life.webp')), (40, 40))


# Load sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hitting+2.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shooting+1.wav'))
POWERUP_COLLECT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'beep-6-96243.mp3'))

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


# Draw the game window
def draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health, health_pack):
    
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    if health_pack:  # Checks if health pack exists
        WIN.blit(HEALTH_IMAGE, (health_pack.x, health_pack.y))  # Blit health image based on health pack's coordinates

    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("Health:" + str(blue_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()





def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0: #LEFT
            blue.x  -= VEL 
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x: #RIGHT
            blue.x  += VEL 
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0: #UP
            blue.y  -= VEL 
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 15:  #DOWN
            blue.y  += VEL 


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
            red.x  -= VEL 
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width <  WIDTH: #RIGHT
            red.x  += VEL 
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
            red.y  -= VEL 
    if keys_pressed[pygame.K_DOWN]  and red.y + VEL + red.height < HEIGHT - 15: #DOWN
            red.y  += VEL 

def handle_bullets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
          bullet.x += BULLET_VEL
          if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                blue_bullets.remove(bullet)
          elif bullet.x > WIDTH:
                blue_bullets.remove(bullet)


    for bullet in red_bullets:
          bullet.x -= BULLET_VEL
          if blue.colliderect(bullet):
                pygame.event.post(pygame.event.Event(BLUE_HIT))
                red_bullets.remove(bullet)
          elif bullet.x < 0:
                red_bullets.remove(bullet)

def draw_winner(text):
      draw_text = WINNER_FONT.render(text, 1, WHITE)
      WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/
                           2, HEIGHT/2 - draw_text.get_height()/2 ))

      pygame.display.update()
      pygame.time.delay(5000)


def create_health():
    side = random.choice(["left", "right"])
    if side == "left":
        return HEALTH_IMAGE.get_rect(topleft=(10, random.randint(10, HEIGHT - 40)))
    else:
        return HEALTH_IMAGE.get_rect(topright=(WIDTH - 10, random.randint(10, HEIGHT - 40)))



def handle_shield_collision(tank, shield, health, shield_exists):
    if tank.colliderect(shield):
        if shield_exists:  # Activate shield only if it exists
            shield_exists = False
            return True, health, shield_exists
    return False, health, shield_exists

def handle_health_collision(tank, health_pack, tank_health, health_pack_exists):
    if tank.colliderect(health_pack):
        if tank_health < 10 and health_pack_exists:  # Increase health by 1 if it's less than 10
            tank_health += 1
            # Play a sound when a tank collides with a health pack
            POWERUP_COLLECT_SOUND.play()

            health_pack_exists = False
            return True, tank_health, health_pack_exists
    return False, tank_health, health_pack_exists


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
   
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:              
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        Screen.blit(self.image, self.rect.topleft)
        return action



    
    # Update the display
    pygame.display.update()

    



def game_logic():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    blue = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    blue_bullets = []

    red_health = 10
    blue_health = 10

    health_pack = None
    health_pack_exists = False
    health_pack_timer = 0
    
    

    clock = pygame.time.Clock()
    run = True
    

    while run:
        clock.tick(FPS)
        health_pack_timer += 1

        if not health_pack_exists and health_pack_timer > 900:  # Check every 15 seconds (900 frames at 60 FPS)
            health_pack = create_health()
            health_pack_exists = True
            health_pack_timer = 0

            side = random.choice(["left", "right"])
            if side == "left":
                health_pack.topleft = (10, random.randint(10, HEIGHT - 40))
            else:
                health_pack.topright = (WIDTH - 10, random.randint(10, HEIGHT - 40))


        if health_pack_exists:

            blue_collision, blue_health, health_pack_exists = handle_health_collision(blue, health_pack, blue_health, health_pack_exists)
            red_collision, red_health, health_pack_exists = handle_health_collision(red, health_pack, red_health, health_pack_exists)

            # If health not collected within 5 seconds, reset
            if not (blue_collision or red_collision) and health_pack_timer > 300:  # 5 seconds (300 frames at 60 FPS)
                health_pack_exists = False
                health_pack_timer = 0


        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()


        winner_text = ""
        if red_health <= 0 :
              winner_text = "Blue Wins!"

        if blue_health <= 0:
              winner_text = "Red Wins!"

        if winner_text != "":
              draw_winner(winner_text)
              break


        
        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed, blue)
        red_handle_movement(keys_pressed, red)
        draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health,  health_pack)
        
        handle_bullets(blue_bullets, red_bullets, blue, red)
       

    
    start_screen()

    start_button = None 
def start_screen():
     
    global start_button 

    run = True
    background_img = pygame.image.load(r"C:\Users\jampel\Documents\spaceship game\Assets\tank-wars-hd.webp")
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    start_img = pygame.image.load(r"C:\Users\jampel\Documents\spaceship game\Assets\start button.png").convert_alpha()

    start_button = Button(300, 150, start_img, 0.5)
    

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_RETURN:  # Check for Enter key press
                    game_logic()


        

            # Handle button click
            if start_button.draw():
                game_logic() 
     
        
        Screen.blit(background_img, (0, 0))

       

        font = pygame.font.Font(None, 56)
        welcome_text = font.render("PRESS ENTER TO START", True, (255, 255, 255))
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        Screen.blit(welcome_text, welcome_rect)
        pygame.display.update()

def main():
    # Call the start screen when the program starts
    start_screen()

if __name__ == "__main__":
    main()