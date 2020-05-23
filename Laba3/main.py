from PIL import Image
import numpy as np
import sys
from math import floor

sys.path.insert(1, 'C:/Users/gerko/Documents/ProcessVisAudioInf/Laba1/functions')

from semitone import change_to_semitone
from binarisation import change_to_binary



def get_Gx(image):
    width, height = image.size
    Gx = np.zeros((width, height)) 
    max_x = 0
    for x in range(width):
        for y in range (height):
            if (x == width - 1 or y == height - 1):
                Gx[x][y] = 0
                continue
            bright_x = image.getpixel((x + 1,y + 1)) - image.getpixel((x,y))
            Gx[x][y] = bright_x
            if (max_x < bright_x):
                max_x = bright_x
    return Gx, max_x



def get_Gy(image):
    width, height = image.size
    Gy = np.zeros((width, height)) 
    max_y = 0
    for x in range(width):
        for y in range (height):
            if (x == width - 1 or y == height - 1):
                Gy[x][y] = 0
                continue
            bright_y = image.getpixel((x,y + 1)) - image.getpixel((x + 1,y))
            Gy[x][y] = bright_y
            if (max_y < bright_y):
                max_y = bright_y
    return Gy, max_y



def get_gradient(Gx, Gy):
    width, height = Gx.shape
    G = np.zeros((width, height))
    max_g = 0
    for x in range(width):
        for y in range(height):
            G[x][y] = abs(Gy[x][y]) + abs(Gx[x][y])
            if (max_g < G[x][y]):
                max_g = G[x][y]
    return G, max_g



def get_normalize(matrix, max_value):
    width, height = matrix.shape
    new_image = Image.new('P', (width, height))
    for x in range(width):
        for y in range(height):
            value = floor(matrix[x][y] * 255 / max_value)
            new_image.putpixel((x,y), value)
    return new_image



def main():
    Olaf_image = change_to_semitone(Image.open("pictures/Olaf.png"))
    Olaf_image.save("pictures/Olaf_semitone.png")
    Gx, max_x = get_Gx(Olaf_image)
    Gy, max_y = get_Gy(Olaf_image)
    G, max_g = get_gradient(Gx, Gy)

    Gx_image = get_normalize(Gx, max_x)
    Gy_image = get_normalize(Gy, max_y)
    G_image = get_normalize(G, max_g)

    binary_gradient_image = change_to_binary(G_image, 1)

    Gx_image.save("pictures/Olaf_Gx.png")
    Gy_image.save("pictures/Olaf_Gy.png")
    G_image.save("pictures/Olaf_G.png")
    binary_gradient_image.save("pictures/Olaf_binary_gradient.png")



if __name__ == "__main__":
    main()