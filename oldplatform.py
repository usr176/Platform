'''
Old platfrom file used as a base. Verticle scroll is not implemented here 
'''
import pygame, random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 60
GRAVITY = 0.5
JUMP_VELOCITY = -10
GWDTH, GHIGHT = WIDTH, 150

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Initialize pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform")
clock = pygame.time.Clock()

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Initialise players
player1 = pygame.Rect(100, HEIGHT - 150, PLAYER_WIDTH, PLAYER_HEIGHT)
player1_vel_y = 0
onGround = False

# Initialize platforms
ground = pygame.Rect(0, HEIGHT - 90, GWDTH, GHIGHT)
platforms = []
for i in range(6):
    thisPlat = [random.randint(50, 700), random.randint(0, 500)]
    platforms.append(thisPlat)
for i in range(len(platforms)):
    platforms[i] = pygame.Rect(platforms[i][0], platforms[i][1], 100, 20)

# Main loop
def main():
    
    global player1_vel_y
    global onGround
    
    # Squish/stretch parameters
    stretch_amount = 10
    squash_timer = 0
    is_running = False   
    
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Movment
        dx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and onGround:
            player1_vel_y = JUMP_VELOCITY
            onGround = False
            squash_timer = 10
        if keys[pygame.K_RIGHT]:
            dx += 5
        if keys[pygame.K_LEFT]:
            dx -= 5
        is_running = dx != 0    
        
        #Gravity
        player1_vel_y += GRAVITY
        player1.y += player1_vel_y
        player1.x += dx
        
        #Collision
        if player1.colliderect(ground):
            player1.y = ground.top - player1.height  # Align with top of ground
            player1_vel_y = 0
            onGround = True
        else:
            onGround = False
        for platform in platforms:
            if player1.colliderect(platform):
                if player1_vel_y > 0:  # Falling down
                    player1.bottom = platform.top
                    player1_vel_y = 0
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
            
        player_rect = pygame.Rect(
        player1.x + (PLAYER_WIDTH - stretch_w) // 2,
        player1.y + (PLAYER_HEIGHT - stretch_h),
        stretch_w,
        stretch_h
    )
        
        # Draw to screen
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, GREEN, ground)
        for i in range(len(platforms)):
            pygame.draw.rect(screen, RED, platforms[i])
        
        # Update screen    
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    main()