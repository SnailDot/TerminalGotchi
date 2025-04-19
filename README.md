# TerminalGotchi
A pyhton terminal based tamagotchi

This is a small python terminal based program that acts a virtual pet that you can leave running in the background. You can feed, play, clean, and put your pet to sleep by clicking a number between 1 through 7, and the program will also track how long the pet has been alive alongside the exact time it was made.

## Commands / Controls:
- Pressing any of these buttons will automatically do the command its attached to. There is also an in-game menu that displays these controls as well
  
1: Feed

2: Play

3: Sleep

4: Clean

5: Save

6: Exit

7: Show Pet's creation date

## STAGES:
- Each stage will last 30 minutes

1: Egg

2: Child

3: Teen

4: Adult

## How it works:
- If Either the Hunger, Clean, or Happy stat hits 0, the pet dies

- if the pet dies, it will delete the save file and close the game.

- Trying to load a save file with an dead pet will make the game delete that save file

- The Hunger, Clean, Happy, And Energy stat are always going down when its awake

- Sleeping will increase your Energy stat

- While Sleeping, the pet wont lose any happy or clean stat points, but it will lose hunger stat points

- When you play with your pet, it will lose a large chunk of its energy stat

- If the energy stat hits 0, the pet will be forced to sleep while it regains it energy
