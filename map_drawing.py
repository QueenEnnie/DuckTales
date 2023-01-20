import pygame
import sys
import os
import images_creation

WIDTH, HEIGHT = 1000, 600
FPS = 60


def load_image(name, colorkey=None):
    surface_color = None
    image_name = os.path.join('data', name)
    if not os.path.isfile(image_name):
        print(f"Файл с изображением '{image_name}' не найден")
        sys.exit()
    my_image = pygame.image.load(image_name)
    if colorkey:
        my_image = my_image.convert()
        if colorkey == -1:
            surface_color = my_image.get_at((0, 0))
        my_image.set_colorkey(surface_color)
    else:
        my_image = my_image.convert_alpha()
    return my_image


def load_map(filename):
    filename = "data/" + filename
    with open(filename, "r") as map_file:
        level_map = [line.strip() for line in map_file]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


def level_generation(level):
    new_player = None
    x_size = len(level[0])
    y_size = len(level)
    for y in range(len(level)):
        for x in range(len(level[y])):
            pass
            # if level[y][x] == '.':
            #     Tile('empty', x, y)
            # elif level[y][x] == '#':
            #     tile = Tile('wall', x, y)
            #     tiles_walls.add(tile)
            # elif level[y][x] == '@':
            #     Tile('empty', x, y)
            #     new_player = Player(x, y)
    return new_player, x_size, y_size


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("move")
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    all_sprites_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
