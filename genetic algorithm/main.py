import random

# mainarr = [[1, 0, 1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0, 0, 1], [0, 0, 1, 1, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1, 0, 1],
#            [0, 0, 0, 1, 0, 1, 1, 1], [0, 1, 0, 0, 1, 0, 1, 1]]
mainarr = [[], [], [], [], [], []]
fitness = []
bestpop = []
newgen = []
child = []
count = 0
goal = 8  # reach a fitness of 8
currentfitness = 0
highestfitness = 0


def generate_starting_array():
    for i in range(len(mainarr)):
        for j in range(8):
            mainarr[i].append(random.randint(0, 1))


generate_starting_array()


def mutate():
    for thislist in mainarr:
        index = random.randint(0, 7)
        if thislist[index] == 0:
            thislist[index] = 1
        else:
            thislist[index] = 0


def fitness_func(arr):
    return sum(arr)


for gen in range(25):
    mainarr.sort(key=fitness_func)
    mainarr.reverse()

    for i in mainarr:
        currentfitness = fitness_func(i)
        fitness.append(currentfitness)
        if currentfitness > highestfitness:
            highestfitness = currentfitness

    print("generation : ", count)
    print(mainarr)
    print("fitness : ", fitness)
    if highestfitness == goal:
        break
    for i in range(3):
        bestpop.append(mainarr[i])

    for i in range(len(bestpop)):
        for j in range(len(bestpop)):
            if i != j:
                child = bestpop[i][0:4] + bestpop[j][4:]
                newgen.append(child)

    mainarr.clear()
    for i in newgen:
        mainarr.append(i)

    mutate()

    count = count + 1

    newgen.clear()
    bestpop.clear()
    fitness.clear()
