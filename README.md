# GA Planta Baixa

**GA Planta Baixa** é um projeto que utiliza algoritmos genéticos para gerar plantas de casas personalizadas. Com base em entradas fornecidas pelo usuário, como nome completo, área da casa e orientação, o sistema gera layouts otimizados que atendem a diversos critérios de design e funcionalidade.

## Tabela de Conteúdos

- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Detalhes do Algoritmo Genético](#detalhes-do-algoritmo-genético)
- [Geração da Planta Baixa](#geração-da-planta-baixa)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Características

- **Geração Automática de Plantas:** Cria layouts de casas com base em parâmetros definidos pelo usuário.
- **Algoritmo Genético:** Utiliza técnicas evolutivas para otimizar o design da planta.
- **Visualização Gráfica:** Desenha a planta gerada com detalhes de cômodos, portas, janelas e mobílias.
- **Personalização:** Ajusta características como número de quartos, banheiros, closets e cômodos especiais com base no nome do usuário.

## Tecnologias Utilizadas

- **Python 3.8+**
- **Bibliotecas:**
  - `numpy`
  - `matplotlib`

## Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento e instalar as dependências necessárias:

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/seu-usuario/ga_planta-baixa.git
   cd ga_planta-baixa
   ```

2. **Crie um Ambiente Virtual:**

   ```bash
   python -m venv .venv
   ```

3. **Ative o Ambiente Virtual:**

   - **Windows:**

     ```bash
     .\\.venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source .venv/bin/activate
     ```

4. **Instale as Dependências:**

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Execute o script principal para iniciar o processo de geração da planta baixa:

```bash
python main.py
```

### Passos:

1. **Entrada do Usuário:**

   - **Nome Completo:** Forneça o nome completo do membro com o maior número de caracteres.
   - **Área da Casa:** Insira a área total da casa em metros quadrados (m²).
   - **Orientação da Casa:** Especifique a orientação da casa (norte, sul, leste, oeste).

2. **Processamento:**

   - O sistema calculará características da casa com base no nome fornecido.
   - Executará o algoritmo genético para gerar a planta baixa otimizada.

3. **Saída:**
   - Visualização gráfica da planta baixa gerada.
   - Informações detalhadas sobre os cômodos e fitness da planta.

## Estrutura do Projeto

```
ga_planta-baixa/
├── constants.py
├── genetic_algorithm.py
├── models.py
├── utils.py
├── main.py
├── requirements.txt
└── README.md
```

- **constants.py:** Define constantes como tipos de cômodos e mobílias disponíveis.
- **genetic_algorithm.py:** Implementa as funções do algoritmo genético, incluindo seleção, crossover, mutação e o ciclo evolutivo.
- **models.py:** Contém as classes `Room` e `FloorPlan` que representam os elementos da planta baixa.
- **utils.py:** Funções utilitárias, como o cálculo de características com base no nome do usuário.
- **main.py:** Ponto de entrada do programa que coordena a entrada do usuário, execução do algoritmo genético e visualização da planta.
- **requirements.txt:** Lista de dependências do projeto.

## Detalhes do Algoritmo Genético

O algoritmo genético implementado no projeto segue os princípios básicos da evolução natural para otimizar a planta baixa:

1. **População Inicial:**

   - Gera uma população inicial de plantas baixas aleatórias que atendem aos critérios básicos.

2. **Avaliação de Fitness:**

   - Cada planta é avaliada com base em múltiplos critérios, como utilização de área, separação de áreas sociais e íntimas, iluminação natural, conexões externas e posição das escadas.

3. **Seleção:**

   - Seleciona os indivíduos com melhor fitness para reprodução, utilizando métodos de seleção ponderada.

4. **Crossover:**

   - Combina características de dois pais para gerar descendentes, assegurando a validade da planta resultante.

5. **Mutação:**

   - Introduz variações aleatórias nas plantas para explorar novas soluções e evitar convergência prematura.

6. **Iteração:**
   - Repete os processos de seleção, crossover e mutação por um número definido de gerações, mantendo a melhor planta encontrada.

## Geração da Planta Baixa

A geração da planta baixa envolve os seguintes passos:

1. **Definição dos Cômodos:**

   - Baseado nas características calculadas a partir do nome do usuário, define o tipo e quantidade de cômodos necessários (quartos, banheiros, cômodos especiais, etc.).

2. **Posicionamento dos Cômodos:**

   - Distribui os cômodos dentro dos limites da casa, evitando sobreposições e respeitando as dimensões definidas.

3. **Adição de Portas e Janelas:**

   - Insere portas entre cômodos adjacentes e janelas nas paredes externas para permitir iluminação natural.

4. **Inserção de Mobílias:**

   - Posiciona mobílias dentro dos cômodos de acordo com os tipos e dimensões especificadas.

5. **Visualização:**
   - Utiliza o `matplotlib` para desenhar a planta baixa, destacando cada cômodo com cores distintas e indicando a disposição das portas, janelas e mobílias.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

1. **Fork o Repositório**
2. **Crie uma Branch para sua Feature:**

   ```bash
   git checkout -b feature/nova-feature
   ```

3. **Commit suas Alterações:**

   ```bash
   git commit -m "Adiciona nova feature"
   ```

4. **Push para a Branch:**

   ```bash
   git push origin feature/nova-feature
   ```

5. **Abra um Pull Request**

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
