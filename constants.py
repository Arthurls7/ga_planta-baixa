from typing import Dict, List, Tuple

ROOMS: Dict[str, Tuple[int, int]] = {
    "Quarto": (12, 30),
    "Banheiro": (3, 8),
    "Cozinha": (10, 15),
    "Sala de Estar": (30, 40),
    "Sala de Jantar": (15, 20),
    "Área de Serviço": (6, 10),
    "Sala de Jogos": (20, 30),
    "Closet": (3, 4),
    "Escritório": (6, 10),
    "Sala de Música": (20, 30),
    "Sala de Ginástica": (20, 30),
    "Corredor": (2, 10),
    "Pátio": (2, 20),
    "Escadas": (4, 5),
}

FURNITURES: Dict[str, List[Tuple[str, float, float]]] = {
    "Sala de Estar": [
        ("Sofá de 2 lugares", 0.82, 1.72),
        ("Sofá de 3 lugares", 0.82, 2.10),
        ("Poltrona", 0.70, 0.80),
        ("Mesa de Café", 1.00, 0.60),
        ("Mesa Lateral", 0.43, 0.40),
    ],
    "Sala de Jantar": [
        ("Mesa de 4 lugares", 0.90, 0.90),
        ("Mesa de 6 lugares", 1.60, 0.90),
        ("Buffet", 0.90, 0.36),
        ("Vitrine", 0.34, 0.84),
    ],
    "Quarto": [
        ("Cama de Casal", 1.44, 1.93),
        ("Cama de Solteiro", 0.94, 1.93),
        ("Mesa de Cabeceira", 0.43, 0.40),
        ("Guarda-roupa de 2 portas", 0.40, 1.00),
        ("Guarda-roupa de 3 portas", 0.40, 1.70),
        ("Cômoda", 0.40, 0.87),
    ],
    "Cozinha": [
        ("Fogão de 4 bocas", 0.58, 0.68),
        ("Fogão de 5 bocas", 0.77, 0.68),
        ("Geladeira de 1 porta", 0.62, 0.75),
        ("Geladeira de 2 portas", 0.83, 0.79),
        ("Armário", 0.34, 1.68),
        ("Pia", 1.00, 0.50),
    ],
    "Banheiro": [
        ("Vaso Sanitário", 0.37, 0.64),
        ("Banheira", 0.71, 1.65),
        ("Pia com Armário", 0.70, 0.45),
        ("Box de Chuveiro", 1.50, 2.00),
    ],
    "Área de Serviço": [
        ("Máquina de Lavar", 0.60, 0.65),
        ("Pia", 0.52, 0.53),
    ],
    "Sala de Jogos": [
        ("Mesa de Sinuca", 1.37, 2.44),
        ("Mesa de Ping Pong", 1.52, 2.74),
        ("Sofá", 0.82, 2.10),
        ("Estante", 0.40, 1.80),
    ],
    "Closet": [
        ("Estante", 0.50, 1.00),
        ("Cabideiro", 0.50, 1.50),
    ],
    "Escritório": [
        ("Mesa de Escritório", 0.80, 1.60),
        ("Cadeira de Escritório", 0.60, 0.60),
        ("Estante de Livros", 0.30, 1.20),
    ],
    "Sala de Música": [
        ("Piano", 1.50, 1.00),
        ("Bateria", 1.50, 1.50),
        ("Amplificador", 0.50, 0.50),
    ],
    "Sala de Ginástica": [
        ("Esteira", 0.80, 1.80),
        ("Bicicleta de Exercício", 0.50, 1.00),
        ("Máquina de Pesos", 2.00, 2.00),
    ],
}
