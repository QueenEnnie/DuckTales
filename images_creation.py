from PIL import Image


def get_scrooge_standing_images():
    image = Image.open("data/scrooge_sheet.png")
    left = image.crop((1, 2, 25, 31))
    right = image.crop((26, 2, 50, 31))
    left.save("data/left.png")
    right.save("data/right.png")
    return {"left": "left.png", "right": "right.png"}


def get_scrooge_with_cane_images():
    image = Image.open("data/scrooge_sheet.png")
    left = image.crop((1, 51, 25, 79))
    right = image.crop((51, 51, 75, 79))
    left.save("data/left_cane.png")
    right.save("data/right_cane.png")
    return {"left": "left_cane.png", "right": "right_cane.png"}


def get_scrooge_walking_images():
    image = Image.open("data/scrooge_sheet.png")
    image.crop((50, 2, 75, 31)).save("data/walking_left_1.png")
    image.crop((0, 2, 26, 31)).save("data/walking_left_2.png")
    # image.crop((75, 0, 97, 32)).save("data/walking_left_2.png")
    # image.crop((96, 0, 121, 32)).save("data/walking_left_3.png")
    image.crop((120, 2, 145, 31)).save("data/walking_right_1.png")
    image.crop((25, 2, 51, 31)).save("data/walking_right_2.png")
    return {"left": ["walking_left_1.png", "walking_left_2.png"],
            "right": ["walking_right_1.png", "walking_right_2.png"]}


def get_scrooge_jumping_images():
    image = Image.open("data/scrooge_sheet.png")
    image.crop((189, 2, 215, 29)).save("data/jumping_left.png")
    image.crop((214, 2, 240, 29)).save("data/jumping_right.png")
    return {"right": "jumping_right.png", "left": "jumping_left.png"}


def get_amazon_landscapes_images():
    image = Image.open("data/amazon_lanscape_sheet.png")
    image.crop((0, 16, 15, 32)).save("data/grass.png")
    image.crop((16, 0, 32, 16)).save("data/trunk.png")
    image.crop((0, 31, 16, 48)).save("data/middle_grass.png")

    image = Image.open("data/DuckTalesMap1.png")
    image.crop((1019, 1360, 1061, 1392)).save("data/stump.png")
    image.crop((9, 1408, 26, 1424)).save("data/earth.png")
    image.crop((0, 1200, 32, 1232)).save("data/leaves.png")
    image.crop((720, 1376, 736, 1392)).save("data/rock.png")
    image.crop((1312, 1392, 1328, 1424)).save("data/thorn.png")

    amazon_images = {"G": "grass.png",
                     "T": "trunk.png",
                     "M": "middle_grass.png",
                     "S": "stump.png",
                     "E": "earth.png",
                     "L": "leaves.png",
                     "R": "rock.png",
                     "H": "thorn.png"}
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

def get_gorilla_images():
    image = Image.open("data/enemies_sheet.png")
    image.crop((6, 3, 34, 34)).save("data/gorilla_walking_1.png")
    image.crop((35, 3, 59, 34)).save("data/gorilla_walking_2.png")
    image.crop((63, 3, 87, 34)).save("data/gorilla_defeated.png")
    return {"walking": ["gorilla_walking_2.png", "gorilla_walking_1.png"],
            "defeated": "gorilla_defeated.png"}


def lives():
    image = Image.open("data/lives.png")
    image.crop((760, 255, 830, 320)).save("data/full_health.png")
    image.crop((845, 255, 915, 320)).save("data/lost_health.png")
    return {"lost": "lost_health.png", "full": "full_health.png"}


get_amazon_landscapes_images()
get_scrooge_with_cane_images()
get_scrooge_jumping_images()
get_scrooge_walking_images()
get_gorilla_images()
lives()



