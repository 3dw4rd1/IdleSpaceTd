import pygame
import sys

class IntroScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_path = "fonts/KarmaticArcade-6Yrp1.ttf"  # Updated font name
        self.title_font = pygame.font.Font(self.font_path, 72)
        self.subtitle_font = pygame.font.Font(self.font_path, 36)
        self.neon_green = (57, 255, 20)
        self.clock = pygame.time.Clock()
        self.blink_timer = 0
        self.blink_interval = 500  # milliseconds

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw title
        title_text = self.title_font.render("IDLE SPACE", True, self.neon_green)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(title_text, title_rect)

        # Draw blinking subtitle
        if self.blink_timer < self.blink_interval:
            subtitle_text = self.subtitle_font.render("INSERT COIN", True, self.neon_green)
            subtitle_rect = subtitle_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
            self.screen.blit(subtitle_text, subtitle_rect)

        pygame.display.flip()

    def update(self):
        self.blink_timer += self.clock.tick(60)
        if self.blink_timer >= self.blink_interval * 2:
            self.blink_timer = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return  # Exit the intro screen and start the game

            self.draw()
            self.update()
