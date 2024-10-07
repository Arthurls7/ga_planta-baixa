import math
import random

from typing import List, Optional, Tuple

from constants import ROOMS, FURNITURES


class Room:
    def __init__(self, room_type: str, floor: int, x: float, y: float, width: float, length: float):
        """
        Classe que representa um cômodo da casa.

        Args:
            room_type (str): Tipo do cômodo (ex: "Banheiro", "Cozinha").
            floor (int): Andar onde o cômodo está localizado (0 para térreo, 1 para primeiro andar, etc.).
            x (float): Posição X na planta.
            y (float): Posição Y na planta.
            width (float): Largura do cômodo.
            length (float): Comprimento do cômodo.
        """

        self.type = room_type
        self.floor = floor  # 0 para térreo, 1 para primeiro andar
        self.x = x  # Posição X na planta
        self.y = y  # Posição Y na planta
        self.width = width
        self.length = length
        self.door_positions: List[Tuple[float, float, float, float]] = []  # Lista de posições das portas
        self.windows: int = random.randint(1, 3)
        self.furnitures: List[dict] = self.generate_furnitures()

    def generate_furnitures(self) -> List[dict]:
        """
        Gera as mobílias para o cômodo, posicionando-as ao longo das paredes.

        Returns:
            List[dict]: Lista de mobílias com seus tipos, dimensões e posições.
        """

        furnitures = []
        occupied_spaces: List[Tuple[float, float, float, float]] = []

        for furniture in FURNITURES.get(self.type, []):
            furniture_type, furniture_width, furniture_length = furniture
            if furniture_width <= self.width and furniture_length <= self.length:
                position = self.find_position_on_walls(furniture_width, furniture_length, occupied_spaces)
                if position:
                    furnitures.append({
                        "type": furniture_type,
                        "width": furniture_width,
                        "length": furniture_length,
                        "position": position,
                    })
                    occupied_spaces.append((position[0], position[1], furniture_width, furniture_length))

        return furnitures

    def find_position_on_walls(self, furniture_width: float, furniture_length: float, occupied_spaces: List[Tuple[float, float, float, float]]) -> Optional[Tuple[float, float]]:
        """
        Encontra uma posição para a mobília ao longo das paredes, evitando sobreposições.

        Args:
            furniture_width (float): Largura da mobília.
            furniture_length (float): Comprimento da mobília.
            occupied_spaces (List[Tuple[float, float, float, float]]): Lista de espaços já ocupados.

        Returns:
            Optional[Tuple[float, float]]: Posição X e Y para a mobília ou None se não encontrar posição.
        """

        walls = [
            # Parede esquerda
            (0, random.uniform(0, self.length - furniture_length)),
            # Parede direita
            (self.width - furniture_width, random.uniform(0, self.length - furniture_length)),
            # Parede inferior
            (random.uniform(0, self.width - furniture_width), 0),
            # Parede superior
            (random.uniform(0, self.width - furniture_width), self.length - furniture_length)
        ]

        for position in walls:
            if not self.check_overlap(position, furniture_width, furniture_length, occupied_spaces):
                return position

        return None

    def check_overlap(self, position: Tuple[float, float], furniture_width: float, furniture_length: float, occupied_spaces: List[Tuple[float, float, float, float]]) -> bool:
        """
        Verifica se a mobília sobrepõe alguma área já ocupada.

        Args:
            position (Tuple[float, float]): Posição X e Y da mobília.
            furniture_width (float): Largura da mobília.
            furniture_length (float): Comprimento da mobília.
            occupied_spaces (List[Tuple[float, float, float, float]]): Lista de espaços já ocupados.

        Returns:
            bool: True se houver sobreposição, False caso contrário.
        """

        x_mob, y_mob = position
        for (x_occ, y_occ, width_occ, length_occ) in occupied_spaces:
            if (
                x_mob < x_occ + width_occ and
                x_mob + furniture_width > x_occ and
                y_mob < y_occ + length_occ and
                y_mob + furniture_length > y_occ
            ):
                return True
        return False

    def add_doors(self, neighboring_rooms: List['Room']) -> None:
        """
        Adiciona portas nas paredes que conectam este cômodo aos vizinhos.

        Args:
            neighboring_rooms (List[Room]): Lista de cômodos vizinhos.
        """

        for neighbor in neighboring_rooms:
            if self.is_adjacent(neighbor):
                door_position = self.find_shared_wall(neighbor)
                if door_position:
                    self.door_positions.append(door_position)

    def is_adjacent(self, other_room: 'Room') -> bool:
        """
        Verifica se este cômodo é adjacente a outro cômodo.

        Args:
            other_room (Room): Outro cômodo para verificar adjacência.

        Returns:
            bool: True se for adjacente, False caso contrário.
        """

        if self.floor != other_room.floor:
            return False
        # Verifica sobreposição de fronteiras
        if (
            self.x == other_room.x + other_room.width or
            self.x + self.width == other_room.x or
            self.y == other_room.y + other_room.length or
            self.y + self.length == other_room.y
        ):
            return True
        return False

    def find_shared_wall(self, other_room: 'Room') -> Optional[Tuple[float, float, float, float]]:
        """
        Encontra a posição para a porta na parede compartilhada com o outro cômodo.

        Args:
            other_room (Room): Outro cômodo com o qual compartilhará a parede.

        Returns:
            Optional[Tuple[float, float, float, float]]: Posição e dimensões da porta ou None.
        """

        if self.x == other_room.x + other_room.width:
            # Parede esquerda de self, direita de other_room
            door_x = self.x
            door_y = max(self.y, other_room.y) + min(self.length, other_room.length) / 2
            return (door_x, door_y, 0.1, 0.8)
        elif self.x + self.width == other_room.x:
            # Parede direita de self, esquerda de other_room
            door_x = self.x + self.width
            door_y = max(self.y, other_room.y) + min(self.length, other_room.length) / 2
            return (door_x, door_y, 0.1, 0.8)
        elif self.y == other_room.y + other_room.length:
            # Parede inferior de self, superior de other_room
            door_x = max(self.x, other_room.x) + min(self.width, other_room.width) / 2
            door_y = self.y
            return (door_x, door_y, 0.8, 0.1)
        elif self.y + self.length == other_room.y:
            # Parede superior de self, inferior de other_room
            door_x = max(self.x, other_room.x) + min(self.width, other_room.width) / 2
            door_y = self.y + self.length
            return (door_x, door_y, 0.8, 0.1)
        else:
            return None


