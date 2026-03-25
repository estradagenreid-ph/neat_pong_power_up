import pygame
import sys
import random
import math
import neat
import os
import time
import pickle 

WIDTH, HEIGHT = 1280, 720
FPS = 60
SAVE_CHECKPOINTS = False
POWER_UPS = True
PLAYER_COLOR = "Green"
OPPONENT_COLOR = "Red"
FOCUSED_GAME_ID = None
GENERATION = 0 - 1
HIGH_SCORE = 0
START_TIME = time.time()
LINE_COLOR = "Grey"


pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Times New Roman", 20, bold=True)
pygame.display.set_caption("Pong AI")

class Power_up:

    def __init__(self):
        self.rect = pygame.Rect(random.randint(300, WIDTH - 300), 
                                random.randint(100, HEIGHT - 100), 30, 30)
        self.type = random.choice(["lightning", "spiral"])
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 10000

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration
    
    # Power up design Vibe Coded From Gemini (2026)
    def draw(self, surface):
        color = (255, 255, 0) if self.type == 'lightning' else (150, 0, 255)
        if self.type == 'lightning':
            pts = [(self.rect.x + 22, self.rect.y + 5), (self.rect.x + 10, self.rect.y + 15),
                   (self.rect.x + 20, self.rect.y + 15), (self.rect.x + 8, self.rect.y + 25)]
            pygame.draw.lines(surface, color, False, pts, 3)
        elif self.type == 'spiral':
            center = self.rect.center
            points = [(center[0] + math.cos(i*0.5)*(14-(i*0.6)), 
                       center[1] + math.sin(i*0.5)*(14-(i*0.6))) 
                      for i in range(20) if (14-(i*0.6)) > 0]
            if len(points) > 1: pygame.draw.lines(surface, color, False, points, 3)

class Pong_Game:

    def __init__(self, game_id, p1, p2, config):
        self.game_id = game_id
        self.p1 = p1 
        self.p2 = p2
        self.net1 = neat.nn.FeedForwardNetwork.create(p1, config)
        self.net2 = neat.nn.FeedForwardNetwork.create(p2, config)

        self.ball = pygame.Rect(WIDTH/2, HEIGHT/2, 16, 16)
        self.p_left = pygame.Rect(50, HEIGHT/2 - 100, 12, 125)
        self.p_right = pygame.Rect(WIDTH - 65, HEIGHT/2 - 100, 12, 125)
        self.paddle_speed = 8.0
        self.p_left_vel = 0
        self.p_right_vel = 0

        self.power_ups = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.hits_l = 0
        self.hits_r = 0
        self.duration = 0.0
        self.reset_ball()

    def reset_ball(self):

        self.ball.center = (WIDTH/2, HEIGHT/2)
        angle_rad = math.radians(random.uniform(-45, 45))
        direction = random.choice([-1, 1])
        self.ball_angle_x = float(math.cos(angle_rad) * direction) # Vector Velocity Formula
        self.ball_angle_y = float(math.sin(angle_rad))
        self.ball_speed = 10.0 

    def game_state(self):

        # Set frame survival reward
        self.p1.fitness += 0.1
        self.p2.fitness += 0.1

        # AI movement
        for (net, pad, genome, side) in ([
            (self.net1, self.p_left, self.p1, "L"),
            (self.net2, self.p_right, self.p2, "R")
        ]):
            
            # Inputs
            inputs = [
                (pad.centery),
                (self.ball.y),
                (abs(pad.x - self.ball.x)),
                (self.ball_speed * self.ball_angle_x),
                (self.ball_speed * self.ball_angle_y)
            ]

            output = net.activate(inputs)
            decision = output.index(max(output))

            if decision == 0:
                genome.fitness -= 0.01
                if side == "L":
                    self.p_left_vel = 0
                else: 
                    self.p_right_vel = 0
            elif decision == 1:
                pad.y += self.paddle_speed
                if side == "L":
                    self.p_left_vel = self.paddle_speed
                else: 
                    self.p_right_vel = self.paddle_speed
            else: 
                pad.y -= self.paddle_speed
                if side == "L":
                    self.p_left_vel = -self.paddle_speed
                else: 
                    self.p_right_vel = -self.paddle_speed

            if pad.top < 0:
                pad.top = 0
            if pad.bottom > HEIGHT:
                pad.bottom = HEIGHT

        # POWER UP LOGIC
        curr_t = pygame.time.get_ticks()

        if GENERATION >= 30 and POWER_UPS == True:
            if curr_t - self.last_spawn_time > 5000:
                num_to_spawn = random.randint(2,6)
                for _ in range(num_to_spawn):
                    self.power_ups.append(Power_up())
                self.last_spawn_time = curr_t

        for pu in self.power_ups[:]:
            if pu.is_expired():
                self.power_ups.remove(pu)
            elif self.ball.colliderect(pu.rect):
                if pu.type == "lightning":
                    self.ball_speed = 15
                else: #Spiral
                    self.ball_speed = max(self.ball_speed, 12)
                    self.ball_angle_y = random.uniform(-0.7, 0.7)
                    self.ball_angle_x = math.sqrt(1 - self.ball_angle_y**2) * (-1 if self.ball_angle_x > 0 else 1)
                self.power_ups.remove(pu)

        # Ball Movement            
        self.ball.x += self.ball_speed * self.ball_angle_x # Vector Velocity
        self.ball.y += self.ball_speed * self.ball_angle_y

        # Ball Wall Collision
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_angle_y *= -1 
            self.ball.y = max (0, min(HEIGHT - self.ball.height, self.ball.y))

        # Paddle Collision w/ relative angular velocity
        for pad, side, player, p_vel in [(
            self.p_left, "L", self.p1, self.p_left_vel),
            (self.p_right, "R", self.p2, self.p_right_vel
        )]: 
            if self.ball.colliderect(pad):

                self.ball_speed = 10.0

                c_pos = (self.ball.centery - pad.centery) / (pad.height / 2)

                momentum = (p_vel / self.paddle_speed) * 0.6

                noise = random.uniform(-0.05, 0.05)

                new_y = (c_pos * 0.4) + momentum + noise

                self.ball_angle_y = max(-0.8, min(0.8, new_y))

                if side == "L":
                    self.ball_angle_x = max(0.4, math.sqrt(abs(1 - self.ball_angle_y **2)))
                    self.p1.fitness += 1
                    self.ball.left = pad.right + 1
                    self.hits_l += 1
                else:
                    self.ball_angle_x = -max(0.4, math.sqrt(abs(1 - self.ball_angle_y **2)))
                    self.p2.fitness += 1
                    self.ball.right = pad.left - 1
                    self.hits_r += 1

        # Scoring
        if self.ball.left <= 0:
            self.p1.fitness -= 500
            self.p2.fitness += 500
            return False
        if self.ball.right >= WIDTH:
            self.p2.fitness -= 500
            self.p1.fitness += 500
            return False
        if max(self.hits_l, self.hits_r) == 50:
            self.p1.fitness -= 500
            self.p2.fitness -= 500
            return False
        
        return True
    
    def draw(self, window):
            
        for pad, colors in [
            (self.p_left, PLAYER_COLOR), 
            (self.p_right, OPPONENT_COLOR)
        ]:
            pygame.draw.rect(window, colors, pad)
        pygame.draw.ellipse(window, (255, 255, 255), self.ball)
        for pu in self.power_ups: pu.draw(window)

