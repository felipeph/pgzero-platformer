
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

BARNACLE_ATTACK_SPEED = 0.2

BEE_WALK_SPEED = 5
BEE_WALK_ANIMATION_SPEED = 0.1 
BEE_ANIMATION_SPEED = 0.1 

SLIMEFIRE_WALK_SPEED = 5
SLIMEFIRE_WALK_ANIMATION_SPEED = 0.1 
SLIMEFIRE_TILES_MIN = 18 * TILE_SIZE
SLIMEFIRE_TILES_MAX = 26 * TILE_SIZE
SLIMEFIRE_ANIMATION_SPEED = 0.1 

# Constantes do objetivo
GOAL_ANIMATION_SPEED = 0.1
GOAL_POSITION = (2 * TILE_SIZE, 5 * TILE_SIZE)



# Constantes de posição inicial
HERO_START_POSITION = TILE_SIZE, HEIGHT / 2 

# --------------------------------------------------------


# ----------- CRIAÇÃO DO HEROI ---------------------------

# Criando e posicionando nosso herói
hero = Actor("hero_idle_1")
hero.pos = HERO_START_POSITION
hero.vy = Y_SPEED_START # Definindo a velocidade vertical
hero.vx = X_SPEED_START # Definindo a velocidade horizontal

# --------------------------------------------------------

# Criando o Actor da bandeira
goal = Actor('goal_animation_0')
# Posicionando o objetivo na posição definida
goal.left, goal.bottom = GOAL_POSITION
goal.frame = 0



# ----------- CRIAÇÃO DOS INIMIGOS -------------------------

# Lista de inimigos inicialmente vazia
enemies_list = []


# Função de criar inimigos com base no nome e posição
def create_enemy(enemy_name, enemy_tile_left, enemy_tile_bottom, enemy_vx):
    
    # Inicialmente cria um actor para o arquivo de imagem
    enemy = Actor(f'{enemy_name}_0')
    
    # Posiciona o inimigo no local desejado
    enemy.bottom = enemy_tile_bottom * TILE_SIZE
    enemy.left = enemy_tile_left * TILE_SIZE

    # Adiciona um atributo para controlar o frame individual da animação
    enemy.frame = 0

    # Colocar velocidade inicial horizontal em cada inimigo
    enemy.vx = enemy_vx

    # Capturar a posição inicial da esquerda do inimigo
    enemy.startleft = enemy.left

    # Insere o inimigo na lista de inimigos
    enemies_list.append(enemy)

# Criando um inimigo tipo barnacle
create_enemy('barnacle_attack', 10, 11, 0)

# Criando outro inimigo tipo barnacle
create_enemy('barnacle_attack', 18, 10, 0)

# Criando um inimigo tipo slime de fogo
create_enemy('slimefire_walkleft', 24, 4, SLIMEFIRE_WALK_SPEED)

# Criando um inimigo tipo abelha
create_enemy('bee_walkleft', 0, 4, BEE_WALK_SPEED)
create_enemy('bee_walkleft', 5, 4, BEE_WALK_SPEED)
create_enemy('bee_walkleft', 10, 4, BEE_WALK_SPEED)
create_enemy('bee_walkleft', 15, 4, BEE_WALK_SPEED)
create_enemy('bee_walkleft', 25, 4, BEE_WALK_SPEED)


# ----------- FIM CRIAÇÃO DOS INIMIGOS -------------------------










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

# Lista de imagens da animação de ataque do barnacle
barnacle_attack_images = animation_images_list('barnacle', 'attack', 4)


# Lista de imagens da animação de caminhar para direita do bee
bee_walk_right_images = animation_images_list('bee', 'walkright', 2)

# Lista de imagens da animação de caminhar para esquerda do bee
bee_walk_left_images = animation_images_list('bee', 'walkleft', 2)

# Lista de imagens da animação de caminhar para direita do slimefire
slimefire_walk_right_images = animation_images_list('slimefire', 'walkright', 2)

# Lista de imagens da animação de caminhar para esquerda do slimefire
slimefire_walk_left_images = animation_images_list('slimefire', 'walkleft', 2)

# Criando a lista de animações do objetivo
goal_images = animation_images_list('goal', 'animation', 2)

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









# ---------- ANIMAÇÃO ATAQUE DO BARNACLE --------------------------------

def animate_barnacle_attack():
    # Para cada inimigo na nossa lista de inimigos
    for enemy in enemies_list:
        # Pega o nome do arquivo da imagem atual do inimigo
        enemy_filename = str(enemy.image)

        # Verifica se o inimigo é um 'barnacle'
        if enemy_filename.startswith('barnacle'):
            
            # 1. GUARDA a posição atual da base do inimigo
            original_bottom = enemy.bottom
            
            # 2. Avança para o próximo quadro da animação
            enemy.frame = (enemy.frame + 1) % len(barnacle_attack_images)
            
            # 3. Atualiza a imagem (o que pode mover a base)
            enemy.image = barnacle_attack_images[enemy.frame]
            
            # 4. RESTAURA a posição da base, garantindo que ela não se mova
            enemy.bottom = original_bottom

# Agenda a execução da animação em um dado intervalo de tempo (segundos)
clock.schedule_interval(animate_barnacle_attack, BARNACLE_ATTACK_SPEED)

# ---------- FIM ANIMAÇÃO ATAQUE DO BARNACLE --------------------------------





# ---------- ANIMAÇÃO DO OBJETIVO --------------------------------

def animate_goal():
    # Avançar para o próximo frame da animação
    goal.frame = (goal.frame + 1) % len(goal_images)

    # Trocar as imagens do actor
    goal.image = goal_images[goal.frame]

# Agenda a execução da animação em um dado intervalo de tempo (segundos)
clock.schedule_interval(animate_goal, GOAL_ANIMATION_SPEED)

# ---------- FIM ANIMAÇÃO DO OBJETIVO --------------------------------

















###################################################################

# ---------- ANIMAÇÃO DO SLIMEFIRE --------------------------------
# Função que anima a troca de sprites do slimefire independente do movimento
def animate_slimefire():

    # Percorrendo cada inimigo na lista
    for enemy in enemies_list:

        # Resgatando o nome do inimigo
        enemy_filename = str(enemy.image)

        # Restagando a posição da base do inimigo
        original_bottom = enemy.bottom

        # Verificando se o inimigo é um "slimefire"
        if enemy_filename.startswith('slimefire'):

            # Avançar um frame na animação do inimigo
            enemy.frame = (enemy.frame + 1) % len(slimefire_walk_left_images)

            # Se o inimigo estiver andando para a direita
            if enemy.vx > 0:
                # Troca a imagem dele para as de caminhada para direita
                enemy.image = slimefire_walk_left_images[enemy.frame]
            
            # Senão
            else:
                # Troca a imagem dele para as de caminhada para esquerda
                enemy.image = slimefire_walk_right_images[enemy.frame]
        
        # Posiciona a base no inimigo no mesmo valor da base original
        enemy.bottom = original_bottom

clock.schedule_interval(animate_slimefire, SLIMEFIRE_ANIMATION_SPEED)

# ---------- FIM ANIMAÇÃO DO SLIMEFIRE --------------------------------






# ---------- ANIMAÇÃO DA ABELHA --------------------------------
# Função que anima a troca de sprites da abelha independente do movimento
def animate_bee():

    # Percorrendo cada inimigo na lista
    for enemy in enemies_list:

        # Resgatando o nome do inimigo
        enemy_filename = str(enemy.image)

        # Verificando se o inimigo é um "bee"
        if enemy_filename.startswith('bee'):

            # Avançar um frame na animação do inimigo
            enemy.frame = (enemy.frame + 1) % len(bee_walk_left_images)

            # Se o inimigo estiver andando para a direita
            if enemy.vx > 0:
                # Troca a imagem dele para as de caminhada para direita
                enemy.image = bee_walk_left_images[enemy.frame]
            
            # Senão
            else:
                # Troca a imagem dele para as de caminhada para esquerda
                enemy.image = bee_walk_right_images[enemy.frame]
        
