import random
from typing import List, Tuple

from models import FloorPlan, Room


def selection(population: List[FloorPlan]) -> Tuple[FloorPlan, FloorPlan]:
    """
    Seleciona dois indivíduos da população para reprodução com base no fitness.

    Args:
        population (List[FloorPlan]): A lista de plantas (indivíduos) na população atual.

    Returns:
        Tuple[FloorPlan, FloorPlan]: Dois indivíduos selecionados para reprodução.
    """

    total_fitness = sum(plan.fitness for plan in population)
    selection_probabilities = [plan.fitness / total_fitness for plan in population]

    return random.choices(population, weights=selection_probabilities, k=2)


def crossover(parent1: FloorPlan, parent2: FloorPlan) -> FloorPlan:
    """
    Realiza o crossover entre dois indivíduos (pais) para gerar um novo indivíduo (filho).
    Garante que o filho tenha arranjos de cômodos válidos.

    Args:
        parent1 (FloorPlan): O primeiro pai.
        parent2 (FloorPlan): O segundo pai.

    Returns:
        FloorPlan: O novo indivíduo gerado a partir do crossover.
    """

    # Seleciona um ponto de corte aleatório
    cut = random.randint(1, min(len(parent1.rooms), len(parent2.rooms)) - 1)
    # Combina os cômodos dos pais
    child_rooms = parent1.rooms[:cut] + parent2.rooms[cut:]

    # Ajusta os cômodos para evitar sobreposições e fora dos limites
    temporary_plan = FloorPlan(
        area=parent1.area,
        orientation=parent1.orientation,
        house_type=parent1.house_type,
        special_room=parent1.special_room,
        bedrooms=parent1.bedrooms,
        bathrooms=parent1.bathrooms,
        closets=parent1.closets,
        rooms=[]
    )

    valid_rooms = []
    for room in child_rooms:
        for _ in range(100):
            # Verifica se o cômodo está dentro dos limites
            if room.width > temporary_plan.house_width or room.length > temporary_plan.house_length:
                # Ajusta as dimensões
                room.width, room.length = temporary_plan.generate_room_dimensions(room.type)

            # Posiciona o cômodo aleatoriamente
            room.x = random.uniform(0, temporary_plan.house_width - room.width)
            room.y = random.uniform(0, temporary_plan.house_length - room.length)

            # Verifica se o cômodo não se sobrepõe com outros
            if not temporary_plan.has_overlap(room, valid_rooms):
                valid_rooms.append(room)
                break
        else:
            # Não foi possível posicionar o cômodo, ignora
            pass

    child = FloorPlan(
        area=parent1.area,
        orientation=parent1.orientation,
        house_type=parent1.house_type,
        special_room=parent1.special_room,
        bedrooms=parent1.bedrooms,
        bathrooms=parent1.bathrooms,
        closets=parent1.closets,
        rooms=valid_rooms
    )

    return child


def mutation(plan: FloorPlan) -> None:
    """
    Realiza mutação em um indivíduo, ajustando a posição, dimensões ou andar de um cômodo.
    Garante que o cômodo mutado esteja dentro dos limites e não sobreponha outros.

    Args:
        plan (FloorPlan): O indivíduo a ser mutado.
    """

    # Seleciona um cômodo aleatório para mutar
    rooms = plan.rooms.copy()
    room = random.choice(rooms)

    # Salva o cômodo original para restauração em caso de falha
    original_room = Room(room.type, room.floor, room.x, room.y, room.width, room.length)

    # Escolhe aleatoriamente o atributo a ser mutado
    attribute = random.choice(['position', 'dimension', 'floor'])

    # Tenta mutar o cômodo
    if attribute == 'position':
        for _ in range(100):
            room.x = random.uniform(0, plan.house_width - room.width)
            room.y = random.uniform(0, plan.house_length - room.length)
            if not plan.has_overlap(room, [r for r in rooms if r != room]):
                break
        else:
            room.x = original_room.x
            room.y = original_room.y
    elif attribute == 'dimension':
        for _ in range(100):
            width, length = plan.generate_room_dimensions(room.type)
            room.width = width
            room.length = length
            if room.x + room.width <= plan.house_width and room.y + room.length <= plan.house_length:
                if not plan.has_overlap(room, [r for r in rooms if r != room]):
                    break
        else:
            room.width = original_room.width
            room.length = original_room.length
    elif attribute == 'floor':
        room.floor = random.randint(0, plan.max_floor - 1)

    plan.rooms = rooms
    plan.fitness = plan.calculate_fitness()


def mutate_rooms(rooms: List[Room]) -> List[Room]:
    """
    Aplica mutação a uma lista de cômodos durante o crossover.

    Args:
        rooms (List[Room]): A lista de cômodos a ser mutada.

    Returns:
        List[Room]: A lista de cômodos após a mutação.
    """

    # Seleciona um cômodo aleatório para mutar
    mutated_rooms = rooms.copy()
    room = random.choice(mutated_rooms)

    # Escolhe aleatoriamente o atributo a ser mutado
    attribute = random.choice(['position', 'dimension', 'floor'])

    if attribute == 'position':
        room.x = random.uniform(0, room.width)
        room.y = random.uniform(0, room.length)
    elif attribute == 'dimension':
        room.width += random.uniform(-1, 1)
        room.length += random.uniform(-1, 1)
    elif attribute == 'floor':
        room.floor = 1 - room.floor  # Alterna entre 0 e 1

    return mutated_rooms


def evolutionary_cycle(
    generations: int, population_size: int, area: float, orientation: str, house_type: str,
    special_room: str, bedrooms: int, bathrooms: int, closets: int
) -> FloorPlan:
    """
    Executa o ciclo evolutivo do algoritmo genético.

    Args:
        generations (int): O número de gerações a serem executadas.
        population_size (int): O tamanho da população.
        area (float): A área da planta.
        orientation (str): A orientação da planta.
        house_type (str): O tipo de casa.
        special_room (str): O cômodo especial.
        bedrooms (int): O número de quartos.
        bathrooms (int): O número de banheiros.
        closets (int): O número de closets.

    Returns:
        FloorPlan: A melhor planta encontrada após o ciclo evolutivo.
    """

    # Gera a população inicial
    population = [
        FloorPlan(area, orientation, house_type, special_room, bedrooms, bathrooms, closets)
        for _ in range(population_size)
    ]

    for _ in range(generations):
        new_population = []

        for _ in range(population_size // 2):
            # Seleção
            parents = selection(population)
            parent1, parent2 = parents[0], parents[1]

            # Cruzamento
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)

            # Mutação
            if random.random() < 0.1:
                mutation(child1)
            if random.random() < 0.1:
                mutation(child2)

            new_population.extend([child1, child2])

        # Combina as populações e seleciona os melhores indivíduos
        population.extend(new_population)
        population = sorted(population, key=lambda p: p.fitness, reverse=True)[:population_size]

    # Retorna a melhor planta
    return population[0]
