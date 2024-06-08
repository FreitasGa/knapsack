import random
from typing import List, Tuple, Dict

Item = Tuple[int, int]
Chromosome = List[bool]

GENERATION_LIMIT = 15

# Função para realizar a seleção por roleta
def roulette_wheel_selection(population: List[Chromosome], fitnesses: List[Dict[str, int]]) -> Chromosome:
    total_fitness = sum(f['fitness'] for f in fitnesses)
    random_fitness = random.uniform(0, total_fitness)
    partial_sum = 0

    for i in range(len(population)):
        partial_sum += fitnesses[i]['fitness']
        if partial_sum >= random_fitness:
            return population[i]

    return population[-1]


# Função para realizar o crossover
def crossover(parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
    crossover_point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Função para realizar a mutação
def mutate(chromosome: Chromosome, mutation_rate: float) -> Chromosome:
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = not chromosome[i]
    return chromosome


# Função para calcular o fitness de um cromossomo
def calculate_fitness(chromosome: Chromosome, capacity: int, items: List[Item]) -> Dict[str, int]:
    total_weight = sum(items[i][1] for i in range(len(chromosome)) if chromosome[i])
    total_value = sum(items[i][0] for i in range(len(chromosome)) if chromosome[i])

    if total_weight > capacity:
        total_value = 0

    return {'fitness': total_value, 'weight': total_weight}

GENERATION_LIMIT = 5
CONVERGENCE_RATE = 0.9
CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.1
ELITISM = False

if __name__ == "__main__":
    items: List[Item] = [(360, 7), (83, 0), (59, 30), (130, 22), (431, 80),
                         (67, 94), (230, 11), (52, 81), (93, 70), (125, 64),
                         (670, 59), (892, 18), (600, 0), (38, 36), (48, 3),
                         (147, 8), (78, 15), (256, 42), (63, 9), (17, 0),
                         (120, 42), (164, 47), (432, 52), (35, 32), (92, 26),
                         (110, 48), (22, 55), (42, 6), (50, 29), (323, 84),
                         (514, 2), (28, 4), (87, 18), (73, 56), (78, 7),
                         (15, 29), (26, 93), (78, 44), (210, 71), (36, 3),
                         (85, 86), (189, 66), (274, 31), (43, 65), (33, 0),
                         (10, 79), (19, 20), (389, 65), (276, 52), (312, 13)]
    quantity = len(items)
    capacity = 850
    size = 10
    generation = 0
    parent1: Chromosome = []
    parent2: Chromosome = []
    threshold = size * CONVERGENCE_RATE

    best_fitness = 0
    best_chromosome = None
    best_items = []

    while generation < GENERATION_LIMIT:
        print("Generation: ", generation)

        # Generate population
        population: List[Chromosome] = []

        if generation == 0:
            population = [[random.choice([True, False]) for _ in range(quantity)] for _ in range(size)]

        print("Population: ", population)
        mutation_rate = 0.001
        crossover_rate = 0.85

        # Calculate fitness
        fitnesses = [calculate_fitness(chromosome, capacity, items) for chromosome in population]

        # Verifica a condição de parada: 90% da população com o mesmo fitness
        unique_fitnesses = set(f['fitness'] for f in fitnesses)
        if len(unique_fitnesses) <= 0.1 * size:
            print('90% da população possui o mesmo fitnesses')
            break

        new_population = []

        while len(new_population) < size:
            parent1 = roulette_wheel_selection(population, fitnesses)
            parent2 = roulette_wheel_selection(population, fitnesses)

            child1, child2 = parent1, parent2

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)

            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.append(child1)

            if len(new_population) < size:
                new_population.append(child2)

        population = new_population

        # Atualizar o melhor cromossomo encontrado
        for i, fitness in enumerate(fitnesses):
            if fitness['fitness'] > best_fitness:
                best_fitness = fitness['fitness']
                best_chromosome = population[i]

        generation += 1

    # Obtém os itens na mochila do melhor cromossomo
    if best_chromosome:
        best_items = [items[i] for i in range(len(best_chromosome)) if best_chromosome[i]]

    print("Melhor fitness: ", best_fitness)
    print("Melhor cromossomo: ", best_chromosome)
    print("Itens na mochila: ", best_items)
    print("Final Population: ", population)
    print("Fitnesses: ", fitnesses)
