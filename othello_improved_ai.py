 # Reversi

import random
import sys

def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'
    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)

def resetBoard(board):
     # Blanks out the board it is passed, except for the original starting position.
     for x in range(8):
         for y in range(8):
             board[x][y] = ' '
     # Starting pieces:
     board[3][3] = 'X'
     board[3][4] = 'O'
     board[4][3] = 'O'
     board[4][4] = 'X'

def getNewBoard():  
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board

def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    board[xstart][ystart] = tile # temporarily set the tile on the board.
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'
    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    board[xstart][ystart] = ' ' # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard

def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
             if isValidMove(board, tile, x, y) != False:
                 validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
         for y in range(8):
             if board[x][y] == 'X':
                xscore += 1
             if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}
 
def enterPlayerTile():
    # Lets the player type which tile they want to be.
    # Returns a list with the player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
 
    # the first element in the list is the player's tile, the second is the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']
 
def whoGoesFirst(player1, player2):
     # Randomly choose the player who goes first.
     if random.randint(0, 1) == 0:
        return player1
     else:
        return player2

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False
 
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True
 
def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()
 
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
 
    return dupeBoard
 
def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def isOnEdge(x,y):
    #return true if it is an edge 
    if x==0 or x ==7 or y ==0 or y ==7:
        return True

def isAvoid27(x,y):
    # return false if the  cords is on row or col 2 7 
    if x==1 or x ==6 or y ==1 or y ==6:
        return False
    return True

def isAvoidAdjCorner(x, y):
    # return fase if it is adj
    if x==0 or x ==1 or x ==6 or x == 7:
        if y==0 or y ==1 or y ==6 or y == 7:
            return False
    return True

def showPoints(player1_Tile, player2_Tile, mode):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    if (mode == 1):
        print('Original ai (X) has %s points. The improved ai (O) has %s points.' % (scores[player1_Tile], scores[player2_Tile]))
    elif (mode == 2):
        print('You have %s points. The improved ai has %s points.' % (scores[player1_Tile], scores[player2_Tile]))
    elif (mode == 3):
        print('You have %s points. The original ai has %s points.' % (scores[player1_Tile], scores[player2_Tile]))

def nextMoveOptions(board,computerTile):
    # return the length of the opponent moves  
    if computerTile == 'X':
        playerTile='O'
    else:
        playerTile='X'
    possibleMoves = getValidMoves(board, playerTile)
    return len(possibleMoves)

def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')
 
    return [x, y]

def adjcornerspots(x,y):
    # if x and y is a corner return the cords of the value  that are adj to the corner, else return empty set
    if x == 0 and y==0:
        return [[0, 1], [1, 1],[1,0]]
    elif x == 0 and y == 7:
        return [[0, 6], [1, 6],[1,7]]
    elif x== 7 and y ==0: 
        return [[7, 1], [6, 1],[6,0]]
    elif x==7 and y ==7:
        return [[7, 6], [6, 7],[6,6]]
    else:
        return []

def getOrginalComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves

    random.shuffle(possibleMoves)
     # always go for a corner if available
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all the possible moves and remember the best scoring move
    bestScore = -1

    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score

    return bestMove

def getImprovedComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    # randomize the order of the possible movesx
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y) and isAvoid27(x,y):
            return [x, y]

    
    bestScore=  -1
    lowestoption =1000 
    bestMove=[]

    # check if their is a save move if there is a save move return the safe move
    if board[0][0] == computerTile:
        temp = adjcornerspots(0,0)
        for x,y in temp:
            if [x,y] in possibleMoves:
                return [x,y]
    if board[0][7] == computerTile:
        temp = adjcornerspots(0,7)
        for x,y in temp:
            if [x,y] in possibleMoves:
                return [x,y]
    if board[7][0] == computerTile:
        temp = adjcornerspots(7,0)
        for x,y in temp:
            if [x,y] in possibleMoves:
                return [x,y]
    if board[7][7] == computerTile:
        temp = adjcornerspots(7,7)
        for x,y in temp:
            if [x,y] in possibleMoves:
                return [x,y]

  


    scores = getScoreOfBoard(board)
    counter = scores['X'] +  scores['O']
    if (counter<44):
        #check if move is a edge move 
        edge=[]
        for x, y in possibleMoves:
            if isOnEdge(x, y) and isAvoid27(x,y):
                edge.append([x, y])
        for x, y in edge:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile, x, y)
            option = nextMoveOptions(dupeBoard,computerTile)
            if lowestoption > option and isAvoid27(x,y) and option != 0:
                bestMove = [x, y]
                lowestoption = option
        if bestMove!= []:
            return bestMove
    
        # 4*4
        for x, y in possibleMoves:
            if isAvoid27(x,y):
                dupeBoard = getBoardCopy(board)
                makeMove(dupeBoard, computerTile, x, y)
                option = nextMoveOptions(dupeBoard,computerTile)
                if lowestoption > option and option != 0:
                    bestMove = [x, y]
                    lowestoption = option
        if bestMove!= []:
            return bestMove

        # 27
        for x, y in possibleMoves:
            if isAvoidAdjCorner(x,y):
                dupeBoard = getBoardCopy(board)
                makeMove(dupeBoard, computerTile, x, y)
                option = nextMoveOptions(dupeBoard,computerTile)
                if lowestoption > option and option != 0:
                    bestMove = [x, y]
                    lowestoption = option
        if bestMove!= []:
            return bestMove

        # adj corner
        for x, y in possibleMoves:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile, x, y)
            option = nextMoveOptions(dupeBoard,computerTile)
            if lowestoption > option and option != 0:
                bestMove = [x, y]
                lowestoption = option
        return bestMove
    elif(counter<50):
        for x, y in possibleMoves:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile, x, y)
            option = nextMoveOptions(dupeBoard,computerTile)
            if lowestoption > option and option != 0:
                bestMove = [x, y]
                lowestoption = option
        return bestMove
    else: 
        #most flip
        for x, y in possibleMoves:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile, x, y)
            score = getScoreOfBoard(dupeBoard)[computerTile]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
    return bestMove
 

# Main runner code 
print('Welcome to Reversi!')

print('Mode 0: original ai vs original ai (control test)')
print('Mode 9: original ai vs improved ai (statistics test)')
print('Mode 1: original ai vs improved ai')
print('Mode 2: player vs original ai')
print('Mode 3: player vs improved ai')

