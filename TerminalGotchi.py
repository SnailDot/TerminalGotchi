import time
import random
import os
import json
from datetime import datetime, timedelta

class TerminalGotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.age = 0
        self.creation_time = datetime.now()  # Store creation time
        self.last_update = datetime.now()
        self.evolution_stage = "egg"
        self.evolution_timer = 0
        self.is_sleeping = False
        self.was_forced_sleep = False
        self.cleanliness = 100
        self.current_pose = 0
        self.position_x = 40
        self.position_y = 10
        self.movement_direction_x = 1
        self.movement_direction_y = 1
        self.screen_width = 80
        self.screen_height = 24
        self.last_screen = None
        self.last_move_time = datetime.now()
        self.last_pose_change = datetime.now()

    def to_dict(self):
        return {
            'name': self.name,
            'hunger': self.hunger,
            'happiness': self.happiness,
            'energy': self.energy,
            'age': self.age,
            'creation_time': self.creation_time.isoformat(),
            'last_update': self.last_update.isoformat(),
            'evolution_stage': self.evolution_stage,
            'evolution_timer': self.evolution_timer,
            'is_sleeping': self.is_sleeping,
            'was_forced_sleep': self.was_forced_sleep,
            'cleanliness': self.cleanliness,
            'current_pose': self.current_pose,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'movement_direction_x': self.movement_direction_x,
            'movement_direction_y': self.movement_direction_y
        }

    @classmethod
    def from_dict(cls, data):
        terminalgotchi = cls(data['name'])
        terminalgotchi.hunger = data['hunger']
        terminalgotchi.happiness = data['happiness']
        terminalgotchi.energy = data['energy']
        terminalgotchi.age = data['age']
        terminalgotchi.creation_time = datetime.fromisoformat(data['creation_time'])
        terminalgotchi.last_update = datetime.fromisoformat(data['last_update'])
        terminalgotchi.evolution_stage = data['evolution_stage']
        terminalgotchi.evolution_timer = data['evolution_timer']
        terminalgotchi.is_sleeping = data['is_sleeping']
        terminalgotchi.was_forced_sleep = data['was_forced_sleep']
        terminalgotchi.cleanliness = data['cleanliness']
        terminalgotchi.current_pose = data['current_pose']
        terminalgotchi.position_x = data['position_x']
        terminalgotchi.position_y = data['position_y']
        terminalgotchi.movement_direction_x = data['movement_direction_x']
        terminalgotchi.movement_direction_y = data['movement_direction_y']
        return terminalgotchi

    def save(self):
        try:
            with open('terminalgotchi_save.json', 'w') as f:
                json.dump(self.to_dict(), f)
            return "Game saved successfully!"
        except Exception as e:
            return f"Error saving game: {e}"

    def update_stats(self):
        current_time = datetime.now()
        time_diff = (current_time - self.last_update).total_seconds() / 60
        
        # Update age based on time since creation
        self.age = int((current_time - self.creation_time).total_seconds() / 60)
        
        # Force sleep if energy is too low
        if self.energy <= 5 and not self.is_sleeping:
            self.is_sleeping = True
            self.was_forced_sleep = True
            print(f"\n{self.name} is too tired and fell asleep!")
        
        # Hunger decreases whether sleeping or not
        self.hunger = max(0, self.hunger - time_diff * (1 if self.is_sleeping else 2))
        
        if not self.is_sleeping:
            self.happiness = max(0, self.happiness - time_diff)
            self.energy = max(0, self.energy - time_diff)
            self.cleanliness = max(0, self.cleanliness - time_diff)
            
            # Cleanliness affects happiness
            if self.cleanliness < 50:
                self.happiness = max(0, self.happiness - time_diff * 0.5)
            
            # Check for death conditions
            if self.hunger <= 0:
                return True
            if self.happiness <= 0:
                return True
            if self.cleanliness <= 0:
                return True
            
            self.evolution_timer += time_diff
            if self.evolution_timer >= 30:
                if self.evolution_stage == "egg":
                    self.evolution_stage = "baby"
                elif self.evolution_stage == "baby":
                    self.evolution_stage = "child"
                elif self.evolution_stage == "child":
                    self.evolution_stage = "teen"
                elif self.evolution_stage == "teen":
                    self.evolution_stage = "adult"
                self.evolution_timer = 0
        else:
            # Recover energy while sleeping
            self.energy = min(100, self.energy + time_diff * 5)
            # Wake up if energy is restored to 1 and was forced to sleep
            if self.energy >= 1 and self.is_sleeping and self.was_forced_sleep:
                self.is_sleeping = False
                self.was_forced_sleep = False
                print(f"\n{self.name} woke up feeling better!")
        
        self.last_update = current_time
        return False

    def move(self):
        current_time = datetime.now()
        if not self.is_sleeping:
            # Only move every 0.5 seconds
            if (current_time - self.last_move_time).total_seconds() >= 0.5:
                self.position_x += self.movement_direction_x
                self.position_y += self.movement_direction_y
                self.last_move_time = current_time
                
                if self.position_x >= self.screen_width - 20:
                    self.movement_direction_x = -1
                elif self.position_x <= 40:
                    self.movement_direction_x = 1
                
                if self.position_y >= self.screen_height - 10:
                    self.movement_direction_y = -1
                elif self.position_y <= 0:
                    self.movement_direction_y = 1
            
            # Only change pose every 2 seconds
            if (current_time - self.last_pose_change).total_seconds() >= 2:
                self.current_pose = (self.current_pose + 1) % 2
                self.last_pose_change = current_time

    def get_ascii_art(self):
        poses = {
            "egg": [
                """
    ██████
  ██      ██
██          ██
██          ██
  ██      ██
    ██████""",
                """
    ██████
  ██      ██
██    ██    ██
██    ██    ██
  ██      ██
    ██████"""
            ],
            "baby": [
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
      ██
      ██""",
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
    ██  ██
      ██"""
            ],
            "child": [
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
      ██
    ██  ██""",
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
    ██  ██
      ██"""
            ],
            "teen": [
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
      ██
    ██  ██
   ██    ██""",
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
    ██  ██
      ██
   ██    ██"""
            ],
            "adult": [
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
      ██
    ██  ██
   ██    ██
  ██      ██""",
                """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
    ██  ██
      ██
   ██    ██
  ██      ██"""
            ]
        }

        if self.is_sleeping:
            return """
    ██████
  ██      ██
██          ██
██    ██    ██
  ██      ██
    ██████
      ██
    ██  ██
   ██    ██
  ██      ██"""

        stage_poses = poses.get(self.evolution_stage, poses["adult"])
        return stage_poses[self.current_pose]

    def get_status(self):
        is_dead = self.update_stats()
        self.move()
        
        # Create screen buffer
        screen = [[' ' for _ in range(self.screen_width)] for _ in range(self.screen_height)]
        
        # Add status
        status = f"""
{self.name}'s Status:
Hunger: {'█' * int(self.hunger // 10)}{'░' * int(10 - self.hunger // 10)} {self.hunger}%
Happiness: {'█' * int(self.happiness // 10)}{'░' * int(10 - self.happiness // 10)} {self.happiness}%
Energy: {'█' * int(self.energy // 10)}{'░' * int(10 - self.energy // 10)} {self.energy}%
Cleanliness: {'█' * int(self.cleanliness // 10)}{'░' * int(10 - self.cleanliness // 10)} {self.cleanliness}%
Age: {self.age} minutes
Stage: {self.evolution_stage.capitalize()}
Status: {'Sleeping' if self.is_sleeping else 'Awake'}""".split('\n')

        for i, line in enumerate(status):
            if i < len(screen):
                for j, char in enumerate(line):
                    if j < len(screen[i]):
                        screen[i][j] = char

        # Add TerminalGotchi
        ascii_art = self.get_ascii_art()
        ascii_lines = ascii_art.strip().split('\n')
        
        for i, line in enumerate(ascii_lines):
            y = self.position_y + i
            if 0 <= y < self.screen_height:
                for j, char in enumerate(line):
                    x = self.position_x + j
                    if 0 <= x < self.screen_width:
                        screen[y][x] = char

        # Add menu
        menu_y = len(status) + 1
        if menu_y < self.screen_height:
            menu = [
                "What would you like to do?",
                "1. Feed",
                "2. Play",
                "3. Sleep/Wake",
                "4. Clean",
                "5. Save",
                "6. Exit",
                "7. Get Creation Time"
            ]
            for i, line in enumerate(menu):
                y = menu_y + i
                if y < self.screen_height:
                    for j, char in enumerate(line):
                        if j < len(screen[y]):
                            screen[y][j] = char

        # Convert screen to string with ANSI codes
        screen_str = '\033[H'  # Move cursor to home position
        for row in screen:
            screen_str += ''.join(row) + '\n'
        
        # Only update if screen has changed
        if screen_str != self.last_screen:
            self.last_screen = screen_str
            return screen_str, is_dead
        return None, is_dead

    def feed(self):
        if not self.is_sleeping:
            self.hunger = min(100, self.hunger + 30)
            self.energy = min(100, self.energy + 10)
            return f"{self.name} enjoyed the meal!"
        return f"{self.name} is sleeping! "

    def play(self):
        if self.is_sleeping:
            return f"{self.name} is sleeping! "
        if self.energy <= 0:
            return f"{self.name} is too tired to play! "
        self.happiness = min(100, self.happiness + 30)
        self.energy = max(0, self.energy - 20)
        return f"{self.name} had fun playing!"

    def sleep(self):
        self.is_sleeping = not self.is_sleeping
        if not self.is_sleeping:
            self.was_forced_sleep = False
        return f"{self.name} {'went to sleep!' if self.is_sleeping else 'woke up!'}"

    def clean(self):
        if not self.is_sleeping:
            self.cleanliness = 100
            return f"{self.name} is now clean!"
        return f"{self.name} is sleeping! "

    def get_creation_time(self):
        return self.creation_time.strftime("%B %d, %Y at %I:%M %p")

def load_saved_game():
    try:
        if not os.path.exists('terminalgotchi_save.json'):
            return None, "No saved game found."
        
        with open('terminalgotchi_save.json', 'r') as f:
            data = json.load(f)
        
        # Check if the pet would be dead in the loaded state
        if data['hunger'] <= 0 or data['happiness'] <= 0 or data['cleanliness'] <= 0:
            os.remove('terminalgotchi_save.json')
            return None, "Your TerminalGotchi has passed away. Starting a new game..."
        
        return TerminalGotchi.from_dict(data), "Game loaded successfully!"
    except Exception as e:
        if os.path.exists('terminalgotchi_save.json'):
            os.remove('terminalgotchi_save.json')
        return None, f"Error loading game: {e}"

def main():
    try:
        # Enable ANSI escape codes on Windows
        if os.name == 'nt':
            os.system('')
        
        # Set text color to green
        print('\033[32m', end='')  # Green text
        
        print("Welcome to TerminalGotchi!")
        print("\nWhat would you like to do?")
        print("1. Load saved TerminalGotchi")
        print("2. Create new TerminalGotchi")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            pet, message = load_saved_game()
            if pet is None:
                print(message)
                choice = "2"  # Force new game creation
            else:
                print(message)
        
        if choice == "2":
            name = input("What would you like to name your TerminalGotchi? ").strip()
            if not name:
                name = "TerminalGotchi"
            pet = TerminalGotchi(name)
        
        # Clear screen and hide cursor
        print('\033[?25l', end='')  # Hide cursor
        print('\033[2J', end='')    # Clear screen
        
        last_message = ""
        while True:
            try:
                # Get screen update
                screen, is_dead = pet.get_status()
                if screen:
                    print(screen, end='', flush=True)
                
                if is_dead:
                    print(f"\nOh no! {pet.name} has passed away...")
                    if os.path.exists('terminalgotchi_save.json'):
                        os.remove('terminalgotchi_save.json')
                    break
                
                # Check for input without blocking
                import msvcrt
                if msvcrt.kbhit():
                    choice = msvcrt.getch().decode('utf-8')
                    if choice == "1":
                        last_message = pet.feed()
                        print("\n" + last_message + " " * 20)
                    elif choice == "2":
                        last_message = pet.play()
                        print("\n" + last_message + " " * 20)
                    elif choice == "3":
                        last_message = pet.sleep()
                        print("\n" + last_message + " " * 20)
                    elif choice == "4":
                        last_message = pet.clean()
                        print("\n" + last_message + " " * 20)
                    elif choice == "5":
                        last_message = pet.save()
                        print("\n" + last_message + " " * 20)
                    elif choice == "6":
                        print(f"\nGoodbye! Thanks for taking care of {pet.name}!")
                        break
                    elif choice == "7":
                        last_message = f"{pet.name} was created on {pet.get_creation_time()}"
                        print("\n" + last_message + " " * 20)
                
                time.sleep(0.05)
                
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                time.sleep(2)
                
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")
    finally:
        # Show cursor and reset terminal
        print('\033[?25h', end='')  # Show cursor
        print('\033[0m', end='')    # Reset terminal (this also resets the color)

if __name__ == "__main__":
    main() 