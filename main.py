import sys
import os
import pygame
from images_creation import *

WIDTH, HEIGHT = 1000, 700
TILES_IMAGES = get_amazon_landscapes_images()
TILE_SIZE = 50
FPS = 60


class Camera:
    def __init__(self):
        self.delta_x = 0
        self.delta_y = 0

    def apply(self, tile_object):
        tile_object.rect.x += self.delta_x
        tile_object.rect.y += self.delta_y

    def update(self, target):
        self.delta_x = -(target.rect.x + target.rect.w // 2 - width // 2)


class ScroogeMcDuck(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__(player_group, all_sprites)

        self.count_lives = 3

        self.cane_attack = False
        self.move_right_left = False
        self.jump = False
        self.reach_higher_point = False
        self.reach_higher_point_in_pain = False
        self.move_on_the_stump = False
        self.return_from_stump_on_the_ground = False
        self.current_injury = False
        self.start_collision = False
        self.falling = False
        self.direction = "left"

        self.delta_walk = 0
        self.delta_jump_y = 20
        self.delta_jump_x = 0

        self.count_iteration_return_ground = 0
        self.count_iteration_left_right = 0
        self.count_iteration_jump = 0
        self.count_pain = 0
        self.count_rise = 0
        self.count_loop = 0

        self.position_x = position_x * TILE_SIZE
        self.position_y = position_y * TILE_SIZE
        self.standing_position_y = 7 * TILE_SIZE

        self.standing_image = get_scrooge_standing_images()
        self.walking_image = get_scrooge_walking_images()
        self.jumping_image = get_scrooge_jumping_images()
        self.images_with_cane = get_scrooge_with_cane_images()
        self.dead_images = get_scrooge_dead_images()

        self.image = load_image(self.standing_image["left"], -1)
        self.image = pygame.transform.scale(self.image, (2 * TILE_SIZE, 2 * TILE_SIZE))
        self.rect = self.image.get_rect().move(self.position_x, self.position_y)

    def stump_collision_walk(self):
        if self.move_on_the_stump:
            self.rect = self.rect.move(self.delta_walk, 0)
            collision = find_collision(self, stump_group)
            self.rect = self.rect.move(-self.delta_walk, 0)
            if not collision:
                self.move_on_the_stump = False
                self.return_from_stump_on_the_ground = True
        if not pygame.sprite.spritecollideany(self, stump_group):
            self.rect = self.rect.move(self.delta_walk, 0)
            collision = pygame.sprite.spritecollideany(self, stump_group)
            self.rect = self.rect.move(-self.delta_walk, 0)
            if collision:
                if collision.rect.x < self.rect.x and self.direction == "left":
                    self.delta_walk = collision.rect.x + collision.rect.w - self.rect.x
                if collision.rect.x > self.rect.x and self.direction == "right":
                    self.delta_walk = collision.rect.x - (self.rect.x + self.rect.w)

    def rock_collision(self):
        if not pygame.sprite.spritecollideany(self, rock_group):
            self.rect = self.rect.move(self.delta_walk, 0)
            collision = find_collision(self, rock_group)
            self.rect = self.rect.move(-self.delta_walk, 0)
            if collision:
                if collision.rect.x < self.rect.x and self.direction == "left":
                    self.delta_walk = collision.rect.x + collision.rect.w - self.rect.x
                if collision.rect.x > self.rect.x and self.direction == "right":
                    self.delta_walk = collision.rect.x - (self.rect.x + self.rect.w)
                self.rect = self.rect.move(self.delta_walk, 0)

    def stump_collision_jump(self):
        if self.move_on_the_stump:
            return

        self.rect = self.rect.move(self.delta_jump_x, self.delta_jump_y)
        collision = find_collision(self, stump_group)
        self.rect = self.rect.move(-self.delta_jump_x, -self.delta_jump_y)

        if collision and collision.rect.x < self.rect.x and self.direction == "left":
            if collision.rect.y + self.delta_jump_y < self.rect.y + self.rect.h < \
                    collision.rect.y + collision.rect.h:
                self.delta_jump_x = collision.rect.x + collision.rect.w - self.rect.x
                self.rect = self.rect.move(self.delta_jump_x, 0)
                self.delta_jump_x = 0
                self.reach_higher_point = True
                self.count_rise = 0
            if collision.rect.y <= self.rect.y + self.rect.h <= collision.rect.y + self.delta_jump_y:
                if collision.rect.x <= self.rect.x <= collision.rect.x + collision.rect.w or \
                        collision.rect.x <= self.rect.x + self.rect.w <= \
                        collision.rect.x + collision.rect.w:
                    self.delta_jump_y = collision.rect.y - self.rect.y - self.rect.h
                    self.rect = self.rect.move(0, self.delta_jump_y)
                    self.jump = False
                    self.cane_attack = False
                    self.move_right_left = False
                    self.move_on_the_stump = True
                    self.reach_higher_point = False
                    self.count_rise = 0
                    self.change_image(self.standing_image[self.direction])

        elif collision and collision.rect.x > self.rect.x and self.direction == "right":
            if collision.rect.y + self.delta_jump_y < self.rect.y + self.rect.h < \
                    collision.rect.y + collision.rect.h:
                self.delta_jump_x = collision.rect.x - self.rect.x - self.rect.w
                self.rect = self.rect.move(self.delta_jump_x, 0)
                self.delta_jump_x = 0
                self.reach_higher_point = False
                self.count_rise = 0
            if collision.rect.y <= self.rect.y + self.rect.h <= collision.rect.y + self.delta_jump_y:
                if collision.rect.x <= self.rect.x <= collision.rect.x + collision.rect.w or \
                        collision.rect.x <= self.rect.x + self.rect.w <= \
                        collision.rect.x + collision.rect.w:
                    self.delta_jump_y = collision.rect.y - self.rect.y - self.rect.h
                    self.rect = self.rect.move(0, self.delta_jump_y)
                    self.jump = False
                    self.cane_attack = False
                    self.move_right_left = False
                    self.move_on_the_stump = True
                    self.reach_higher_point = False
                    self.count_rise = 0
                    self.change_image(self.standing_image[self.direction])

    def return_on_the_ground(self):
        self.move_right_left = False
        delta = 2 * TILE_SIZE // 10
        if self.count_iteration_return_ground == 0:
            self.change_image(self.jumping_image[self.direction])
        if self.count_iteration_return_ground == 15:
            self.change_image(self.standing_image[self.direction])
        if self.count_iteration_return_ground % 2 == 0:
            self.rect = self.rect.move(0, delta)
            self.count_iteration_return_ground += 1
        else:
            self.count_iteration_return_ground += 1

        if find_collision(self, grass_group):
            self.return_from_stump_on_the_ground = False

    def change_image(self, image_name):
        self.image = load_image(image_name, -1)
        self.image = pygame.transform.scale(self.image, (100, 100))

    def moving_forward_backward(self):
        if self.count_loop % 8 == 0:
            current_image = self.count_iteration_left_right % len(self.walking_image[self.direction])
            self.change_image(self.walking_image[self.direction][current_image])
            self.count_iteration_left_right += 1
        if self.count_iteration_left_right == 2:
            self.rect = self.rect.move(self.delta_walk, 0)
            self.move_right_left = False
            self.count_iteration_left_right = 0
        self.count_loop += 1

    def jumping(self):
        self.delta_jump_y = 20
        if self.count_iteration_jump % 4 == 0:
            if not self.reach_higher_point:
                if self.count_rise < 10:
                    self.change_image(self.jumping_image[self.direction])
                    self.rect = self.rect.move(self.delta_jump_x, -self.delta_jump_y)
                    self.count_rise += 1
                else:
                    self.reach_higher_point = True
            else:
                self.rect = self.rect.move(self.delta_jump_x, self.delta_jump_y)
                collision = find_collision(self, grass_group)
                self.rect = self.rect.move(-self.delta_jump_x, -self.delta_jump_y)
                if not collision:
                    self.change_image(self.jumping_image[self.direction])
                    self.rect = self.rect.move(self.delta_jump_x, self.delta_jump_y)
                else:
                    self.rect = self.rect.move(self.delta_jump_x, self.delta_jump_y)
                    self.reach_higher_point = False
                    self.jump = False
                    self.cane_attack = False
                    self.delta_jump_x = 0
                    self.change_image(self.standing_image[self.direction])
                    self.count_rise = 0
        self.count_iteration_jump += 1

    def cane_attacking(self):
        if self.jump:
            image_name = self.images_with_cane[self.direction]
            self.change_image(image_name)
        else:
            self.jump = False

    def injury(self):
        if not self.current_injury:
            if not self.start_collision:
                if self.count_lives > 0:
                    self.count_lives -= 1
                else:
                    self.falling = True
                    self.current_injury = False
            self.current_injury = True
            self.change_image(self.dead_images[self.direction])
            self.start_collision = True
        if self.count_pain < 10 and not self.reach_higher_point_in_pain:
            self.rect = self.rect.move(0, -5)
            self.count_pain += 1
        else:
            if self.count_pain > 0:
                self.rect = self.rect.move(0, 5)
                self.count_pain -= 1
                self.reach_higher_point_in_pain = True
            else:
                image_name = self.standing_image[self.direction]
                if self.jump:
                    image_name = self.jumping_image[self.direction]
                self.change_image(image_name)
                self.current_injury = False
                self.reach_higher_point_in_pain = False

    def death(self):
        self.rect = self.rect.move(0, 10)

    def update(self, move_event=None):
        if self.current_injury:
            self.injury()
            return

        if self.falling:
            self.death()
            return

        if move_event in ["left", "right"]:
            self.direction = move_event
            if self.jump:
                if move_event == "right":
                    self.delta_jump_x = 10
                elif move_event == "left":
                    self.delta_jump_x = -10
                self.delta_jump_y = 20
                self.reach_higher_point = False
            else:
                self.move_right_left = True
                if move_event == "right":
                    self.delta_walk = 20
                elif move_event == "left":
                    self.delta_walk = -20

        if move_event == "jump":
            self.jump = True

        if move_event == "cane_attack":
            if self.jump:
                self.cane_attack = True
            else:
                self.cane_attack = False

        self.stump_collision_walk()
        self.rock_collision()

        if self.move_right_left:
            self.moving_forward_backward()

        if self.move_on_the_stump:
            self.jump = False

        if self.jump:
            self.stump_collision_jump()
            self.jumping()

        if self.cane_attack:
            self.cane_attacking()

        if self.return_from_stump_on_the_ground:
            self.return_on_the_ground()


class GorillaEnemy(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__(enemy_group, all_sprites)
        self.delta_walk = -20
        self.count_loop = 0
        self.count_movement = 0
        self.count_falling = 0
        self.direction = "left"

        self.move = True
        self.falling = False
        self.stump_height = None
        self.move_on_stump = False
        self.walking_image = get_gorilla_images()["walking"]
        self.defeated_image = get_gorilla_images()["defeated"]

        self.position_x = position_x * TILE_SIZE
        self.position_y = (position_y + 2) * TILE_SIZE

        self.image = load_image(self.walking_image[self.direction][0], -1)
        self.image = pygame.transform.scale(self.image, (2 * TILE_SIZE, 2 * TILE_SIZE))
        self.rect = self.image.get_rect().move(self.position_x, self.position_y)

        self.set_direction()
        self.change_image(self.walking_image[self.direction][0])

    def change_image(self, image_name):
        self.image = load_image(image_name, -1)
        self.image = pygame.transform.scale(self.image, (100, 100))

    def moving(self):
        if self.count_loop % 5 == 0:
            current_image = self.count_movement % len(self.walking_image)
            self.change_image(self.walking_image[self.direction][current_image])
            self.count_movement += 1
        if self.count_movement == 2:
            self.rect = self.rect.move(self.delta_walk, 0)
            self.count_movement = 0
        self.count_loop += 1

    def stump_collision(self):
        self.rect = self.rect.move(self.delta_walk, 0)
        collision = find_collision(self, stump_group)
        self.rect = self.rect.move(-self.delta_walk, 0)
        if self.move_on_stump:
            if not collision:
                self.rect = self.rect.move(self.delta_walk, self.stump_height)
                self.move_on_stump = False
        else:
            if collision:
                self.stump_height = collision.rect.h
                self.rect = self.rect.move(self.delta_walk, -self.stump_height)
                self.move_on_stump = True
                self.delta_walk = -self.delta_walk

    def set_direction(self):
        if player.rect.x < self.rect.x:
            self.direction = "left"
        else:
            self.direction = "right"

    def check_rock_collision(self):
        self.rect = self.rect.move(self.delta_walk, 0)
        collision = find_collision(self, rock_group)
        self.rect = self.rect.move(-self.delta_walk, 0)
        if collision:
            if collision.rect.x < self.rect.x and self.direction == "left":
                self.delta_walk = collision.rect.x + collision.rect.w - self.rect.x + 1000
            if collision.rect.x > self.rect.x and self.direction == "right":
                self.delta_walk = collision.rect.x - (self.rect.x + self.rect.w) + 1000
            self.rect = self.rect.move(self.delta_walk, 0)

    def collision_with_hero(self):
        if pygame.sprite.collide_mask(self, player):
            if player.cane_attack:
                self.change_image(self.defeated_image[self.direction])
                self.move = False
                self.falling = True
            else:
                player.injury()
        else:
            player.start_collision = False

    def fall(self):
        if self.count_falling % 2 == 0:
            self.rect = self.rect.move(0, 10)
        self.count_falling += 1
        if self.rect.y > 1000:
            self.falling = False

    def update(self, move_event=None):
        if self.move:
            if self.direction == "left":
                self.delta_walk = -20
            else:
                self.delta_walk = 20
            self.collision_with_hero()
            self.stump_collision()
            self.check_rock_collision()
            self.moving()
        if self.falling:
            self.fall()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(TILES_IMAGES[tile_type])
        if tile_type == "S":
            self.image = pygame.transform.scale(self.image, (3 * TILE_SIZE, 2 * TILE_SIZE))
            pos_y -= 1
            self.add(stump_group)
        elif tile_type == "H":
            self.image = pygame.transform.scale(self.image, (1 * TILE_SIZE, 2 * TILE_SIZE))
            pos_y -= 1
            # self.add(stump_group)
        else:
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)


def find_collision(current_object, group):
    x_1 = current_object.rect.x
    y_1 = current_object.rect.y
    width_1 = current_object.rect.w
    height_1 = current_object.rect.h
    for elem in group:
        x_2 = elem.rect.x
        y_2 = elem.rect.y
        width_2 = elem.rect.w
        height_2 = elem.rect.h
        if ((x_1 <= x_2 <= (x_1 + width_1)) and (y_1 <= y_2 <= (y_1 + height_1))) or \
                ((x_2 <= x_1 <= (x_2 + width_2)) and (y_2 <= y_1 <= (y_2 + height_2))) or \
                ((x_2 <= x_1 <= (x_2 + width_2)) and (y_1 <= y_2 <= (y_1 + height_1))) or \
                ((x_1 <= x_2 <= (x_1 + width_1)) and (y_2 <= y_1 <= (y_2 + height_2))):
            return elem
    return False


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
                player = ScroogeMcDuck(x, y + 2)
                player_group.add(player)
            elif level_map[y][x] == "M":
                grass = Tile(level_map[y][x], x, y + 2)
                grass_group.add(grass)
            elif level_map[y][x] == "R":
                rock = Tile(level_map[y][x], x, y + 2)
                rock_group.add(rock)
            elif level_map[y][x] == "A":
                # pass
                enemy = GorillaEnemy(x, y)
                enemy_group.add(enemy)
            else:
                if level_map[y][x] != ".":
                    Tile(level_map[y][x], x, y + 2)
    return player


def start_screen():
    image = pygame.transform.scale(load_image('screensaver.jpeg'), (WIDTH, HEIGHT))
    screen.blit(image, (0, 0))

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def lives_and_score():
    black_part = pygame.Surface([WIDTH, 2 * TILE_SIZE])
    black_part.fill(pygame.Color("black"))
    screen.blit(black_part, (0, 0))

    font = pygame.font.Font(None, 46)
    string_rendered = font.render("HEALTH:", True, pygame.Color("white"))
    string_rect = string_rendered.get_rect()
    string_rect.top = 35
    string_rect.x = WIDTH // 10
    screen.blit(string_rendered, string_rect)

    full_lives = player.count_lives
    lost_lives = 3 - player.count_lives

    lives_images = lives()
    lives_x = 250
    lives_y = 36
    for i in range(full_lives):
        image = load_image(lives_images["full"])
        image = pygame.transform.scale(image, (TILE_SIZE // 2, TILE_SIZE // 2))
        screen.blit(image, (lives_x, lives_y))
        lives_x += TILE_SIZE // 2 + 4

    for i in range(lost_lives):
        image = load_image(lives_images["lost"])
        image = pygame.transform.scale(image, (TILE_SIZE // 2, TILE_SIZE // 2))
        screen.blit(image, (lives_x, lives_y))
        lives_x += TILE_SIZE // 2 + 4

    string_rendered = font.render(f"MONEY: {'40000'}", True, pygame.Color("white"))
    string_rect = string_rendered.get_rect()
    string_rect.top = 35
    string_rect.x = WIDTH // 2 + WIDTH // 10
    screen.blit(string_rendered, string_rect)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("DuckTales")
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    start_screen()

    sky_colour = get_sky_colour()
    screen.fill(sky_colour)

    camera = Camera()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    # gorilla group creation???
    stump_group = pygame.sprite.Group()
    grass_group = pygame.sprite.Group()
    rock_group = pygame.sprite.Group()

    player = level_generation()

    clock = pygame.time.Clock()
    running = True

    move_left = False
    move_right = False

    while running:
        jump = False
        cane_attack = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                jump = True
            if keys[pygame.K_x]:
                cane_attack = True

        if move_right:
            player_group.update("right")
        if move_left:
            player_group.update("left")
        if jump:
            player_group.update("jump")
        if cane_attack:
            player_group.update("cane_attack")

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill(sky_colour)
        lives_and_score()

        player_group.update()
        enemy_group.update()

        all_sprites.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
