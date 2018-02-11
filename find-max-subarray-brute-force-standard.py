from random import randint

def generateRandomArray(length):
    array = []
    for i in range(0, length):
        array.append(randint(-1000, 1000))
    return array


def algorithm(array):
    bestStartIndex = 0
    bestEndIndex = 0
    bestSum = 0
    for i in range(0, len(array)):
        currentSum = array[i]
        for j in range(i + 1, len(array)):
            currentSum += array[j]
            if currentSum > bestSum:
                bestSum = currentSum
                bestStartIndex = i
                bestEndIndex = j
    return bestStartIndex, bestEndIndex, bestSum

testArray = [13,-3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
bestStartIndex, bestEndIndex, bestSum = algorithm(testArray)
if bestStartIndex != 7 or bestEndIndex != 10 or bestSum != 43:
   print("FAIL!")
   exit(1)


arrayToTest = generateRandomArray(25000)

#so slow!
bestStartIndex, bestEndIndex, bestSum = algorithm(arrayToTest)
print(bestStartIndex, bestEndIndex, bestSum)