mode = input ("Enter one of the modes: ")
if(mode == '0'): #test mode for statistics - original ai 1 vs original ai 2
    original_ai1_victories = 0
    original_ai2_victories = 0
    tied_games = 0
    games_run = 0
    games_to_run = input ("Enter games to run: ")
    while True:
        mainBoard = getNewBoard()
        resetBoard(mainBoard)
        original_ai1_Tile= "X"
        original_ai2_Tile = "O"
        showHints = False
        turn = whoGoesFirst('original ai 1', 'original ai 2')

        while True:
            if turn == 'original ai 1':            
                try:
                    x, y = getOrginalComputerMove(mainBoard, original_ai1_Tile)
                except:
                    break
                makeMove(mainBoard, original_ai1_Tile, x, y)
    
                if getValidMoves(mainBoard, original_ai2_Tile) == []:
                    scores = getScoreOfBoard(mainBoard)
                    counter = scores['X'] +  scores['O']
                    if counter ==64:
                        break
                    else:
                        turn = 'original ai 2'
                else:
                    turn = 'original ai 2'
            # original ai 2 turn
            else:
                try:
                    x, y = getOrginalComputerMove(mainBoard, original_ai2_Tile)
                except:
                    break
                makeMove(mainBoard, original_ai2_Tile, x, y)
    
                if getValidMoves(mainBoard, original_ai1_Tile) == []:
                    scores = getScoreOfBoard(mainBoard)
                    counter = scores['X'] +  scores['O']
                    if counter ==64:
                        break
                    else:
                        turn = 'original ai 1'
                else:
                    turn = 'original ai 1'
        scores = getScoreOfBoard(mainBoard)

        if scores[original_ai1_Tile] > scores[original_ai2_Tile]:
            original_ai1_victories = original_ai1_victories + 1
            games_run = games_run + 1
            print('Orginal ai 1 won by %s points!' % (scores[original_ai1_Tile] - scores[original_ai2_Tile])) 
        elif scores[original_ai1_Tile] < scores[original_ai2_Tile]:
            original_ai2_victories = original_ai2_victories + 1
            games_run = games_run + 1
            print('Orginal ai 2 won by %s points!' % (scores[original_ai2_Tile] - scores[original_ai1_Tile]))
        else:
            tied_games = tied_games + 1
            games_run = games_run + 1
            print('The game was a tie!')
        if (games_run >= int(games_to_run)):
            print("-------------------------------------")
            print("Games simulated: ", games_to_run)
            print("Original ai 1 victories: ", original_ai1_victories)
            print("Original ai 2 victories: ", original_ai2_victories)
            print("Tied games: ", tied_games)
            victories_original_ai2_percentage_no_tie = (original_ai2_victories/(int(games_to_run)-tied_games))*100
            victories_original_ai2_percentage_with_with_win_tie = ((original_ai2_victories+tied_games)/(int(games_to_run)))*100
            victories_original_ai2_percentage_with_with_lose_tie = ((original_ai2_victories)/(int(games_to_run)))*100
            print("Percentage of victories of the original ai 2 (excluding tied games): {:.2f}%".format(victories_original_ai2_percentage_no_tie))
            print("Percentage of victories of the original ai 2 (where tied games are victories): {:.2f}%".format(victories_original_ai2_percentage_with_with_win_tie))
            print("Percentage of victories of the original ai 2 (where tied games are loses): {:.2f}%".format(victories_original_ai2_percentage_with_with_lose_tie))
            print("-------------------------------------")
            break
elif(mode == '9'): #test mode for statistics - original ai vs improved ai (statistics)
    original_ai_victories = 0
    improved_ai_victories = 0
    tied_games = 0
    games_run = 0
    games_to_run = input ("Enter games to run: ")
    while True:
        mainBoard = getNewBoard()
        resetBoard(mainBoard)
        original_ai_Tile= "X"
        improved_ai_Tile = "O"
        showHints = False
        turn = whoGoesFirst('original ai','improved ai')

        while True:
            # original ai's turn
            if turn == 'original ai':            
                try:
                    x, y = getOrginalComputerMove(mainBoard, original_ai_Tile)
                except:
                    break
                makeMove(mainBoard, original_ai_Tile, x, y)
    
                if getValidMoves(mainBoard, improved_ai_Tile) == []:
                    scores = getScoreOfBoard(mainBoard)
                    counter = scores['X'] +  scores['O']
                    if counter ==64:
                        break
                    else:
                        turn = 'improved ai'
                else:
                    turn = 'improved ai'
            # improved ai turn
            else:
                try:
                    x, y = getImprovedComputerMove(mainBoard, improved_ai_Tile)
                except:
                    break
                makeMove(mainBoard, improved_ai_Tile, x, y)
    
                if getValidMoves(mainBoard, original_ai_Tile) == []:
                    scores = getScoreOfBoard(mainBoard)
                    counter = scores['X'] +  scores['O']
                    if counter ==64:
                        break
                    else:
                        turn = 'original ai'
                else:
                    turn = 'original ai'
        scores = getScoreOfBoard(mainBoard)

        if scores[original_ai_Tile] > scores[improved_ai_Tile]:
            original_ai_victories = original_ai_victories + 1
            games_run = games_run + 1
            print('Orginal ai won by %s points!' % (scores[original_ai_Tile] - scores[improved_ai_Tile])) 
        elif scores[original_ai_Tile] < scores[improved_ai_Tile]:
            improved_ai_victories = improved_ai_victories + 1
            games_run = games_run + 1
            print('Improved ai won by %s points!' % (scores[improved_ai_Tile] - scores[original_ai_Tile]))
        else:
            tied_games = tied_games + 1
            games_run = games_run + 1
            print('The game was a tie!')
        #print(games_run)
        if (games_run >= int(games_to_run)):
            print("-------------------------------------")
            print("Games simulated: ", games_to_run)
            print("Original ai victories: ", original_ai_victories)
            print("Improved ai victories: ", improved_ai_victories)
            print("Tied games: ", tied_games)
            victories_improved_ai_victories_percentage_no_tie = (improved_ai_victories/(int(games_to_run)-tied_games))*100
            victories_improved_ai_victories_percentage_with_win_tie = ((improved_ai_victories+tied_games)/(int(games_to_run)))*100
            victories_improved_ai_victories_percentage_with_lose_tie = ((improved_ai_victories)/(int(games_to_run)))*100
            print("Percentage of victories of the improved ai (excluding tied games): {:.2f}%".format(victories_improved_ai_victories_percentage_no_tie))
            print("Percentage of victories of the improved ai (where tied games are victories): {:.2f}%".format(victories_improved_ai_victories_percentage_with_win_tie))
            print("Percentage of victories of the improved ai (where tied games are loses): {:.2f}%".format(victories_improved_ai_victories_percentage_with_lose_tie))
            print("-------------------------------------")
            break
