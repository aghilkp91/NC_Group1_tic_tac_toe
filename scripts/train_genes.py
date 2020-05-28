import argparse
import json
from matplotlib import pyplot as plt
import numpy as np
import os
import time

from game_ai import Game_AI


PLAYER1 = 'PLAYER 1'
PLAYER2 = 'PLAYER 2'
TIE = 'Tie'


def _build_random_gene_mutation(best_genes, evolution_rate):
    """
    Build a random mutation of the best genes based on the specified evolution rate
    """
    aggressive_mutation = np.random.random()
    defensive_mutation = np.random.random()
    random_mutation = np.random.random()

    aggressive_mutation = np.random.choice([1, -1]) * evolution_rate * aggressive_mutation / (aggressive_mutation + defensive_mutation + random_mutation)
    defensive_mutation = np.random.choice([1, -1]) * evolution_rate * defensive_mutation / (aggressive_mutation + defensive_mutation + random_mutation)

    evolved_genes = [0, 0, 0]
    evolved_genes[0] = int(min(max(best_genes[0] + aggressive_mutation, 0), 100))
    evolved_genes[1] = int(min(max(best_genes[1] + defensive_mutation, 0), 100))
    evolved_genes[1] = int(min(evolved_genes[1], 100 - evolved_genes[0]))
    evolved_genes[2] = int(100 - evolved_genes[1] - evolved_genes[0])

    return evolved_genes


def _check_winner(player_1_filled, player_2_filled):
    """
    Check if the game is over based on the player filled tuples
    """
    for i in range(3):
        if (sum([player_1_filled[i][j] for j in range(3)]) > 2) or (sum([player_1_filled[j][i] for j in range(3)]) > 2):
            return(PLAYER1)
        elif (sum([player_2_filled[i][j] for j in range(3)]) > 2) or (sum([player_2_filled[j][i] for j in range(3)]) > 2):
            return(PLAYER2)
    if (player_1_filled[0][0] + player_1_filled[1][1] + player_1_filled[2][2] > 2) or (player_1_filled[0][2] + player_1_filled[1][1] + player_1_filled[2][0] > 2):
        return(PLAYER1)
    if (player_2_filled[0][0] + player_2_filled[1][1] + player_2_filled[2][2] > 2) or (player_2_filled[0][2] + player_2_filled[1][1] + player_2_filled[2][0] > 2):
        return(PLAYER2)
    if sum([sum([player_1_filled[i][j] for i in range(3)]) for j in range(3)]) + sum([sum([player_2_filled[i][j] for i in range(3)]) for j in range(3)]) > 8:
        return(TIE)


def _play_game(ai1, ai2, starting_player=PLAYER1, board_size=3):
    """
    Plays a game between the two AIs
    """
    player_1_filled = [[0 for j in range(board_size)] for i in range(board_size)]
    player_2_filled = [[0 for j in range(board_size)] for i in range(board_size)]

    is_game_over = False
    current_player = starting_player
    while not is_game_over:
        if current_player == PLAYER1:
            new_position = ai1.choose_position(player_1_filled, player_2_filled)
            player_1_filled[new_position[0]][new_position[1]] = 1
        else:
            new_position = ai2.choose_position(player_2_filled, player_1_filled)
            player_2_filled[new_position[0]][new_position[1]] = 1
        current_player = PLAYER2 if current_player == PLAYER1 else PLAYER1
        winner = _check_winner(player_1_filled, player_2_filled)
        if winner:
            return winner


def _export_gene_evolution_plot(best_genes_log, gene_plot_path):
    """
    Build and export a png plot depicting the evolution of the best genes
    """
    plt.rcParams["figure.figsize"] = (16, 9)

    axes = plt.gca()
    axes.set_ylim([0, 100])

    plt.plot(list(range(len(best_genes_log))), [best_genes_log[i][0] for i in range(len(best_genes_log))], color='red', label='Aggressive')
    plt.plot(list(range(len(best_genes_log))), [best_genes_log[i][1] for i in range(len(best_genes_log))], color='green', label='Defensive')
    plt.plot(list(range(len(best_genes_log))), [best_genes_log[i][2] for i in range(len(best_genes_log))], color='blue', label='Random')
    plt.legend(loc='upper left')

    plt.title('Gene Evolution')
    plt.xlabel('Predicted Cycle')
    plt.xlabel('Gene Strength')

    plt.savefig(gene_plot_path)
    plt.clf()


def main(evolution_cycles, epoch_size, starting_genes, evolution_rate, best_genes_path, gene_plot_path, show_evolution_output):
    """
    Game AI trainer
    """
    best_genes_log = []
    best_genes = starting_genes

    print('### STARTING EVOLUTION ###')

    start_time = time.time()

    for i in range(evolution_cycles):
        evolved_genes = _build_random_gene_mutation(best_genes, evolution_rate)

        ai1 = Game_AI(best_genes[0], best_genes[1], best_genes[2])
        ai2 = Game_AI(evolved_genes[0], evolved_genes[1], evolved_genes[2])

        results = {}
        results[PLAYER1] = 0
        results[PLAYER2] = 0
        results[TIE] = 0

        starting_player = PLAYER1
        for _ in range(epoch_size):
            results[_play_game(ai1, ai2, starting_player)] += 1
            starting_player = PLAYER2 if starting_player == PLAYER1 else PLAYER1

        if show_evolution_output:
            print('Evolution Cycle: {0}'.format(i))
            print('Best Genes: {0}'.format(best_genes))
            print('Current Mutated Genes: {0}'.format(evolved_genes))
            print('Results: {0}'.format((int(100 * results[PLAYER1] / epoch_size), int(100 * results[PLAYER2] / epoch_size), int(100 * results[TIE] / epoch_size))))
            print('--------------------------------------------------')

        if results[PLAYER2] > results[PLAYER1]:
            best_genes = evolved_genes
        best_genes_log.append(best_genes)

    print('### RUNNING EVOLUTION TOOK {0} SECONDS ###'.format(round(time.time() - start_time, 1)))

    best_genes_dict = {'aggressive_gene': float(best_genes[0]), 'defensive_gene': float(best_genes[1]), 'random_gene': float(best_genes[2])}
    json.dump(best_genes_dict, open(best_genes_path, 'w'))

    _export_gene_evolution_plot(best_genes_log, gene_plot_path)


def run(verbose):
    """
    Run the program using the cli inputs
    """
    EVOLUTION_CYCLES = 30
    EPOCH_SIZE = 1000
    STARTING_GENES = (40, 40, 20)
    EVOLUTION_RATE = 20
    BEST_GENES_PATH = os.path.join(os.path.dirname(__file__), '../data/best_genes.json')
    GENE_PLOT_PATH = os.path.join(os.path.dirname(__file__), '../data/gene_evolution.png')
    SHOW_EVOLUTION_OUTPUT = bool(verbose)

    main(EVOLUTION_CYCLES, EPOCH_SIZE, STARTING_GENES, EVOLUTION_RATE, BEST_GENES_PATH, GENE_PLOT_PATH, SHOW_EVOLUTION_OUTPUT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tic Toe Game Evolution AI Trainer')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Output the evolution cycle results')
    args = parser.parse_args()

    try:
        run(args.verbose)
    except Exception as e:
        print(e)
