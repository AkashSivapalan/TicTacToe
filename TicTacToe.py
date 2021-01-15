from math import inf as infinity
import random

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


class user:
    def __init__(self, playerChar):
        self._player = playerChar

    def canMove(self, move):
        box = moves[move]
        if board[box[0]][box[1]] == 'X' or board[box[0]][box[1]] == 'O':
            return False
        return True

    def playerTurn(self):
        print("It is the players turn.")
        printBoard()

        move = self.playerMove()
        while (not self.canMove(move)):
            print("Enter a valid space!")
            move=self.playerMove()

        box = moves[move]
        board[box[0]][box[1]] = self._player
        printBoard()


    def playerMove(self):

        boxIndex= emptyBoxIndex()
        move = -1
        while(move not in boxIndex):
            try:
                userInput = int(input("Type in the number of the box you want to place a piece: "))
                move = int(userInput)
            except (ValueError):
                print("Enter a valid space. Must be INTERGER!")
                move =-1
        return move

    def getPlayerChar(self):
        return self._player



class comp():
    def __init__(self, playerChar, compChar):
        self._comp = compChar
        self._player = playerChar

    def minimax(self, currentBoard, depth, player):
        result = ""
        if player == compTest:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, infinity]

        if depth == 0 or gameOver(currentBoard):
            if win(currentBoard, self._comp):
                result = "comp"
            elif win(currentBoard, self._player):
                result = "player"
            elif depth == 0:
                result = "tie"
            score = scores[result]
            return [-1, -1, score]

        for box in empty_Cells(currentBoard):
            x, y = box[0], box[1]
            if player == 1:
                currentBoard[x][y] = self._comp
            elif player == -1:
                currentBoard[x][y] = self._player
            score = self.minimax(currentBoard, depth - 1, -player)
            currentBoard[x][y] = 0
            score[0], score[1] = x, y

            if player == compTest:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

        return best


class hardComp(comp):
    def __init__(self, playerChar, compChar):
        super().__init__(playerChar, compChar)

    def compTurn(self):
        print("It is the computers turn")
        depth = len(empty_Cells(board))
        if depth == 9:
            board[0][0] = self._comp
            print(board)
        else:
            best_move = self.minimax(board, depth, compTest)
            board[best_move[0]][best_move[1]] = self._comp
        printBoard()


class easyComp(comp):
    def __init__(self, playerChar, compChar):
        super().__init__(playerChar, compChar)

    def compTurn(self):
        print("It is the computers turn")
        depth = empty_Cells(board)

        rand = random.randint(0, len(depth) - 1)
        box = depth[rand]
        board[box[0]][box[1]] = self._comp
        printBoard()


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

    gameMode = ''
    while gameMode != 'E' and gameMode != 'H':
        try:
            print('')
            gameMode = input("Please choose to play on easy(E) or hard(H) mode: ").upper()
        except(ValueError):
            print("Choose between easy(E) or hard(H)")

    if gameMode == 'E':
        print("You will be playing on easy mode.")
    else:
        print("You will be playing on hard mode")

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

    player = user(playerChoice)
    if gameMode == 'H':
        comp = hardComp(playerChoice, compChoice)
    else:
        comp = easyComp(playerChoice, compChoice)

    print("Hello")

    if order == 'S':
        comp.compTurn()
    while (not gameOver(board)):
        player.playerTurn()
        if gameOver(board):
            break
        comp.compTurn()

    if win(board, playerChoice):
        print("Congrats, You win")
    elif win(board, compChoice):
        print("AWW YOU LOSE")
    else:
        print("It is a tie")


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

def emptyBoxIndex():
    empty = []
    count=0
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            count+=1
            if col == 0:
                empty.append(count)
    return empty

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


if __name__ == '__main__':
    print("Hello Player")
    printBoard()
    playGame()
