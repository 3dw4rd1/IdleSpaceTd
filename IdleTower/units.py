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
        self.color = (180, 0, 0)  # Darker red
        self.highlight_color = (255, 60, 60)  # Lighter red for details
        self.engine_color = (255, 165, 0)  # Orange for engine glow
        self.base_speed = 1
        self.damage = 5
        self.value = 1
        self.health = 10
        self.size = 15  # Slightly larger for more detail

    def draw(self, screen):
        # Calculate angle to target for proper orientation
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        
        # Main body
        points = [
            (self.x + math.cos(angle) * self.size, self.y + math.sin(angle) * self.size),
            (self.x + math.cos(angle + 2.5) * self.size, self.y + math.sin(angle + 2.5) * self.size),
            (self.x + math.cos(angle - 2.5) * self.size, self.y + math.sin(angle - 2.5) * self.size)
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # Cockpit
        cockpit_pos = (int(self.x + math.cos(angle) * self.size * 0.5), 
                       int(self.y + math.sin(angle) * self.size * 0.5))
        pygame.draw.circle(screen, self.highlight_color, cockpit_pos, int(self.size * 0.2))
        
        # Wing details
        wing_points1 = [points[0], points[1], 
                        (self.x + math.cos(angle + 2.2) * self.size * 0.7, 
                         self.y + math.sin(angle + 2.2) * self.size * 0.7)]
        wing_points2 = [points[0], points[2], 
                        (self.x + math.cos(angle - 2.2) * self.size * 0.7, 
                         self.y + math.sin(angle - 2.2) * self.size * 0.7)]
        pygame.draw.polygon(screen, self.highlight_color, wing_points1, 2)
        pygame.draw.polygon(screen, self.highlight_color, wing_points2, 2)
        
        # Engine glow
        engine_pos = (int(self.x - math.cos(angle) * self.size * 0.7), 
                      int(self.y - math.sin(angle) * self.size * 0.7))
        pygame.draw.circle(screen, self.engine_color, engine_pos, int(self.size * 0.3))
        
        # Engine trails
        for i in [-1, 0, 1]:
            offset = i * self.size * 0.2
            start_x = engine_pos[0] + math.sin(angle) * offset
            start_y = engine_pos[1] - math.cos(angle) * offset
            end_x = start_x - math.cos(angle) * self.size * 0.5
            end_y = start_y - math.sin(angle) * self.size * 0.5
            pygame.draw.line(screen, self.engine_color, (start_x, start_y), (end_x, end_y), 2)

    def update(self):
        super().update()
        # Add a slight wobble to the movement for a more dynamic feel
        self.x += math.sin(pygame.time.get_ticks() * 0.01) * 0.1
        self.y += math.cos(pygame.time.get_ticks() * 0.01) * 0.1

class SpiderUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (0, 255, 0)  # Bright green for the main body
        self.leg_color = (0, 200, 0)  # Slightly darker green for legs
        self.booster_color = (0, 255, 255)  # Cyan for boosters
        self.base_speed = 1
        self.damage = 5
        self.value = 1
        self.health = 10
        self.size = 15  # Slightly larger for more detail

    def draw(self, screen):
        # Calculate angle to target for proper orientation
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        
        # Main body (oval shape)
        pygame.draw.ellipse(screen, self.color, (self.x - self.size/2, self.y - self.size/3, self.size, self.size*2/3))
        
        # Glowing core
        core_size = self.size / 3
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), int(core_size))
        
        # Spider legs (4 pairs)
        for i in range(4):
            angle_offset = math.pi/4 + (i * math.pi/2)
            leg_length = self.size * 0.8
            
            for side in [-1, 1]:
                leg_angle = angle + (angle_offset * side)
                end_x = self.x + math.cos(leg_angle) * leg_length
                end_y = self.y + math.sin(leg_angle) * leg_length
                
                # Draw each leg as two segments for a more organic look
                mid_x = self.x + math.cos(leg_angle) * leg_length * 0.6
                mid_y = self.y + math.sin(leg_angle) * leg_length * 0.6
                
                pygame.draw.line(screen, self.leg_color, (self.x, self.y), (mid_x, mid_y), 2)
                pygame.draw.line(screen, self.leg_color, (mid_x, mid_y), (end_x, end_y), 2)
        
        # Boosters (opposite to the direction of movement)
        booster_angle = angle + math.pi
        booster_length = self.size * 0.4
        for i in [-1, 0, 1]:
            offset = i * self.size * 0.2
            start_x = self.x + math.cos(booster_angle) * offset
            start_y = self.y + math.sin(booster_angle) * offset
            end_x = start_x - math.cos(angle) * booster_length
            end_y = start_y - math.sin(angle) * booster_length
            
            pygame.draw.line(screen, self.booster_color, (start_x, start_y), (end_x, end_y), 3)

    def update(self):
        super().update()
        # Add a slight pulsating effect to the core
        core_pulse = math.sin(pygame.time.get_ticks() * 0.01) * 0.2 + 0.8
        self.core_size = self.size / 3 * core_pulse

class CircleUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (0, 0, 255)  # Blue
        self.light_color = (100, 100, 255)  # Light blue for lights and beam
        self.size = 20  # Increased size for more detail
        self.base_speed = 1.2
        self.damage = 3
        self.value = 1
        self.health = 8
        self.angle = 0  # For circular movement
        self.beam_active = False
        self.beam_timer = 0

    def draw(self, screen):
        # Main body
        pygame.draw.ellipse(screen, self.color, (self.x - self.size, self.y - self.size//2, self.size*2, self.size))
        
        # Top dome
        pygame.draw.arc(screen, self.light_color, (self.x - self.size*0.7, self.y - self.size*0.7, self.size*1.4, self.size*0.7), math.pi, 2*math.pi, 2)
        
        # Lights
        for i in range(8):
            angle = i * math.pi / 4
            light_x = self.x + math.cos(angle) * self.size * 0.8
            light_y = self.y + math.sin(angle) * self.size * 0.4
            pygame.draw.circle(screen, self.light_color, (int(light_x), int(light_y)), 2)
        
        # Beam (activates periodically)
        if self.beam_active:
            beam_surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.polygon(beam_surface, (*self.light_color, 100), 
                                [(self.size, self.size), (self.size*0.7, self.size*2), (self.size*1.3, self.size*2)])
            screen.blit(beam_surface, (self.x - self.size, self.y))

def update(self):
        super().update()
        
        # Subtle circular movement
        self.angle += 0.02  # Reduced from 0.1 for slower rotation
        offset_x = math.sin(self.angle) * 1.5  # Reduced from 5 for smaller circles
        offset_y = math.cos(self.angle) * 1.5
        
        # Apply offsets, but maintain overall direction towards target
        target_angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        self.x += math.cos(target_angle) * self.speed * 0.9 + offset_x * 0.1
        self.y += math.sin(target_angle) * self.speed * 0.9 + offset_y * 0.1
        
        # Beam activation (less frequent)
        self.beam_timer += 1
        if self.beam_timer >= 180:  # Activate every 180 frames (about 3 seconds at 60 FPS)
            self.beam_active = not self.beam_active
            self.beam_timer = 0

class DiamondUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (255, 255, 0)  # Yellow
        self.glow_color = (255, 165, 0)  # Orange glow
        self.size = 15  # Slightly larger for more detail
        self.base_speed = 0.9
        self.damage = 6
        self.value = 3
        self.health = 12
        self.angle = 0  # For serpentine movement
        self.wave_amplitude = 20  # Adjust for more or less wavy movement

    def draw(self, screen):
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        
        # Main body
        body_length = self.size * 2
        body_width = self.size * 0.8
        body_points = [
            (self.x + math.cos(angle) * body_length, self.y + math.sin(angle) * body_length),
            (self.x - math.cos(angle) * body_length, self.y - math.sin(angle) * body_length),
        ]
        pygame.draw.line(screen, self.color, body_points[0], body_points[1], int(body_width))
        
        # Fins
        fin_length = self.size * 0.8
        fin_angles = [2*math.pi/3, 4*math.pi/3]
        for fin_angle in fin_angles:
            fin_x = self.x - math.cos(angle) * body_length * 0.7
            fin_y = self.y - math.sin(angle) * body_length * 0.7
            fin_end_x = fin_x + math.cos(angle + fin_angle) * fin_length
            fin_end_y = fin_y + math.sin(angle + fin_angle) * fin_length
            pygame.draw.line(screen, self.color, (fin_x, fin_y), (fin_end_x, fin_end_y), 2)
        
        # Nose cone
        nose_length = self.size * 0.6
        nose_width = self.size * 0.4
        nose_end = (self.x + math.cos(angle) * (body_length + nose_length), 
                    self.y + math.sin(angle) * (body_length + nose_length))
        pygame.draw.line(screen, self.color, body_points[0], nose_end, int(nose_width))
        
        # Glowing engine

class StarUnit(BaseUnit):
    def __init__(self, screen_width, screen_height, target):
        super().__init__(screen_width, screen_height, target)
        self.color = (255, 0, 255)  # Purple
        self.engine_color = (255, 165, 0)  # Orange for engine glow
        self.size = 10  # Adjust size as needed
        self.base_speed = 0.7
        self.damage = 10
        self.value = 5
        self.health = 20
        self.burst_chance = 0.01  # 1% chance of burst movement per frame

    def draw(self, screen):
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        
        # Main body
        body_length = self.size * 1.5
        body_width = self.size * 0.4
        pygame.draw.line(screen, self.color, 
                         (self.x - math.cos(angle) * body_length/2, self.y - math.sin(angle) * body_length/2),
                         (self.x + math.cos(angle) * body_length/2, self.y + math.sin(angle) * body_length/2),
                         int(body_width))
        
        # Wings
        wing_span = self.size * 1.2
        wing_width = self.size * 0.2
        wing_angles = [math.pi/4, -math.pi/4]
        for wing_angle in wing_angles:
            wing_cos = math.cos(wing_angle)
            wing_sin = math.sin(wing_angle)
            wing_start = (self.x + wing_sin * body_width/2, self.y - wing_cos * body_width/2)
            wing_end = (self.x + wing_sin * wing_span, self.y - wing_cos * wing_span)
            pygame.draw.line(screen, self.color, wing_start, wing_end, int(wing_width))
            # Mirror the wing
            wing_start = (self.x - wing_sin * body_width/2, self.y + wing_cos * body_width/2)
            wing_end = (self.x - wing_sin * wing_span, self.y + wing_cos * wing_span)
            pygame.draw.line(screen, self.color, wing_start, wing_end, int(wing_width))
        
        # Cockpit
        cockpit_pos = (int(self.x + math.cos(angle) * body_length * 0.3), 
                       int(self.y + math.sin(angle) * body_length * 0.3))
        pygame.draw.circle(screen, (200, 200, 200), cockpit_pos, int(body_width * 0.4))
        
        # Engine glow
        engine_pos = (int(self.x - math.cos(angle) * body_length * 0.8), 
                      int(self.y - math.sin(angle) * body_length * 0.8))
        pygame.draw.circle(screen, self.engine_color, engine_pos, int(body_width * 0.3))

    def update(self):
        super().update()
        
        # Random burst movement
        if random.random() < self.burst_chance:
            burst_speed = self.base_speed * 5  # 5 times normal speed
            angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
            self.x += math.cos(angle) * burst_speed
            self.y += math.sin(angle) * burst_speed

def spawn_random_unit(screen_width, screen_height, target):
    unit_classes = [TriangleUnit, CircleUnit, SpiderUnit, DiamondUnit, StarUnit]
    return random.choice(unit_classes)(screen_width, screen_height, target)
