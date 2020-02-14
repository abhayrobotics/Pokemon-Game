import pygame
import sys
import random
import math
from pygame import mixer
import time

#  initialse the pygame
pygame.init()

# TITLE AND LOGO
pygame.display.set_caption("Pokemon")
icon = pygame.image.load('sprites/icon.png')
pygame.display.set_icon(icon)

# Global variables
SCREENWIDTH = 850
SCREENHEIGHT = 520
GROUNDY = 0.87 * SCREENHEIGHT
CHARACTER_IN_CONTROL = "player"  # default case

# create the Screen
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# Background
backgroundImg = pygame.image.load('sprites/background2.png')

# trees

treeX_change = 0

tree1 = pygame.image.load('sprites/tree1.png')
tree2 = pygame.image.load('sprites/tree2.png')
tree3 = pygame.image.load('sprites/tree3.png')
# tree4 = pygame.image.load('sprites/tree4.png')
tree5 = pygame.image.load('sprites/tree5.png')
all_trees = [tree1, tree2, tree3, tree5]
tree_list = []
treeX = [400, 400 + random.randint(150, 400), 800 + random.randint(150, 400)]

# Player
playerImg = pygame.image.load('sprites/player.png')
playerX = 100
playerY = GROUNDY - playerImg.get_height()
playerY_min = GROUNDY - playerImg.get_height()
playerX_change = 0
playerY_change = 0
playerY_max = GROUNDY - playerImg.get_height() - 130
player_jumping_status = False
player_jumping_dir = 0

# pokeball
pokeballImg = pygame.image.load('sprites/pokeball.png')
pokeballX = 100
pokeballY = GROUNDY - pokeballImg.get_height() - 100
pokeballX_change = 0
pokeballY_change = 0
pokeball_status = "ready"

# POKEMON
bulbasaurImg = pygame.image.load('sprites/bulbasaur.png')
bulbasaurX = 200
bulbasaurY = GROUNDY - bulbasaurImg.get_height()
bulbasaurY_min = GROUNDY - bulbasaurImg.get_height()
bulbasaurY_change = 0
bulbasaurY_max = GROUNDY - bulbasaurImg.get_height() - 100
bulbasaur_jumping_status = False
bulbasaur_jumping_dir = 0

# Boss enemy
squirtelV3Img = pygame.image.load('sprites/squirtelV3.png')
squirtelV3X = 600
squirtelV3Y = GROUNDY - squirtelV3Img.get_height()


class Jump():
    # this class provides jumping technique to any character
    GROUNDY = 0.87 * SCREENHEIGHT

    def __init__(self, characterImg, characterX, characterY, characterY_change, characterY_max, jumping_status,
                 jumping_dir):
        self.characterImg = characterImg
        self.characterX = characterX
        self.characterY_change = characterY_change
        self.characterY = characterY
        self.characterY_max = characterY_max
        self.jumping_status = jumping_status
        self.jumping_dir = jumping_dir

    def jumpTechnique(self):
        # print("class ", self.jumping_status)

        self.characterY_change = 0
        # print(self.characterY, self.characterY_max)
        if self.jumping_status:
            if (GROUNDY - self.characterImg.get_height() + 15 >= self.characterY >= self.characterY_max) \
                    and self.jumping_dir == "up":
                # 15 px above is safety factor( must not be removed)
                # print("up")
                self.characterY_change = -5
            if self.characterY <= self.characterY_max and self.jumping_dir == "up":
                # print("direction change")
                self.jumping_dir = "down"
                self.characterY_change = +5
            if (GROUNDY - self.characterImg.get_height() >= self.characterY >= self.characterY_max) \
                    and self.jumping_dir == "down":
                # print("down")
                self.characterY_change = +5
            if self.characterY > GROUNDY - self.characterImg.get_height() and self.jumping_dir == "down":
                self.characterY_change = 0
                self.characterY = GROUNDY - self.characterImg.get_height()  # reset self.characterY position
                self.jumping_status = False

        return self.characterY_change, self.jumping_dir, self.jumping_status


# Blitting Functions
def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


def pokeball(x, y):
    screen.blit(pokeballImg, (x, y))


def bulbasaur(x, y):
    screen.blit(bulbasaurImg, (x, y))


def squirtelV3(x, y):
    screen.blit(squirtelV3Img, (x, y))


def tree_blit(chosen_tree, x, y):
    # blit a tree
    screen.blit(chosen_tree, (x, y))


# logical Functions

