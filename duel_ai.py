import pygame
import pickle
import neat
import os
import pong_final_power_up
from pong_final_power_up import Pong_Game, Power_up  

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60

def duel_ai(config_path, p1_pickle, p2_pickle):

    pong_final_power_up.GENERATION = 30 

    # Setup NEAT Config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Load Both AI
    with open(p1_pickle, "rb") as f:
        genome1 = pickle.load(f)
    with open(p2_pickle, "rb") as f:
        genome2 = pickle.load(f)

    # Create Networks
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    # Initialize Pygame & Game
    pygame.init()

    ai1_score = 0
    ai2_score = 0
    score_font = pygame.font.SysFont("Consolas", 60, bold=True)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    game = Pong_Game(0, genome1, genome2, config)
    game.gen = 30
    
    # Overwrite the nets in the game object with our loaded ones
    game.net1 = net1
    game.net2 = net2

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Run Game State
        if not game.game_state():
            # Check who scored before resetting the ball
            if game.ball.left <= 0:
                ai2_score += 1  # AI 2 (Right) scored
            elif game.ball.right >= WIDTH:
                ai1_score += 1  # AI 1 (Left) scored

            game.reset_ball()

        # Draw
        window.fill((10, 10, 25))
        game.draw(window)

        window.fill((10, 10, 25))
        game.draw(window)

        # Draw Match Score (centered)
        score_text = f"{ai1_score} : {ai2_score}"
        score_surf = score_font.render(score_text, True, (255, 255, 255))
        window.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 50))
        
        # Add Labels
        font = pygame.font.SysFont("Consolas", 24)
        window.blit(font.render(f"AI 1 ({p1_pickle})", True, (0, 255, 0)), (100, 20))
        window.blit(font.render(f"AI 2 ({p2_pickle})", True, (255, 0, 0)), (WIDTH - 300, 20))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    c_path = "config-final_power_up.txt"
    duel_ai(c_path, "GEN 10 AI.pkl", "GEN 81 AI.pkl")
