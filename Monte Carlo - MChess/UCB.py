import copy
import random
import math
import time

def UCB(board, n):
    """
    Algorithme d'UCB pour trouver le best move.

    :param board: de MChess
    :param n: nombre de playouts
    :return: best move à partir du board
    """
    moves = [i for i in board.legal_moves]

    sumScores = [0.0 for x in range(len(moves))]
    nbVisits = [0 for x in range(len(moves))]
    for i in range(n):  # on fait les n tirages et on apprend au fur et à mesure
        bestScore = 0
        bestMove = moves[0]
        place = 0
        for m in range(len(moves)):  # on calcule le score de chaque coût
            if nbVisits[m] > 0:
                score = sumScores[m] / nbVisits[m] + 0.4 * math.sqrt(math.log(i) / nbVisits[m])
            else:
                score = 10000000  # on explore tout !! du dernier au premier
            if score > bestScore:
                bestScore = score
                bestMove = moves[m]
                place = m
        b = copy.deepcopy(board)
        b.push(bestMove)  # on joue le meilleur score
        r = playout(b)

        sumScores[place] += r  # on met à jour les poids
        nbVisits[place] += 1
    bestScore = 0
    bestMove = moves[0]
    for m in range(1, len(moves)):  # on renvoie le meilleur move
        score = sumScores[m]
        if score > bestScore:
            bestScore = score
            bestMove = moves[m]
    return bestMove

def score(board):
    """
    Renvoie 1 si WHITE gagne, 0 sinon
    :param board:
    :return:
    """
    return 1 if board.result(claim_draw=True)=="1-0" else 0


def playout(b):
    """

    Joue une partie aléatoire et renvoie le score.
    :param b:
    :return:
    """
    start = time.time()
    while (True):
        moves = b.legal_moves
        moves = [i for i in moves]
        if b.is_game_over():
            return score(b)
        n = random.randint(0, len(moves) - 1)
        b.push(moves[n])