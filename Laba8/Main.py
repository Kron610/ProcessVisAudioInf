from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from math import floor




def process_image(image, figure_path, figure_path2):
    new_image = image
    width, height = new_image.size
    arr = np.zeros(256, dtype = 'uint32')
    for x in range(width):
        for y in range(height):
            arr[new_image.getpixel((x,y))] += 1
    x_values = range(256)
    y_values = arr
    rel_arr = np.zeros(256)
    for i in range(256):
        rel_arr[i] = arr[i]
    for i in range(256):
        rel_arr[i] /= (width * height)

    plt.bar(x_values, y_values)
    plt.savefig(figure_path)

    for i in range(1, 256):
        rel_arr[i] = rel_arr[i-1] + rel_arr[i]
    arr2 = np.zeros(256, dtype = 'uint32')
    for i in range(256):
        arr2[floor(255 * rel_arr[i])] = arr[i]
    for x in range(width):
        for y in range(height):
            new_image.putpixel((x,y), floor(255 * rel_arr[new_image.getpixel((x,y))]))
    x_values = range(256)
    y_values = arr2
    plt.clf()
    plt.bar(x_values, y_values)
    plt.savefig(figure_path2)
    plt.clf()
    return new_image

def main():
    image = Image.open("pictures/ht_picture1.bmp")
    new_image = process_image(image, "pictures/hist1.png", "pictures/r_hist1.png")
    new_image.save("pictures/r_picture1.bmp")

    image = Image.open("pictures/ht_picture2.bmp")
    new_image = process_image(image, "pictures/hist2.png", "pictures/r_hist2.png")
    new_image.save("pictures/r_picture2.bmp")

    image = Image.open("pictures/ht_picture3.bmp")
    new_image = process_image(image, "pictures/hist3.png", "pictures/r_hist3.png")
    new_image.save("pictures/r_picture3.bmp")



if __name__ == "__main__":
    main()
