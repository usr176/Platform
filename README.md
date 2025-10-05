# Platform Jumper 

## Controls

**UP** to Jump <br>
**Hold down and then press up** to jump higher <br>
**Left** Move Left <br>
**Right** Move Right

# Endless Platforms
#### Video Demo: https://www.youtube.com/watch?v=q2OyEp_dBy8 
#### Description

Endless Platforms is an infinite vertical scroller built using Python and Pygame, where the player jumps from platform to platform to climb higher. As the player’s score increases, the background  blends toward red and begins to camouflage the platforms, making the game more challenging. The player can also charge jumps by crouching, adding more emphasis on timing. The goal is to reach the highest possible score without falling. The game also features a UI, animations, and a main menu with interactive buttons.

### UI Design and Game States
One of the main challenges during development was designing a user interface that felt clean and did not cluttered the game screen. Implementing menus or overlays required careful layout design. The player must always start at the menu and the game's logic should not be running when the player is browsing the menu and vice versa. To manage this, I separated the game's logic into distinct game states: "menu", "playing", and "game over". This separation allowed me to isolate UI elements per state, avoiding interference between gameplay mechanics and interface components. This approach also made it easier to build responsive buttons, overlays, and restart/menu navigation features without affecting core gameplay logic.

### Designing Buttons
While designing the UI, I also had to build buttons and make sure they are responsive and carry out their task. To achive this goal, I made a custom function `drawButton()`, which renders the button onto the screen while also checking if the player is hovering mouse over the button. The function changes the button's design and color accordingly, and if the player clicks on the button, The function will return a confirmation and we can use that to change game states. The function is called inside the main gameloop. It should be noted that the function while return `True` only if the mouse is hovering over the button and is clicked. The button is alwats generated onto screen, even if the function returns `False`.

### Platform Generation and Optimization
Another challenge was resource management, especially with platforms. Initially, I considered continuously spawning new platforms as the player ascended and deleting any platforms that are no longer visible, but then I had a better approach that would use comparitively lesser lines of code. I opted to recycle existing platforms. As platforms scroll off the screen (i.e., fall below view), they are repositioned above with new randomized x-positions and small vertical gaps. This ensures a continuous stream of platforms while keeping the platform list constant in size, allowing the game to run efficiently even as the score climbs into the hundreds or thousands. This also allowed me to set an initial list of platforms that always spawned at specified coordinates when the game starts.

### Animations
I decided to settle for a simple pygame rect as the player. To make movement feel smooth and experience fluid. I decided to add animations Initially, The animations and physics were implemented on the same pygame rct object, however this led to unexpected result when the player would constanly move or fall. I decided to seprate rects for animations and physics, and only draw the animated rect to the screen while the physics (i.e gravity) worked behind the scenes. <br>
I decided to add animations for squishing when the player jumped and landed, and squashing/slimming when the player runs.
