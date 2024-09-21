import pygame
import math

class UI:
    def __init__(self, width, height, town_centre):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 18)  # Reduced from 36 to 18
        self.resources = 0
        self.level = 1
        self.town_centre = town_centre
        self.buttons = [
            Button("Upgrade Laser", 5, 5, 100, 25),    # Reduced size and adjusted position
            Button("Place Bomb", 5, 35, 100, 25),      # Reduced size and adjusted position
            Button("Upgrade Bomb", 5, 65, 100, 25),    # Reduced size and adjusted position
            Button("Upgrade Health", 5, 95, 100, 25),  # Reduced size and adjusted position
            Button("Activate AntiGrav", 5, 125, 100, 25),
            Button("Upgrade AntiGrav", 5, 155, 100, 25)
        ]
        self.placing_bomb = False
        self.buttons.extend([
            Button("Spawn Spaceship", 5, 185, 100, 25),
            Button("Upgrade Spaceship", 5, 215, 100, 25)
        ])
        self.buttons.append(Button("Upgrade Harvesting", 5, 245, 100, 25))  # Add new button
        self.harvesting_level = 0  # Track harvesting upgrade level

    def draw(self, screen):
        # Draw resources
        resource_text = self.font.render(f"Resources: {self.resources}", True, (255, 255, 255))
        screen.blit(resource_text, (self.width - 110, 5))  # Adjusted position

        # Draw level
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (self.width - 110, 25))  # Adjusted position

        # Draw town centre health
        health_text = self.font.render(f"Health: {self.town_centre.health}/{self.town_centre.max_health}", True, (255, 255, 255))
        screen.blit(health_text, (self.width - 110, 45))  # Position below level

        # Draw buttons with costs
        for button in self.buttons:
            button.draw(screen)
            cost = self.get_action_cost(button.text)
            cost_text = self.font.render(f"Cost: {cost}", True, (255, 255, 255))
            screen.blit(cost_text, (button.rect.right + 5, button.rect.centery - 7))  # Adjusted position

        # Draw new button for Upgrade Harvesting
        harvesting_button = self.buttons[-1]  # Get the last button (Upgrade Harvesting)
        harvesting_button.draw(screen)
        cost_text = self.font.render(f"Cost: 50", True, (255, 255, 255))
        screen.blit(cost_text, (harvesting_button.rect.right + 5, harvesting_button.rect.centery - 7))

        # If placing bomb, show cursor
        if self.placing_bomb:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_missile(screen, mouse_pos, 10, 128)  # Reduced missile size

    def draw_missile(self, screen, pos, size, alpha):
        missile_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.polygon(missile_surface, (255, 0, 0, alpha), [
            (size, 0),
            (size * 2, size * 2),
            (size, size * 1.5),
            (0, size * 2)
        ])
        screen.blit(missile_surface, (pos[0] - size, pos[1] - size))

    def get_action_cost(self, action):
        if action == "Upgrade Laser":
            return 50
        elif action == "Place Bomb":
            return self.town_centre.bomb_cost
        elif action == "Upgrade Bomb":
            return 100  # You can adjust this cost as needed
        elif action == "Upgrade Health":
            return 100
        elif action == "Activate AntiGrav":
            return 50
        elif action == "Upgrade AntiGrav":
            return 50
        elif action == "Spawn Spaceship":
            return 200
        elif action == "Upgrade Spaceship":
            return 100
        elif action == "Upgrade Harvesting":
            return 50
        return 0

    def handle_event(self, event):
        if self.placing_bomb and event.type == pygame.MOUSEBUTTONDOWN:
            self.placing_bomb = False
            if self.resources >= self.town_centre.bomb_cost:
                return ("Place Bomb", event.pos)
            else:
                return "Cannot Afford Bomb"

        for button in self.buttons:
            if button.is_clicked(event):
                cost = self.get_action_cost(button.text)
                if self.resources >= cost:
                    if button.text == "Upgrade Harvesting":
                        return "Upgrade Harvesting"
                    return button.text
                else:
                    return f"Cannot Afford {button.text}"

        return None

    def update_resources(self, amount):
        self.resources += amount

    def update_level(self, level):
        self.level = level

    def upgrade_harvesting(self):
        if self.resources >= 50:
            self.resources -= 50
            self.harvesting_level += 1
            return True
        return False

    # ... (other methods remain the same)

class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 16)  # Reduced from 24 to 16

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
