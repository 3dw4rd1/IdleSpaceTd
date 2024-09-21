import pygame
import math

class TownCentre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 50
        self.health = 1000
        self.max_health = 1000
        self.base_color = (192, 192, 192)  # Silver base color
        self.highlight_color = (220, 220, 220)  # Lighter silver for highlights
        self.shadow_color = (160, 160, 160)  # Darker silver for shadows

        # Laser attack properties
        self.laser_damage = 10
        self.laser_cooldown = 1000  # 1 second in milliseconds
        self.laser_range = 100
        self.last_laser_time = 0
        self.laser_target = None
        self.laser_line = None
        self.laser_level = 1

        # Bomb attack properties
        self.bomb_damage_amount = 50
        self.bomb_radius = 100
        self.bomb_cooldown = 5000  # 5 seconds in milliseconds
        self.last_bomb_time = 0
        self.bomb = None
        self.bomb_size = 20
        self.bomb_timer = 0
        self.bomb_duration = 2000  # 2 seconds in milliseconds
        self.explosion = None
        self.explosion_duration = 1000  # 1 second in milliseconds
        self.explosion_start_time = 0
        self.bomb_cost = 5
        self.bomb_upgrade_level = 1

        # Anti-grav properties
        self.anti_grav_active = False
        self.anti_grav_radius = 150
        self.anti_grav_slow = 0.5  # 50% slow
        self.anti_grav_level = 1

        # Health regeneration properties
        self.health_upgrade_level = 0
        self.health_regen = 0
        self.last_regen_time = pygame.time.get_ticks()

    def update(self, units, current_time):
        self.laser_attack(units, current_time)
        self.update_bomb(current_time)
        self.update_explosion(current_time)
        self.bomb_damage(units)

        if self.health_regen > 0:
            if current_time - self.last_regen_time >= 2000:  # 2 seconds
                self.health = min(self.health + self.health_regen, self.max_health)
                self.last_regen_time = current_time

    def laser_attack(self, units, current_time):
        if current_time - self.last_laser_time >= self.laser_cooldown:
            closest_unit = min(units, key=lambda u: math.hypot(u.x - self.x, u.y - self.y), default=None)
            if closest_unit and math.hypot(closest_unit.x - self.x, closest_unit.y - self.y) <= self.laser_range:
                closest_unit.take_damage(self.laser_damage)
                self.laser_target = closest_unit
                self.laser_line = ((self.x, self.y), (closest_unit.x, closest_unit.y))
                self.last_laser_time = current_time
            else:
                self.laser_target = None
                self.laser_line = None
        elif current_time - self.last_laser_time >= 100:  # Clear laser after 100ms
            self.laser_target = None
            self.laser_line = None

    def upgrade_health(self):
        self.health_upgrade_level += 1
        self.max_health += 100
        self.health = min(self.health + 100, self.max_health)
        
        if self.health_upgrade_level % 3 == 0:
            self.health_regen += 1

        return self.health_regen

    def upgrade_laser(self):
        self.laser_level += 1
        self.laser_damage += 5
        self.laser_cooldown = max(100, self.laser_cooldown - 100)  # Minimum cooldown of 100ms
        self.laser_range += 2  # Increase range by 2 each level
        
        print(f"Laser Upgraded - Level: {self.laser_level}, Damage: {self.laser_damage}, Frequency: {1000/self.laser_cooldown:.2f} shots/second, Range: {self.laser_range}")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def place_bomb(self, x, y):
        self.bomb = (x, y)
        self.bomb_timer = pygame.time.get_ticks()

    def update_bomb(self, current_time):
        if self.bomb and current_time - self.bomb_timer >= self.bomb_duration:
            self.explode_bomb()

    def explode_bomb(self):
        self.explosion = self.bomb
        self.explosion_start_time = pygame.time.get_ticks()
        self.bomb = None

    def update_explosion(self, current_time):
        if self.explosion and current_time - self.explosion_start_time >= self.explosion_duration:
            self.explosion = None

    def bomb_damage(self, units):
        if self.explosion:
            for unit in units:
                distance = math.hypot(unit.x - self.explosion[0], unit.y - self.explosion[1])
                if distance <= self.bomb_radius:
                    unit.take_damage(self.bomb_damage_amount)

    def upgrade_bomb(self):
        self.bomb_upgrade_level += 1
        self.bomb_damage_amount += 25
        self.bomb_radius += 20
        print(f"Bomb Upgraded - Level: {self.bomb_upgrade_level}, Damage: {self.bomb_damage_amount}, Radius: {self.bomb_radius}")

    def activate_anti_grav(self):
        self.anti_grav_active = True
        print("AntiGrav Activated")

    def upgrade_anti_grav(self):
        self.anti_grav_level += 1
        self.anti_grav_radius += 25
        self.anti_grav_slow = max(0.1, self.anti_grav_slow - 0.1)  # Minimum 10% speed (90% slow)
        print(f"AntiGrav Upgraded - Level: {self.anti_grav_level}, Slow: {self.anti_grav_slow*100:.1f}%, Radius: {self.anti_grav_radius}")

    def apply_anti_grav(self, unit):
        if self.anti_grav_active:
            distance = math.hypot(unit.x - self.x, unit.y - self.y)
            if distance <= self.anti_grav_radius:
                return self.anti_grav_slow
        return 1.0

    def draw(self, screen):
        # Draw anti-grav field if active
        if self.anti_grav_active:
            anti_grav_surface = pygame.Surface((self.anti_grav_radius * 2, self.anti_grav_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(anti_grav_surface, (0, 100, 255, 30), (self.anti_grav_radius, self.anti_grav_radius), self.anti_grav_radius)
            screen.blit(anti_grav_surface, (self.x - self.anti_grav_radius, self.y - self.anti_grav_radius))

        # Main central structure
        # Base structure
        pygame.draw.polygon(screen, self.base_color, [
            (self.x - self.radius // 3, self.y - self.radius),
            (self.x + self.radius // 3, self.y - self.radius),
            (self.x + self.radius // 4, self.y + self.radius),
            (self.x - self.radius // 4, self.y + self.radius)
        ])
        
        # Angled details
        pygame.draw.line(screen, self.highlight_color, (self.x - self.radius // 3, self.y - self.radius), (self.x - self.radius // 4, self.y + self.radius), 2)
        pygame.draw.line(screen, self.shadow_color, (self.x + self.radius // 3, self.y - self.radius), (self.x + self.radius // 4, self.y + self.radius), 2)
        
        # Horizontal lines for a more technological look
        for i in range(1, 6):
            y = self.y - self.radius + (self.radius * 2 // 5) * i
            pygame.draw.line(screen, self.highlight_color, (self.x - self.radius // 3, y), (self.x + self.radius // 3, y), 1)
        
        # Additional angled details
        pygame.draw.line(screen, self.shadow_color, (self.x - self.radius // 6, self.y - self.radius), (self.x, self.y + self.radius // 2), 2)
        pygame.draw.line(screen, self.highlight_color, (self.x + self.radius // 6, self.y - self.radius), (self.x, self.y + self.radius // 2), 2)
        
        # Top dome
        pygame.draw.ellipse(screen, self.highlight_color, (self.x - self.radius // 3, self.y - self.radius * 1.2, self.radius * 2 // 3, self.radius // 2))
        
        # Rotating rings
        for i in range(3):
            y_offset = self.radius * 0.5 * i
            pygame.draw.ellipse(screen, self.base_color, (self.x - self.radius, self.y - self.radius // 4 + y_offset, self.radius * 2, self.radius // 2), 4)
            pygame.draw.arc(screen, self.highlight_color, (self.x - self.radius, self.y - self.radius // 4 + y_offset, self.radius * 2, self.radius // 2), math.pi, 2*math.pi, 2)
            pygame.draw.arc(screen, self.shadow_color, (self.x - self.radius, self.y - self.radius // 4 + y_offset, self.radius * 2, self.radius // 2), 0, math.pi, 2)
        
        # Side structures
        for angle in [30, 150, 210, 330]:
            x = self.x + int(math.cos(math.radians(angle)) * self.radius * 0.8)
            y = self.y + int(math.sin(math.radians(angle)) * self.radius * 0.8)
            pygame.draw.rect(screen, self.base_color, (x - 5, y - 15, 10, 30))
            pygame.draw.line(screen, self.highlight_color, (x - 5, y - 15), (x - 5, y + 15), 2)
            pygame.draw.line(screen, self.shadow_color, (x + 5, y - 15), (x + 5, y + 15), 2)
        
        
        # Energy core
        core_radius = self.radius // 4
        core_surface = pygame.Surface((core_radius * 2, core_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(core_surface, (200, 230, 255, 100), (core_radius, core_radius), core_radius)
        screen.blit(core_surface, (self.x - core_radius, self.y - core_radius))
        
        # Pulsating energy effect
        pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5
        pulse_radius = int(core_radius + pulse * 5)
        pygame.draw.circle(screen, (200, 230, 255, 50), (self.x, self.y), pulse_radius, 2)

        # Draw health bar
        health_bar_width = 100
        health_bar_height = 2
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x - health_bar_width // 2, self.y + self.radius + 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - health_bar_width // 2, self.y + self.radius + 10, int(health_bar_width * health_ratio), health_bar_height))

        # Draw laser if active
        if self.laser_line:
            pygame.draw.line(screen, (255, 0, 0), self.laser_line[0], self.laser_line[1], 2)

    def draw_bomb_and_explosion(self, screen):
        # Draw bomb
        if self.bomb:
            pygame.draw.circle(screen, (255, 0, 0), self.bomb, self.bomb_size)
        
        # Draw explosion
        if self.explosion:
            explosion_alpha = max(0, 255 - (pygame.time.get_ticks() - self.explosion_start_time) / self.explosion_duration * 255)
            explosion_surface = pygame.Surface((self.bomb_radius * 2, self.bomb_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(explosion_surface, (255, 165, 0, int(explosion_alpha)), (self.bomb_radius, self.bomb_radius), self.bomb_radius)
            screen.blit(explosion_surface, (self.explosion[0] - self.bomb_radius, self.explosion[1] - self.bomb_radius))
