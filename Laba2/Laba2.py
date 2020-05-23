from PIL import Image
import numpy as np
import scipy.stats as stats




def dilation(image):
    width, height = image.size
    aperture_size = 3
    new_image = Image.new('P', (width, height)) 
    s2 = aperture_size // 2
    matrix_image = np.array(image, dtype = 'uint32')
    for i in range(height):
        for j in range(width):
            x1 = j - s2
            x2 = j + s2
            y1 = i - s2
            y2 = i + s2
        
            if (x1 < 0):
                x1 = 0
            
            if (x2 >= width):
                x2 = width - 1
            
            if (y1 < 0):
                y1 = 0
            
            if (y2 >= height):
                y2 = height - 1
                
            aperture = matrix_image[y1:y2+1,x1:x2+1]
            value = max(aperture.flatten())
            new_image.putpixel((j, i), int(value))
    return new_image



def erosion(image):
    width, height = image.size
    aperture_size = 3
    new_image = Image.new('P', (width, height)) 
    s2 = aperture_size // 2
    matrix_image = np.array(image, dtype = 'uint32')
    for i in range(height):
        for j in range(width):
            x1 = j - s2
            x2 = j + s2
            y1 = i - s2
            y2 = i + s2
        
            if (x1 < 0):
                x1 = 0
            
            if (x2 >= width):
                x2 = width - 1
            
            if (y1 < 0):
                y1 = 0
            
            if (y2 >= height):
                y2 = height - 1
                
            aperture = matrix_image[y1:y2+1,x1:x2+1]
            value = min(aperture.flatten())
            new_image.putpixel((j, i), int(value))
    return new_image



def closing(image):
    new_image = dilation(image)
    return erosion(new_image)



def different(image, new_image):
    width, height = image.size
    dif_image = Image.new('P', (width, height))
    for x in range(width):
        for y in range(height):
            dif_image.putpixel((x, y), abs(image.getpixel((x,y)) - new_image.getpixel((x,y))))
    return dif_image
    


def main():
    text_image = Image.open("pictures/new_text.bmp")
    new_image = closing(text_image)
    new_image.save("pictures/closing_text.bmp")
    new_image.show()
    text_differ = different(text_image, new_image)
    text_differ.save("pictures/text_differ.bmp")
    text_differ.show()
    Disgusting_Men = Image.open("pictures/newDisgustingMen.bmp")
    new_Disgusting_Men = closing(Disgusting_Men)
    new_Disgusting_Men.save("pictures/closingDisgustingMen.bmp")
    new_Disgusting_Men.show()
    Disgusting_Men_differ = different(Disgusting_Men, new_Disgusting_Men)
    Disgusting_Men_differ.save("pictures/DisgustingMenDiffer.bmp")
    Disgusting_Men_differ.show()
    woman_picture = Image.open("pictures/woman_picture.bmp")
    new_woman_picture = closing(woman_picture)
    new_woman_picture.save("pictures/closingwoman_picture.bmp")
    new_woman_picture.show()
    woman_picture_differ = different(woman_picture, new_woman_picture)
    woman_picture_differ.save("pictures/woman_picture_differ.bmp")
    woman_picture_differ.show()

if __name__ == "__main__":
    main()