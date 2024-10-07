from typing import List, Tuple

LETTER_TABLE = {
    'a': 1, 'e': 3, 'i': 2, 'n': 1, 'r': 14, 'v': 13, 'y': 10,
    'b': 2, 'f': 4, 'j': 11, 'o': 10, 's': 9, 'x': 12,
    'c': 3, 'g': 5, 'l': 6, 'p': 7, 't': 8, 'z': 11,
    'd': 4, 'h': 5, 'm': 6, 'q': 7, 'u': 8, 'w': 9
}


def calculate_characteristics(full_name: str) -> Tuple[int, int, int]:
    """
    Calculate the characteristics of the house based on the provided full name.

    Args:
        full_name (str): The full name to be analyzed.

    Returns:
        Tuple[int, int, int]: A tuple containing three integers representing the characteristics.
    """
    # Converte o nome completo para minúsculas e divide em partes
    names: List[str] = full_name.lower().split()
    results: List[int] = []

    # Calcula a soma dos valores das letras para cada parte do nome
    for name in names:
        total = sum(LETTER_TABLE.get(letter, 0) for letter in name if letter.isalpha())
        results.append(total)

    # Calcula os restos das divisões conforme especificado
    remainder1 = results[0] % 3 if len(results) > 0 else 0
    remainder2 = results[1] % 4 if len(results) > 1 else 0
    remainder3 = results[2] % 4 if len(results) > 2 else 0

    return remainder1, remainder2, remainder3
