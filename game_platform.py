import pygame, random
import pygame.freetype

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 60
PLAYER_X, PLAYER_Y = 400, 480
GRAVITY = 0.5
JUMP_VELOCITY = -12
PWDTH, PHIGHT = 140, 20 
GAME_OVER = False

font = pygame.font.Font("PokemonGb-RAeo.ttf", 15)
score = 0
highscore = 0

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BG_COLOR = (230, 220, 221)
BG = BG_COLOR
# Initialize pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform")
clock = pygame.time.Clock()

icon = pygame.image.load("icon.png")
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)

# Initialise players
player_rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
player_vel_y = 0
onGround = False

# Initialize/Build platforms
platforms = [[PLAYER_X - 20, PLAYER_Y + 70, PWDTH, PHIGHT],
             [120, 480, PWDTH, PHIGHT],
             [200, 370, PWDTH, PHIGHT],
             [500, 520, PWDTH, PHIGHT],
             [420, 300, PWDTH, PHIGHT],
             [210, 220, PWDTH, PHIGHT],
             [600, 170, PWDTH, PHIGHT],
             [500, 100, PWDTH, PHIGHT]]

#Function: list -> list
#Returns the updated list to generate platforms
def updatePlatfroms(list, playerY, change):
    global score
    
    if playerY < 250:
        for i in range(len(list)):
            list[i][1] += change
    for item in range(len(list)):
        if list[item][1] > 600:
            list[item] = [random.randint(10, 750), random.randint(-50, -10), PWDTH, PHIGHT]
            score += 1
    return list
        
# Main loop
def main():
    
    global player_vel_y
    global onGround
    global player_rect
    global platforms
    global score, highscore
    global GAME_OVER
    
    #Squish/stretch parameters
    stretch_amount = 10
    squash_timer = 0
    is_running = False   
    
    
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BG)
        
        hscoreText = font.render('Highest: ' + str(highscore), True, BLUE, WHITE)
        screen.blit(hscoreText, (5, 10))
        scoreText = font.render('Score: ' + str(score), True, BLUE, WHITE)
        screen.blit(scoreText, (5, 35))
        
        # Platforms
        blocks = []
        for i in range(len(platforms)):
            block = pygame.draw.rect(screen, RED, platforms[i], 0, 4)
            blocks.append(block)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movment
        dx = 0                              #Horizontal Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and GAME_OVER:
            score = 0
            player_rect.x, player_rect.y = PLAYER_X, PLAYER_Y
            platforms = [[PLAYER_X - 20, PLAYER_Y + 70, PWDTH, PHIGHT],
             [120, 480, PWDTH, PHIGHT],
             [200, 370, PWDTH, PHIGHT],
             [500, 520, PWDTH, PHIGHT],
             [420, 300, PWDTH, PHIGHT],
             [210, 220, PWDTH, PHIGHT],
             [600, 170, PWDTH, PHIGHT],
             [500, 100, PWDTH, PHIGHT]]
        
        if keys[pygame.K_UP] and onGround:
            player_vel_y = JUMP_VELOCITY
            onGround = False
            squash_timer = 10
        if keys[pygame.K_RIGHT]: 
            dx += 5
        if keys[pygame.K_LEFT]:
            dx -= 5
        is_running = dx != 0
            
        #Gravity
        if not GAME_OVER:
            player_vel_y += GRAVITY
            player_rect.y += player_vel_y
            player_rect.x += dx
        
        # Collision
         
        # Vertical Collision
        onGround = False
        for block in blocks:
            if player_rect.colliderect(block) and player_vel_y > 0 and not onGround and player_rect.bottom <= block.bottom:
                player_rect.bottom = block.top 
                player_vel_y = 0
                onGround = True
            elif player_rect.colliderect(block) and player_rect.top < block.bottom:
                player_vel_y = 0
        
        # Horizontal Collision
            if player_rect.colliderect(block):
                if dx > 0 and player_rect.right > block.left:
                    player_rect.right = block.left 
                    onGround = True
                elif dx < 0 and player_rect.left < block.right:
                    player_rect.left = block.right 
                    onGround = True
        
                  
        # Animation properties
        stretch_w, stretch_h = PLAYER_WIDTH, PLAYER_HEIGHT
        
        if not onGround:
            # Jumping — stretch up
            stretch_w -= stretch_amount
            stretch_h += stretch_amount
        elif is_running:
            # Running — squash slightly
            stretch_w += stretch_amount // 2
            stretch_h -= stretch_amount // 2
        elif squash_timer > 0:
            # Jump squash start``
            stretch_w += stretch_amount
            stretch_h -= stretch_amount
            squash_timer -= 1
        elif keys[pygame.K_DOWN]:
            # Crouching - squash down
            stretch_h -= stretch_amount
            stretch_w += stretch_amount
        
        
        
        animated_rect = pygame.Rect(
        player_rect.x + (PLAYER_WIDTH - stretch_w) // 2,
        player_rect.y + (PLAYER_HEIGHT - stretch_h),
        stretch_w,
        stretch_h
    )
        
              
        platforms = updatePlatfroms(platforms, player_rect.y, 4)    
              
        # Draw to screen
        pygame.draw.rect(screen, BLUE, animated_rect)
        
        # Game Over
        if player_rect.y > HEIGHT:
            GAME_OVER = True
            player_vel_y = 0
           
            gmText = font.render('Game Over!', True, BLUE, WHITE)
            rsText = font.render('Space to Restart.', True, BLUE, WHITE)
            screen.blit(gmText, (WIDTH / 2 - 70, HEIGHT / 2))
            screen.blit(rsText, (WIDTH / 2 - 95, HEIGHT / 2 + 30))

        else:
            GAME_OVER = False
        
        # Update screen    
        pygame.display.update()
        
        if score > highscore:
            highscore = score

    pygame.quit()
    
if __name__ == "__main__":
    main()