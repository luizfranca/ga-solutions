import random

def mutation(elemento):
    x1 = random.randint(0, 2)
    y1 = random.randint(0, 2)

    x2 = random.randint(0, 2)
    y2 = random.randint(0, 2)

    element[y1][x1], element[y2][x2] = element[y2][x2], element[y1][x1]

    return element

def fitness(element):
    
    error = 0
    for i in range(3):
        if sum(element[i]) != 15:
            error += 1

    column1, column2, column3 = 0, 0, 0
    for i in element:
    	column1 += i[0]
    	column2 += i[1]
    	column3 += i[2]

    if column1 != 15:
    	error += 1

    if column2 != 15:
        error += 1

    if column3 != 15:
        error += 1
    	
    if (element[0][0] + element[1][1] + element[2][2]) != 15:
        error += 1

    if (element[0][2] + element[1][1] + element[2][0]) != 15:
        error += 1

    return error

def printElement(element):
	for i in element:
		print (i)

element = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
scoreElement = fitness(element)

generation = 0

print (("="*30) + " fitness: " + str(scoreElement) + " generation " + str(generation))
print ("")
printElement (element)

while (fitness(element) != 0 ):
    mutant = mutation(element)
    mutant = mutation(mutant)

    score = fitness(mutant)

    if (score < scoreElement):
        scoreElement = score
        element = mutant

    generation += 1
    print (("="*30) + " fitness: " + str(scoreElement) + " generation " + str(generation))
    print ("")
    printElement (element)