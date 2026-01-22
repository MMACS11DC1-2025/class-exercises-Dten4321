# Final Pygame Video Game Prioject: ~*Little Happanenings of Mizhou: Episode 0.5*~
## Description
A report of a stolen "device" has been sent to the village office of which the new mayor, Jiang must resolve.
## Instructions
The following section will explain how to play the game. **Bolded** words will be explained in the ***Mechanics*** Section
### Gameplay:
- Arrow keys to move
- Z key to confirm, advnace dialogue, or to **Shoot**
- X key to **Bomb**
- Shift to enter **Focus Mode**
- Esc to pause game

## Mechanics
The following section will explain core mechanics of the Game

#### Example Screenshot
![demoImage](imageDemo.png)
1. The Player
2. Numeber of **Lives**
3. Number of **Bombs**
4. The **Boss**
5. Some enemy Bullets
6. A **Bomb** item
7. Player bullets
8. Boss health
9. Points

### Resources
The two main resources of this game are **Lives** and **Bombs**

### Lives
The number of **Lives** the player has are shown at the bottom left of the screen as red hats. It determines how many times the player can get hit. The player gets hit after contacting a bullet (of any colour), a crate which has not been, a yinyang orb, or the boss. After being hit, the player will respawn at the starting position. The player may gain more lives by picking it up as an itemwith the same look as the icon of lives. Lives may only be dropped by yinyang orbs.

### Bombs
The number of **Bombs** the player has are shown at the bottom right of the screen as three intersecting spears. To use a bomb, press the X key. doing this will clear the screen of all enemies, all crates, and deal 300 damage to the boss.

### Shooting
Pressing the Z key will produce bullets from the player. These bullets will deal damage to crates, yinyang orbs, and bosses.

### Crates and Yinyang orbs
These are the only non-boss enemies in the game which may take damage from bullets. After being "killed," they drop **Items**. Crates only drop **Points** and **Bombs**, while yinyang orbs may drop points, bombs and lives.

### Bosses
Bosses are special characters that must be defeated to advance the story. They will cycle between a few different attacks until they are defeated.

# Development
## Changelog
### 01/22/2026
### V 0.4.1
- fixed bug where enemies did not clear after defeating a boss

### 01/21/2026
### V 0.4.0
- added Pause Screen

### 01/20/2026
### V 0.3.2
- added end screen
- game over screen properly restarts

### 01/19/2026
### V 0.3.1
- added backdrop for stage 3
- added title and game over screens
- new fonts

### 01/18/2026
### V 0.3.0
- Added Debug Mode
- Finished stage 1, stage 2
- finished boss behavior for stage 1 and stage 2
- added particles
- added background + paralax
- added theme for all stages
- added all dialogue "trees"
### 01/17/2026
### V 0.2.5
- Added Dialogue
- added more attacks and enlongated stage 1
- added lives and "bombs"
### 01/16/2026
### V 0.2.4
- Added shooter yinyangs
- added player bullet collision
### 01/15/2026
### V 0.2.3
- Made Yinyang orbs larger and red
- Added stage music
### 01/14/2026
### V 0.2.2
- Added yinyang orbs
### V 0.2.1
- Implemented Stage
### V 0.2.0
- Implemented Boss movement
### 01/11/2026
### V 0.1.1
- Added Collision when touching boss or enemy and menu music
### 01/09/2026
### V 0.1.0
- Changed classes to use pygame.sprite Class for easier work (In progress)
### V 0.0.5
- Added Menu
### 01/08/2026
### V 0.0.4
- Added Boss Movements and another attack type
### 01/07/2026
### V 0.0.3
- Added Boss Bullets
### 01/06/2026
### V 0.0.2
- Focus mode flair is transparent
- Player Bullets are transparent
- Level 2 boss sprite added
- Placeholder music added
### V 0.0.1
- Focus Mode added
- Bullets can be shot by the player
### V 0.0.0 
- Player sprite made
- Basic movement added