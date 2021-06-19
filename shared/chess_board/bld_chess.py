# TODO:
# Make board
# make it possible to move peices 
# Check if moves are legal
# Check if checkmate is reached or peices is in check.

def create_board():
    pieces_order = ["r","n","b","k","q","b","n","r"] # Each letter gives position
    board = [[]] 
    for _ in range(8):
        row = []
        for _ in range(9):
            row.append("")
        board.append(row)
    board[1] = ["", "wr","wn","wb","wk","wq","wb","wn","wr"]
    board[2] = ["","wp","wp","wp","wp","wp","wp","wp","wp"]
    board[8] = ["", "br","bn","bb","bk","bq","bb","bn","br"]
    board[7] = ["", "bp","bp","bp","bp","bp","bp","bp","bp"]
    print(board)
    return board

def start_game(board):
    still_playing = True
    white_turn = True
    while still_playing:
        if white_turn:
            board = try_move("w",board)
        else:
            move = input("What is the coordinate of the peice you want to move and the coordinate you want to move the piece to for example d8 d6:")
            board = try_move("b",board)
        white_turn != white_turn

def invert_1_8(num):
    return 8-num


def try_move(color, board):
    
    while True:
        if color == "w":
            print("It is white's turn")
        else:
            print("It is black's turn")
        initial = get_move()
        initial_coords_array = [invert_1_8(ord(initial[0]) - 65), int(initial[1])]
        final = get_move()
        final_coords_array = [invert_1_8(ord(final[0]) -65), int(final[1])]
        piece = board[initial_coords_array[1]][initial_coords_array[0]]
        board[initial_coords_array[1]][initial_coords_array[0]] = ""
        board[final_coords_array[1]][final_coords_array[0]] = piece
        break
        
    print("move complete")
    invis = False
    if not invis:
        show_board(board)
    return board

def show_board(board):
    for row in board:
        for piece in row:
            if piece == "":
                print("   ",end="")
            else:
                print(piece+" ",end="")
            
        print()

def get_move():
    move_recieved = False
    while move_recieved == False:
        move = input("What is the coordinate of the peice you want to move for example d2: ").upper()
        if verify_move_string(move):
            return move
        print("Move not proper")


def verify_move_string(initial):
    try:
        files_in_chess = ["a", "b", "c", "d", "e", "f","g","h"]
        if type(initial[0]) == str:
            if initial[0].lower() in files_in_chess:
                return verify_move_int(initial)
            return False
    except:
        return False

def verify_move_int(initial):
    try:
        if type(initial[1]) == int:
            if initial[1] < 1 or initial[1] > 8:
                return initial[1] 
    except:
        return False
            
if __name__ == "__main__":
    board = create_board()
    start_game(board)