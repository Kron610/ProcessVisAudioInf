from PIL import Image
from math import floor


def change_to_semitone(image):
    width, height = image.size
    newImage = Image.new('P', (width, height))
    for x in range(width):
        for y in range(height):
            color = image.getpixel((x,y))
            bright = floor(0.3 * color[0] + 0.59 * color[1] +  0.11 *color[2])
            newImage.putpixel((x, y), bright)
    return newImage