
# ---------------- CONSTANTES ----------------------------

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

# Constantes de animação
HERO_IDLE_SPEED = 0.1
HERO_WALK_SPEED = 0.1

# --------------------------------------------------------


# ----------- CRIAÇÃO DO HEROI ---------------------------

# Criando e posicionando nosso herói
hero_start_position = TILE_SIZE, HEIGHT / 2
hero = Actor("hero_idle_1")
hero.pos = hero_start_position
hero.vy = Y_SPEED_START # Definindo a velocidade vertical
hero.vx = X_SPEED_START # Definindo a velocidade horizontal
hero_height_start = hero.height

# --------------------------------------------------------






#----------  FUNÇÃO DE CONSTRUÇÃO DA FASE ----------------
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


# Lendo os arquivos das plataformas e obstáculos
platforms = build("mapa_plataformas.csv", TILE_SIZE)
obstacles = build("mapa_obstaculos.csv", TILE_SIZE)

#-------------------------------------------------------------------#







# ----------------- FUNÇÕES DE COLISÃO -----------------------

# Função de colisão horizontal com plataformas
def collision_platform_x():

    # Estados iniciais
    platform_left = False # Não encosta na esquerda da plataforma
    platform_right = False # Não enconsta a direita da plataforma

    # Olhando cada tile em cada plataforma
    for tile in platforms:
        # Se o herói colidir com um tile
        if hero.colliderect(tile):
            # Se herói indo para a esquerda
            if hero.vx < 0:
                # Colocar o herói colado na plataforma
                hero.left = tile.right
                # Encostou na esquerda da plataforma
                platform_left = True
            # Se o herói está indo para a direita
            elif hero.vx > 0:
                # Colar o heroi na plataforma
                hero.right = tile.left 
                # Encostou na direita da plataforma
                platform_right = True
    return platform_left, platform_right


# Função de colisão vertical com plataformas
def collision_platform_y():

    # Definindo o estado da colisão como falso
    platform_under = False # Não está acima da plataforma
    platform_over = False # Não está abaixo da plataforma

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

    return platform_under, platform_over

# ------------------------------------------------------------







# ---------- CRIANDO LISTAS DE IMAGENS PARA ANIMAÇÃO ----------

# Função de geração da lista por actor e animation
def animation_images_list(actor, animation, list_size):
    # Começamos criando uma lista vazia
    images_list=[]
    # Percorremos cada índice do menor que o tamanho da lista
    for i in range(list_size):
        # Acrescentamos na lista cada imagem no formato indicado
        images_list.append(f'{actor}_{animation}_{i}')

    return images_list


# Lista de imagens da animação idle do hero
hero_idle_images = animation_images_list('hero', 'idle', 18)

# Lista de imagens da animação de caminhar para direita do hero
hero_walk_right_images = animation_images_list('hero', 'walk_right', 2)

# Lista de imagens da animação de caminhar para esquerda do hero
hero_walk_left_images = animation_images_list('hero', 'walk_left', 2)


# ----------------------------------------------------------------





# ---------- FUNÇÕES DE ANIMACÕES ---------------------------------

# ---------- ANIMAÇÃO IDLE DO HERO --------------------------------

# Definindo o primeiro frame da animação
hero_idle_frame = 0

# Criando a função de animação sem parâmetros
def animate_hero_idle():
    # Resgatando a variável do frame inicial
    global hero_idle_frame

    # Condições para execução da animação
    # Herói sem velocidade horizontal nem vertical
    if hero.vx == 0 and hero.vy == 0:
        # Avança para o próximo quadro da animação
        # O operador '%' (módulo) faz com que a contagem volte a 0 quando chegar ao fim da lista.
        hero_idle_frame = (hero_idle_frame + 1) % len(hero_idle_images)
        
        # Atualiza a imagem do herói para a imagem do quadro atual.
        hero.image = hero_idle_images[hero_idle_frame]

# Agenda a execução da animação em um dado intervalo de tempo (segundos)
clock.schedule_interval(animate_hero_idle, HERO_IDLE_SPEED)

