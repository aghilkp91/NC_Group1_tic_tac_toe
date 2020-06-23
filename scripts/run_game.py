import argparse
import json
import pygame
import sys

from game import Game


def main(board_width, board_height, title, fps, should_use_ai, ai_genes, should_use_minimax, run_loop):
    """
    Main game loop
    """
    pygame.init()
    screen = pygame.display.set_mode([board_width, board_height])
    pygame.display.set_caption(title)
    pygame.font.init()
    clock = pygame.time.Clock()
    comp_vs_comp = False
    if (should_use_minimax and should_use_ai):
        comp_vs_comp = True
    game = Game(board_width, board_height, should_use_ai, ai_genes, should_use_minimax, comp_vs_comp)
    curr_loop = 0
    run_maximum = int(run_loop) if run_loop else -1

    while True:
        no_of_games = game.get_no_of_games()
        if run_maximum != -1 and no_of_games > run_maximum:
            results = game.get_results()
            print_result(results)
            pygame.quit()
            sys.exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                results = game.get_results()
                print_result(results)
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and comp_vs_comp == False:
                game.notify_click(event.pos)
        game.draw(screen)
        game.update(screen)

        pygame.display.update()
        clock.tick(fps)

def print_result(results):
    for key, value in results.items():
        print(key, ' : ', value)


def run(should_use_ai, should_use_minimax, run_loop):
    """
    Run the program using the cli inputs
    """
    BOARD_WIDTH = 800
    BOARD_HEIGHT = 600
    TITLE = 'Tic-Tac-Toe'
    FPS = 60
    AI_GENES = None

    SHOULD_USE_AI = bool(should_use_ai)
    if SHOULD_USE_AI:
        print('Using AI...')
        ai_genes_dict = json.load(open("data/best_genes.json", 'r'))
        AI_GENES = (float(ai_genes_dict['aggressive_gene']), float(ai_genes_dict['defensive_gene']), float(ai_genes_dict['random_gene']))

    SHOULD_USE_MINIMAX = bool(should_use_minimax)
    print(run_loop)

    main(BOARD_WIDTH, BOARD_HEIGHT, TITLE, FPS, SHOULD_USE_AI, AI_GENES, SHOULD_USE_MINIMAX, run_loop)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tic Toe Game vs Evolution AI vs Minimax')
    parser.add_argument('-e', '--use-ai', dest='use_ai', action='store_true', help='Enable the evolutionary algorithm and instead play a 2-person game')
    parser.add_argument('-m', '--use-minimax', dest='use_minimax', action='store_true',
                        help='Enable the minimax and instead play a 2-person game')
    parser.add_argument('-n', '--run-loop', dest='run_loop',
                        help='Run the game for given number of times')
    args = parser.parse_args()

    try:
        run(args.use_ai, args.use_minimax, args.run_loop)
    except Exception as e:
        print(e)
