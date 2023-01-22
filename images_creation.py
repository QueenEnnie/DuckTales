import pygame
from PIL import Image


def get_scrooge_standing_images():
    image = Image.open("data/scrooge_sheet.png")
    left = image.crop((0, 0, 26, 32))
    right = image.crop((25, 0, 51, 32))
    left.save("data/left.png")
    right.save("data/right.png")
    return {"left": "left.png", "right": "right.png"}


def get_scrooge_walking_images():
    image = Image.open("data/scrooge_sheet.png")
    image.crop((50, 0, 75, 32)).save("data/walking_left_1.png")
    image.crop((0, 0, 26, 32)).save("data/walking_left_2.png")
    # image.crop((75, 0, 97, 32)).save("data/walking_left_2.png")
    # image.crop((96, 0, 121, 32)).save("data/walking_left_3.png")
    image.crop((120, 0, 145, 32)).save("data/walking_right_1.png")
    image.crop((25, 0, 51, 32)).save("data/walking_right_2.png")
    return {"left": ["walking_left_1.png", "walking_left_2.png"],
            "right": ["walking_right_1.png", "walking_right_2.png"]}


def get_amazon_landscapes_images():
    image = Image.open("data/amazon_lanscape_sheet.png")
    image.crop((0, 16, 15, 32)).save("data/grass.png")
    image.crop((16, 0, 32, 16)).save("data/trunk.png")
    image.crop((0, 31, 16, 48)).save("data/middle_grass.png")

    image = Image.open("data/DuckTalesMap1.png")
    image.crop((1019, 1360, 1061, 1392)).save("data/stump.png")
    image.crop((9, 1408, 26, 1424)).save("data/earth.png")
    image.crop((0, 1200, 32, 1232)).save("data/leaves.png")

    amazon_images = {"G": "grass.png",
                     "T": "trunk.png",
                     "M": "middle_grass.png",
                     "S": "stump.png",
                     "E": "earth.png",
                     "L": "leaves.png"}
    return amazon_images


def get_sky_colour():
    image = Image.open("data/DuckTalesMap1.jpg")
    pixels = image.load()
    return pixels[0, 0]
    # width, length = image.size
    # print(width, length)
    # summa_r, summa_b, summa_g = 0, 0, 0
    # for i in range(width):
    #     for j in range(length):
    #         print(pixels[i, j])
    #         r, g, b = pixels[i, j]
    #         summa_r += r
    #         summa_b += b
    #         summa_g += g
    #         print(r, g, b)
    # pixels = image.load()


# def get_sky_colour():
#     image = pygame.image.load("data/DuckTalesMap1.png").copy()
#     colour = image.get_at((0, 0))
#     return colour[0], colour[1], colour[3]


get_amazon_landscapes_images()



