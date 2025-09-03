from PIL import Image

def flip_h(input_filename, output_filename):
    try:
        # Abre a imagem original
        img = Image.open(input_filename)

        # Inverte a imagem horizontalmente
        # FLIP_LEFT_RIGHT é a constante que realiza o espelhamento horizontal
        img_inverted = img.transpose(Image.FLIP_LEFT_RIGHT)

        # Salva a nova imagem
        img_inverted.save(output_filename)

        print("Imagem invertida com sucesso!")

    except FileNotFoundError:
        print("Erro: O arquivo 'imagem_original.jpg' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

flip_h('slimefire_walkleft_1.png', 'slimefire_walkright_1.png')