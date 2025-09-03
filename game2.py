# Constantes de tiles
TILE_SIZE = 64 # Cada tijolinho tem 64 pixels
ROWS = 15 # Quantidade de linhas
COLS = 30 # Quantidade de colunas

# Definir o tamanho e nome da janela
WIDTH = TILE_SIZE * COLS # Largura X
HEIGHT = TILE_SIZE * ROWS # Altura Y
TITLE = "Jogo de Plataforma" # Nome da Janela

# Constantes da física do jogo
GRAVITY = 0.5 # Gravidade
Y_SPEED_START = 0 # Velocidade Y inicial
X_SPEED_START = 0 # Velocidade X inicial
JUMP_FORCE = -15 # Força do pulo
X_SPEED = 5 # Velocidade horizontal do herói.

# Criando e posicionando nosso herói
hero_start_position = TILE_SIZE, HEIGHT / 2
hero = Actor("hero")
hero.pos = hero_start_position
hero.vy = Y_SPEED_START # Definindo a velocidade vertical
hero.vx = X_SPEED_START # Definindo a velocidade horizontal
hero.on_ground = False # Adicionado para controlar o pulo

#---------------  FUNÇÃO DE CONSTRUÇÃO DA FASE ---------------------
# Construir os elementos antes de desenhar
def build(filename, tile_size):
    # Abrindo o arquivo como leitura
    with open(filename, "r") as f:
        # Extraindo o conteúdo e quebrando linhas
        contents = f.read().splitlines()
    
    # Quebrando as linhas
    contents = [c.split(",") for c in contents]
    
    # Percorrendo cada uma das linhas entre as disponíveis
    for row in range(len(contents)):
        # Percorrendo cada coluna dessa linha
        for col in range(len(contents[0])):
            # Extrair o elemento de cada linha e coluna
            val = contents[row][col]
            # Testar se o valor na posição é valido
            if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
                contents[row][col] = int(val)
    
    # Criação dos itens que serão construidos
    items = []

    # Caminhando pelas linhas
    for row in range(len(contents)):
        # Caminhando pelas colunas
        for col in range(len(contents[0])):
            # Extraindo o elemento da posição
            tile_num = contents[row][col]
            # Verificar se o espaço não é vazio
            if tile_num != -1:
                # Criação dos Actors
                item = Actor(f"tiles/tile_{tile_num:04d}")
                # Posicionar os Actors
                item.topleft = (tile_size * col, tile_size * row)
                # Reunindo todos os itens
                items.append(item)
    return items

#-------------------------------------------------------------------#


# Lendo os arquivos das plataformas e obstáculos
platforms = build("mapa_plataformas.csv", TILE_SIZE)
obstacles = build("mapa_obstaculos.csv", TILE_SIZE)

# ----------------- FUNÇÕES DE COLISÃO -----------------------

# Função de colisão horizontal com plataformas
def move_and_collide_x():
    hero.x += hero.vx
    for tile in platforms:
        if hero.colliderect(tile):
            if hero.vx > 0:
                hero.right = tile.left
            elif hero.vx < 0:
                hero.left = tile.right
            hero.vx = 0 # Para o movimento horizontal ao colidir


# Função de colisão vertical com plataformas
def move_and_collide_y():
    hero.y += hero.vy
    hero.on_ground = False # Presume que o herói está no ar
    for tile in platforms:
        if hero.colliderect(tile):
            if hero.vy > 0:
                hero.bottom = tile.top
                hero.vy = 0
                hero.on_ground = True # Confirma que o herói está no chão
            elif hero.vy < 0:
                hero.top = tile.bottom
                hero.vy = 0 # Zera a velocidade para não grudar no teto

# ------------------------------------------------------------
    

# Desenhar elementos na tela
def draw():
    # Limpando elementos da tela
    screen.clear()
    # Preenchendo a tela de azul celeste
    screen.fill("skyblue")
    # Desenhar o herói
    hero.draw()
    # Desenhar cada elemento de plataforma na tela
    for platform in platforms:
        platform.draw()
    # Desenhar cada elemento dos obstáculos
    for obstacle in obstacles:
        obstacle.draw()
    


# Atualizar cada frame
def update():
    # Movimento Horizontal
    if keyboard.left:
        hero.vx = -X_SPEED
    elif keyboard.right:
        hero.vx = X_SPEED
    else:
        hero.vx = 0
    
    move_and_collide_x()

    # Movimento Vertical e Gravidade
    hero.vy += GRAVITY
    move_and_collide_y()

    # Pulo
    if keyboard.space and hero.on_ground:
        hero.vy = JUMP_FORCE

    # Colisão com obstáculos (exemplo de reset)
    for obstacle in obstacles:
        if hero.colliderect(obstacle):
            hero.pos = hero_start_position