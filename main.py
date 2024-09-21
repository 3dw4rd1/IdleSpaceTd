import pygame
import random
from towncentre import TownCentre
from units import spawn_random_unit
from ui import UI
from levelmanager import LevelManager
from spaceship import Spaceship
from background import SpaceBackground  # Import the new background class
from introscreen import IntroScreen

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Tower Defense")

# Set up the clock
clock = pygame.time.Clock()

# Create game objects
background = SpaceBackground(WIDTH, HEIGHT)  # Create the background
town_centre = TownCentre(WIDTH // 2, HEIGHT // 2)
ui = UI(WIDTH, HEIGHT, town_centre)  # Pass town_centre to UI
level_manager = LevelManager()

# Initialize units list
units = []

# Initialize spaceships list
spaceships = []

# Unit spawning variables
base_spawn_interval = 60  # Base frames between spawns

# TODO: Remove this line after testing
ui.resources = 10000  # Start with 200 resources for testing purposes

def main():
    # Create the intro screen
    intro_screen = IntroScreen(screen)

    # Run the intro screen
    intro_screen.run()

    # Initialize game variables
    spawn_timer = 0

    # Main game loop
    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            # Handle UI events
            action = ui.handle_event(event)
            if action:
                if action == "Upgrade Harvesting":
                    if ui.upgrade_harvesting():
                        print(f"Harvesting Upgraded - Level: {ui.harvesting_level}")
                        for unit in units:
                            unit.value += 1  # Increase the value of all existing units
                    # ... (other action handling)

                elif action == "Upgrade Laser":
                    if ui.resources >= 50:
                        ui.update_resources(-50)
                        town_centre.upgrade_laser()
                        print(f"Laser Upgraded - Level: {town_centre.laser_level}, Damage: {town_centre.laser_damage}, Frequency: {1000/town_centre.laser_cooldown:.2f} shots/second")
                    else:
                        print("Not enough resources to upgrade Laser")

                elif isinstance(action, tuple) and action[0] == "Place Bomb":
                    if ui.resources >= town_centre.bomb_cost:
                        ui.update_resources(-town_centre.bomb_cost)
                        town_centre.place_bomb(*action[1])
                        print(f"Bomb Placed - Cost: {town_centre.bomb_cost}")
                    else:
                        print("Not enough resources to place Bomb")

                elif action == "Upgrade Bomb":
                    if ui.resources >= 100:
                        ui.update_resources(-100)
                        town_centre.upgrade_bomb()
                        print(f"Bomb Upgraded - Level: {town_centre.bomb_upgrade_level}, Damage: {town_centre.bomb_damage_amount}, Radius: {town_centre.bomb_radius}")
                    else:
                        print("Not enough resources to upgrade Bomb")

                elif action == "Upgrade Health":
                    if ui.resources >= 100:
                        ui.update_resources(-100)
                        health_regen = town_centre.upgrade_health()
                        print(f"Health Upgraded - Max Health: {town_centre.max_health}, "
                              f"Current Health: {town_centre.health}, "
                              f"Health Regen: {health_regen} per 2 seconds")
                    else:
                        print("Not enough resources to upgrade Health")

                elif action.startswith("Cannot Afford"):
                    print(action)  # You might want to show this message to the player in the UI

                elif action == "Activate AntiGrav":
                    if ui.resources >= 50 and not town_centre.anti_grav_active:
                        ui.update_resources(-50)
                        town_centre.activate_anti_grav()
                        print("AntiGrav Activated")
                    elif town_centre.anti_grav_active:
                        print("AntiGrav is already active")
                    else:
                        print("Not enough resources to activate AntiGrav")

                elif action == "Upgrade AntiGrav":
                    if ui.resources >= 50 and town_centre.anti_grav_active:
                        ui.update_resources(-50)
                        town_centre.upgrade_anti_grav()
                        print(f"AntiGrav Upgraded - Level: {town_centre.anti_grav_level}, Slow: {town_centre.anti_grav_slow*100:.1f}%, Radius: {town_centre.anti_grav_radius}")
                    elif not town_centre.anti_grav_active:
                        print("AntiGrav needs to be activated first")
                    else:
                        print("Not enough resources to upgrade AntiGrav")

                elif action == "Spawn Spaceship":
                    if ui.resources >= 200:
                        ui.update_resources(-200)
                        spaceships.append(Spaceship(WIDTH, HEIGHT, town_centre))
                        print("Spaceship spawned")

                elif action == "Upgrade Spaceship":
                    if ui.resources >= 100 and spaceships:
                        ui.update_resources(-100)
                        for ship in spaceships:
                            ship.upgrade()
                        print("Spaceships upgraded")

        # Spawn new units
        spawn_timer += 1
        spawn_interval = level_manager.get_spawn_interval(base_spawn_interval)
        if spawn_timer >= spawn_interval:
            new_unit = spawn_random_unit(WIDTH, HEIGHT, town_centre)
            new_unit.speed = level_manager.get_unit_speed(new_unit.speed)
            units.append(new_unit)
            spawn_timer = 0

        # Update units
        for unit in units[:]:
            slow_factor = town_centre.apply_anti_grav(unit)
            unit.speed *= slow_factor  # Apply slow effect
            unit.update()
            unit.speed /= slow_factor  # Reset speed for next frame

        # Update spaceships
        for ship in spaceships:
            ship.update(units, current_time, spaceships)  # Pass the list of spaceships

        # Update game objects
        town_centre.update(units, current_time)
        defeated_units = 0
        for unit in units[:]:  # Use a copy of the list to safely remove items
            unit.update()
            if unit.collides_with(town_centre):
                town_centre.take_damage(unit.damage)
                ui.update_resources(unit.value)
                units.remove(unit)
                defeated_units += 1
            elif unit.health <= 0:
                ui.update_resources(unit.value)
                units.remove(unit)
                defeated_units += 1

        # Apply bomb damage if explosion is active
        if town_centre.explosion:
            town_centre.bomb_damage(units)

        # Update level manager
        level_manager.update(defeated_units)
        ui.update_level(level_manager.level)

        # Check game over condition
        if town_centre.health <= 0:
            running = False

        # Draw everything
        screen.fill((0, 0, 0))  # Clear the screen with black
        background.draw(screen)  # Draw the space background
        town_centre.draw(screen)
        for unit in units:
            unit.draw(screen)
        for ship in spaceships:
            ship.draw(screen, current_time)  # Pass current_time to draw method
        town_centre.draw_bomb_and_explosion(screen)  # Draw bomb and explosion on top of units
        ui.draw(screen)

        # Draw bomb cursor if placing
        if ui.placing_bomb:
            mouse_pos = pygame.mouse.get_pos()
            ui.draw_missile(screen, mouse_pos, 20, 128)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main()
