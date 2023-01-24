import pygame
import sys
import os
import images_creation

WIDTH, HEIGHT = 1000, 600
FPS = 60
TILES_IMAGES = images_creation.get_amazon_landscapes_images()
TILE_SIZE = 50


class Camera:
    def __init__(self):
        self.delta_x = 0
        self.delta_y = 0

    def apply(self, tile_object):
        tile_object.rect.x += self.delta_x
        tile_object.rect.y += self.delta_y
        # print(tile_object.rect.x)

    def update(self, target):
        # if target.rect.x > 150:
        self.delta_x = -(target.rect.x + target.rect.w // 2 - width // 2)
        # if self.delta_x > 0:
        #     print(self.delta_x, target.rect.x)
        # self.delta_y = -(target.rect.y + target.rect.h // 2 - height // 2)


class ScroogeMcDuck(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__(player_group, all_sprites)
        self.move = False
        self.direction = None
        self.count_change = 0
        self.count_loop = 0

        self.position_x = position_x * TILE_SIZE
        self.position_y = position_y * TILE_SIZE

        self.standing_image = images_creation.get_scrooge_standing_images()
        self.walking_image = images_creation.get_scrooge_walking_images()

        self.image = load_image(self.standing_image["left"], -1)
        self.image = pygame.transform.scale(self.image, (2 * TILE_SIZE, 2 * TILE_SIZE))
        self.rect = self.image.get_rect().move(self.position_x + 2, self.position_y)

    def check_stump_collision(self):
        collision = pygame.sprite.spritecollideany(self, stump_group)
        if collision:
            if (collision.rect.x <= self.rect.x and
                self.direction == "left") or (collision.rect.x > self.rect.x
                                              and self.direction == "right"):
                self.move = False

    def update(self, move_event=None):
        if move_event in ["right", "left"]:
            self.move = True
            self.direction = move_event
        delta = -20 if self.direction == "left" else 20

        self.check_stump_collision()

        if self.move:
            if self.count_loop % 8 == 0:
                current_image = self.count_change % len(self.walking_image[self.direction])
                image_name = self.walking_image[self.direction][current_image]
                self.image = load_image(image_name, -1)
                self.image = pygame.transform.scale(self.image, (100, 100))
                self.count_change += 1
            if self.count_change == 2:
                self.rect = self.rect.move(delta, 0)
                self.move = False
                self.count_change = 0
            self.count_loop += 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(TILES_IMAGES[tile_type])
        if tile_type == "S":
            self.image = pygame.transform.scale(self.image, (3 * TILE_SIZE, 2 * TILE_SIZE))
            pos_y -= 1
            self.add(stump_group)
        else:
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
    global player
    level_map = load_map("first_level_map.txt")
    new_player = None
    x_size = len(level_map[0])
    y_size = len(level_map)
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == "P":
                player = ScroogeMcDuck(x, y)
                player_group.add(player)
            else:
                if level_map[y][x] != ".":
                    Tile(level_map[y][x], x, y)
    return player


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("move")
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    sky_colour = images_creation.get_sky_colour()
    screen.fill(sky_colour)

    camera = Camera()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    stump_group = pygame.sprite.Group()

    player = level_generation()

    clock = pygame.time.Clock()
    running = True
    move_left_long = False
    move_right_long = False
    while running:
        move_left = False
        move_right = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left_long = True
                if event.key == pygame.K_RIGHT:
                    move_right_long = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left_long = False
                if event.key == pygame.K_RIGHT:
                    move_right_long = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                move_left = True
            if keys[pygame.K_RIGHT]:
                move_right = True

        if move_right_long:
            player_group.update("right")
        if move_left_long:
            player_group.update("left")

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill(sky_colour)
        player_group.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
