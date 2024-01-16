import sys; args = sys.argv[1:]

diff_games = 0
distinct_boards = 1
seen = set()

def main():
    default_board = "........."
    
    # i actually don't understand how this works 
    # b/c it doesn't account for boards starting
    # with o, but it still works
    tttoe(default_board, "x")
    
    print(distinct_boards, diff_games)

def tttoe(board, turn):
    global diff_games, distinct_boards, seen

    seen.add(board)

    if won(board) or completed(board):
        diff_games += 1
        return

    possible_choices = choices(board, turn)

    for choice in possible_choices:
        if not choice in seen: distinct_boards += 1
        tttoe(choice, "x" if turn == "o" else "o")


def choices(board, turn):
    possibles = set()

    for i in range(len(board)):
        if board[i] == ".":
            t_board = board[:i] + turn + board[i+1:]
            possibles.add(t_board)
            
    return possibles

def won(board):
    winnings = {
        (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (0,4,8),
        (2,4,6)
    }

    for plr in {"x", "o"}:
        for i,j,k in winnings:
            if board[i] == plr and board[j] == plr and board[k] == plr:
                return True
            
    return False

def completed(board):
    if "." in board:
        return False
    return True

if __name__ == "__main__":
    main()

