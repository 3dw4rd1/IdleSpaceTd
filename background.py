import pygame
import random
import math
import time

class SpaceBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []
        self.galaxies = []
        self.planets = []
        self.shooting_star = None
        self.last_shooting_star_time = time.time()
        self.shooting_star_interval = 11  # 10 minutes in seconds
        self.generate_stars(200)
        self.generate_galaxies(3)
        self.generate_planets(5)
        self.comet = None
        self.last_comet_time = time.time()
        self.comet_interval = 15  # 90 seconds

    def generate_stars(self, num_stars):
        for _ in range(num_stars):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 3)
            brightness = random.randint(100, 255)
            self.stars.append((x, y, size, brightness))

    def generate_galaxies(self, num_galaxies):
        for _ in range(num_galaxies):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(15, 50)  # Reduced size by about 1/3
            rotation = random.uniform(0, math.pi * 2)
            self.galaxies.append((x, y, size, rotation))

    def generate_planets(self, num_planets):
        for _ in range(num_planets):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(10, 30)
            # Duller, more moon-like colors
            color = (random.randint(50, 100), random.randint(50, 100), random.randint(50, 100))
            self.planets.append((x, y, size, color))

    def generate_shooting_star(self):
        if random.choice([True, False]):
            # Vertical movement (top to bottom)
            start_x = random.randint(0, self.width)
            start_y = 0
            end_x = start_x + random.randint(-self.width//2, self.width//2)
            end_y = self.height
        else:
            # Horizontal movement (left to right or right to left)
            start_y = random.randint(0, self.height)
            if random.choice([True, False]):
                start_x = 0
                end_x = self.width
            else:
                start_x = self.width
                end_x = 0
            end_y = start_y + random.randint(-self.height//2, self.height//2)

        duration = random.uniform(0.5, 1.5)  # Duration of the shooting star animation
        start_time = time.time()
        self.shooting_star = (start_x, start_y, end_x, end_y, start_time, duration)

    def generate_comet(self):
        if random.choice([True, False]):
            # Vertical movement (top to bottom)
            start_x = random.randint(0, self.width)
            start_y = 0
            end_x = start_x + random.randint(-self.width//2, self.width//2)
            end_y = self.height
        else:
            # Horizontal movement (left to right or right to left)
            start_y = random.randint(0, self.height)
            if random.choice([True, False]):
                start_x = 0
                end_x = self.width
            else:
                start_x = self.width
                end_x = 0
            end_y = start_y + random.randint(-self.height//2, self.height//2)

        duration = random.uniform(2, 3)  # Duration of the comet animation
        start_time = time.time()
        self.comet = (start_x, start_y, end_x, end_y, start_time, duration)

    def draw(self, screen):
        # Create a transparent black surface
        background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 200))  # Transparent black

        # Draw stars
        for star in self.stars:
            pygame.draw.circle(background, (star[3], star[3], star[3]), (star[0], star[1]), star[2])

        # Draw galaxies
        for galaxy in self.galaxies:
            surface = pygame.Surface((galaxy[2]*2, galaxy[2]*2), pygame.SRCALPHA)
            for _ in range(50):  # Reduced number of stars in galaxies
                angle = random.uniform(0, math.pi * 2)
                distance = random.uniform(0, galaxy[2])
                x = int(math.cos(angle) * distance) + galaxy[2]
                y = int(math.sin(angle) * distance) + galaxy[2]
                size = random.randint(1, 2)
                color = (random.randint(100, 200), random.randint(100, 200), random.randint(150, 200), random.randint(50, 150))
                pygame.draw.circle(surface, color, (x, y), size)
            rotated_surface = pygame.transform.rotate(surface, math.degrees(galaxy[3]))
            background.blit(rotated_surface, (galaxy[0] - rotated_surface.get_width()//2, galaxy[1] - rotated_surface.get_height()//2))

        # Draw planets
        for planet in self.planets:
            pygame.draw.circle(background, planet[3], (planet[0], planet[1]), planet[2])
            # Add a subtle highlight to give a 3D effect
            highlight = (min(planet[3][0] + 30, 255), min(planet[3][1] + 30, 255), min(planet[3][2] + 30, 255))
            pygame.draw.circle(background, highlight, (planet[0] - planet[2]//4, planet[1] - planet[2]//4), planet[2]//4)

        # Draw shooting star
        current_time = time.time()
        if current_time - self.last_shooting_star_time > self.shooting_star_interval:
            if self.shooting_star is None:
                self.generate_shooting_star()
            elif current_time - self.shooting_star[4] > self.shooting_star[5]:
                self.shooting_star = None
                self.last_shooting_star_time = current_time
            else:
                self.draw_shooting_star(screen, current_time)

        # Draw comet
        if current_time - self.last_comet_time > self.comet_interval:
            if self.comet is None:
                self.generate_comet()
            elif current_time - self.comet[4] > self.comet[5]:
                self.comet = None
                self.last_comet_time = current_time
            else:
                self.draw_comet(screen, current_time)

        screen.blit(background, (0, 0))

    def draw_shooting_star(self, screen, current_time):
        progress = (current_time - self.shooting_star[4]) / self.shooting_star[5]
        x = int(self.shooting_star[0] + (self.shooting_star[2] - self.shooting_star[0]) * progress)
        y = int(self.shooting_star[1] + (self.shooting_star[3] - self.shooting_star[1]) * progress)
        
        # Draw a small, bright white circle for the shooting star
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)
        
        # Add a subtle trail
        for i in range(1, 6):
            trail_x = int(x - i * (x - self.shooting_star[0]) / 5)
            trail_y = int(y - i * (y - self.shooting_star[1]) / 5)
            alpha = 255 - i * 40  # Fade out the trail
            pygame.draw.circle(screen, (255, 255, 255, alpha), (trail_x, trail_y), 1)
        
        # Add a subtle glow
        glow_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 255, 255, 100), (5, 5), 5)
        screen.blit(glow_surf, (x - 5, y - 5), special_flags=pygame.BLEND_ADD)

    def draw_comet(self, screen, current_time):
        progress = (current_time - self.comet[4]) / self.comet[5]
        x = int(self.comet[0] + (self.comet[2] - self.comet[0]) * progress)
        y = int(self.comet[1] + (self.comet[3] - self.comet[1]) * progress)
        
        # Draw comet tail
        tail_length = 40  # Increased tail length
        tail_width = 4  # Slightly increased tail width
        angle = math.atan2(self.comet[3] - self.comet[1], self.comet[2] - self.comet[0])
        tail_end_x = x - tail_length * math.cos(angle)
        tail_end_y = y - tail_length * math.sin(angle)
        
        # Create a gradient effect for the tail
        for i in range(tail_length):
            alpha = 255 - int(255 * i / tail_length)
            color = (255, 165 + int(90 * i / tail_length), 0, alpha)
            pos = (int(x - i * math.cos(angle)), int(y - i * math.sin(angle)))
            pygame.draw.circle(screen, color, pos, tail_width - int(3 * i / tail_length))
        
        # Draw comet head
        pygame.draw.circle(screen, (255, 255, 200), (x, y), 4)  # Brighter, slightly larger head
        
        # Add a glow effect
        glow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 200, 100, 100), (10, 10), 10)
        screen.blit(glow_surf, (x - 10, y - 10), special_flags=pygame.BLEND_ADD)