def randomtree():
    # choose a random tree
    return random.choice(all_trees)


if __name__ == '__main__':

    # Generate 3  random Trees
    no_of_trees = 1
    while no_of_trees <= 3:
        tree_list.append(randomtree())
        no_of_trees += 1

    running = True
    # main loop
    while running:
        # print(running)
        # RGB value
        screen.fill((0, 0, 0))

        # background img
        screen.blit(backgroundImg, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    treeX_change = -2
                    print("Right")
                if event.key == pygame.K_LEFT:
                    treeX_change = +2
                    print("Left")

                if event.key == pygame.K_b and player_jumping_status == False:
                    CHARACTER_IN_CONTROL = "bulbasaur"
                if event.key == pygame.K_p and bulbasaur_jumping_status == False:
                    CHARACTER_IN_CONTROL = "player"

                if event.key == pygame.K_SPACE:

                    # SHOOT event depending on CHARACTER_IN_CONTROL
                    if CHARACTER_IN_CONTROL == "player":
                        pokeballX = playerX + 30
                        pokeballY = playerY + 30
                        pokeballX_change = 6
                        print("Player Shoot")
                        pokeball_status = "fire"
                    if CHARACTER_IN_CONTROL == "bulbasaur":
                        pass

                if event.key == pygame.K_UP:
                    # Jump event depending on CHARACTER_IN_CONTROL

                    # Jumping event player
                    if bulbasaur_jumping_status == False and CHARACTER_IN_CONTROL == "player":
                        print("Player JUMP")
                        player_jumping_status = True
                    # print(f"jumping_status is{jumping_status}")
                    player_jumping_dir = "up"

                    # Jumping event Bulbasaur
                    if player_jumping_status == False and CHARACTER_IN_CONTROL == "bulbasaur":
                        print("Bulbasaur JUMP")
                        bulbasaur_jumping_status = True
                    # print(f"jumping_status is{jumping_status}")
                    bulbasaur_jumping_dir = "up"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    # tree will move only when player moves
                    treeX_change = 0
                if event.key == pygame.K_LEFT:
                    # tree will move only when player moves
                    treeX_change = 0

        # tree generator
        # incrementing x coordinate and then  using x to put in randam tree generator
        # ( random in choosing tree + random in distance between tree) two list simultaneously --zip
        for tree_X_coordinate, k in zip(treeX, tree_list):
            a = treeX.index(tree_X_coordinate)  # finding index a
            # print(a)
            tree_X_coordinate += treeX_change
            treeX[a] = tree_X_coordinate  # changing the incremented x
            # print(k, tree_X_coordinate, 200)
            tree_blit(k, tree_X_coordinate, 200)

        # if tree exists from window , spawning new random tree
        if treeX[0] + tree_list[0].get_width() < -200:
            # swapping tree and x position ( deleting tree with index 0 and adding a new tree)
            treeX[0], treeX[1] = treeX[1], treeX[2]
            tree_list[0], tree_list[1] = tree_list[1], tree_list[2]
            tree_list[2] = randomtree()
            treeX[2] = 900 + random.randint(100, 400)

        # player jump
        if CHARACTER_IN_CONTROL == "player":
            player_jump = Jump(playerImg, playerX, playerY, playerY_change, playerY_max, player_jumping_status,
                               player_jumping_dir)
            playerY_change, player_jumping_dir, player_jumping_status = player_jump.jumpTechnique()

        # bulbasaur jump
        if CHARACTER_IN_CONTROL == "bulbasaur":
            bulbasaur_jump = Jump(bulbasaurImg, bulbasaurX, bulbasaurY, bulbasaurY_change, bulbasaurY_max,
                                  bulbasaur_jumping_status, bulbasaur_jumping_dir)
            bulbasaurY_change, bulbasaur_jumping_dir, bulbasaur_jumping_status = bulbasaur_jump.jumpTechnique()

        # blitting  pokeball when shoot
        if pokeball_status == "fire":
            # print(pokeballX,pokeballY)
            screen.blit(pokeballImg, (pokeballX, pokeballY))

        # player Movement
        playerY += playerY_change
        player(playerX, playerY)

        # bulbasaur Movement
        bulbasaurY += bulbasaurY_change
        # bulbasaur(bulbasaurX, bulbasaurY)

        # pokeball Movement
        pokeballX += pokeballX_change

        # enemy
        squirtelV3(squirtelV3X, squirtelV3Y)
        pygame.display.update()
