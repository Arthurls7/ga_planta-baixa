import random
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

from utils import calculate_characteristics
from genetic_algorithm import evolutionary_cycle

from constants import ROOMS


def draw_floor_plan(house_plan) -> None:
    """
    Desenha a planta da casa, incluindo cômodos, portas, janelas e mobílias.

    Args:
        house_plan: Objeto contendo os detalhes da planta da casa.

    Returns:
        None
    """

    # Cria uma figura para cada andar da casa
    num_floors = house_plan.max_floor
    # Ajusta o tamanho da figura com base no número de andares
    fig, axes = plt.subplots(1, num_floors, figsize=(10 * num_floors, 10))

    if num_floors == 1:
        axes = [axes]

    titles = [f"Planta do Andar {floor}" for floor in range(num_floors)]

    for ax, title in zip(axes, titles):
        ax.set_title(title)
        ax.set_xlim(0, house_plan.house_width)
        ax.set_ylim(0, house_plan.house_length)
        ax.set_aspect("equal")
        ax.invert_yaxis()

    # Define as cores para cada tipo de cômodo
    colors = plt.cm.Set3(np.linspace(0, 1, len(ROOMS)))
    color_map = dict(zip(ROOMS.keys(), colors))

    # Desenha os cômodos, portas, janelas e mobílias
    for room in house_plan.rooms:
        ax = axes[room.floor]

        # Adiciona um retângulo representando o cômodo
        rectangle = Rectangle(
            (room.x, room.y),
            room.width,
            room.length,
            fill=True,
            facecolor=color_map.get(room.type, "gray"),
            edgecolor="black",
            linewidth=2,
        )
        ax.add_patch(rectangle)

        # Adiciona o texto com o tipo do cômodo no centro
        ax.text(
            room.x + room.width / 2,
            room.y + room.length / 2,
            room.type,
            ha="center",
            va="center",
            wrap=True,
            fontsize=8,
        )

        # Desenha as portas do cômodo
        for door in room.door_positions:
            door_x, door_y, door_width, door_height = door
            door_rect = Rectangle(
                (door_x, door_y),
                door_width,
                door_height,
                fill=True,
                facecolor="brown",
                edgecolor="black",
            )
            ax.add_patch(door_rect)

        # Desenha as janelas do cômodo
        for _ in range(room.windows):
            # Escolhe uma parede aleatória para adicionar a janela
            wall = random.choice(['left', 'right', 'bottom', 'top'])

            # Define a posição e tamanho da janela com base na parede escolhida
            if wall == 'left':
                window_x = room.x
                window_y = room.y + random.uniform(0, room.length - 1)
                window_width, window_height = 0.1, 1
            elif wall == 'right':
                window_x = room.x + room.width - 0.1
                window_y = room.y + random.uniform(0, room.length - 1)
                window_width, window_height = 0.1, 1
            elif wall == 'bottom':
                window_x = room.x + random.uniform(0, room.width - 1)
                window_y = room.y
                window_width, window_height = 1, 0.1
            else:  # top
                window_x = room.x + random.uniform(0, room.width - 1)
                window_y = room.y + room.length - 0.1
                window_width, window_height = 1, 0.1

            window = Rectangle(
                (window_x, window_y),
                window_width,
                window_height,
                fill=True,
                facecolor="lightblue",
                edgecolor="black",
            )
            ax.add_patch(window)

        # Desenha a mobília do cômodo
        for furniture in room.furnitures:
            furn_x = room.x + furniture["position"][0]
            furn_y = room.y + furniture["position"][1]
            furn_rect = Rectangle(
                (furn_x, furn_y),
                furniture["width"],
                furniture["length"],
                fill=True,
                facecolor="gray",
                edgecolor="black",
                alpha=0.5,
            )
            ax.add_patch(furn_rect)
            ax.text(
                furn_x + furniture["width"] / 2,
                furn_y + furniture["length"] / 2,
                furniture["type"],
                ha="center",
                va="center",
                fontsize=6,
                wrap=True,
            )

    # Adiciona a orientação da casa
    orientation_text = f"N\n^\n|\n \n{house_plan.orientation.capitalize()}"

    # Adiciona o texto de orientação em cada figura
    for ax in axes:
        ax.text(
            1.02, 0.5, orientation_text, transform=ax.transAxes, va="center", ha="left"
        )

    plt.tight_layout()
    plt.show()


# Ponto de entrada do programa
if __name__ == "__main__":
    # Solicitar entrada do usuário
    full_name = input("Digite o nome completo do membro com o maior número de caracteres: ")
    area = float(input("Digite a área da casa em m²: "))
    orientation = input("Digite a orientação da casa (norte, sul, leste, oeste): ").lower()

    # Calcular características com base no nome
    remainder1, remainder2, remainder3 = calculate_characteristics(full_name)

    # Definir características da casa com base nos restos
    if remainder1 == 0:
        house_type = "2 andares e uma laje"
    elif remainder1 == 1:
        house_type = "2 andares e um sótão"
    else:
        house_type = "2 andares e um porão"

    if remainder2 == 0:
        special_room = "Sala de Música"
    elif remainder2 == 1:
        special_room = "Sala de Ginástica"
    elif remainder2 == 2:
        special_room = "Escritório"
    else:
        special_room = "Sala de Jogos"

    if remainder3 == 0:
        bedrooms = 3
        bathrooms = 2
        closets = 2
    elif remainder3 == 1:
        bedrooms = 2
        bathrooms = 3
        closets = 2
    elif remainder3 == 2:
        bedrooms = 3
        bathrooms = 3
        closets = 1
    else:
        bedrooms = 2
        bathrooms = 3
        closets = 1

    # Exibir as características definidas
    print(f"\nA casa terá {house_type}, um(a) {special_room}, {bedrooms} quartos, {bathrooms} banheiros e {closets} closets.")

    # Executar o algoritmo genético para gerar a planta
    best_plan = evolutionary_cycle(
        generations=1000,          # Aumentar o número de gerações
        population_size=200,        # Aumentar o tamanho da população
        area=area,
        orientation=orientation,
        house_type=house_type,
        special_room=special_room,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        closets=closets,
    )

    # Desenhar a planta gerada
    draw_floor_plan(best_plan)

    # Exibir informações sobre a planta gerada
    print("\nInformações da planta gerada:")
    for room in best_plan.rooms:
        print(f"Cômodo: {room.type}, Andar: {room.floor}")
        print(f"Posição: ({room.x:.2f}, {room.y:.2f})")
        print(f"Tamanho: {room.width:.2f}m x {room.length:.2f}m")
        print(f"Janelas: {room.windows}")
        for furniture in room.furnitures:
            print(
                f"  Mobília: {furniture['type']}, Tamanho: {furniture['width']:.2f}m x {furniture['length']:.2f}m, Posição: {furniture['position']}"
            )
        print()

    print(f"Fitness da planta: {best_plan.fitness}")
