from PIL import Image
import numpy as np
from math import floor, log2



def change_to_halftone(image):
    width, height = image.size
    newImage = Image.new('P', (width, height))
    for x in range(width):
        for y in range(height):
            color = image.getpixel((x,y))
            bright = floor(0.3 * color[0] + 0.59 * color[1] +  0.11 *color[2])
            newImage.putpixel((x, y), bright)
    return newImage



def energy(matrix):
    ASM = 0
    for x in range(256):
        for y in range(256):
            ASM += matrix[x][y] ** 2
    return ASM



def max_probability(matrix):
    return max([max(item) for item in matrix])



def entropy(matrix):
    ENT = 0
    for x in range(256):
        for y in range(256):
            if (matrix[x][y] > 0):
                ENT += matrix[x][y] * log2(matrix[x][y])
    return -ENT



def trace(matrix):
    return np.trace(matrix)



def get_matrix_image(image):
    new_image = change_to_halftone(image)
    arr = np.zeros((256,256), dtype='uint32')
    width, height = new_image.size
    for x in range(width):
        for y in range(height):
            if (x != 0):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x-1,y))]+=1
            if (x != width - 1):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x+1,y))]+=1
            if (y != 0):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x,y-1))]+=1
            if (y != height - 1):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x,y+1))]+=1
    matrix_image = Image.new('P', (256, 256))
    data = matrix_image.load()
    max_ = max([max(item) for item in arr])
    for x in range(256):
        for y in range(256):
            data[x,y] = int((arr[x][y] * 255 / max_))
    return matrix_image



def get_signs(image):
    new_image = change_to_halftone(image)
    arr = np.zeros((256,256), dtype='float')
    width, height = new_image.size
    for x in range(width):
        for y in range(height):
            if (x != 0):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x-1,y))]+=1
            if (x != width - 1):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x+1,y))]+=1
            if (y != 0):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x,y-1))]+=1
            if (y != height - 1):
                arr[new_image.getpixel((x,y))][new_image.getpixel((x,y+1))]+=1
    K = 4 * width * height - 2 * (width + height)
    for x in range(256):
        for y in range(256):
            arr[x][y] /= K
    return (energy(arr), max_probability(arr), entropy(arr), trace(arr))




def main():
    image = Image.open("pictures/picture1.jpg")
    matrix_image = get_matrix_image(image)
    matrix_image.save("pictures/matrix_image.bmp")
    print(get_signs(image))

    image = Image.open("pictures/picture2.jpg")
    matrix_image = get_matrix_image(image)
    matrix_image.save("pictures/matrix_image2.bmp")
    print(get_signs(image))

    image = Image.open("pictures/picture3.jpg")
    matrix_image = get_matrix_image(image)
    matrix_image.save("pictures/matrix_image3.bmp")
    print(get_signs(image))

    image = Image.open("pictures/picture3.jpg")
    matrix_image = get_matrix_image(image)
    matrix_image.save("pictures/matrix_image3.bmp")
    print(get_signs(image))



if __name__ == "__main__":
    main()