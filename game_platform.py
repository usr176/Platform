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
GAME_STATE = "menu"
MAX_BLEND_SCORE = 1000

font = pygame.font.Font("PokemonGb-RAeo.ttf", 13)
largeFont = pygame.font.FontType("PokemonGb-RAeo.ttf", 22)
score = 0
highscore = 0

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (100, 180, 255)
LIGHT_ORANGE = (255, 180, 80)
DARK_ORANGE = (200, 120, 40)
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

# Function
# Initialize/Build platforms
def initPlatforms(platforms):
    platforms = [[PLAYER_X - 20, PLAYER_Y + 70, PWDTH, PHIGHT],
                [120, 480, PWDTH, PHIGHT],
                [200, 370, PWDTH, PHIGHT],
                [500, 520, PWDTH, PHIGHT],
                [420, 300, PWDTH, PHIGHT],
                [210, 220, PWDTH, PHIGHT],
                [600, 170, PWDTH, PHIGHT],
                [500, 100, PWDTH, PHIGHT]]
    return platforms

platforms = []
platforms = initPlatforms(platforms)

#Function: list -> list
#Returns the updated list to generate platforms
def updatePlatfroms(list, playerY, change):
    global score
    
    if playerY < 250:
        for i in range(len(list)):
            list[i][1] += change
    
    for i in range(len(list)):
        if list[i][1] > HEIGHT:
                score += 1
                
                # Reference platform: either last platform, or a random one
                last_platform = list[len(list) - 1] 
                last_x, last_y = last_platform[0], last_platform[1]
                
                # Random but jumpable vertical gap
                new_y = random.randint(-40, -10)

                # Horizontal offset within jumpable range (positive or negative)
                x_offset = random.randint(-200, 200)
                new_x = max(10, min(last_x + x_offset, WIDTH - PWDTH - 10))  # Clamp to screen

                list[i] = [new_x, new_y, PWDTH, PHIGHT]
    return list
    
# Function: int -> list
# Create surface for labels
def createSurface(text, bg_color, border_color=None, padding=10, alpha=255):
    textRect = text.get_rect()
    surface = pygame.Surface((textRect.width + 2 * padding, textRect.height + 2 * padding), pygame.SRCALPHA)

    # Fill with background (with transparency)
    surface.fill((*bg_color, alpha))

    # Optional border
    if border_color:
        pygame.draw.rect(surface, border_color, surface.get_rect(), width=2)

    # Blit text onto box
    surface.blit(text, (padding, padding))

    return surface

# Function: int, string -> list
# Draws a button to screen 
def drawButton(
    surface, text, x, y, w, h,
    font, text_color, bg_color,
    border_color, hover_color=None,
    border_thickness=5
):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    hovered = x + w > mouse[0] > x and y + h > mouse[1] > y
    fill_color = hover_color if hover_color and hovered else bg_color

    # Background
    pygame.draw.rect(surface, fill_color, (x, y, w, h))
    # Border
    pygame.draw.rect(surface, border_color, (x, y, w, h), border_thickness)

    # Text
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
    surface.blit(text_surf, text_rect)

    return hovered and click[0] == 1
        
# Function
# Blends background at score intervals
def blendBackground(base_color, target_color, ratio):
    ratio = max(0, min(1, ratio))  # Clamp between 0 and 1
    blended = tuple(
        int(base_color[i] + (target_color[i] - base_color[i]) * ratio)
        for i in range(3)
    )
    return blended


