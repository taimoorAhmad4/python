import random
import string

char_choices = string.ascii_letters
# char_choices = char_choices + "!@#$%^&*()1234567890{}:<>?[];',. /|\""
char_choices = char_choices + " "
random.seed(random.randint(10, 20))

generationarr = []
word = "big black fox"
word_arr = []
fitness = []
bestpop = []
newgen = []
child = []
newword = []
count = 0
goal = 0  # reach a fitness of 8
print("goal , ",goal)
currentfitness = 0
highestfitness = 0

# x = bin(ord(i))


def encode_word():
    x = 0b0000000
    for i in word:
        # x = ord(i)
        word_arr.append(i)


encode_word()
goal=len(word_arr)
print("initial word", word_arr)


def gen_words():
    for m in range(30):
        rand_letters = random.choices(char_choices, k=len(word_arr))  # where k is the number of required rand_letters
        generationarr.append(rand_letters)


def mutate():
    index = -1
    delta = 0
    for i in generationarr:

        while index == -1:
            index = random.randint(0, len(i)-1)
            if i[index] == word_arr[index]:
                index = -1

        delta = random.randint(-3, 3)
        c = random.choices(char_choices)

        i[index] = c[0]
        c = chr(ord(i[index]) + delta)

        if(c in char_choices):
            i[index] = c



def fitness_func(arr):
    total = 0

    for i, j in zip(arr, word_arr):
        if i == j:
            total = total + 1
    # fitness.append(total)
    return total


gen_words()

for generation_no in range(5000):
    generationarr.sort(key=fitness_func)
    generationarr.reverse()

    for i in generationarr:
        currentfitness = fitness_func(i)
        fitness.append(currentfitness)
        if currentfitness > highestfitness:
            highestfitness = currentfitness


    print("generation : ", generation_no)
    print(generationarr)
    print("fitness : ", fitness)
    if highestfitness == goal:
        break
    for i in range(6):
        bestpop.append(generationarr[i])

    for i in range(len(bestpop)):
        for j in range(len(bestpop)):
            if i != j:
                child = bestpop[i][0:5] + bestpop[j][5:]
                newgen.append(child)

    generationarr.clear()
    generationarr = newgen[:]

    mutate()

    newgen.clear()
    bestpop.clear()
    fitness.clear()