clock.schedule_interval(animate_bee, BEE_ANIMATION_SPEED)

# ---------- FIM ANIMAÇÃO DA ABELHA --------------------------------




# ---------- MOVIMENTO DA ABELHA --------------------------------

# Função que movimenta cada abelha
def bee_walk():

    # Percorre todos os inimigos
    for enemy in enemies_list:

        # Recolhe o nome do arquivo 
        enemy_filename = str(enemy.image)

        # Verifica se o nome começa com "bee"
        if enemy_filename.startswith('bee'):

            # Desloca o inimigo para esquerda
            enemy.x = enemy.x - enemy.vx
            
            # Verifica se chegou na borda da tela
            if enemy.left < 0 or enemy.right > WIDTH:

                # Inverte a velocidade do inimigo
                enemy.vx = - enemy.vx


# -----------FIM MOVIMENTO DA ABELHA --------------------------------





# ---------- MOVIMENTO DO SLIMEFIRE --------------------------------

# Função que movimenta o slimefire
def slimefire_walk():

    # Percorre a lista de todos os inimigos
    for enemy in enemies_list:

        # Resgata o nome do arquivo de imagem
        enemy_filename = str(enemy.image)

        # Verifica se o inimigo é um slimefire
        if enemy_filename.startswith('slimefire'):

            # Desloca o inimigo para a esquerda
            enemy.x = enemy.x - enemy.vx
            

            if enemy.left < SLIMEFIRE_TILES_MIN or enemy.right > SLIMEFIRE_TILES_MAX:
                enemy.vx = - enemy.vx


# -----------FIM MOVIMENTO DO SLIMEFIRE --------------------------------










##########################################################












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

    # Desenhando o objetivo
    goal.draw()

    # Desenhando os inimigos 
    # Para cada inimigo na lista de inimigos
    for enemy in enemies_list: 
        # Desenha o inimigo na tela
        enemy.draw() 


# ---------- FIM DESENHANDO ELEMENTOS NA TELA -----------------------------

    


# ---------- ATUALIZANDO ELEMENTOS NA TELA --------------------------------

def update():

# ------------------- DESLOCAMENTO DOS INIMIGOS ---------------------------
    slimefire_walk()
    bee_walk()
# ------------------- FIM DESLOCAMENTO DOS INIMIGOS -----------------------

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




# ---------------- COLISAO COM OBSTACULOS (MORTE) ---------------------------

    # Caminha por todos os obstáculos verificando a colisão
    for obstacle in obstacles:
        # Se a colisão ocorrer
        if hero.colliderect(obstacle):
            # Herói volta para o início do jogo
            hero.pos = HERO_START_POSITION
            # Para o loop depois da colisão
            break
        
# ---------------- FIM COLISAO COM OBSTACULOS (MORTE) -----------------------


# ---------------- COLISAO COM INIMIGOS (MORTE) ---------------------------

    # Caminha por todos os inimigos verificando a colisão
    for enemy in enemies_list:
        # Se a colisão ocorrer
        if hero.colliderect(enemy):
            # Herói volta para o início do jogo
            hero.pos = HERO_START_POSITION
            # Para o loop depois da colisão
            break
        
# ---------------- FIM COLISAO COM INIMIGOS (MORTE) -----------------------




# ---------------- COLISAO COM BORDAS LATERAIS DA TELA --------------------
    # Se o herói está mais a esquerda do que zero
    if hero.left < 0:
        # Posiciona sua esquerda em zero para ele não cair
        hero.left = 0
    
    # Se o herói está mais a direita que a largura da borda
    if hero.right > WIDTH:
        # Posiciona sua direita na borda da tela
        hero.right = WIDTH

# ---------------- FIM COLISAO COM BORDAS LATERAIS DA TELA ------------------



    if hero.colliderect(goal):
        hero.pos = HERO_START_POSITION