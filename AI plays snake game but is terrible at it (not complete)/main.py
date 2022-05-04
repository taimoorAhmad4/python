# https://github.com/python-engineer/python-fun/tree/master/snake-pygame
# https://github.com/Bbowen100/SnakeGame
# I used the above repositories to create this code.
import pygame
import time
import random
from enum import Enum
from collections import namedtuple
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Sequential
from nn import get_model
import math as m
import numpy as np

# Constants
BLOCK_SIZE = 20
# SPEED = 10
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN1 = (72, 161, 77)
GREEN2 = (11, 102, 35)
BLACK = (0, 0, 0)
foodImg = pygame.image.load('apple.png')
i = 0
model = get_model()


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

    def __init__(self, w=640, h=480, SPEED=10):
        self.w = w
        self.h = h
        self.SPEED = SPEED
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.experience = []
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def collectExperience(self, experience):
        self.experience.append(experience)
        return self.experience

    def getState(self):
        return [self.head.x, self.head.y, self.food.x, self.food.y]

    def distance(self, state):
        snake_x = state[0]
        snake_y = state[1]
        apple_x = state[2]
        apple_y = state[3]
        d = m.sqrt(m.pow((apple_x - snake_x), 2) + m.pow((apple_y - snake_y), 2))
        return d

    def getreward(self, oldState,newState):

        # -500 for restarting the game
        if (self.iscollision()):
            return -500
        # reward +10 if snake is closer to apple, -10 if snake is farther
        # and +100 if the snake gets the apple
        oldDistance = self.distance(oldState)
        newDistance = self.distance(newState)
        if (oldDistance > newDistance):
            if (newDistance == 0):
                return 1000
            else:
                return 10
        elif (oldDistance < newDistance):
            return -100
        else:
            return 0  # same spot: Unlikely but for debugging purposes


    def _place_food(self):  # randomly generate food positions
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:  # if food generated where snake exists, generate location again
            self._place_food()

    def updateUI(self):
        self.display.fill(WHITE)

        for point in self.snake:  # draw a block at every location in snake list
            pygame.draw.circle(self.display, GREEN1, (point.x + 10, point.y + 10), BLOCK_SIZE / 2)
            pygame.draw.circle(self.display, GREEN2, (point.x + 10, point.y + 10), BLOCK_SIZE / 3)
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

    def iscollision(self):
        # hits boundry
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def play_step(self, action):
        # collect user input
        global reward
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if action == 2 and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif action == 1 and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif action == 3 and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif action == 4 and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        # move

        self._move(self.direction)
        self.snake.insert(0, self.head)
        # check if game over
        reward = 0
        game_over = False
        if self.iscollision() or self.frame_iteration > 1000 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score, self.getState()

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        # update ui and clock
        self.updateUI()
        self.clock.tick(self.SPEED)
        # return game over and score
        game_over = False
        return reward, game_over, self.score, self.getState()


total_reward = 0


def main():
    global total_reward
    game = snakegame()
    epsilon = 1
    batch_size = 10
    frame = 0
    # loop

    while True:

        # predict
        if (epsilon > 0.1):
            epsilon -= (0.9 / 10)

            # decide which direction the snake will go
        if (random.random() < epsilon):
            action = random.choice([1, 2, 3, 4])  # take a random direction
        else:
            # get action prediction from the model
            state = np.array(game.getState())
            prediction = model.predict(np.array([state])).flatten().tolist()
            # print(prediction)
            action = prediction.index(max(prediction))
            frame += 1
        # action = predict()
        oldstate = game.getState()
        _, game_over, score, newstate = game.play_step(action)
        reward= game.getreward(oldstate, newstate)

        predOutput = model.predict(np.array([newstate])).flatten().tolist()
        # predOutput[action] = reward
        experience = [newstate, reward]
        getexperience = game.collectExperience(experience)  # record experience

        if (frame == batch_size):
            # get training set from experience
            Xtrain = []
            Ytrain = []
            loss = 0
            for ele in getexperience:
                Xtrain.append(ele[0])
                Ytrain.append(ele[1])

            loss = model.fit(np.array(Xtrain), np.array(Ytrain),
                             batch_size=batch_size, epochs=10)
            # reset frames and expereince
            frame = 0
            experience = []
            getexperience = []
        # train

        # model.train
        total_reward += reward
        # print("total reward : ", total_reward, " : ", act)
        if game_over:
            total_reward = 0
            main()


if __name__ == '__main__':
    main()