class FloorPlan:
    def __init__(
        self,
        area: float,
        orientation: str,
        house_type: str,
        special_room: str,
        bedrooms: int,
        bathrooms: int,
        closets: int,
        rooms: Optional[List[Room]] = None
    ):
        """
        Classe que representa a planta da casa.

        Args:
            area (float): Área total da casa em metros quadrados.
            orientation (str): Orientação da casa (norte, sul, leste, oeste).
            house_type (str): Tipo da casa (ex: "2 andares e uma laje").
            special_room (str): Tipo de cômodo especial.
            bedrooms (int): Número de quartos.
            bathrooms (int): Número de banheiros.
            closets (int): Número de closets.
            rooms (Optional[List[Room]]): Lista de cômodos já existentes (opcional).
        """

        self.area: float = area
        self.orientation: str = orientation
        self.house_type: str = house_type
        self.special_room: str = special_room
        self.bedrooms: int = bedrooms
        self.bathrooms: int = bathrooms
        self.closets: int = closets

        self.house_width, self.house_length = self.generate_floor_dimensions()
        self.max_floor: int = 2 if '2 andares' in self.house_type else 1  # Número de andares

        self.rooms: List[Room] = rooms if rooms is not None else self.generate_random_rooms()

        self.fitness: float = self.calculate_fitness()

    def generate_random_rooms(self) -> List[Room]:
        """
        Gera os cômodos aleatoriamente, garantindo que estejam dentro dos limites e não se sobreponham.

        Returns:
            List[Room]: Lista de cômodos gerados.
        """

        rooms = []
        mandatory_rooms = [
            ("Cozinha", 1),
            ("Sala de Estar", 1),
            ("Sala de Jantar", 1),
            ("Área de Serviço", 1),
            ("Banheiro", 1),  # Social bathroom
            ("Quarto", self.bedrooms),
            ("Banheiro", self.bathrooms - 1),  # Remaining bathrooms
            ("Closet", self.closets),
            (self.special_room, 1),
        ]

        if '2 andares' in self.house_type:
            mandatory_rooms.append(("Escadas", 1))

        for room_type, quantity in mandatory_rooms:
            for _ in range(quantity):
                for attempt in range(100):
                    width, length = self.generate_room_dimensions(room_type)
                    if width > self.house_width or length > self.house_length:
                        continue  # Tenta novamente com dimensões diferentes
                    floor = random.randint(0, self.max_floor - 1)
                    x = random.uniform(0, self.house_width - width)
                    y = random.uniform(0, self.house_length - length)
                    new_room = Room(room_type, floor, x, y, width, length)
                    if not self.has_overlap(new_room, rooms):
                        rooms.append(new_room)
                        break
        return rooms

    def has_overlap(self, new_room: Room, rooms: List[Room]) -> bool:
        """
        Verifica se o novo cômodo sobrepõe algum cômodo existente.

        Args:
            new_room (Room): Novo cômodo a ser verificado.
            rooms (List[Room]): Lista de cômodos existentes.

        Returns:
            bool: True se houver sobreposição, False caso contrário.
        """

        for room in rooms:
            if room.floor == new_room.floor and self.check_overlap(room, new_room):
                return True
        return False

    def generate_floor_dimensions(self) -> Tuple[float, float]:
        """
        Gera as dimensões da planta com base na área total.

        Returns:
            Tuple[float, float]: Largura e comprimento da casa.
        """

        min_ratio = 0.5
        max_ratio = 2.0

        max_area = self.area
        ratio = random.uniform(min_ratio, max_ratio)

        house_length = math.sqrt(max_area * ratio)
        house_width = max_area / house_length

        return house_width, house_length

    def generate_room_dimensions(self, room_type: str) -> Tuple[float, float]:
        """
        Gera dimensões (largura e comprimento) para um cômodo, com base nos limites definidos.

        Args:
            room_type (str): Tipo do cômodo.

        Returns:
            Tuple[float, float]: Largura e comprimento do cômodo.
        """

        min_area, max_area = ROOMS.get(room_type, (6, 10))
        area = random.uniform(min_area, max_area)

        min_ratio = 0.5
        max_ratio = 2.0

        for _ in range(100):
            length = random.uniform(2, math.sqrt(area))
            width = area / length
            ratio = length / width
            if min_ratio <= ratio <= max_ratio:
                return width, length

        # Se não conseguir encontrar dimensões adequadas, retorna padrão
        return math.sqrt(min_area), math.sqrt(min_area)

    def allocate_mandatory_rooms(self, mandatory_rooms: List[Tuple[str, int]]) -> None:
        """
        Aloca os cômodos obrigatórios na planta, garantindo que não haja sobreposição.

        Args:
            mandatory_rooms (List[Tuple[str, int]]): Lista de tipos de cômodos e suas quantidades.
        """

        for room_type, quantity in mandatory_rooms:
            for _ in range(quantity):
                for _ in range(100):  # Limite de tentativas para evitar loop infinito
                    width, length = self.generate_room_dimensions(room_type)

                    floor = random.randint(0, self.max_floor - 1)

                    x = random.uniform(0, self.house_width - width)
                    y = random.uniform(0, self.house_length - length)

                    temp_room = Room(room_type, floor, x, y, width, length)

                    if not self.has_overlap(temp_room, self.rooms):
                        self.rooms.append(temp_room)
                        break

    def check_overlap(self, room1: Room, room2: Room) -> bool:
        """
        Verifica se dois cômodos se sobrepõem.

        Args:
            room1 (Room): Primeiro cômodo.
            room2 (Room): Segundo cômodo.

        Returns:
            bool: True se houver sobreposição, False caso contrário.
        """

        return not (
            room1.x + room1.width <= room2.x or
            room2.x + room2.width <= room1.x or
            room1.y + room1.length <= room2.y or
            room2.y + room2.length <= room1.y
        )

    def mark_grid(self, floor: int, x: float, y: float, width: float, length: float) -> None:
        """
        Marca o espaço ocupado pelo cômodo na grade.

        Args:
            floor (int): Andar do cômodo.
            x (float): Posição X do cômodo.
            y (float): Posição Y do cômodo.
            width (float): Largura do cômodo.
            length (float): Comprimento do cômodo.
        """

        x_start = int(x)
        y_start = int(y)

        x_end = int(x + width)
        y_end = int(y + length)

        for i in range(y_start, y_end):
            for j in range(x_start, x_end):
                self.grade[floor][i][j] = 1  # Assumindo que self.grade é uma estrutura pré-definida

    def unmark_grid(self, floor: int, x: float, y: float, width: float, length: float) -> None:
        """
        Desmarca o espaço ocupado pelo cômodo na grade (usado na mutação).

        Args:
            floor (int): Andar do cômodo.
            x (float): Posição X do cômodo.
            y (float): Posição Y do cômodo.
            width (float): Largura do cômodo.
            length (float): Comprimento do cômodo.
        """

        x_start = int(x)
        y_start = int(y)

        x_end = int(x + width)
        y_end = int(y + length)

        for i in range(y_start, y_end):
            for j in range(x_start, x_end):
                self.grade[floor][i][j] = 0  # Assumindo que self.grade é uma estrutura pré-definida

    def find_neighbors(self, current_room: Room) -> List[Room]:
        """
        Encontra os cômodos vizinhos ao current_room.

        Args:
            current_room (Room): Cômodo atual para encontrar vizinhos.

        Returns:
            List[Room]: Lista de cômodos vizinhos.
        """

        neighbors = []
        for room in self.rooms:
            if room != current_room and current_room.is_adjacent(room):
                neighbors.append(room)

        return neighbors

    def fill_empty_areas(self) -> None:
        """
        Preenche áreas vazias com pátios e corredores.

        Nota:
            Implementação opcional.
        """

        pass

    def calculate_fitness(self) -> float:
        """
        Calcula o valor de fitness da planta.

        Returns:
            float: Valor de fitness da planta.
        """

        fitness = 0

        num_overlaps = self.count_overlaps()
        num_out_of_bounds = self.count_out_of_bounds()
        num_missing_rooms = self.check_all_rooms_present()

        if num_overlaps > 0 or num_out_of_bounds > 0 or num_missing_rooms > 0:
            # Penaliza fortemente plantas inválidas
            fitness -= (num_overlaps * 1000 + num_out_of_bounds * 1000 + num_missing_rooms * 1000)
            return fitness  # Retorna cedo pois a planta é inválida

        # Se a planta é válida, avalia outros critérios
        fitness += self.evaluate_area_utilization()
        fitness += self.evaluate_area_separation()
        fitness += self.evaluate_natural_light()
        fitness += self.evaluate_external_connections()
        fitness += self.evaluate_staircase_position()

        return fitness

    def count_overlaps(self) -> int:
        """
        Conta o número de sobreposições entre os cômodos.

        Returns:
            int: Número de sobreposições.
        """

        overlaps = 0
        for i, room1 in enumerate(self.rooms):
            for room2 in self.rooms[i+1:]:
                if room1.floor == room2.floor and self.check_overlap(room1, room2):
                    overlaps += 1

        return overlaps

    def count_out_of_bounds(self) -> int:
        """
        Conta quantos cômodos estão fora dos limites da planta.

        Returns:
            int: Número de cômodos fora dos limites.
        """

        out_of_bounds = 0
        for room in self.rooms:
            if (room.x < 0 or room.y < 0 or
                room.x + room.width > self.house_width or
                    room.y + room.length > self.house_length):
                out_of_bounds += 1

        return out_of_bounds

    def check_all_rooms_present(self) -> int:
        """
        Verifica se todos os cômodos obrigatórios estão presentes.

        Returns:
            int: Número de cômodos faltantes.
        """

        required_types = {
            "Cozinha": 1,
            "Sala de Estar": 1,
            "Sala de Jantar": 1,
            "Área de Serviço": 1,
            "Banheiro": self.bathrooms,
            "Quarto": self.bedrooms,
            "Closet": self.closets,
            self.special_room: 1,
        }

        if '2 andares' in self.house_type:
            required_types["Escadas"] = 1

        present_types = {}
        for room in self.rooms:
            present_types[room.type] = present_types.get(room.type, 0) + 1

        missing = 0
        for room_type, quantity in required_types.items():
            if present_types.get(room_type, 0) < quantity:
                missing += quantity - present_types.get(room_type, 0)

        return missing

    def evaluate_area_utilization(self) -> float:
        """
        Avalia a porcentagem de área utilizada na planta.

        Returns:
            float: Porcentagem de área utilizada.
        """

        area_used = 0
        for floor in range(self.max_floor):
            area_used += sum(sum(row) for row in self.grade[floor])  # Assumindo que self.grade é uma grade binária

        total_area = self.house_width * self.house_length * self.max_floor

        return (area_used / total_area) * 100

    def evaluate_area_separation(self) -> float:
        """
        Avalia a separação entre áreas sociais e íntimas.

        Returns:
            float: Pontuação da separação de áreas.
        """

        score = 0

        social_areas = ["Sala de Estar", "Sala de Jantar", "Cozinha"]
        private_areas = ["Quarto", "Banheiro", "Closet"]

        for room in self.rooms:
            if room.type in social_areas:
                for other_room in self.rooms:
                    if other_room.type in private_areas:
                        distance = self.calculate_distance(room, other_room)
                        if distance < 3:
                            score -= 10  # Penaliza se áreas sociais e íntimas estão próximas
            else:
                score += 10  # Valoriza áreas privadas isoladas

        return score

    def calculate_distance(self, room1: Room, room2: Room) -> float:
        """
        Calcula a distância entre dois cômodos.

        Args:
            room1 (Room): Primeiro cômodo.
            room2 (Room): Segundo cômodo.

        Returns:
            float: Distância entre os cômodos. Retorna infinito se estiverem em andares diferentes.
        """

        if room1.floor != room2.floor:
            return float('inf')  # Não considerar distância entre andares diferentes

        x1 = room1.x + room1.width / 2
        y1 = room1.y + room1.length / 2
        x2 = room2.x + room2.width / 2
        y2 = room2.y + room2.length / 2

        return math.hypot(x1 - x2, y1 - y2)

    def evaluate_natural_light(self) -> float:
        """
        Avalia a proximidade dos cômodos com as paredes externas para iluminação natural.

        Returns:
            float: Pontuação da iluminação natural.
        """

        score = 0
        for room in self.rooms:
            if self.is_near_external_walls(room):
                score += 20  # Valoriza cômodos próximos às paredes externas

        return score

    def is_near_external_walls(self, room: Room) -> bool:
        """
        Verifica se o cômodo está próximo das paredes externas.

        Args:
            room (Room): Cômodo a ser verificado.

        Returns:
            bool: True se estiver próximo, False caso contrário.
        """

        margin = 1  # Considerar margem de 1 metro
        if (
            room.x <= margin or
            room.x + room.width >= self.house_width - margin or
            room.y <= margin or
            room.y + room.length >= self.house_length - margin
        ):
            return True

        return False

    def evaluate_external_connections(self) -> float:
        """
        Avalia se os cômodos têm portas conectando ao exterior.

        Returns:
            float: Pontuação das conexões externas.
        """

        score = 0
        exterior_connected_rooms = ["Sala de Estar", "Cozinha"]

        for room in self.rooms:
            if room.type in exterior_connected_rooms:
                if self.is_near_external_walls(room):
                    score += 30  # Valoriza cômodos conectados externamente

        return score

    def evaluate_staircase_position(self) -> float:
        """
        Avalia a posição das escadas na planta.

        Returns:
            float: Pontuação da posição das escadas.
        """

        score = 0
        staircases = [room for room in self.rooms if room.type == "Escadas"]

        center_x = self.house_width / 2
        center_y = self.house_length / 2

        for staircase in staircases:
            distance_to_center = self.calculate_distance_to_center(staircase, center_x, center_y)
            score += max(0, 10 - distance_to_center) * 10  # Valoriza escadas próximas ao centro

        return score

    def calculate_distance_to_center(self, room: Room, center_x: float, center_y: float) -> float:
        """
        Calcula a distância do cômodo até o centro da planta.

        Args:
            room (Room): Cômodo a ser medido.
            center_x (float): Coordenada X do centro.
            center_y (float): Coordenada Y do centro.

        Returns:
            float: Distância até o centro.
        """

        room_center_x = room.x + room.width / 2
        room_center_y = room.y + room.length / 2

        return math.hypot(room_center_x - center_x, room_center_y - center_y)