# Main loop
def main():
    
    global player_vel_y
    global onGround
    global player_rect
    global platforms, BG
    global score, highscore
    global GAME_OVER, GAME_STATE
    
    #Squish/stretch parameters
    stretch_amount = 10
    squash_timer = 0
    is_running = False   
    
    
    running = True
    while running:
        
        clock.tick(FPS)
        screen.fill(BG)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        if GAME_STATE == "menu":
            
            BG = BG_COLOR
            
            # Title
            title_text = largeFont.render("Main Menu", True, BLUE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
            
            # Play Button
            if drawButton(
                screen, "Play", WIDTH//2 - 100, 250, 200, 70,
                font, WHITE, BLUE, (8, 18, 158), LIGHT_BLUE
            ):
                GAME_STATE = "playing"
            
            if drawButton(
                screen, "Quit", WIDTH//2 - 100, 350, 200, 70,
                font, WHITE, BLUE, (8, 18, 158), LIGHT_BLUE
            ):
                running = False
                
        elif GAME_STATE == "playing":
                
            # Start Game
            
            
            if score < 50:
                blend_ratio = 0.0
            elif score >= 500:
                blend_ratio = 1.0
            else:
                step_index = (score - 50) // 50 + 1
                total_steps = (500 - 50) // 50 + 1
                blend_ratio = step_index / total_steps
            if blend_ratio >= 1:
                BG = RED
            else:
                BG = blendBackground(BG_COLOR, RED, blend_ratio)
            
            '''
            Platforms
            '''
            
            blocks = []
            for i in range(len(platforms)):
                block = pygame.draw.rect(screen, RED, platforms[i], 0, 4)
                blocks.append(block)
            
            '''
            Movement
            '''
            
            dx = 0                              #Horizontal Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and GAME_OVER:
                score = 0
                player_rect.x, player_rect.y = PLAYER_X, PLAYER_Y
                platforms = initPlatforms(platforms)
                BG = BG_COLOR
            
            if keys[pygame.K_UP] and onGround:
                player_vel_y = JUMP_VELOCITY
                onGround = False
                squash_timer = 10
            if not GAME_OVER:
                if keys[pygame.K_RIGHT]: 
                    dx += 5
                if keys[pygame.K_LEFT]:
                    dx -= 5
            is_running = dx != 0
            
            '''    
            Gravity
            '''
            if not GAME_OVER:
                player_vel_y += GRAVITY
                
            '''                
             Collision
            '''
            # Verticle Movement and Collision
            onGround = False
            player_rect.y += player_vel_y

            for block in blocks:
                if player_rect.colliderect(block):
                    if player_vel_y > 0 and player_rect.bottom <= block.bottom:
                        # Falling and hitting top of platform
                        player_rect.bottom = block.top
                        player_vel_y = 0
                        onGround = True
                    
            
            # Horizontal Movement 
            player_rect.x += dx
                    
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
            
            # Draw score to screen
            hscoreText = font.render('Highest: ' + str(highscore), True, BLUE, WHITE)
            hscoreBox = createSurface(hscoreText, bg_color=(255, 255, 255), border_color=(0, 0, 0), alpha= 255)
            screen.blit(hscoreBox, (5, HEIGHT - 50))
        
            scoreText = font.render('Score: ' + str(score), True, BLUE, WHITE)
            scoreBox = createSurface(scoreText, bg_color=(255, 255, 255), border_color=(0, 0, 0), alpha= 255)
            screen.blit(scoreBox, (5, HEIGHT - 90))
            
            # Game Over
            if player_rect.y > HEIGHT:
                GAME_OVER = True
                player_vel_y = 0
            
                gmText = largeFont.render('Game Over!', True, WHITE)
                rsText = font.render('Space to Restart.', True, WHITE)
                
                # Create styled boxes
                gmBox = createSurface(gmText, bg_color=LIGHT_ORANGE, border_color=DARK_ORANGE, alpha= 255)
                rsBox = createSurface(rsText, bg_color=LIGHT_ORANGE, border_color=DARK_ORANGE, alpha= 255)
                
                # Position boxes at the center of screen
                gmRect = gmBox.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                rsRect = rsBox.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45))
                
                screen.blit(gmBox, gmRect)
                screen.blit(rsBox, rsRect)
                
                # Back to menu button
                if drawButton(
                    screen,
                    "Back to Menu",
                    WIDTH // 2 - 100,
                    HEIGHT // 2 + 120,
                    200,
                    50,
                    font,
                    WHITE,
                    LIGHT_ORANGE,
                    DARK_ORANGE,
                    hover_color=(255, 200, 100)
                ):
                    GAME_STATE = "menu"
                    GAME_OVER = False
                    score = 0
                    player_rect.x, player_rect.y = PLAYER_X, PLAYER_Y
                    platforms = initPlatforms(platforms)
                    BG = BG_COLOR

            else:
                GAME_OVER = False
            
            if score > highscore:
                highscore = score
                
        # Update screen    
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    main()