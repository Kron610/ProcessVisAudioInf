from PIL import Image
from math import floor

def change_size(image, coefficient, format_ = 'RGBA'):
    width, height = image.size
    new_width = floor(width * coefficient)
    new_height = floor(height * coefficient)
    newImage = Image.new(format_, (new_width, new_height)) 
    for x in range(new_width):
        for y in range(new_height):
            newImage.putpixel((x, y), image.getpixel((floor(x / coefficient), floor(y / coefficient))))
    return newImage