# NC_Group1_tic_tac_toe

###Goal
Our goal is to build an algorithm, using evolutionary algorithm and minimax,
which will follow the Tic Tac Toe game rules and will be able to play against each other. We will compare the performance
of both algorithm.

### Usage:
* Run ` make install ` to install the python dependencies
* Next run ` make train ` in order to train "optimal" genes which the game ai can use to play against you (The genes are stored in "./data/best_genes.json")
* Play against the trained ai by running ` python3 script/run-game.py -e `
* Play against the minimax by running ` python3 script/run-game.py -m `
