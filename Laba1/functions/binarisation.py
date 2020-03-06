from PIL import Image, ImageDraw
from math import floor, sqrt
from functions.oversampling import *
import numpy as np
import scipy.stats as stats


def get_integral_image(image):
    width, height = image.size
    integral_image = np.zeros((height, width))
    for i in range(height):
        sum_ = 0
        for j in range(width):
            sum_ += image.getpixel((j, i))
            if (i == 0):
                integral_image[i][j] = sum_
            else:
                integral_image[i][j] = integral_image[i-1][j] + sum_
    return integral_image



def get_matrices(matrix_image, integral_image):
    height, width = matrix_image.shape
    M = np.zeros((height, width))
    stdev = np.zeros((height, width))
    r = 15
    s2 = r // 2
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
            
            count = (x2 - x1) * (y2 - y1)
            sum_ = integral_image[y2][x2] - integral_image[y1][x2] - integral_image[y2][x1] + integral_image[y1][x1]
            M[i][j] = floor(sum_ / count)
            aperture = matrix_image[y1:y2+1,x1:x2+1]
            stdev[i][j] = floor(sqrt(stats.describe(aperture.flatten())[3]))
    
    return M, stdev



def change_to_binary(image, N):
    new_image = change_size(image, 1/N, 'P')
    matrix_image = np.array(new_image, dtype = 'uint32')
    width, height = new_image.size
    integral_image = get_integral_image(new_image)
    M, stdev = get_matrices(matrix_image, integral_image)         
    bottom_bound, upper_bound = stats.describe(matrix_image.flatten())[1]    
    binary_image = Image.new('1', (width, height))    
    for i in range(height):
        for j in range(width):
            if (matrix_image[i][j] < bottom_bound):
                binary_image.putpixel((j, i), 0)
            else:
                if (matrix_image[i][j] > upper_bound):
                    binary_image.putpixel((j, i), 1)
                else:
                    t = M[i][j] - 0.2 * stdev[i][j]
                    if (matrix_image[i][j] > t):
                        binary_image.putpixel((j, i), 1)
                    else:
                        binary_image.putpixel((j, i), 0)
    
    return binary_image