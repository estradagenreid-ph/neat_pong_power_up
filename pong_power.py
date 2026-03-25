import pygame, sys, random, math

# Initial Setup
pygame.init()
clock = pygame.time.Clock()

# Sets up game window
game_width = 1280
game_height = 720
screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('Pong AI')

# Define Color palette 
bg_color = pygame.Color("black")
light_grey = (200, 200, 200)
player_color = pygame.Color("green")
opp_color = pygame.Color("red")

# Define Game shapes/sprites
ball = pygame.Rect(game_width / 2 - 7, game_height / 2 - 15 , 15, 15)
player = pygame.Rect(game_width - 65, game_height / 2 - 70 , 10, 140)
opponent = pygame.Rect(50, game_height /2 - 70, 10, 140)

# Define ball speed
ball_speed_horizontal = 10
ball_speed_vertical = 10

# Define paddle speeds
player_speed = 0
opponent_speed = 0

# Define x and y variables
x = 0
y = 0

class PowerUp:

    # Initializes the class when called and defining methods
    def __init__(self):
        self.size = 30
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.type = random.choice(['lightning', 'spiral'])
        self.active = True
        self.spawn_pos()
        self.spawn_time = pygame.time.get_ticks()

    def spawn_pos(self):
        # Keeps the power-up in the field of play, away from the immediate paddle areas
        self.rect.x = random.randint(200, game_width - 200)
        self.rect.y = random.randint(100, game_height - 100)

    def draw(self, surface):
        if self.active:
            color = (255, 255, 0) if self.type == 'lightning' else (150, 0, 255)
            
            if self.type == 'lightning':
                # Defining 4 points to create a sharp 'Z' bolt
                # 1. Top Right, 2. Middle (leaning right), 3. Middle (leaning left), 4. Bottom Left
                pts = [
                    (self.rect.x + 22, self.rect.y + 5),  # Top Right
                    (self.rect.x + 10, self.rect.y + 15), # Middle bend
                    (self.rect.x + 20, self.rect.y + 15), # Middle horizontal
                    (self.rect.x + 8, self.rect.y + 25)   # Bottom Left
                ]
                pygame.draw.lines(surface, color, False, pts, 3)
                
            elif self.type == 'spiral':
                center = self.rect.center
                points = []
                # We create a spiral by increasing the angle while decreasing the radius
                for i in range(0, 20):
                    angle = i * 0.5  # Controls how tight the spiral is
                    radius = 14 - (i * 0.6)  # Starts at 14px and shrinks inward
                    if radius > 0:
                        # Convert Polar (angle/radius) to Cartesian (x/y)
                        px = center[0] + math.cos(angle) * radius
                        py = center[1] + math.sin(angle) * radius
                        points.append((px, py))
                
                if len(points) > 1:
                    pygame.draw.lines(surface, color, False, points, 3)

def reset():
    global x, y, ball_speed_horizontal, power_ups, powerup_timer

    ball_speed_horizontal = 10

    # Clears Power Ups at every Reset
    power_ups.clear()

    # Starts power up clock at beginning of reset
    powerup_timer = pygame.time.get_ticks()

    # Centers ball
    ball.center = (game_width / 2, game_height / 2)
    
    # Calculate initial direction once
    angle_deg = random.randint(-45, 45)
    if abs(angle_deg) < 10: 
        angle_deg = 10 if angle_deg >= 0 else -10
        
    angle = math.radians(angle_deg)
    # Determine horizontal direction
    direction = random.choice([-1, 1])
    x = math.cos(angle) * direction
    y = math.sin(angle)

def ball_movement():

    # We'll just use horizontal as 'Total Speed'
    global x, y, ball_speed_horizontal 
    
    # Use the same speed variable here
    ball.x += ball_speed_horizontal * x
    ball.y += ball_speed_horizontal * y 

power_ups = []
powerup_timer = pygame.time.get_ticks()
reset()


