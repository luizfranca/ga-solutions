import random

class Genome:

    def __init__(self, mp = 20, size = 5, ):
        self.genome = []
        self.mp = mp
        self.size = size
        for i in xrange(self.size):
            self.genome += [random.randint(0, 1)]
            
    def bitwise(self):
        for i in range(self.size):
            if (random.randint(0, 99) < self.mp):
                self.genome[i] = 1 if self.genome[i] == 0 else 0

    def fitness(self):
        score = 0
        factor = 1
        for i in range(self.size - 1, -1, -1):
            score += factor if self.genome[i] == 1 else 0
            factor *= 2
        return score ** 2

class SGA:
    # select True = tournament, False roulette
    # crossover True = uniform, False one point
    def __init__(self, popSize = 4, select = True, crossover = True, elitism = True, elitismSize = 1): 
        self.popSize = popSize
        self.pop = []
        self.select = select
        self.cross = crossover
        self.elitism = elitism
        self.elitismSize = elitismSize

        for i in xrange(self.popSize):
            self.pop += [Genome()]
    
    def printElements(self):
        for i in self.pop:
            print "Element: " + str(i.genome) + " fitness: " + str(i.fitness())
    # nSelect represents the number of pairs
    def roulette(self, nSelect = 1):
        auxPop = sorted(self.pop, key = lambda genome : genome.fitness())
        aux = []
        selected = []

        for i in xrange(nSelect * 2):
            totalScore = float(sum(e.fitness() for e in auxPop))
            r = random.uniform(0, 1)
            relativeFitness = 0 

            for j in range(len(auxPop)):
                if totalScore == 0:
                    relativeFitness = 0
                else:
                    relativeFitness += auxPop[j].fitness() / totalScore

                if r <= relativeFitness:
                    selected += [auxPop[j]]
                    del auxPop[j]
                    break

        return selected
    # nSelect represents the number of pairs
    def tournament(self, nSelect = 1, tourSize = 2):
        auxIndex = range(self.popSize)
        selected = []
        for i in xrange(nSelect * 2):
            
            if (len(auxIndex) == 1):
                selected += [self.pop[aux[0]]]
                break

            aux = []
            for j in xrange(tourSize):
                n = random.randint(0, len(auxIndex) - 1)
                aux += [auxIndex[n]]
                del auxIndex[n]

            aux = sorted(aux, key = lambda i : self.pop[i].fitness(), reverse = True)
            selected += [self.pop[aux[0]]]
            del aux[0]
            auxIndex += aux

        return selected

    def selection(self, nSelect = 1):
        return self.tournament(nSelect) if self.select else self.roulette(nSelect)

    def onePoint(self, parent1, parent2):
        point = random.randint(0, 4)
        
        child1 = Genome()
        child1.genome = parent1.genome[:point] + parent2.genome[point:]
        
        child2 = Genome()
        child2.genome = parent2.genome[:point] + parent1.genome[point:]

        return [child1, child2]

    def uniform(self, parent1, parent2):
        child1 = Genome()
        child2 = Genome()
        for i in range(len(parent1.genome)):
            coin = random.randint(0,1)
            if (coin == 1):
                child1.genome[i] = parent1.genome[i]
                child2.genome[i] = parent2.genome[i]
            else:
                child1.genome[i] = parent2.genome[i]
                child1.genome[i] = parent1.genome[i]

        return [child1, child2]

    def crossover(self, parent1, parent2):
        return self.uniform(parent1, parent2) if self.cross else self.onePoint(parent1, parent2)

    def run(self):
        gen = 0
        bestScore = 0

        self.pop = sorted(self.pop, key = lambda i : i.fitness(), reverse = True)

        bestElement = self.pop[0]

        while (bestScore < 961):
            parents = self.selection(1)

            for i in range(len(parents)):
                del self.pop[self.pop.index(parents[i])]

            children = []

            for i in range(1):
                children += self.crossover(parents[i * 2], parents[i * 2 + 1])

            for i in children:
                i.bitwise()

            
            self.pop += children            

            if (self.elitism):
                self.pop += [bestElement]
                self.pop = sorted(self.pop, key = lambda i : i.fitness(), reverse = True)
                self.pop = self.pop[: - self.elitismSize]

            self.pop = sorted(self.pop, key = lambda i : i.fitness(), reverse = True)
            if bestScore < self.pop[0].fitness():
                bestScore = self.pop[0].fitness()
                bestElement = self.pop[0]

            gen += 1
            print "bestElement " + str(bestElement.genome) + " fitness: " + str(bestScore) + " gen: " + str(gen)
            self.printElements()
            print "="*60
        

sga = SGA(4, False, False, False)
sga.run()