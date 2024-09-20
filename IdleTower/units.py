import pygame
import math
import random

class BaseUnit:
    def __init__(self, screen_width, screen_height, target):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.target = target
        self.size = 10  # Base size reduced by 50% (from typical 20 to 10)
        self.base_speed = 1  # This is the base speed
        self.speed = self.base_speed  # This will be adjusted by the level manager
        self.spawn()

    def spawn(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])
        padding = 50
        if side == 'top':
            self.x = random.randint(0, self.screen_width)
            self.y = -padding
        elif side == 'right':
            self.x = self.screen_width + padding
            self.y = random.randint(0, self.screen_height)
        elif side == 'bottom':
            self.x = random.randint(0, self.screen_width)
            self.y = self.screen_height + padding
        else:  # left
            self.x = -padding
            self.y = random.randint(0, self.screen_height)

    def update(self):
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed

    def collides_with(self, other):
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < (self.size + other.radius)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True  # Unit is destroyed
        return False

class TriangleUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (255, 0, 0)  # Red
        self.base_speed = 1
        self.damage = 5
        self.value = 1
        self.health = 10
        # Note: We're not setting size here, so it will use the base size

    def draw(self, screen):
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size / 2, self.y + self.size / 2),
            (self.x + self.size / 2, self.y + self.size / 2)
        ]
        pygame.draw.polygon(screen, self.color, points, 2)

class SquareUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (0, 255, 0)  # Green
        self.size = 12  # Slightly larger than base
        self.base_speed = 0.8
        self.damage = 8
        self.value = 2
        self.health = 15

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.size/2, self.y - self.size/2, self.size, self.size), 2)

class CircleUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (0, 0, 255)  # Blue
        self.size = 8  # Slightly smaller than base
        self.base_speed = 1.2
        self.damage = 3
        self.value = 1
        self.health = 8

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, 2)

class DiamondUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (255, 255, 0)  # Yellow
        self.size = 11  # Slightly larger than base
        self.base_speed = 0.9
        self.damage = 6
        self.value = 3
        self.health = 12

    def draw(self, screen):
        points = [
            (self.x, self.y - self.size),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x - self.size, self.y)
        ]
        pygame.draw.polygon(screen, self.color, points, 2)

class StarUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (255, 0, 255)  # Magenta
        self.size = 13  # Larger than base
        self.base_speed = 0.7
        self.damage = 10
        self.value = 5
        self.health = 20

    def draw(self, screen):
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10
            radius = self.size if i % 2 == 0 else self.size / 2
            points.append((
                self.x + radius * math.sin(angle),
                self.y - radius * math.cos(angle)
            ))
        pygame.draw.polygon(screen, self.color, points, 2)

def spawn_random_unit(screen_width, screen_height, target):
    unit_classes = [TriangleUnit, SquareUnit, CircleUnit, DiamondUnit, StarUnit]
    return random.choice(unit_classes)(screen_width, screen_height, target)