elif(mode == '1'): #original ai vs improved ai with show play
    while True:
        # Reset the board and game.
        mainBoard = getNewBoard()
        resetBoard(mainBoard)
        stopper = input().lower()
        original_ai_Tile= "X"
        improved_ai_Tile = "O"
        showHints = False
        turn = whoGoesFirst('original ai','improved ai')
        print('The ' + turn + ' will go first.')

        while True:
            # original ai's turn
            if turn == 'original ai':
                drawBoard(mainBoard)
                showPoints(original_ai_Tile, improved_ai_Tile, 1)
                input('Press Enter to see the orginal ai\'s move.')
                try:
                    x, y = getOrginalComputerMove(mainBoard, original_ai_Tile)
                except:
                    break
                makeMove(mainBoard, original_ai_Tile, x, y)
    
                if getValidMoves(mainBoard, improved_ai_Tile) == []:

                    break
                else:
                    turn = 'improved ai'
    
            else:
                # improved ai's turn.
                drawBoard(mainBoard)
                showPoints(original_ai_Tile, improved_ai_Tile, 1)
                input('Press Enter to see the improved ai\'s move.')
                try:
                    x, y = getImprovedComputerMove(mainBoard, improved_ai_Tile)
                except:
                    break
                makeMove(mainBoard, improved_ai_Tile, x, y)
    
                if getValidMoves(mainBoard, original_ai_Tile) == []:

                    break
                else:
                    turn = 'original ai'

        # Display the final score.
        drawBoard(mainBoard)
        scores = getScoreOfBoard(mainBoard)

        print('X (original ai) scored %s points. O (improved ai) scored %s points.' % (scores['X'], scores['O']))
        if scores[original_ai_Tile] > scores[improved_ai_Tile]:
            print('Orginal ai won by %s points!' % (scores[original_ai_Tile] - scores[improved_ai_Tile]))
            
        elif scores[original_ai_Tile] < scores[improved_ai_Tile]:
            print('Improved ai won by %s points!' % (scores[improved_ai_Tile] - scores[original_ai_Tile]))
        else:
            print('The game was a tie!')
        if not playAgain():
            break
