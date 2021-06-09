import random

class Product:
    def __init__(self,name,weight,value):
        self.name = name
        self.weight = weight
        self.value = value

        
def fileToListOfProducts(filename):
    f = open(filename, "r")
    list_of_product = []
    index = 0
    for line in f:
        a = line.split()
        if len(a) == 2 and index != 0:
            list_of_product.append(Product(index,int(a[1]),int(a[0])))
        index+=1
    f.close()
    return list_of_product

a = fileToListOfProducts("low-dimensional/f1_l-d_kp_10_269")
print(len(a))

class Evolution:
    def __init__(self,products,size,limit):
        self.products = products
        self.length= len(self.products)
        self.population = []
        self.limit = limit
        self.size = size
        self.bestOne = None
        self.bestValue = 0
        self.bestWeight = 0
        self.chromosome_with_fitness = []

    def generate_chromosomes(self):
        chromosomes = []
        for i in range(self.length):
            if random.randint(1,1000) % 2 == 0:
                chromosomes.append(1)
            else:
                chromosomes.append(0)
        return chromosomes

    def generate_population(self):
        for i in range(self.size):
            self.population.append(self.generate_chromosomes())
        self.calculate_population_fitness()
        print(self.chromosome_with_fitness)
        self.population =  self.chromosome_with_fitness

    def fitness_of_chromosome(self,chromosome,limit):
        weight = 0
        value = 0
        for i in range(len(self.products)):
            if chromosome[i] == 1:
                weight += self.products[i].weight
                value  += self.products[i].value
                if weight > limit:
                    return 0,0
        return value,weight

    def calculate_population_fitness(self):
        for chromosome in self.population:
            if len(chromosome) != 3:
                score = self.fitness_of_chromosome(chromosome,self.limit)
                self.chromosome_with_fitness.append([chromosome, score[0],score[1]])
            else:
                score = self.fitness_of_chromosome(chromosome[0],self.limit)
                self.chromosome_with_fitness.append([chromosome[0]]+ [score[0],score[1]])

    def sorted_chromosome_fitness(self):
        self.chromosome_with_fitness.sort(key = lambda x: x[1])
        return self.chromosome_with_fitness

    def roulette_wheel(self):
        total = 0
        for i in self.population:
            total += i[1]
        pick = random.randint(0, total+1)
        current = 0
        for chromosome in self.population:
            current += chromosome[1]
            if current > pick:
                return chromosome

    def binary_tournament_selection(self):
        parents = random.choices(self.population, k=2)
        parents.sort(key=lambda x:x[1])
        return parents[-1]

    def truncation_selection(self):
        return self.population[-1]

    def random_selection(self):
        pick = random.randint(0,len(self.population)-1)
        return (self.population[pick])
    
    def rank_based_selection(self):
        rank = 1
        currFitness = self.chromosome_with_fitness[0][1]
        for i in range(len(self.population)):
            if len(self.population[i])<=4:
                if currFitness < self.population[i][1]:
                    currFitness = self.population[i][1]
                    rank += 1
                    self.population[i].append(rank)
                else:
                    self.population[i].append(rank)
        total_rank = sum([ i[3] for i in self.population])
        accumilated_weight = 0
        for i in range(len(self.population)):
            accumilated_weight += (self.population[i][3]/total_rank) * 100
            self.population[i][1] = accumilated_weight
        pick = random.uniform(0.0, accumilated_weight)
        for i in self.population:
            if i[1] >= pick:
                return i
        

        
        
    def selection_pair(self):
        return random.choices(population = self.population,weights = [self.fitness_of_chromosome(chromosome,self.limit) for chromosome in self.population],k = 2)

    def crossover(self,a , b):
        chromosome_slice = random.randint(1,self.size-1)
        kid1 = a[:chromosome_slice]+b[chromosome_slice:]
        kid2 = b[:chromosome_slice]+a[chromosome_slice:]
        return kid1, kid2

    def mutation(self,chromosome, probability):
        for i in range(len(chromosome)):
            p = random.randint(1,100)%100
            if p < probability:
                if chromosome[i] == 1:
                   chromosome[i] == 0
                elif chromosome[i] == 0:
                    chromosome[i] == 1
        return chromosome

    def average_values(self):
        t = 0
        for i in self.population:
            t += i[1]
        avg = t/ len(self.population)
        return avg

    def evolution(self,genCount):
        self.generate_population()
        for i in range(genCount):
            next_generation = []
            if self.population[-1][1] >= self.limit:
                break
            for j in range(5):
                #parent1 = self.binary_tournament_selection()
                #parent2 = self.binary_tournament_selection()
                #parent1 = self.roulette_wheel()
                #parent2 = self.roulette_wheel()
                parent1 = self.random_selection()
                parent2 = self.random_selection()
                #parent1 = self.truncation_selection()
                #parent2 = self.truncation_selection()
                #parent1 = self.rank_based_selection()
                #parent2 = self.rank_based_selection()
                kid1 , kid2 = self.crossover(parent1[0],parent2[0])
                kid1 = self.mutation(kid1,50)
                kid2 = self.mutation(kid2,50)
                next_generation += kid1,kid2

            
            temp = self.population
            self.population = next_generation            
            self.calculate_population_fitness()
            self.population = self.chromosome_with_fitness+temp[11:30]
            print('Generation : '+str(i+1)+' avg score: '+str(self.average_values()))
        self.chromosome_with_fitness = []
        self.population.sort(key=lambda x:x[1])
        self.bestOne = self.population[-1]
        self.bestOne = self.population[0]
        return self.population[-1],i
                
            

    def bestValueWeight(self):
        for i in range(len(self.products)):
            self.bestValue += self.products[i].value * self.bestOne[i]
            self.bestWeight += self.products[i].weight * self.bestOne[i]

            
    

e = Evolution(a,30,269)
for i in range(1,11):
    print("Iteration Number",i)
    print(e.evolution(100))
#s = e.calculate_population_fitness()
#print(s)
#print(e.sorted_chromosome_fitness())
#e.rank_based_selection()
#print(e.chromosome_with_fitness)
#print(s)

#print(e.evolution(1000)[0][0]) # if you want to make this work only return value in fitness chromosome
#e.bestValueWeight()
#print(e.bestValue)
#print(e.bestWeight)
