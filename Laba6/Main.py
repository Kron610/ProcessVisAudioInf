import pandas as pd
import numpy as np

from PIL import Image


#Оставляем у числа только 3 знака после запятой
def toFixed(numObj, digits=3):
    return f"{numObj:.{digits}f}2"


#Все бинарные изображения почему-то имеют значения не 1 и 0, а 255 и 0. Эта функция исправляет проблему.
def foo(item):
    if (item == 255):
        return 1
    return 0



def weight_of_black(image, arr):
    area = (arr[0], arr[1], arr[2], arr[3])
    symbol = image.crop(area)
    width, height = symbol.size
    sum_ = 0
    for x in range(width):
        for y in range(height):
            sum_ += foo(symbol.getpixel((x,y)))
    return width * height - sum_, (width * height - sum_) / (width * height)



def coords_of_center_of_gravity(image, arr):
    area = (arr[0], arr[1], arr[2], arr[3])
    symbol = image.crop(area)
    width, height = symbol.size
    sum1 = 0
    sum2 = 0
    for x in range(width):
        for y in range(height):
            sum1 += (x + 1) * (1 - foo(symbol.getpixel((x,y))))
    for x in range(width):
        for y in range(height):
            sum2 += (y + 1) * (1 - foo(symbol.getpixel((x,y)))) 
    weight = weight_of_black(image, arr)
    return sum1 / weight[0] , sum2 / weight[0]



def norm_coords_of_center_of_gravity(image, arr):
    area = (arr[0], arr[1], arr[2], arr[3])
    symbol = image.crop(area)
    width, height = symbol.size
    sum1 = 0
    sum2 = 0
    for x in range(width):
        for y in range(height):
            sum1 += (x + 1)* (1 - foo(symbol.getpixel((x,y))))
    for x in range(width):
        for y in range(height):
            sum2 += (y + 1) * (1 - foo(symbol.getpixel((x,y)))) 
    weight = weight_of_black(image, arr)[0]
    return ((sum1 / weight) - 1) / (width - 1),  ((sum2 / weight) - 1) / (height - 1)



def norm_axial_moments_of_inertia(image, arr):
    area = (arr[0], arr[1], arr[2], arr[3])
    symbol = image.crop(area)
    width, height = symbol.size
    sum1 = 0
    sum2 = 0
    center = coords_of_center_of_gravity(image, arr)
    for x in range(width):
        for y in range(height):
            sum1 += ((1 - foo(symbol.getpixel((x,y)))) * ((y + 1 - center[1]) ** 2))
    for x in range(width):
        for y in range(height):
            sum2 += ((1 - foo(symbol.getpixel((x,y)))) * ((x + 1 - center[0]) ** 2))
    return sum1 / ((width ** 2) + (height ** 2)), sum2 / ((width ** 2) + (height ** 2))


#Мера близости
def p_measure(d):
    return 1/(1 + 0.8 * d)



class Predictor:
    def __init__(self, X, y):
        self.X = X
        self.y = y
    def predict(self, X):
        predictions = []
        for vls in X:
            d = 0
            for index, value in enumerate(vls):
                d += (self.X[:, index] - value)**2
            d=np.sqrt(d)
            idx = np.argsort(d)
            predictions.append([(self.y[index], float(toFixed(p_measure(d[index]), 5))) for index in idx])
        return predictions



def process_image(df_data, image, arrs):
    df = pd.DataFrame({'A' : [weight_of_black(image, arr)[1] for arr in arrs],
                   'B' : [norm_coords_of_center_of_gravity(image, arr)[0] for arr in arrs],
                   'C' : [norm_coords_of_center_of_gravity(image, arr)[1] for arr in arrs],
                   'D' : [norm_axial_moments_of_inertia(image, arr)[0] for arr in arrs],
                   'E' : [norm_axial_moments_of_inertia(image, arr)[1] for arr in arrs]})

    columns = ['symbol', 'B', 'E', 'F', 'I', 'J']
    train = df_data[columns]
    X_train = train.drop(columns = ['symbol']).values
    y_train = train['symbol'].values
    X_test = df.values

    #Нормируем
    mean_ = X_train.mean(axis=0)
    std_ = X_train.std(axis=0)

    X_train = (X_train - mean_) / std_
    X_test = (X_test - mean_) / std_

    max_ = X_train.max(axis=0)
    min_ = X_train.min(axis=0)

    X_train = (X_train - min_) / (max_ - min_)
    X_test = (X_test - min_) / (max_ - min_)

    predictor = Predictor(X_train, y_train)
    predictions = predictor.predict(X_test)
    string = ''
    for item in predictions:
        string += item[0][0]

    return string, predictions

def main():
    df_data = pd.read_csv("signs.csv", sep=';')

    #1 картинка
    image = Image.open("cropped_text.bmp")
    with open("coords.txt") as file:
        lines = file.readlines()
    arrs = []
    for line in lines:
        string = line.split(' ')
        string.pop()
        arr = []
        for item in string:
            arr.append(int(item))
        arrs.append(arr)
    string, predictions = process_image(df_data, image, arrs)
    with open("predictions.txt", 'w', encoding = "utf-8") as f:
        for item in predictions:
            f.write(str(item) + "\n")
    print(string)

    #2 картинка
    image = Image.open("cropped_text2.bmp")
    with open("coords2.txt") as file:
        lines = file.readlines()
    arrs = []
    for line in lines:
        string = line.split(' ')
        string.pop()
        arr = []
        for item in string:
            arr.append(int(item))
        arrs.append(arr)
    string, predictions = process_image(df_data, image, arrs)
    with open("predictions2.txt", 'w', encoding = "utf-8") as f:
        for item in predictions:
            f.write(str(item) + "\n")
    print(string)

    #3 картинка
    image = Image.open("cropped_text3.bmp")
    with open("coords3.txt") as file:
        lines = file.readlines()
    arrs = []
    for line in lines:
        string = line.split(' ')
        string.pop()
        arr = []
        for item in string:
            arr.append(int(item))
        arrs.append(arr)
    string, predictions = process_image(df_data, image, arrs)
    with open("predictions3.txt", 'w', encoding = "utf-8") as f:
        for item in predictions:
            f.write(str(item) + "\n")
    print(string)



if __name__ == "__main__":
    main()