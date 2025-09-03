from PIL import Image
import os

def encolher_imagem_gradualmente(caminho_imagem, num_imagens, decremento_em_pixels):
    """
    Encolhe a altura de uma imagem, criando um número específico de frames.

    Args:
        caminho_imagem (str): O caminho para a imagem de entrada.
        num_imagens (int): O número total de imagens a serem criadas na sequência.
    """
    if num_imagens < 2:
        print("Erro: O número de imagens deve ser pelo menos 2.")
        return

    try:
        img_original = Image.open(caminho_imagem)
    except FileNotFoundError:
        print(f"Erro: Imagem não encontrada em '{caminho_imagem}'")
        return

    nome_imagem = caminho_imagem[:-4]
    largura, altura_original = img_original.size
    altura_final = altura_original + num_imagens  # A altura mínima da imagem final

    # Calcula o quanto a altura deve diminuir a cada passo (frame)
    decremento_por_passo = decremento_em_pixels

    for i in range(num_imagens):
        # Calcula a nova altura para a imagem atual
        nova_altura = int(altura_original + (i * decremento_por_passo))
        
        # Garante que a altura não seja menor que a altura final
        if nova_altura > altura_final:
            nova_altura = altura_final

        # Redimensiona a imagem para a nova altura
        img_redimensionada = img_original.resize((largura, nova_altura))

        # Define o nome do arquivo de saída
        nome_arquivo_saida = f"{nome_imagem}_{i}.png"

        # Salva a imagem
        img_redimensionada.save(nome_arquivo_saida)
        print(f"Imagem salva: {nome_arquivo_saida} (altura: {nova_altura} pixels)")

# --- Exemplo de Uso ---
# Substitua 'hero_idle_1.png' pelo nome do seu arquivo de imagem
caminho_da_imagem = 'hero.png' 
# Defina quantas imagens você quer na sua animação
quantidade_de_frames = 10 

decremento = 1

encolher_imagem_gradualmente(caminho_da_imagem, quantidade_de_frames, decremento)