import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS, EXIT_DELAY_MS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)

    font = pygame.font.Font(None, 48)
    text_surface = font.render("Game Over", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=screen.get_rect().center)

    score = 0
    game_over = False
    game_over_time = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        dt = clock.tick(60) / 1000

        if not game_over:
            updatable.update(dt)

            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    log_event("player_hit")
                    print("Game over!")
                    print(f"Score: {score}")
                    game_over = True
                    game_over_time = pygame.time.get_ticks()
                    break

            for asteroid in list(asteroids):
                for shot in list(shots):
                    if shot.collides_with(asteroid):
                        score += 1
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()
                        break

        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)

        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        if game_over:
            screen.blit(text_surface, text_rect)
            if pygame.time.get_ticks() - game_over_time >= EXIT_DELAY_MS:
                pygame.display.flip()
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main()
