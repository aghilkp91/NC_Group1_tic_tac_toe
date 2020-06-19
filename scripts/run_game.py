import argparse
import json
import pygame
import sys

from game import Game


def main(board_width, board_height, title, fps, should_use_ai, ai_genes):
    """
    Main game loop
    """
    pygame.init()
    screen = pygame.display.set_mode([board_width, board_height])
    pygame.display.set_caption(title)
    pygame.font.init()
    clock = pygame.time.Clock()
    game = Game(board_width, board_height, should_use_ai, ai_genes)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.notify_click(event.pos)

        game.draw(screen)
        game.update(screen)

        pygame.display.update()
        clock.tick(fps)


def run(genes_json, should_use_ai):
    """
    Run the program using the cli inputs
    """
    BOARD_WIDTH = 800
    BOARD_HEIGHT = 600
    TITLE = 'Tic-Tac-Toe'
    FPS = 60

    SHOULD_USE_AI = bool(should_use_ai)
    if SHOULD_USE_AI:
        print('Using AI...')

    ai_genes_dict = json.load(open(genes_json, 'r'))
    AI_GENES = (float(ai_genes_dict['aggressive_gene']), float(ai_genes_dict['defensive_gene']), float(ai_genes_dict['random_gene']))

    main(BOARD_WIDTH, BOARD_HEIGHT, TITLE, FPS, SHOULD_USE_AI, AI_GENES)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tic Toe Game vs Evolution AI')
    parser.add_argument('genes_json', help='Path for json containing AI gene data')
    parser.add_argument('-n', '--no-ai', dest='no_ai', action='store_false', help='Disable the game ui and instead play a 2-person game')
    args = parser.parse_args()

    try:
        run(args.genes_json, args.no_ai)
    except Exception as e:
        print(e)
