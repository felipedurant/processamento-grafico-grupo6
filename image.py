from PIL import Image

def generate_image(color_matrix : list, width : int, heigth : int,
                   image_path: str, background_color : tuple = (255, 255, 255)):
    if not ".ppm" in image_path:
        image_path = image_path + ".ppm"
    image_file = open(image_path, "w")
    image_file.write("P3\n")
    image_file.write(str(width) + " " + str(heigth) + "\n")
    image_file.write("255\n")
    for y in range(heigth):
        for x in range(width):
            r = background_color[0]
            g = background_color[1]
            b = background_color[2]
            if color_matrix[y] != [] and color_matrix[y][x] != None:
                r = color_matrix[y][x][0]
                g = color_matrix[y][x][1]
                b = color_matrix[y][x][2]
            image_file.write(str(r) + " " + str(g) + " " + str(b))
            image_file.write("\n")
    image_file.close()
    ppm_to_jpg(image_path)

def ppm_to_jpg(image_path : str):
    image = Image.open(image_path)
    image.save(image_path[:-4] + ".jpg")


### Classe "Image"
##  - Propósito: Manipula a criação e manipulação de imagens, possivelmente gerando a saída final da renderização.
 ## - Funções Comuns: Carregamento, salvamento e manipulação de imagens, armazenamento de dados de pixel.
