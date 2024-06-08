import random
from typing import List, Tuple

type Item = Tuple[int, int]
type Chromosome = List[bool]

GENERATION_LIMIT = 5



if __name__ == "__main__":
    items: List[Item] = [(4, 12), (2, 1), (10, 4), (1, 1), (2, 2)]
    quantity = len(items)
    capacity = 15
    size = 10

    generation = 0

    while True:
        print("Generation: ", generation)

        # Generate population
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

        print("Final Population: ", population)
        print("Fitnesses: ", fitnesses)

        break