# -----------FIM ANIMAÇÃO IDLE DO HERO -------------------------------





# ---------- ANIMAÇÃO DE CAMINHADA DO HERO ---------------------------
# Definindo o primeiro frame da animação
hero_walk_frame = 0

# Criando a função de animação sem parâmetros
def animate_hero_walk():
    # Resgatando a variável do frame inicial
    global hero_walk_frame

    # A animação só deve acontecer se o herói estiver realmente andando.
    # Condições para andar para a direita
    if hero.vy == 0 and hero.vx > 0:
        # Avança para o próximo quadro da animação
        # O operador '%' (módulo) faz com que a contagem volte a 0 quando chegar ao fim da lista.
        hero_walk_frame = (hero_walk_frame + 1) % len(hero_walk_right_images)
        
        # Atualiza a imagem do herói para a imagem do quadro atual.
        hero.image = hero_walk_right_images[hero_walk_frame]
    
    # Condições para andar para a esquerda
    elif hero.vy == 0 and hero.vx < 0:
        # Avança para o próximo quadro da animação
        # O operador '%' (módulo) faz com que a contagem volte a 0 quando chegar ao fim da lista.
        hero_walk_frame = (hero_walk_frame + 1) % len(hero_walk_left_images)
        
        # Atualiza a imagem do herói para a imagem do quadro atual.
        hero.image = hero_walk_left_images[hero_walk_frame]

# Agenda a execução da animação em um dado intervalo de tempo (segundos)
clock.schedule_interval(animate_hero_walk, HERO_WALK_SPEED)

# ---------- FIM ANIMAÇÃO DE CAMINHADA DO HERO ---------------------------







# ---------- DESENHANDO ELEMENTOS NA TELA --------------------------------
def draw():
    # Limpando elementos da tela
    screen.clear()
    # Preenchendo a tela de azul celeste
    screen.fill("skyblue")

    # Desenhar cada elemento de plataforma na tela
    for platform in platforms:
        platform.draw()
    # Desenhar cada elemento dos obstáculos
    for obstacle in obstacles:
        obstacle.draw()

    # Desenhar o herói
    hero.draw()

# ---------- FIM DESENHANDO ELEMENTOS NA TELA -----------------------------

    


# ---------- ATUALIZANDO ELEMENTOS NA TELA --------------------------------

def update():

# ---------------- GRAVIDADE E COLISÕES VERTICAIS ----------------------
    # Definir a velocidade vertical com a gravidade
    hero.vy = hero.vy + GRAVITY # Velocidade vertical atual mais gravidade

    # Mudar a posição vertical do herói de acordo com a velocidade
    hero.y = hero.y + hero.vy # Posição vertical atual mais velocidade vertical
    
    # Verificar colisão por cima ou por baixo da plataforma
    platform_under, platform_over = collision_platform_y()

# ---------------- FIM GRAVIDADE E COLISÕES VERTICAIS --------------------



# ---------------- SALTO DO HEROI ----------------------------------------

    # Física do pulo do herói
    # Verifica se a barra de espaço foi tocada
    if keyboard.space:
        # Verifica se ele está em cima de uma plataforma
        if platform_under:
            # Muda a velocidade vertical para executar o pulo
            hero.vy = JUMP_FORCE

    # Resetando a velocidade horizontal
    hero.vx = 0

# ---------------- FIM SALTO DO HEROI --------------------------------------



# ---------------- CAMINHADA DO HEROI --------------------------------------

    # Verificar o toque nas teclas de seta
    # Pressionando a tecla esquerda do teclado
    if keyboard.left:
        hero.vx = -X_SPEED # Velocidade para esquerda é negativa
    
    # Pressionando a tecla direita do teclado
    if keyboard.right:
        hero.vx = X_SPEED # Velocidade para direita positiva
    
    # Atualizando a posição horizontal do herói
    hero.x = hero.x + hero.vx

    # Verificar colisões pela esquerda e direita
    platform_left, platform_right = collision_platform_x()

# ---------------- FIM CAMINHADA DO HEROI -----------------------------------