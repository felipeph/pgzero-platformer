# Constantes de tiles
TILE_SIZE = 64 # Cada tijolinho tem 64 pixels
ROWS = 15 # Quantidade de linhas
COLS = 30 # Quantidade de colunas

# Definir o tamanho e nome da janela
WIDTH = TILE_SIZE * COLS # Largura X
HEIGHT = TILE_SIZE * ROWS # Altura Y
TITLE = "Jogo de Plataforma" # Nome da Janela

# Criando e posicionando nosso herói
hero = Actor("hero")
hero.pos = WIDTH / 2 , HEIGHT / 2 # Centro da Tela

# Construir os elementos antes de desenhar
def build(filename, tile_size):
    # Abrindo o arquivo como leitura
    with open(filename, "r") as f:
        # Extraindo o conteúdo e quebrando linhas
        contents = f.read().splitlines()
    return contents

# Lendo o arquivo das plataformas
platforms = build("mapa_plataformas.csv", TILE_SIZE)

# Imprimir o conteúdo das plataformas
print(platforms)

# Desenhar elementos na tela
def draw():
    # Limpando elementos da tela
    screen.clear()
    # Preenchendo a tela de azul celeste
    screen.fill("skyblue")
    # Desenhar o herói
    hero.draw()

# Atualizar cada frame
def update():
    pass