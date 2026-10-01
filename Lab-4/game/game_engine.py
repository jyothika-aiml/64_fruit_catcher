import random
import pygame
from game.basket import Basket
from game.fruit import Fruit


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []

        self.score = 0
        self.lives = 3

        # Dynamic difficulty
        self.spawn_delay = 750
        self.min_spawn_delay = 300

        self.speed_multiplier = 1.0
        self.max_speed_multiplier = 2.0

        # Particle effects
        self.particles = []

        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def create_particles(self, x, y, color):
        for _ in range(12):
            particle = {
                "x": float(x),
                "y": float(y),
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-4, -1),
                "life": random.randint(20, 35),
                "color": color
            }

            self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.2
            particle["life"] -= 1

            if particle["life"] <= 0:
                self.particles.remove(particle)

    def update(self):
        if self.game_state != "PLAYING":
            self.update_particles()
            return

        # Move basket
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        # Dynamic difficulty based on score
        self.spawn_delay = max(
            self.min_spawn_delay,
            750 - (self.score * 30)
        )

        self.speed_multiplier = min(
            self.max_speed_multiplier,
            1.0 + (self.score * 0.05)
        )

        # Spawn fruits
        now = pygame.time.get_ticks()

        if now - self.last_spawn_time >= self.spawn_delay:
            self.fruits.append(
                Fruit(
                    self.width,
                    self.speed_multiplier
                )
            )
            self.last_spawn_time = now

        basket_rect = self.basket.rect

        # Update fruits
        for fruit in self.fruits[:]:
            fruit.update()

            # Fruit caught by basket
            if basket_rect.colliderect(fruit.rect):

                # Create splash particles
                self.create_particles(
                    fruit.x,
                    fruit.y,
                    fruit.color
                )

                # Rotten fruit decreases life
                if fruit.is_rotten:
                    self.lives -= 1

                    if self.lives <= 0:
                        self.game_state = "GAME_OVER"

                # Normal fruit increases score
                else:
                    self.score += 1

                self.fruits.remove(fruit)
                continue

            # Fruit missed / hits floor
            if fruit.is_missed(self.height):

                # Create splash particles at floor
                self.create_particles(
                    fruit.x,
                    self.height - 25,
                    fruit.color
                )

                self.lives -= 1
                self.fruits.remove(fruit)

                if self.lives <= 0:
                    self.game_state = "GAME_OVER"

        # Update particles
        self.update_particles()

    def reset(self):
        self.basket = Basket(self.width, self.height)
        self.fruits.clear()
        self.particles.clear()

        self.score = 0
        self.lives = 3

        self.spawn_delay = 750
        self.speed_multiplier = 1.0

        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

    def render(self, screen):
        screen.fill((28, 32, 40))

        # Ground
        ground_y = self.height - 25

        pygame.draw.rect(
            screen,
            (45, 50, 60),
            (0, ground_y, self.width, 25)
        )

        # Basket
        self.basket.render(screen)

        # Fruits
        for fruit in self.fruits:
            fruit.render(screen)

        # Particle effects
        for particle in self.particles:
            pygame.draw.circle(
                screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                3
            )

        # Score
        score_surf = self.font_medium.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(score_surf, (25, 20))

        # Lives
        lives_surf = self.font_medium.render(
            f"Lives: {self.lives}",
            True,
            (240, 80, 80)
        )

        screen.blit(
            lives_surf,
            (
                self.width - lives_surf.get_width() - 25,
                20
            )
        )

        # Game Over
        if self.game_state == "GAME_OVER":

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render(
                "GAME OVER",
                True,
                (235, 70, 70)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2 - over_surf.get_width() // 2,
                    self.height // 2 - 40
                )
            )

            final_surf = self.font_medium.render(
                f"Final Score: {self.score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                final_surf,
                (
                    self.width // 2 - final_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )

            restart_surf = self.font_medium.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )