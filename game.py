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
    pass