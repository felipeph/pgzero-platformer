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
# Função de colisão com plataformas
def collision_platform_y():

    # Definindo o estado da colisão como falso
    platform_under = False # Não está acima da plataforma
    platform_over = False # Não está abaixo da plataforma
    platform_left = False # Não está abaixo da plataforma
    platform_right = False # Não está abaixo da plataforma

    # Olhar em cada tile de cada a plataforma
    for tile in platforms:
        # Se o herói colidir com qualquer tile
        if hero.colliderect(tile):
            
            # Se o herói estiver caindo (velocidade y > 0)
            if hero.vy > 0:
                # Colocar a base do herói no topo do tile
                hero.bottom = tile.top
                # Fazer ele parar de cair
                hero.vy = 0
                # Avisar que está em cima de uma plataforma
                platform_under = True
                
            # Senão estiver caindo, ainda pode estar subindo ou parado
            # Se o herói estiver subindo (velocidade y < 0)
            elif hero.vy < 0:
                # Colocar a cabeça do herói na base da plataforma
                hero.top = tile.bottom 
                # Fazer ele começar a cair
                hero.vy = 0
                platform_over = True
            
            elif hero.vx > 0:
                hero.right = tile.left
                hero.vx = 0
                platform_left = True
            elif hero.vx < 0:
                hero.left = tile.right
                hero.vx = 0
                platform_right = True

    return platform_under, platform_over, platform_left, platform_right
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
    # Definir a velocidade vertical com a gravidade
    hero.vy = hero.vy + GRAVITY # Velocidade vertical atual mais gravidade

    # Mudar a posição vertical do herói de acordo com a velocidade
    hero.y = hero.y + hero.vy # Posição vertical atual mais velocidade vertical
    
    # Verificar colisão por cima ou por baixo da plataforma
    platform_under, platform_over, platform_left, platform_right = collision_platform_y()

    # Se o usuário teclar a barra de espaço
    if keyboard.space:
        # Permitir pulo apenas se estiver sobre plataforma
        if platform_under:
            # Muda instantaneamente a velocidade vertical para o pulo
            hero.vy = JUMP_FORCE   
    
    # Resetando a velocidade horizontal
    hero.vx = 0

    # Verificar o toque nas teclas de seta
    # Pressionando a tecla esquerda do teclado
    if keyboard.left:
        if platform_left:
            hero.vx = 0
        else: 
            hero.vx = -X_SPEED # Velocidade para esquerda é negativa
    
    # Pressionando a tecla direita do teclado
    if keyboard.right:
        if platform_right:
            hero.vx = 0
        else:
            hero.vx = X_SPEED # Velocidade para direita positiva
    
    # Atualizando a posição horizontal do herói
    hero.x = hero.x + hero.vx

        

