import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import math

n_options = random.randint(4,8)
# n_options = 7
n_sqrd = n_options * n_options

generationarr = []
this_list = []
fitness = []
bestpop = []
newgen = []
goal = 0


def mutate():
    index = -1
    delta = -2
    for i in generationarr:
        index = random.randint(0, len(i) - 1)
        delta = random.randint(0, n_options-1)
        i[index] = delta


def gen_initial_positions():
    for l in range(6):
        for m in range(n_options):
            pos = random.randint(0, n_options - 1)
            this_list.append(pos)
        generationarr.append(this_list[:])
        this_list.clear()


gen_initial_positions()
print(generationarr)


def fitness_func(arr):
    total = 0  # smaller total means better fitness

    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j:  # check not same coloumn (not possible in our implementation anyway)
                if arr[i] == arr[j]:  # check row
                    total += 1
                else:  # check diagnol
                    if abs(arr[j] - arr[i]) == abs(j - i):
                        total += 1
    total = total / 2
    return total


for generation_no in range(5000):
    generationarr.sort(key=fitness_func)

    for i in generationarr:
        fitness.append(fitness_func(i))
    print("generation : ", generation_no)
    print(generationarr)
    print("fitness : ", fitness)
    if fitness[0] == goal:
        break

    for i in range(3):
        bestpop.append(generationarr[i])

    for i in range(len(bestpop)):
        for j in range(len(bestpop)):
            if i != j:
                child = bestpop[i][0:math.floor(n_options / 2)] + bestpop[j][math.floor(n_options / 2):]
                # print("child : ",child)
                newgen.append(child)

    generationarr.clear()
    generationarr = newgen[:]

    mutate()

    newgen.clear()
    bestpop.clear()
    fitness.clear()
plt.title("N Queen Solution")
plt.scatter(range(len(generationarr[0])), generationarr[0])
plt.grid()
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))

plt.show()
