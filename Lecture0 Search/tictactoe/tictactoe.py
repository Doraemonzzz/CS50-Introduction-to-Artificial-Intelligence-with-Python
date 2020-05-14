"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                o += 1
    
    if x <= o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.append((i, j))
                
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    if board[i][j] != EMPTY:
        raise BaseException
    p = player(board)
    newboard = copy.deepcopy(board)
    newboard[i][j] = p
    
    return newboard
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    w = None
    #检查行
    for i in range(3):
        j = 1
        while j < 3 and board[i][j - 1] == board[i][j]:
            j += 1
        if j == 3:
            w = board[i][0]
            break
    #检查列
    for i in range(3):
        j = 1
        while j < 3 and board[j - 1][i] == board[j][i]:
            j += 1
        if j == 3:
            w = board[0][i]
            break
    #检查对角线
    i = 1
    while i < 3 and board[i][i] == board[i - 1][i - 1]:
        i += 1
    if i == 3:
        w = board[0][0]
        
    i = 1
    while i < 3 and board[i][2 - i] == board[i - 1][3 - i]:
        i += 1
    if i == 3:
        w = board[0][2]
        
    return w


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    action = actions(board)
    #无法再做动作
    if action == []:
        return True
    w = winner(board)
    #有胜者
    if w == X or w == O:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0

def Max(board):
    if terminal(board):
        return utility(board), None
    value = -1e9
    act = None
    action = actions(board)
    for a in action:
        V, A = Min(result(board, a))
        if V > value:
            value = V
            act = a
        
    return value, act
        
def Min(board):
    if terminal(board):
        return utility(board), None
    value = 1e9
    act = None
    action = actions(board)
    for a in action:
        V, A = Max(result(board, a))
        if V < value:
            value = V
            act = a
        
    return value, act

def Max_prone(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    act = None
    action = actions(board)
    for a in action:
        V, A = Min_prone(result(board, a), alpha, beta)
        if V > alpha:
            alpha = V
            act = a
        if alpha >= beta:
            return beta, act
        
    return alpha, act

def Min_prone(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    act = None
    action = actions(board)
    for a in action:
        V, A = Max_prone(result(board, a), alpha, beta)
        if V < beta:
            beta = V
            act = a
        if alpha >= beta:
            return alpha, act
        
    return beta, act

'''
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    p = player(board)
    if p == X:
        return Max(board)[-1]
    else:
        return Min(board)[-1]
'''
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    p = player(board)
    alpha = -1e9
    beta = 1e9
    if p == X:
        return Max_prone(board, alpha, beta)[-1]
    else:
        return Min_prone(board, alpha, beta)[-1]
