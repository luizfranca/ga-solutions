import random
import matplotlib.pyplot as plt
import sys

class Gen:

	curGen = 1
	genID = 1

	def __init__(self, x = 0, y = 0, createRandom = True, dominatedBy = 0, mutationRate = 20):
		if createRandom:
			x = random.uniform(-3, 3)
			y = random.uniform(-3, 3)

		self.genID = Gen.genID
		self.gen = [x, y]
		self.generation = Gen.curGen
		self.dominatedBy = dominatedBy
		self.mutationRate = mutationRate

		Gen.genID += 1

	def mutate(self):
		for i in range(len(self.gen)):
			if random.randint(0, 100) > self.mutationRate:
				self.gen[i] = random.uniform(-3, 3)

	# f1(x, y) = x + y + 1
	def fitness1(self):
		return sum(self.gen) + 1
	# f2(x, y) = x**2 + 2y - 1
	def fitness2(self):
		return self.gen[0] ** 2 + self.gen[1] * 2 - 1

class NSGAII:

	def __init__(self, popSize = 20, genLimit = 20):
		self.pop = []
		self.fronts = []
		self.popSize = popSize
		self.genLimit = genLimit
		for i in xrange(self.popSize):
			self.pop += [Gen()]

	def dominates(self, x, y):
		#does x dominate y
		if x.fitness1() < y.fitness1() and x.fitness2() < y.fitness2():
			return True

		return False

	def sortByNonDominance(self, pop):

		for i in range(len(pop)):
			element = pop[i]
			element.dominatedBy = 0
			for j in range(len(pop)):
				if i == j:
					continue
				if self.dominates(pop[j], element):
					element.dominatedBy += 1

		pop = sorted(pop, key = lambda x : x.dominatedBy)

		return pop

	def getFronts(self, pop):
		f = 0
		fronts = [[]]

		currentDominace = pop[0].dominatedBy

		for i in range(len(pop)):
			element = pop[i]
			if element.dominatedBy != currentDominace:
				currentDominace = element.dominatedBy
				fronts += [[]]
				f += 1

			fronts[f] += [pop[i]]

		return fronts

	def crowdingDistance(self, front):

		cdX = [0] * len(front)
		cdX[0]  = float("inf")
		cdX[-1] = float("inf")
		fXMax = 7
		fXMin = -5

		cdY = [0] * len(front)
		cdY[0]  = float("inf")
		cdY[-1] = float("inf")
		fYMax = 14
		fYMin = -7

		cd = [0] * len(front)
		cd[0]  = float("inf")
		cd[-1] = float("inf")

		for i in range(1, len(front) - 1): 
			cdX[i] = (front[i + 1].fitness1() + front[i - 1].fitness2()) / (fXMax - fXMin)

			cdY[i] = (front[i + 1].fitness2() + front[i - 1].fitness2()) / (fYMax - fYMin)

			cd[i] = cdX[i] + cdY[i]

		return cd

	def selection(self, tourSize = 2):
		# tournament using non dominance and crowding distance

		cd = []

		for i in self.fronts:
			cd += self.crowdingDistance(i)

		matingPool = []

		pool = self.pop[:]

		for i in range(self.popSize):
			elements = []
			cds = []

			if len(pool) < tourSize:
				tourSize = len(pool)

			for j in range(tourSize):
				index = random.randint(0, len(pool) - 1)
				elements += [(pool[index])]
				cds += [cd[index]]

				del cd[index]
				del pool[index]

			bestElement = 0
			for k in range(len(elements)):
				if elements[bestElement].dominatedBy == elements[k].dominatedBy:
					if cds[k] < cds[bestElement]:
						bestElement = k
				elif elements[k].dominatedBy < elements[bestElement].dominatedBy:
					bestElement = k

			matingPool += [elements[bestElement]]

			del elements[bestElement]
			del cds[bestElement]

			pool += elements
			cd += cds

		return matingPool

	def crossover(self, element1, element2):
		alfa = random.uniform(0, 1)

		x1 = element1.gen[0] * alfa + element2.gen[0] * (1 - alfa)
		y1 = element1.gen[1] * alfa + element2.gen[1] * (1 - alfa)

		child1 = Gen(x1, y1, createRandom = False)

		x2 = element1.gen[0] * (1 - alfa) + element2.gen[0] * alfa
		y2 = element1.gen[1] * (1 - alfa) + element2.gen[1] * alfa

		child2 = Gen(x2, y2, createRandom = False)

		return [child1, child2]

	def nextGen(self, matingPool):
		Gen.curGen += 1

		gen = []

		size = len(matingPool)
		if len(matingPool) % 2 != 0:
			gen += self.crossover(matingPool[-1], matingPool[-1])
			size -= 1

		for i in range(0, size, 2):
			gen += self.crossover(matingPool[i], matingPool[i + 1])

		for i in range(len(gen)):
			gen[i].mutate()

		return gen

	def printPop(self):

		# nsgaii.sortByNonDominance()

		for i in range (len(self.pop)):
			print "id: " + str(self.pop[i].genID) + " x: " + str(self.pop[i].gen[0]) + " y: " + str(self.pop[i].gen[1]) + " f1: " + str(nsgaii.pop[i].fitness1()) + " f2: " + str(nsgaii.pop[i].fitness2()) + " dominatedBy: " + str(nsgaii.pop[i].dominatedBy)

	def plot(self, pool = []):
		plotList = []

		if len(pool) == 0:
			self.pop = self.sortByNonDominance(self.pop) 
			fronts = self.getFronts(self.pop)
		else:
			pool = self.sortByNonDominance(pool)
			fronts = self.getFronts(pool)

		for i in range(len(fronts)):
			
			for j in fronts[i]:
				if (i == 0):
					plt.plot([j.fitness1()], j.fitness2(),  'ro')
				else:
					plt.plot([j.fitness1()], j.fitness2(),  'bo')
				# print j.fitness1(), j.fitness2()

		#plt.plot(plotList)
		plt.xlabel('f1')
		plt.ylabel('f2')
		plt.title('NSGA-II')
		# plt.axis([-5, 7, -7, 14])
		plt.grid(True)
		plt.show()

	def run(self):

		bigPool = [] #all solutions ever created

		bigPool = self.pop[:]

		self.pop = self.sortByNonDominance(self.pop) # sort the pop by order of non dominance

		self.fronts = self.getFronts(self.pop)

		matingPool = self.selection() # it should always be called after sortByNonDominance

		children = self.nextGen(matingPool)

		for i in range(self.genLimit):
			bigPool += children[:]

			self.pop += children

			self.pop = self.sortByNonDominance(self.pop) # sort by non dominance

			self.pop = self.pop[:self.popSize] # Get Survivos 

			self.pop = self.sortByNonDominance(self.pop) 

			self.fronts = self.getFronts(self.pop)

			matingPool = self.selection()

			children = self.nextGen(matingPool)

		self.printPop()
		self.plot(bigPool) # switch to self.pop instead of bigPool to just plot the last generation

# nsgaii = NSGAII(popSize = int(sys.argv[1]), genLimit = int(sys.argv[2]))
nsgaii = NSGAII(popSize = 20, genLimit = 30) 
nsgaii.run()
