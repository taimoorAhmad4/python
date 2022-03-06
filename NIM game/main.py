import math

dic = {}
initial_mytuple = [7]
queue = []
mytuple = []
count = 0
all_mytuples = []
dic_traversal_queue = []

initialTurn = True
gameQueue = []
previousMove = initial_mytuple
minWon = False
minTurn = True
gameEnd = False


class MoveInfo:
    moveWeight = 0
    minWinsWithThisMove = False
    moveItself = []


def get_combos(num, count, imytuple_copy_recieve):
    mytuple.clear()
    copy_recieved = []
    sortme = ()

    for u in range(num - 1, math.floor(num / 2), -1):
        for v in range(1, math.ceil(num / 2)):
            if (u + v) == num and u != v:
                for m in imytuple_copy_recieve:
                    copy_recieved.append(m)

                count = count + 1

                copy_recieved.append(u)
                copy_recieved.append(v)

                y = tuple(copy_recieved)
                copy_recieved.clear()
                sortme = sorted(y, reverse=True)
                y = sortme

                mytuple.append(y)

    return (mytuple)


def find_mytuple_combos(imytuple, count):
    global all_mytuples
    j = ()
    # print("imytuple", imytuple)
    imytuple_copy = []
    for i in imytuple:

        # imytuple_copy.remove(i)
        if i != 0:  # if not initital node ka zero
            if i == 1:
                break
            elif i == 2:
                break
            else:
                for m in imytuple:
                    imytuple_copy.append(m)

                imytuple_copy.remove(i)

                all_mytuples = get_combos(i, count, imytuple_copy)
                j = j + tuple(all_mytuples)
                imytuple_copy.clear()
        else:
            imytuple.remove(0)

    k = list(j)

    # print("key : ", imytuple, " value : " , j)
    dic[str(imytuple)] = j

    while len(k) != 0:
        node = k.pop()
        queue.append(node)
        # print("node",node)


def traverseQueue(count):
    while len(queue) != 0:
        # print(len(queue), "     ", queue)
        node = queue.pop(0)
        find_mytuple_combos(node, count)


# /////////////////////////////code above creates a tree/////////////////////////////////////


def traverse_dic(i):
    dic_traversal_queue.append(i)
    weight = 0  # weight is starting from 0 since the code runs one last time even after last element in queue
    minWins = False
    while len(dic_traversal_queue) != 0:
        # print("node before", dic_traversal_queue)
        weight = weight + 1
        # print("weight", weight)
        node = dic_traversal_queue.pop(0)
        # print("node after", dic_traversal_queue)
        child = dic[str(node)]

        for i in child:
            if i not in dic_traversal_queue:
                dic_traversal_queue.append(i)

        # print("dic_traversal_queue",dic_traversal_queue)
    if weight % 2 == 1:# min loses
        minWins = False

    else: # min wins
        minWins = True


    this_move = MoveInfo()
    this_move.moveWeight = weight
    this_move.minWinsWithThisMove = minWins
    this_move.moveItself = i

    return this_move


def get_availaible_moves(node):
    child = dic[str(node)]
    return child


def heuristic(childRecieve):
    indx = 0
    bestMoveChoice = MoveInfo()


    print("availaible options for MAX", childRecieve)
    for i in childRecieve:

        currentMoveInfo = traverse_dic(i)

        if bestMoveChoice.moveWeight == 0: # first node visited
            bestMoveChoice.moveWeight = currentMoveInfo.moveWeight
            bestMoveChoice.minWinsWithThisMove = currentMoveInfo.minWinsWithThisMove
            bestMoveChoice.moveItself = i

        else:
            if bestMoveChoice.minWinsWithThisMove==True:
                if currentMoveInfo.minWinsWithThisMove==False: # new move has a win possibility for MAX
                    bestMoveChoice.moveWeight = currentMoveInfo.moveWeight
                    bestMoveChoice.minWinsWithThisMove = currentMoveInfo.minWinsWithThisMove
                    bestMoveChoice.moveItself = i
                else:
                    if bestMoveChoice.moveWeight < currentMoveInfo.moveWeight: # max still loses but it will lose slower
                        bestMoveChoice.moveWeight = currentMoveInfo.moveWeight
                        bestMoveChoice.minWinsWithThisMove = currentMoveInfo.minWinsWithThisMove
                        bestMoveChoice.moveItself = i
            else:
                if currentMoveInfo.minWinsWithThisMove==False:
                    if bestMoveChoice.moveWeight > currentMoveInfo.moveWeight:  # max still loses but it will lose faster
                        bestMoveChoice.moveWeight = currentMoveInfo.moveWeight
                        bestMoveChoice.minWinsWithThisMove = currentMoveInfo.minWinsWithThisMove
                        bestMoveChoice.moveItself = i




    return bestMoveChoice.moveItself

def min_plays(preMove):
    if initialTurn:
        # node=previousMove.pop()
        child = get_availaible_moves(preMove)
        # preMove.pop()
        # preMove.clear()

        i = 1
        if (len(child) != 0):  # if option availaible
            for option in child:
                print("enter ", i, " for : ", option)
                i = i + 1
            choice = input("your choice : ")

            preMove = child[int(choice) - 1]
            return preMove
        else:
            return [-1]


def max_plays(preMove):
    if initialTurn:
        # node=previousMove.pop()
        child = get_availaible_moves(preMove)
        # preMove.pop()
        preMove.clear()

        # //////////get best move//////////
        maxMove = heuristic(child)
        # heuristic([initial_mytuple])
        # /////////////////////////////////
        print("best possible move for MAX ", maxMove)
        i = 1
        if (len(child) != 0):   # if option availaible

            preMove = maxMove
            return preMove
        else:
            return [-1]


def play(minTurnRecieve, prevMove):
    global gameEnd
    pMove = prevMove
    while gameEnd != True:
        if minTurnRecieve == True:
            if (pMove[0] == -1):
                gameEnd = True
            else:
                print("MIN turn")
                pMove = min_plays(pMove)
                minTurnRecieve = False
        else:
            if (pMove[0] == -1):
                gameEnd = True
            else:
                print("MAX turn")
                pMove = max_plays(pMove)
                minTurnRecieve = True
                # gameEnd=True
    if gameEnd == True:
        if minTurnRecieve == True:
            print("MAX is out of options:->>>>> MIN wins")
        else:
            print("MIN is out of options:->>>>> MAX wins")


# dic_traversal_queue.append(initial_mytuple)
queue.append(initial_mytuple)
traverseQueue(count)

# traverse_dic(initial_mytuple) # this will display the complete game tree


print("Starting node -> ", previousMove)
play(minTurn, previousMove)
# print(dic[str(initial_mytuple)])