elif(mode == '2'): #player vs improved ai with show play 
    while True:
        # Reset the board and game.
        mainBoard = getNewBoard()
        resetBoard(mainBoard)
        playerTile, computerTile = enterPlayerTile()
        showHints = False
        turn = whoGoesFirst('player','improved ai')
        print('The ' + turn + ' will go first.')

        while True:
            if turn == 'player':
                # Player's turn.
                if showHints:   
                    validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(mainBoard)
                showPoints(playerTile, computerTile, 2)
                move = getPlayerMove(mainBoard, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit() # terminate the program
                elif move == 'hints':
                    showHints = not showHints
                    continue

                else:
                    makeMove(mainBoard, playerTile, move[0], move[1])
                if getValidMoves(mainBoard, computerTile) == []:
                    break
                else:
                    turn = 'improved ai'
    
            else:
                # Computer's turn.
                drawBoard(mainBoard)
                showPoints(playerTile, computerTile, 2)
                input('Press Enter to see the improved ai\'s move.')
                try:
                    x, y = getImprovedComputerMove(mainBoard, computerTile)
                except:
                    break
                makeMove(mainBoard, computerTile, x, y)
    
                if getValidMoves(mainBoard, playerTile) == []:

                    break
                else:
                    turn = 'player'

        # Display the final score.
        drawBoard(mainBoard)
        scores = getScoreOfBoard(mainBoard)
        if (playerTile == 'X'):
            print('X (%s) scored %s points. O (%s) scored %s points.' % ('you', scores['X'], 'improved ai', scores['O']))
        else:
            print('X (%s) scored %s points. O (%) scored %s points.' % ('improved ai', scores['X'], 'you', scores['O']))
        if scores[playerTile] > scores[computerTile]:
            print('You beat the improved ai by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
        elif scores[playerTile] < scores[computerTile]:

            print('You lost. The improved ai beat you by %s points!' % (scores[computerTile] - scores[playerTile]))
        else:
            print('The game was a tie!')
        if not playAgain():
            break
elif(mode == '3'): #player vs original ai with show play 
    while True:
        # Reset the board and game.
        mainBoard = getNewBoard()
        resetBoard(mainBoard)
        playerTile, computerTile = enterPlayerTile()
        showHints = False
        turn = whoGoesFirst('player','original ai')
        print('The ' + turn + ' will go first.')

        while True:
            if turn == 'player':
                # Player's turn.
                if showHints:   
                    validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(mainBoard)
                showPoints(playerTile, computerTile, 3)
                move = getPlayerMove(mainBoard, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit() # terminate the program
                elif move == 'hints':
                    showHints = not showHints
                    continue

                else:
                    makeMove(mainBoard, playerTile, move[0], move[1])
                if getValidMoves(mainBoard, computerTile) == []:
                    break
                else:
                    turn = 'original ai'
    
            else:
                # Computer's turn.
                drawBoard(mainBoard)
                showPoints(playerTile, computerTile, 3)
                input('Press Enter to see the original ai\'s move.')
                try:
                    x, y = getOrginalComputerMove(mainBoard, computerTile)
                except:
                    break
                makeMove(mainBoard, computerTile, x, y)
    
                if getValidMoves(mainBoard, playerTile) == []:

                    break
                else:
                    turn = 'player'

        # Display the final score.
        drawBoard(mainBoard)
        scores = getScoreOfBoard(mainBoard)
        if (playerTile == 'X'):
            print('X (%s) scored %s points. O (%s) scored %s points.' % ('you', scores['X'], 'original ai', scores['O']))
        else:
            print('X (%s) scored %s points. O (%) scored %s points.' % ('original ai', scores['X'], 'you', scores['O']))
        if scores[playerTile] > scores[computerTile]:
            print('You beat the original ai by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
        elif scores[playerTile] < scores[computerTile]:

            print('You lost. The original ai beat you by %s points!' % (scores[computerTile] - scores[playerTile]))
        else:
            print('The game was a tie!')
        if not playAgain():
            break