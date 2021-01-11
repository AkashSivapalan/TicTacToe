from math import inf as infinity

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

moves = {
    1: [0, 0], 2: [0, 1], 3: [0, 2],
    4: [1, 0], 5: [1, 1], 6: [1, 2],
    7: [2, 0], 8: [2, 1], 9: [2, 2],
}

compTest = 1

scores = {"comp": 1, "player": -1, "tie": 0}


def printBoard():
    count = 1

    for x in range(0, 3):
        for y in range(0, 3):
            symbol = board[x][y]
            if symbol != 'X' and symbol != 'O':
                symbol = count
            if y != 2:
                endChar = " |"
            else:
                endChar = " "
            print(f' {symbol}', end=endChar)
            count += 1
        print('\n -   -   -')


def win(currentBoard, symbol):
    win_state = [
        [currentBoard[0][0], currentBoard[0][1], currentBoard[0][2]],
        [currentBoard[1][0], currentBoard[1][1], currentBoard[1][2]],
        [currentBoard[2][0], currentBoard[2][1], currentBoard[2][2]],
        [currentBoard[0][0], currentBoard[1][0], currentBoard[2][0]],
        [currentBoard[0][1], currentBoard[1][1], currentBoard[2][1]],
        [currentBoard[0][2], currentBoard[1][2], currentBoard[2][2]],
        [currentBoard[0][0], currentBoard[1][1], currentBoard[2][2]],
        [currentBoard[2][0], currentBoard[1][1], currentBoard[0][2]],
    ]
    if [symbol, symbol, symbol] in win_state:
        return True
    else:
        return False


def canMove(move):
    box = moves[move]
    if board[box[0]][box[1]] == 'X' or board[box[0]][box[1]] == 'O':
        return False
    return True


def playGame():
    compChoice = ''
    playerChoice = ''
    while playerChoice != 'X' and playerChoice != 'O':
        try:
            print('')
            playerChoice = input("Please choose to be either X or O: ").upper()
        except (EOFError, KeyboardInterrupt):
            print("Good bye")
            exit()
        except (ValueError):
            print("Choose between options X and O")
    if playerChoice == 'X':
        compChoice = 'O'
    else:
        compChoice = 'X'

    print(f"Player Character: {playerChoice}\nComp Character: {compChoice}")

    order = ''
    while order != 'F' and order != 'S':
        try:
            print('')
            order = input("Please choose to go either first(F) or second(S): ").upper()
        except (EOFError, KeyboardInterrupt):
            print("Good bye")
            exit()
        except (ValueError):
            print("Choose between options F and S")

    if order == 'S':
        compTurn(compChoice, playerChoice)
    while (not gameOver(board)):
        playerTurn(playerChoice)
        if gameOver(board):
            break
        compTurn(compChoice, playerChoice)


    if win(board, playerChoice):
        print("Congrats, You win")
    elif win(board, compChoice):
        print("AWW YOU LOSE")
    else:
        print("Tie")


def playerTurn(playerChoice):
    print("It is the players turn.")
    printBoard()

    move = int(input("Type in the number of the box you want to place a piece: "))

    while (not canMove(move)) or (move > 9) or (move < 1):
        print("Enter a valid space!")
        move = int(input("Type in the number of the box you want to place a piece: "))
    box = moves[move]
    board[box[0]][box[1]] = playerChoice
    printBoard()
    return


def compTurn(compChoice, playerChoice):
    print("It is the computers turn")
    depth = len(empty_Cells(board))
    if depth == 9:
        board[0][0] = compChoice
        print(board)
    else:
        best_move = minimax(board, depth, compChoice, playerChoice, compTest)
        board[best_move[0]][best_move[1]] = compChoice
    printBoard()


def minimax(currentBoard, depth, compChoice, playerChoice, player):
    result = ""
    if player == compTest:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, infinity]

    if depth == 0 or gameOver(currentBoard):
        if win(currentBoard, compChoice):
            result = "comp"
        elif win(currentBoard, playerChoice):
            result = "player"
        elif depth == 0:
            result = "tie"
        score = scores[result]
        return [-1, -1, score]

    for box in empty_Cells(currentBoard):
        x, y = box[0], box[1]
        if player == 1:
            currentBoard[x][y] = compChoice
        elif player == -1:
            currentBoard[x][y] = playerChoice
        score = minimax(currentBoard, depth - 1, compChoice, playerChoice, -player)
        currentBoard[x][y] = 0
        score[0], score[1] = x, y

        if player == compTest:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def gameOver(currentBoard):
    depth = len(empty_Cells(currentBoard))

    if win(currentBoard, 'X') or win(currentBoard, 'O') or depth == 0:
        return True

    return False


def empty_Cells(currentBoard):
    empty = []
    for x, row in enumerate(currentBoard):
        for y, col in enumerate(row):
            if col == 0:
                empty.append([x, y])
    return empty


if __name__ == '__main__':
    print("Hello Player")
    printBoard()
    playGame()