def eval_genomes(genomes, config):

    global GENERATION, FOCUSED_GAME_ID, FPS, HIGH_SCORE
    GENERATION += 1
    gen_start = time.time()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    genome_list = []
    
    for genome in genomes:
        if isinstance(genome, tuple):
            genome = genome[1]
        else:
            genome = genome
        genome.fitness = 0.0
        genome_list.append(genome)

    games = []
    for i in range(0, len(genome_list), 2):
        if i + 1 < len(genome_list):
            g1 = genome_list[i]
            g2 = genome_list[i + 1]
            games.append(Pong_Game(i, g1, g2, config))

    while games:

        if FPS > 0:
            dt = clock.tick(FPS) / 1000.0
        else:
            dt = clock.tick(1000.0) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    FPS = 0
                if event.key == pygame.K_s:
                    FPS = 60 
                if event.key == pygame.K_F11:
                    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for game in games[:]:
            game.duration += dt

            if not game.game_state():
                games.remove(game)

            max_fit = max(game.p1.fitness, game.p2.fitness)
            if max_fit > HIGH_SCORE:
                HIGH_SCORE = max_fit

        window.fill((10, 10, 25))
        if games:

            current_best = max(games, key=lambda g: (g.p1.fitness + g.p2.fitness))
            if FOCUSED_GAME_ID is None or not any(g.game_id == FOCUSED_GAME_ID for g in games):
                FOCUSED_GAME_ID = current_best.game_id

            display_game = next((g for g in games if g.game_id == FOCUSED_GAME_ID), current_best)
            display_game.draw(window)

            now = time.time()
            hud = [
                f"Generation: {GENERATION}",
                f"Current Gen Time: {now - gen_start: .1f}s",
                f"Active Pairs: {len(games)}",
                f"Best Ever: {HIGH_SCORE: .0f}",
                f"Volley Count: {display_game.hits_l + display_game.hits_r}",
                f"L-fit: {display_game.p1.fitness: .1f} | R-fit: {display_game.p2.fitness: .1f}",
                f"Total: {int(now - START_TIME) // 60}m {int((now-START_TIME)%60)}s",
                f"FPS: {'MAX' if FPS == 0 else FPS}"
            ]
            for i, text in enumerate(hud):
                window.blit(FONT.render(text, True, (0, 255, 200)), (20, 20 + i*25))

        pygame.draw.aaline(window, LINE_COLOR, (WIDTH /2, 0), (WIDTH / 2, HEIGHT))
        
        pygame.display.flip()


def neat_run():

    global GENERATION, HIGH_SCORE
    config_path = os.path.join(os.path.dirname(__file__), "config-final_power_up.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    checkpoint_file = "None"

    if os.path.exists(checkpoint_file):
        p = neat.Checkpointer.restore_checkpoint(checkpoint_file)

        GENERATION = p.generation
        for g in p.population():
            if g.fitness is not None:
                all_fitness = g.fitness

        HIGH_SCORE = max(all_fitness) if all_fitness else 0
    else:
        p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    if SAVE_CHECKPOINTS:
        p.add_reporter(neat.Checkpointer(10, filename_prefix="pong-checkpont-"))

    winner = p.run(eval_genomes, 10000)

    with open("best_ai.pkl", "wb") as f:
        pickle.dump(winner,f)
        print("BEST AI saved to best_ai.pkl")

if __name__ == "__main__":
    neat_run()