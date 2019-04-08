import sys
import pygame
import ctypes

from health import health_bar
from background.background import Background
from actors.player import Player
from actors.enemy import Enemy
from utilities.node import Node
from utilities import globals


def main():
    pygame.init()

    screen_width, screen_height = 1280, 720
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    if screen_width > 1920 and screen_height > 1080:
        screen_width, screen_height = 1920, 1080
    elif screen_width < 800 and screen_height < 600:
        print("Your screen resolution is too low")
        sys.exit(0)

    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("Small py game demo")

    background01 = Background('resources/sprites/background_space01.jpg', screen)
    background01.set_location(0, 0)
    background02 = Background('resources/sprites/background_space02.jpg', screen)
    background02.set_location(0, screen_height)

    node_background01 = Node(background01)
    node_background02 = Node(background02)
    node_background01.set_next(node_background02)
    node_background02.set_next(node_background01)

    start_point = [screen.get_rect().centerx, screen.get_rect().centery]
    main_player = Player(screen)
    main_player.set_location(start_point[0], start_point[1])
    main_player.start()
    main_player_health_bar = health_bar.HealthBar('resources/sprites/health_bar.png', screen, main_player)
    main_player_health_bar.set_location(15, 15)

    enemy_start_point = [screen.get_rect().centerx, screen.get_rect().top]
    enemy = Enemy(screen)
    enemy.set_location(enemy_start_point[0], enemy_start_point[1])
    enemy.start()

    main_player.add_target(enemy)
    enemy.add_target(main_player)

    background_node = node_background01
    next_background_node = node_background01.next()
    background = background_node.get_value()
    next_background = next_background_node.get_value()
    background.set_location(0, 0)
    next_background.set_location(0, -screen.get_height())

    is_game_running = True

    while is_game_running:
        main_player_health_bar.draw_health_bar()
        screen.blit(main_player.get_image(), main_player.get_rect())
        screen.blit(enemy.get_image(), enemy.get_rect())
        pygame.display.update()

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and
                pygame.key.get_pressed()[pygame.K_ESCAPE]) or event.type == pygame.QUIT:
                is_game_running = False

        if pygame.key.get_pressed()[pygame.K_RIGHT] and (main_player.get_rect().right < screen.get_rect().right):
            main_player.move(globals.DIRECTION["RIGHT"])

        elif pygame.key.get_pressed()[pygame.K_LEFT] and (main_player.get_rect().left > screen.get_rect().left):
            main_player.move(globals.DIRECTION["LEFT"])

        if pygame.key.get_pressed()[pygame.K_UP] and (main_player.get_rect().top > screen.get_rect().top):
            main_player.move(globals.DIRECTION["TOP"])

        elif pygame.key.get_pressed()[pygame.K_DOWN] and (main_player.get_rect().bottom < screen.get_rect().bottom):
            main_player.move(globals.DIRECTION["BOTTOM"])

        background.move(globals.DIRECTION["BOTTOM"])
        next_background.move(globals.DIRECTION["BOTTOM"])
        if background.get_rect().top > screen.get_rect().bottom:
            background.set_location(0, -screen.get_height())
            background_node = next_background_node
            next_background_node = next_background_node.next()
            background = background_node.get_value()
            next_background = next_background_node.get_value()

        screen.blits(blit_sequence=[(background.get_image(), background.get_rect()),
                                    (next_background.get_image(), next_background.get_rect())])

    sys.exit(0)


main()
