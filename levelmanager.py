class LevelManager:
    def __init__(self):
        self.level = 1
        self.spawn_rate_multiplier = 1.0
        self.speed_multiplier = 0.5  # Start at 50% speed
        self.xp = 0
        self.xp_to_next_level = 100

    def update(self, defeated_units):
        self.xp += defeated_units
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.2)  # Increase XP required for next level
        self.spawn_rate_multiplier *= 1.05  # Increase spawn rate by 5%
        self.speed_multiplier = min(1.0, self.speed_multiplier + 0.05)  # Increase speed by 5%, max 100%
        print(f"Level Up! Level: {self.level}, Speed: {self.speed_multiplier*100:.0f}%, Spawn Rate: {self.spawn_rate_multiplier:.2f}")

    def get_spawn_interval(self, base_interval):
        return max(int(base_interval / self.spawn_rate_multiplier), 1)

    def get_unit_speed(self, base_speed):
        return base_speed * self.speed_multiplier
