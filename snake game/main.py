# https://github.com/python-engineer/python-fun/tree/master/snake-pygame
# I made a few changes to Patrick Loeber's code from the above git repository
import pygame
import time
import random
from enum import Enum
from collections import namedtuple

# Constants
BLOCK_SIZE = 20
# SPEED = 10
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN1 = (72, 161, 77)
GREEN2 = (11, 102, 35)
BLACK = (0, 0, 0)
foodImg = pygame.image.load('apple.png')

headImg = pygame.image.load('shead5.png')
headImg = pygame.transform.rotate(headImg, 90)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)


font = pygame.font.SysFont('arial', 25)


class snakegame:

    def __init__(self, w=640, h=480, SPEED = 10):
        self.w = w
        self.h = h
        self.SPEED = SPEED

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))  # set dimensions of the window
        pygame.display.set_caption('Snake')  # window name
        self.clock = pygame.time.Clock()
        # init game state
        self.direction = Direction.RIGHT  # initial direction of movement
        self.head = Point(self.w / 2, self.h / 2)  # initial position of head

        # initially the snake has 3 blocks so snake is a list that has locations of these three blocks
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()



    def intro_game(self):

        intro = True

        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] >= self.w / 3 and mouse[0] <= (self.w / 3) + 50 and  mouse[1] >= (self.h / 1.85) and mouse[1] <= (self.h / 1.85)+20:
                        return True
                    if mouse[0] >= self.w / 3 and mouse[0] <= (self.w / 3) + 50 and  mouse[1] >= (self.h / 1.65) and mouse[1] <= (self.h / 1.65)+20:
                        return False


            self.display.fill(WHITE)
            text = font.render("Sssssssssnakeeeeeee", True, GREEN1)
            self.display.blit(text, [(self.w / 3), (self.h / 2)])
            text2 = font.render("Play", True, GREEN2)
            self.display.blit(text2, [(self.w / 3), (self.h / 1.85)])
            text3 = font.render("Quit", True, GREEN2)
            self.display.blit(text3, [(self.w / 3), (self.h / 1.65)])

            pygame.display.update()
            self.clock.tick(15)

    def _place_food(self):  # randomly generate food positions
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:  # if food generated where snake exists, generate location again
            self._place_food()

    def updateUI(self):
        self.display.fill(WHITE)


        for point in self.snake:  # draw a block at every location in snake list
            if point == self.snake[0]:
                self.display.blit(headImg, (point.x, point.y))
            else:
                pygame.draw.circle(self.display, GREEN1, (point.x+10, point.y+10), BLOCK_SIZE/2)
                pygame.draw.circle(self.display, GREEN2, (point.x+10, point.y+10 ), BLOCK_SIZE/3)
        # pygame.draw.rect(self.display, RED, pygame.image(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        self.display.blit(foodImg, (self.food.x, self.food.y))
        text = font.render("Score : " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])  # 0,0 is the position of the text
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        # print("snakeeee : ",len(self.snake))
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)

    def _iscollision(self):
        # hits boundry
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def play_step(self):
        # collect user input
        global headImg
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction == Direction.UP:
                        headImg2 = pygame.transform.rotate(headImg, 90)
                        headImg=headImg2
                    elif self.direction == Direction.DOWN:
                        headImg2 = pygame.transform.rotate(headImg, -90)
                        headImg = headImg2
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction == Direction.UP:
                        headImg2 = pygame.transform.rotate(headImg, -90)
                        headImg = headImg2
                    elif self.direction == Direction.DOWN:
                        headImg2 = pygame.transform.rotate(headImg, 90)
                        headImg = headImg2

                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    if self.direction == Direction.RIGHT:
                        headImg2 = pygame.transform.rotate(headImg, 90)
                        headImg = headImg2
                    elif self.direction == Direction.LEFT:
                        headImg2 = pygame.transform.rotate(headImg, -90)
                        headImg = headImg2
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction == Direction.RIGHT:
                        headImg2 = pygame.transform.rotate(headImg, -90)
                        headImg = headImg2
                    elif self.direction == Direction.LEFT:
                        headImg2 = pygame.transform.rotate(headImg, 90)
                        headImg = headImg2
                    self.direction = Direction.DOWN
        # move
        self._move(self.direction)
        self.snake.insert(0, self.head)
        # check if game over
        game_over = False
        if self._iscollision():
            game_over = True
            return game_over, self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            self.SPEED += 1
            self._place_food()
        else:
            self.snake.pop()
        # update ui and clock
        self.updateUI()
        self.clock.tick(self.SPEED)
        # return game over and score
        game_over = False
        return game_over, self.score





def main():
    game = snakegame()

    # loop
    play = game.intro_game()
    if play == False:
        pygame.quit()
        quit()

    while True:

        game_over, score = game.play_step()


        if game_over == True:
            play = game.intro_game()
            if play == False:
                pygame.quit()
                quit()
            else:
                main()


if __name__ == '__main__':
    main()
