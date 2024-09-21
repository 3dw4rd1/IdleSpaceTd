import pygame
import math
import random

class Spaceship:
    def __init__(self, screen_width, screen_height, town_centre):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.town_centre = town_centre
        self.size = 25  # 1.25x the BaseUnit size of 20
        self.speed = 2
        self.detect_radius = 100
        self.attack_radius = 80
        self.laser_damage = 20
        self.laser_cooldown = 500  # milliseconds
        self.last_shot = 0
        self.patrol_angle = 0
        self.patrol_speed = 0.02  # Adjust this to change patrol speed
        self.spawn()
        self.laser_duration = 100  # Duration to show the laser in milliseconds
        self.laser_end_time = 0  # Time when the current laser should stop being drawn
        self.laser_target = None  # The current target of the laser
        self.separation_distance = 50  # Desired separation between spaceships
        self.alignment_factor = 0.1  # How much to align with average direction
        self.cohesion_factor = 0.1  # How much to move towards the center of mass
        self.target_angle = self.angle
        self.rotation_speed = 0.1  # Adjust this value to change how quickly the spaceship rotates

    def spawn(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            self.x = random.randint(0, self.screen_width)
            self.y = -self.size
        elif side == 'right':
            self.x = self.screen_width + self.size
            self.y = random.randint(0, self.screen_height)
        elif side == 'bottom':
            self.x = random.randint(0, self.screen_width)
            self.y = self.screen_height + self.size
        else:  # left
            self.x = -self.size
            self.y = random.randint(0, self.screen_height)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self, units, current_time, spaceships):
        target_detected = False
        for unit in units:
            distance = math.hypot(unit.x - self.x, unit.y - self.y)
            if distance <= self.detect_radius:
                target_detected = True
                self.target_angle = math.atan2(unit.y - self.y, unit.x - self.x)
                if distance <= self.attack_radius and current_time - self.last_shot >= self.laser_cooldown:
                    unit.take_damage(self.laser_damage)
                    self.last_shot = current_time
                    self.laser_end_time = current_time + self.laser_duration
                    self.laser_target = (unit.x, unit.y)  # Store the target's position
                break

        if not target_detected:
            self.flock(spaceships)

        # Smoothly rotate towards the target angle
        angle_diff = (self.target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        if abs(angle_diff) > 0.01:  # Only rotate if the difference is significant
            self.angle += angle_diff * self.rotation_speed

        # Move
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Wrap around screen
        self.x %= self.screen_width
        self.y %= self.screen_height

    def flock(self, spaceships):
        separation = [0, 0]
        alignment = [0, 0]
        cohesion = [0, 0]
        count = 0

        for other in spaceships:
            if other != self:
                distance = math.hypot(other.x - self.x, other.y - self.y)
                if distance < self.separation_distance:
                    separation[0] += self.x - other.x
                    separation[1] += self.y - other.y
                if distance < self.detect_radius:
                    alignment[0] += math.cos(other.angle)
                    alignment[1] += math.sin(other.angle)
                    cohesion[0] += other.x
                    cohesion[1] += other.y
                    count += 1

        if count > 0:
            # Normalize and apply factors
            alignment[0] /= count
            alignment[1] /= count
            cohesion[0] = cohesion[0] / count - self.x
            cohesion[1] = cohesion[1] / count - self.y

        # Calculate patrol position
        patrol_radius = self.town_centre.anti_grav_radius + self.size
        patrol_x = self.town_centre.x + math.cos(self.patrol_angle) * patrol_radius
        patrol_y = self.town_centre.y + math.sin(self.patrol_angle) * patrol_radius

        # Combine all influences
        target_x = patrol_x + separation[0] + alignment[0] * self.alignment_factor + cohesion[0] * self.cohesion_factor
        target_y = patrol_y + separation[1] + alignment[1] * self.alignment_factor + cohesion[1] * self.cohesion_factor

        # Instead of setting self.angle directly, set self.target_angle
        self.target_angle = math.atan2(target_y - self.y, target_x - self.x)

        # Update patrol angle
        self.patrol_angle += self.patrol_speed

    def draw(self, screen, current_time):
        # Draw spaceship body
        points = [
            (self.x + self.size * math.cos(self.angle), self.y + self.size * math.sin(self.angle)),
            (self.x + self.size/2 * math.cos(self.angle + 2.5), self.y + self.size/2 * math.sin(self.angle + 2.5)),
            (self.x + self.size/2 * math.cos(self.angle - 2.5), self.y + self.size/2 * math.sin(self.angle - 2.5))
        ]
        pygame.draw.polygon(screen, (200, 200, 200), points)

        # Draw engine glow
        glow_pos = (int(self.x - self.size/2 * math.cos(self.angle)), int(self.y - self.size/2 * math.sin(self.angle)))
        pygame.draw.circle(screen, (0, 100, 255), glow_pos, int(self.size/4))

        # Draw laser if it's active
        if current_time < self.laser_end_time and self.laser_target:
            laser_start = (int(self.x), int(self.y))
            laser_end = self.laser_target
            pygame.draw.line(screen, (255, 0, 0), laser_start, laser_end, 2)  # Red laser with width 2

    def upgrade(self):
        self.detect_radius += 20
        self.attack_radius += 15
        self.laser_damage += 5
        self.laser_cooldown = max(100, self.laser_cooldown - 50)
        
        # Debug print statement
        print(f"Spaceship Upgraded - Detect Radius: {self.detect_radius}, Attack Radius: {self.attack_radius}, "
              f"Laser Damage: {self.laser_damage}, Laser Cooldown: {self.laser_cooldown}ms, "
              f"Shots per second: {1000/self.laser_cooldown:.2f}")
