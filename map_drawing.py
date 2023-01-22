import pygame
import sys
import os
import images_creation

WIDTH, HEIGHT = 1000, 600
FPS = 60
TILES_IMAGES = images_creation.get_amazon_landscapes_images()
TILE_SIZE = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(TILES_IMAGES[tile_type])
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)


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


def level_generation():
    level_map = load_map("first_level_map.txt")
    new_player = None
    x_size = len(level_map[0])
    y_size = len(level_map)
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] != ".":
                Tile(level_map[y][x], x, y)
    # return new_player, x_size, y_size


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("move")
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    sky_colour = images_creation.get_sky_colour()
    print(sky_colour)

    screen.fill(sky_colour)

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    level_generation()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(FPS)
        screen.fill(sky_colour)
        all_sprites.draw(screen)
    pygame.quit()
