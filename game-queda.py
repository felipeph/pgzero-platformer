# Constantes de tiles
TILE_SIZE = 64
ROWS = 15
COLS = 30

# Definir o tamanho e nome da janela
WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS
TITLE = "Jogo de Plataforma"

# Constantes da física do jogo
GRAVIDADE = 0.5
VELOCIDADE_Y_INICIAL = 0
VELOCIDADE_X = 5
FORCA_PULO = -15

# Criando e posicionando nosso herói
hero = Actor("hero")
hero.pos = TILE_SIZE , HEIGHT / 2
hero.vy = VELOCIDADE_Y_INICIAL
hero.vx = 0

# --- NOVA FUNÇÃO PARA REINICIAR O JOGO ---
def reiniciar_jogo():
    """ Coloca o herói de volta na posição inicial e zera suas velocidades. """
    hero.pos = TILE_SIZE, HEIGHT / 2
    hero.vy = VELOCIDADE_Y_INICIAL
    hero.vx = 0

# Construir os elementos antes de desenhar
def build(filename, tile_size):
    # (Seu código da função build continua igual)
    with open(filename, "r") as f:
        contents = f.read().splitlines()
    
    contents = [c.split(",") for c in contents]
    
    for row in range(len(contents)):
        for col in range(len(contents[0])):
            val = contents[row][col]
            if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
                contents[row][col] = int(val)
    
    items = []

    for row in range(len(contents)):
        for col in range(len(contents[0])):
            tile_num = contents[row][col]
            if tile_num != -1:
                item = Actor(f"tiles/tile_{tile_num:04d}")
                item.topleft = (tile_size * col, tile_size * row)
                items.append(item)
    return items

# Lendo os arquivos das plataformas e obstáculos
platforms = build("mapa_plataformas.csv", TILE_SIZE)
obstacles = build("mapa_obstaculos.csv", TILE_SIZE)
tiles_solidos = platforms + obstacles

# Desenhar elementos na tela
def draw():
    # (Seu código da função draw continua igual)
    screen.clear()
    screen.fill("skyblue")
    hero.draw()
    for platform in platforms:
        platform.draw()
    for obstacle in obstacles:
        obstacle.draw()

# Funções para tratar as colisões
def checar_colisao_vertical():
    # (Seu código da função checar_colisao_vertical continua igual)
    for tile in tiles_solidos:
        if hero.colliderect(tile):
            if hero.vy > 0:
                hero.bottom = tile.top
                hero.vy = 0
            elif hero.vy < 0:
                hero.top = tile.bottom
                hero.vy = 0

def checar_colisao_horizontal():
    # (Seu código da função checar_colisao_horizontal continua igual)
    for tile in tiles_solidos:
        if hero.colliderect(tile):
            if hero.vx > 0:
                hero.right = tile.left
            elif hero.vx < 0:
                hero.left = tile.right

# Atualizar cada frame
def update():
    # --- Lógica de Movimento ---
    hero.vx = 0
    
    if keyboard.left:
        hero.vx = -VELOCIDADE_X
    if keyboard.right:
        hero.vx = VELOCIDADE_X
    
    if keyboard.space:
        hero.y += 1
        plataformas_embaixo = hero.collidelistall(tiles_solidos)
        hero.y -= 1
        if plataformas_embaixo:
             hero.vy = FORCA_PULO

    # --- ADICIONADO: Checagem da tecla de reinício ---
    if keyboard.r:
        reiniciar_jogo()

    # --- Lógica da Física e Colisão ---
    hero.vy += GRAVIDADE
    
    hero.y += hero.vy
    checar_colisao_vertical()

    hero.x += hero.vx
    checar_colisao_horizontal()