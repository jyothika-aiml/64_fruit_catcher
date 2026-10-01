import random
import pygame


class Fruit:
    def __init__(self, screen_width, speed_multiplier=1.0):
        self.screen_width = screen_width

        # 20% chance of being a rotten fruit / hazard
        self.is_rotten = random.random() < 0.20

        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2

        # Fruit becomes faster as difficulty increases
        base_speed = random.uniform(4.0, 6.5)
        self.speed = base_speed * speed_multiplier

        if self.is_rotten:
            self.color = (60, 180, 60)
        else:
            self.color = random.choice([
                (230, 45, 45),
                (245, 140, 30),
                (160, 60, 200),
            ])

    def update(self):
        self.y += self.speed

    def is_missed(self, screen_height):
        return self.y > screen_height

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        center = (int(self.x), int(self.y))

        pygame.draw.circle(
            surface,
            self.color,
            center,
            self.radius
        )

        if self.is_rotten:
            pygame.draw.line(
                surface,
                (20, 20, 20),
                (int(self.x - 7), int(self.y - 7)),
                (int(self.x + 7), int(self.y + 7)),
                3
            )

            pygame.draw.line(
                surface,
                (20, 20, 20),
                (int(self.x + 7), int(self.y - 7)),
                (int(self.x - 7), int(self.y + 7)),
                3
            )
        else:
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (int(self.x - 4), int(self.y - 4)),
                3
            )