# Initiate Game State
while True:

        # Handles user input with 'events'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            elif event.key == pygame.K_UP:
                player_speed -= 7
            elif event.key == pygame.K_s:
                opponent_speed += 7
            elif event.key == pygame.K_w:
                opponent_speed -= 7
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            elif event.key == pygame.K_UP:
                player_speed += 7
            elif event.key == pygame.K_s:
                opponent_speed -= 7
            elif event.key == pygame.K_w:
                opponent_speed += 7

    # Initiate ball movement
    ball_movement()       

    # Initiate Paddle Movement
    player.y += player_speed
    opponent.y += opponent_speed

    # Paddle Border detection
    if player.top <= 0:
        player.top = 0
    if player.bottom >= game_height:
        player.bottom = game_height
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= game_height:
        opponent.bottom = game_height


    # Conditional to detect ball border detection
    if ball.top <= 0:
        y *= -1
        ball.top = 0
    elif ball.bottom >= game_height:
        y *= -1
        ball.bottom = game_height 
    if ball.left <= 0 or ball.right >= game_width:
        reset()


    # Power-up Collision Logic
    for p in power_ups[:]:
        if ball.colliderect(p.rect):
            if p.type == 'lightning':
                if ball_speed_horizontal < 40: # Capped so it's not impossible
                    ball_speed_horizontal *= 1.5 
            elif p.type == 'spiral':
                x *= -1
                y = max(-0.9, min(0.9, y + random.uniform(-0.2, 0.2)))
                # Recalculate x to keep the speed perfectly consistent
                x = math.sqrt(1 - y**2) * (-1 if x < 0 else 1)
            power_ups.remove(p)
            if len(power_ups) == 0:
                powerup_timer = pygame.time.get_ticks()

        elif pygame.time.get_ticks() - p.spawn_time > 10000:
            power_ups.remove(p)
            if len(power_ups) == 0:
                powerup_timer = pygame.time.get_ticks()

    # Respawn logic: If 5 seconds have passed since the last one was taken
    if len(power_ups) == 0:
        current_time = pygame.time.get_ticks()
        if current_time - powerup_timer > 5000:
            for i in range(random.randint(1,3)):
                power_ups.append(PowerUp())

    # For the Player (Right)
    if ball.colliderect(player):
        if x > 0: 
            # 1. Calculate the raw vertical hit position (-1 to 1)
            collision_pos = (ball.centery - player.centery) / (player.height / 2)
            
            # 2. Clamp y and apply the vector math
            # We use 0.9 to ensure we don't go perfectly vertical
            y = max(-0.9, min(0.9, collision_pos * 0.8))
            x = -math.sqrt(1 - y**2) # -sqrt because it's bouncing LEFT
            
            ball.right = player.left
            ball_speed_horizontal = 10 # Reset speed after hit

    # For the Opponent (Left)
    if ball.colliderect(opponent):
        if x < 0: 
            # 1. Calculate the raw vertical hit position (-1 to 1)
            collision_pos = (ball.centery - opponent.centery) / (opponent.height / 2)
            
            # 2. Clamp y and apply the vector math
            y = max(-0.9, min(0.9, collision_pos * 0.8))
            x = math.sqrt(1 - y**2) # +sqrt because it's bouncing RIGHT
            
            ball.left = opponent.right
            ball_speed_horizontal = 10 # Reset speed after hit

    # Render Game backgrounds 
    screen.fill(bg_color)  

    # Draw the power-up on top of the background
    for p in power_ups:
        p.draw(screen) 

    # Draw Game Visuals
    
    # Draw Player Paddle (Split into 3 sections)
    third_h = player.height / 3
    # Top 3rd
    pygame.draw.rect(screen, (0, 0, 255), (player.x, player.y, player.width, third_h))
    # Middle 3rd
    pygame.draw.rect(screen, player_color, (player.x, player.y + third_h, player.width, third_h))
    # Bottom 3rd
    pygame.draw.rect(screen, (255, 255, 0), (player.x, player.y + 2 * third_h, player.width, third_h))

    # Draw Opponent Paddle (Split into 3 sections)
    # Top 3rd
    pygame.draw.rect(screen, (128, 0, 128), (opponent.x, opponent.y, opponent.width, third_h))
    # Middle 3rd
    pygame.draw.rect(screen, opp_color, (opponent.x, opponent.y + third_h, opponent.width, third_h))
    # Bottom 3rd
    pygame.draw.rect(screen, (255, 165, 0), (opponent.x, opponent.y + 2 * third_h, opponent.width, third_h))

    # Draw Ball
    pygame.draw.ellipse(screen, light_grey, ball)

    # Render Anti-Aliasing middle line
    pygame.draw.aaline(screen, light_grey, (game_width/2, 0), (game_width/2, game_height))

    # Updates Game Window (at 60 FPS)
    pygame.display.flip()
    clock.tick(60)

