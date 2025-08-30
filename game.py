# Definir o tamanho da janela
# Largura de 640 pixels
WIDTH = 640
# Altura de 480 pixels
HEIGHT = 480

# Nome da Janela
TITLE = "Jogo de Plataforma"

# Criando o nosso herói
hero = Actor("hero")

# Posicionando o herói no centro da tela
hero.pos = WIDTH / 2 , HEIGHT / 2

# Desenhar elementos na tela
def draw():
    # Limpando elementos da tela
    screen.clear()
    # Preenchendo a tela de azul celeste
    screen.fill("skyblue")
    # Desenhar o herói
    hero.draw()