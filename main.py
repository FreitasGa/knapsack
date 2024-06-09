import random
from typing import List, Tuple

Item = Tuple[int, int]
Chromosome = List[bool]

GENERATION_LIMIT = 1000

CONVERGENCE_RATE = 0.9
CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.001

ELITISM = False

# Selection methods (0: Roulette Wheel Selection, 1: Group Selection)
SELECTION_METHOD = 0

if __name__ == "__main__":
    items: List[Item] = [(135, 70), (139, 73), (149, 77), (150, 80), (156, 82), (163, 87), (173, 90), (184, 94),
                         (192, 98), (201, 106), (210, 110), (214, 113), (221, 115), (229, 118), (240, 120)]
    quantity = len(items)
    capacity = 750
    size = 100

    generation = 0
    population: List[Chromosome] = []
    parent1: Chromosome = []
    parent2: Chromosome = []

    best_chromosome: Chromosome = []
    best_fitness = 0

    while generation < GENERATION_LIMIT:
        # print("Generation: ", generation)

        # Generate initial population
        if generation == 0:
            population = [[random.choice([True, False]) for _ in range(quantity)] for _ in range(size)]

        # print("Population: ", population)

        # Calculate fitness
        fitness = []

        for chromosome in population:
            fit = 0
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
                fit = value

            fitness.append(fit)

        fitness_sum = sum(fitness)

        # print("Population After Fitness: ", population)
        # print("Fitness: ", fitness)
        # print("Fitness Sum: ", fitness_sum)

        # Check if the population has converged (90%)
        unique_fitness = set(fitness)
        threshold = round(1 - CONVERGENCE_RATE, 2) * size

        if len(unique_fitness) <= threshold:
            print("Population has converged!")

            fittest = max(fitness)

            if fittest > best_fitness:
                index = fitness.index(fittest)
                best_chromosome = population[index]
                best_fitness = fitness[index]

            break

        # Create new population
        new_population = []

        # If elitism is enabled, keep 2 of the fittest chromosomes
        if ELITISM:
            sorted_fitness = sorted(fitness, reverse=True)

            for i in range(2):
                index = fitness.index(sorted_fitness[i])
                new_population.append(population[index])

            # print("New Population After Elitism: ", new_population)

        while True:
            if SELECTION_METHOD == 1:
                # Select parents by Group Selection
                indexes = list(range(size))
                indexes.sort(key=lambda x: fitness[x], reverse=True)

                groups = [
                    indexes[:size // 4],
                    indexes[size // 4: size // 2],
                    indexes[size // 2: 3 * size // 4],
                    indexes[3 * size // 4:]
                ]

                for i in range(2):
                    rand = random.random()

                    if rand >= 0.50:
                        group = groups[0]
                    elif 0.50 > rand >= 0.30:
                        group = groups[1]
                    elif 0.30 > rand >= 0.15:
                        group = groups[2]
                    else:
                        group = groups[3]

                    if i == 0:
                        parent1 = population[random.choice(group)]
                    else:
                        parent2 = population[random.choice(group)]
            else:
                # Select parents by Roulette Wheel Selection
                for i in range(2):
                    limit = random.randint(0, fitness_sum)
                    partial_sum = 0

                    for index, fit in enumerate(fitness):
                        partial_sum += fit

                        if partial_sum >= limit:
                            if i == 0:
                                parent1 = population[index]
                            else:
                                parent2 = population[index]

                            break

            # print("Parent 1: ", parent1)
            # print("Parent 2: ", parent2)

            child1, child2 = parent1, parent2

            # print("Child 1: ", child1)
            # print("Child 2: ", child2)

            # Crossover
            if random.random() < CROSSOVER_RATE:
                point = random.randint(0, quantity - 1)

                child1 = parent1[:point] + parent2[point:]
                child2 = parent2[:point] + parent1[point:]

            # print("Child 1 After Crossover: ", child1)
            # print("Child 2 After Crossover: ", child2)

            # Mutation
            for i in range(quantity):
                if random.random() < MUTATION_RATE:
                    child1[i] = not child1[i]

                if random.random() < MUTATION_RATE:
                    child2[i] = not child2[i]

            # print("Child 1 After Mutation: ", child1)
            # print("Child 2 After Mutation: ", child2)

            new_population.append(child1)
            new_population.append(child2)

            if len(new_population) >= size:
                break

        population = new_population

        # Find the fittest chromosome
        fittest = max(fitness)

        if fittest > best_fitness:
            index = fitness.index(fittest)
            best_chromosome = population[index]
            best_fitness = fitness[index]

        generation += 1

    best_items = [items[index] for (index, present) in enumerate(best_chromosome) if present]

    print("Crossover Rate: ", CROSSOVER_RATE)
    print("Mutation Rate: ", MUTATION_RATE)
    print("Elitism: ", ELITISM)
    print("Population Size: ", size)
    print("Selection Method: ", SELECTION_METHOD == 1 and "Group" or "Roulette Wheel")
    print("Generation: ", generation)
    print("Population: ", population)
    print("Best Chromosome: ", best_chromosome)
    print("Best Fitness: ", best_fitness)
    print("Best Items: ", best_items)
