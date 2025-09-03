from PIL import Image

def recortar_personagem(caminho_imagem_entrada, caminho_imagem_saida):
    """
    Recorta uma imagem para remover o fundo transparente ao redor de um objeto.

    Args:
        caminho_imagem_entrada (str): O caminho para o arquivo da imagem original.
        caminho_imagem_saida (str): O caminho para salvar a imagem recortada.
    """
    try:
        # 1. Abre a imagem
        img = Image.open(caminho_imagem_entrada)

        # 2. Converte a imagem para o modo RGBA para garantir que ela tenha um canal
        #    de transparência (Alfa). Isso é crucial para detectar o fundo.
        img = img.convert("RGBA")

        # 3. Pega a "bounding box" (caixa delimitadora) do conteúdo da imagem.
        #    A função getbbox() retorna uma tupla de 4 elementos (esquerda, topo, direita, baixo)
        #    que representa as coordenadas dos pixels que não são totalmente transparentes.
        #    É um algoritmo de busca bem otimizado.
        bbox = img.getbbox()

        # 4. Verifica se uma bounding box foi encontrada (ou seja, a imagem não é vazia)
        if bbox:
            # 5. Recorta a imagem usando as coordenadas encontradas
            imagem_recortada = img.crop(bbox)

            # 6. Salva a nova imagem recortada no caminho de saída
            imagem_recortada.save(caminho_imagem_saida, "PNG")
            print(f"Imagem recortada com sucesso e salva em: {caminho_imagem_saida}")
        else:
            # Isso aconteceria se a imagem fosse inteiramente transparente
            print("Não foi encontrado conteúdo na imagem para recortar.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_imagem_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- EXECUÇÃO DO SCRIPT ---

# for i in range(3):
    
#     # Nome do arquivo de imagem original
arquivo_de_entrada = 'slime_fire_walk_left_1.png'

    # Nome que o arquivo final terá
arquivo_de_saida = arquivo_de_entrada

    # Chama a função para executar a tarefa
recortar_personagem(arquivo_de_entrada, arquivo_de_saida)