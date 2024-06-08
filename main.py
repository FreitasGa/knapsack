import random
from typing import List, Tuple

type Item = Tuple[int, int]
type Chromosome = List[bool]

GENERATION_LIMIT = 5
CONVERGENCE_RATE = 0.9
CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.1
ELITISM = False

if __name__ == "__main__":
    items: List[Item] = [(4, 12), (2, 1), (10, 4), (1, 1), (2, 2)]
    quantity = len(items)
    capacity = 15
    size = 10

    generation = 0
    parent1: Chromosome = []
    parent2: Chromosome = []
    threshold = size * CONVERGENCE_RATE

    while True:
        print("Generation: ", generation)

        # Generate population
        population: List[Chromosome] = []

        if generation == 0:
            population = [[random.choice([True, False]) for _ in range(quantity)] for _ in range(size)]

        print("Population: ", population)

        # Calculate fitness
        fitnesses = []

        for chromosome in population:
            fitness = 0
            value = sum([items[index][0] for (index, present) in enumerate(chromosome) if present])
            weight = sum([items[index][1] for (index, present) in enumerate(chromosome) if present])

            # Remove items until weight is less than capacity
            while weight > capacity:
                index = random.randint(0, quantity - 1)

                if chromosome[index]:
                    chromosome[index] = False
                    value -= items[index][0]
                    weight -= items[index][1]

            if weight <= capacity:
                fitness = value

            fitnesses.append(fitness)

        print("Population After Fitness: ", population)
        print("Fitnesses: ", fitnesses)

        # Check if the population has converged (90%)
        if fitnesses.count(fitnesses[0]) >= threshold:
            print("Converged")
            break

        # Select parents by Roulette Wheel Selection
        fitness_sum = sum(fitnesses)
        print("Fitness Sum: ", fitness_sum)

        for i in range(2):
            limit = random.randrange(0, size)
            partial_sum = 0

            for index, fitness in enumerate(fitnesses):
                partial_sum += fitness

                if partial_sum >= limit:
                    if i == 0:
                        parent1 = population[index]
                    else:
                        parent2 = population[index]
                    break

        print("Parent 1: ", parent1)
        print("Parent 2: ", parent2)

        generation += 1
        break
