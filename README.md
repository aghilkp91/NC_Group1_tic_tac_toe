# NC_Group1_tic_tac_toe

###Goal
Our goal is to build a ​classification algorithm, using a random forest classification method and evolutionary algorithm,
which will follow the Tic Tac Toe game rules and will be able to play against each other. We will compare the performance
of both algorithm.

### Usage:
* Run ` make install ` to install the python dependencies
* Next run ` make train ` in order to train "optimal" genes which the game ai can use to play against you (The genes are stored in "./data/best_genes.json")
* Play between evolutionary and minimax run ` python3 scripts/run-game.py -m -e -n 149 `
