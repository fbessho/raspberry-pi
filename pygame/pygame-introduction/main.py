# encoding: utf-8
import pygame
import tmx

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()
        self.jump = pygame.mixer.Sound('jump.wav')
        self.shoot = pygame.mixer.Sound('shoot.wav')
        self.explosion = pygame.mixer.Sound('explosion.wav')

        self.tilemap = tmx.load('map.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)

        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)

        while True:
            dt = clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.tilemap.update(dt / 1000., self)
            screen.fill((200, 200, 200))
            # screen.blit(background, (0, 0))
            self.tilemap.draw(screen)
            pygame.display.flip()

            if self.player.is_dead:
                print "YOU DIED"
                return

class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load('bullet.png')
    def __init__(self, location, direction, *groups):
        super(Bullet, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = direction
        self.lifespan = 1

    def update(self, dt, game):
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return
        self.rect.x += self.direction * 400 * dt

        if pygame.sprite.spritecollide(self, game.enemies, True):
            game.explosion.play()
            self.kill()

class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load('enemy.png')
    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = 1

    def update(self, dt, game):
        self.rect.x += self.direction * 100 * dt
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            self.direction *= -1
            break
        if self.rect.colliderect(game.player.rect):
            game.player.is_dead = True

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.right_image = pygame.image.load('player-right.png')
        self.left_image = pygame.image.load('player-left.png')
        self.image = self.right_image
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0;
        self.is_dead = False
        self.direction = 1
        self.gun_cooldown = 0

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.image = self.left_image
            self.direction = -1
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.image = self.right_image
            self.direction = 1
        if key[pygame.K_LSHIFT] and not self.gun_cooldown:
            if self.direction > 0:
                Bullet(self.rect.midright, 1, game.sprites)
            else:
                Bullet(self.rect.midleft, -1, game.sprites)
            self.gun_cooldown = 1
            game.shoot.play()

        self.gun_cooldown = max(0, self.gun_cooldown - dt)
        
        if self.resting: # 地上に停止
            self.dy = 0
            if key[pygame.K_SPACE]:
                self.dy = -500
                game.jump.play()
        else: # 空中
            self.dy = min(400, self.dy+40)

        self.rect.y += self.dy * dt

        new = self.rect
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            blockers = cell['blockers']
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                new.bottom = cell.top
                self.resting = True
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.resting = True

        game.tilemap.set_focus(new.x, new.y)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)

