from functions.semitone import *
from functions.oversampling import *
from functions.binarisation import *


def main():
    M = 3
    N = 5
    #1) Растяжение изображения в M раз
    WallE_image = Image.open("pictures/WallE/WallE.bmp")
    new_WallE_image = change_size(WallE_image, M)
    new_WallE_image.save("pictures/WallE/newWallE.bmp")
    new_WallE_image.show()

    #2) Сжатие изображения в N раз
    Elsa_image = Image.open("pictures/Elsa/Elsa.bmp")
    new_Elsa_image = change_size(Elsa_image, 1/N)
    new_Elsa_image.save("pictures/Elsa/newElsa.bmp")
    new_Elsa_image.show()

    #3) Передискретизация изображения в K=M/N раз путём растяжения и последующего сжатия
    TLOFTR_image = Image.open("pictures/TheLordOfTheRings/TheLordOfTheRings.bmp")
    new_TLOFTR_image = change_size(TLOFTR_image, M)
    new_TLOFTR_image = change_size(new_TLOFTR_image, 1/N)
    new_TLOFTR_image.save("pictures/TheLordOfTheRings/newTheLordOfTheRings.bmp")
    new_TLOFTR_image.show()

    #4) Передискретизация изображения в K раз за один проход.
    Vinni_Puh_image = Image.open("pictures/VinniPuh/VinniPuh.bmp")
    new_Vinni_Puh_image = change_size(Vinni_Puh_image, M/N)
    new_Vinni_Puh_image.save("pictures/VinniPuh/new_VinniPuh.bmp")
    new_Vinni_Puh_image.show()

    #Приведение полноцветного изображения к полутоновому.
    Disgusting_Men_image = Image.open("pictures/DisgustingMen/DisgustingMen.bmp")
    new_Disgusting_Men_image = change_to_semitone(Disgusting_Men_image)
    new_Disgusting_Men_image.save("pictures/DisgustingMen/newDisgustingMen.bmp")
    text_image = Image.open("pictures/text/text.bmp")
    new_text_image = change_to_semitone(text_image)
    new_text_image.save("pictures/text/new_text.bmp")

    #Приведение полутонового изображения к монохромному методом пороговой обработки.
    #  Алгоритм адаптивной бинаризации Ниблэка.
    binary_image = change_to_binary(new_text_image, 4)
    binary_image.show()

    
if __name__ == "__main__":
    main()