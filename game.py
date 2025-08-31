
TILE_SIZE = 64
ROWS = 30
COLS = 15

# Definir o tamanho e nome da janela
WIDTH = TILE_SIZE * ROWS # Largura X
HEIGHT = TILE_SIZE * COLS # Altura Y
TITLE = "Jogo de Plataforma" # Nome da Janela

# Criando e posicionando nosso herói
hero = Actor("hero")
hero.pos = WIDTH / 2 , HEIGHT / 2 # Centro da Tela

# Desenhar elementos na tela
def draw():
    # Limpando elementos da tela
    screen.clear()
    # Preenchendo a tela de azul celeste
    screen.fill("skyblue")
    # Desenhar o herói
    hero.draw()

def update():
    pass