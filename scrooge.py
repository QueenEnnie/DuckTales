import pygame
import sys
import os
import images_creation

WIDTH, HEIGHT = 1000, 600
FPS = 60


class ScroogeMcDuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites_group)
        self.move = False
        self.direction = None
        self.count_change = 0
        self.count_loop = 0
        self.standing_image = images_creation.get_scrooge_standing_images()
        self.walking_image = images_creation.get_scrooge_walking_images()
        self.image = load_image(self.standing_image["left"], -1)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect().move(600, 300)

    def update(self, move_event=None):
        if move_event in ["right", "left"]:
            self.move = True
            self.direction = move_event
        delta = -20 if self.direction == "left" else 20
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


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("move")
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    all_sprites_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    player = ScroogeMcDuck()
    player_group.add(player)

    clock = pygame.time.Clock()
    running = True
    move_left = False
    move_right = False
    while running:
        left = False
        right = False
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
            if keys[pygame.K_LEFT]:
                left = True
            if keys[pygame.K_RIGHT]:
                right = True

        if move_right:
            if right:
                player_group.update("right")
                print(1)
            else:
                print("NO")
        if move_left:
            player_group.update("left")

        screen.fill("black")
        player_group.update()
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
