from bitstring import Bits

X_LOC=0 #beginning of bits for locations of x's
O_LOC=81 #beginning of bits for locations of o's
PREV_MOV=162 #beginning of bits for previous move location
TURN=171 #bit for player to move
X_VIC=172 #beginning of bits for x field victories
O_VIC=181 #beginning of bits for o field victories
X_W=190 #bit for x won
O_W=191 #bit for o won
#full bitstring length = 192

VICTORIES=(
    Bits(bin='0b111000000'), #across top
    Bits(bin='0b000111000'), #across middle
    Bits(bin='0b000000111'), #across bottom
    Bits(bin='0b100100100'), #down left
    Bits(bin='0b010010010'), #down middle
    Bits(bin='0b001001001'), #down right
    Bits(bin='0b100010001'), #diagonal \
    Bits(bin='0b001010100'), #diagonal /
)

def possible_moves(gamestate):
    moves=[]
    lastmove=9
    for i, b in enumerate(gamestate[PREV_MOV:PREV_MOV+9]): #set lastmove to the location of the previous move
        if b:
            lastmove=i
    if lastmove!=9: #if the last move
        for i, vic in enumerate(VICTORIES):
            if (gamestate[X_LOC+lastmove*9:X_LOC+lastmove*9+9]&vic==vic
                or gamestate[O_LOC+lastmove*9:O_LOC+lastmove*9+9]&vic==vic):
                lastmove=9
        if (gamestate[X_LOC+lastmove*9:X_LOC+lastmove*9+9]|
            gamestate[O_LOC+lastmove*9:O_LOC+lastmove*9+9]
            ==Bits(hex='0b111111111')):
            lastmove=9
    for i in range(9):
        if lastmove==i or lastmove==9:
            if gamestate[X_VIC+i] or gamestate[O_VIC+i]:
                continue
            for j in range(9):
                if not (gamestate[X_LOC+i*9+j] or gamestate[O_LOC+i*9+j]):
                    moves=moves+[(i+1,j+1)]
    return tuple(moves)

def check_legal(gamestate, move):
    return move in possible_moves(gamestate)

def make_move(gamestate, move):
    if not check_legal(gamestate, move):
        return False
    new_bin="0b"
    if gamestate[TURN]:
        new_bin=(new_bin+
        gamestate[X_LOC:X_LOC+81].bin +
        gamestate[O_LOC:O_LOC+(move[0]-1)*9+move[1]-1].bin + '1' +
            gamestate[O_LOC+(move[0]-1)*9+move[1]:O_LOC+81].bin +
        '0'*(move[1]-1)+'1'+'0'*(9-move[1]) +
        '0')
        new_bin=(new_bin+
        gamestate[X_VIC:X_VIC+9].bin +
        gamestate[O_VIC:O_VIC+move[0]-1].bin +
            str(int(subgrid_winner(Bits(bin=new_bin), move[0], 'O'))) +
            gamestate[O_VIC+move[0]:O_VIC+9].bin)
        new_bin=(new_bin+
        str(int(gamestate[X_W])) +
        str(int(total_winner(Bits(bin=new_bin), 'O'))))
    else:
        new_bin=(new_bin+
        gamestate[X_LOC:X_LOC+(move[0]-1)*9+move[1]-1].bin + '1' +
            gamestate[X_LOC+(move[0]-1)*9+move[1]:X_LOC+81].bin +
        gamestate[O_LOC:O_LOC+81].bin +
        '0'*(move[1]-1)+'1'+'0'*(9-move[1]) +
        '1')
        new_bin=(new_bin+
        gamestate[X_VIC:X_VIC+move[0]-1].bin +
            str(int(subgrid_winner(Bits(bin=new_bin), move[0], 'X'))) +
            gamestate[X_VIC+move[0]:X_VIC+9].bin +
        gamestate[O_VIC:O_VIC+9].bin)
        new_bin=(new_bin+
        str(int(total_winner(Bits(bin=new_bin), 'X'))) +
        str(int(gamestate[O_W])))
    return Bits(bin=new_bin)

def gamestate_to_string(gamestate):
    ORDER_FOR_TO_STRING = [0, 1, 2, 9, 10, 11, 18, 19, 20, 3, 4, 5, 12, 13, 14,
    21, 22, 23, 6, 7, 8, 15, 16, 17, 24, 25, 26, 27, 28, 29, 36, 37, 38, 45, 46,
    47, 30, 31, 32, 39, 40, 41, 48, 49, 50, 33, 34, 35, 42, 43, 44, 51, 52, 53,
    54, 55, 56, 63, 64, 65, 72, 73, 74, 57, 58, 59, 66, 67, 68, 75, 76, 77, 60,
    61, 62, 69, 70, 71, 78, 79, 80]
    chars = [' ']*81
    for i, x in enumerate(gamestate[X_LOC:X_LOC+81]):
        if x:
            chars[i]='X'
        elif gamestate[O_LOC+i]:
            chars[i]='O'
    string = ""
    for i in range(9):
        for j in range(9):
            string += chars[ORDER_FOR_TO_STRING[i*9+j]]
            if (j+1)%3:
                string += '|'
            elif j==8 and (i+1)%3:
                string += "\n" + ("-+-+-\u25AE"*2) + "-+-+-\n"
            elif j==8 and i!=8:
                string += "\n" + ("\u25AC"*17) + "\n"
            elif j!=8:
                string += "\u25AE"
            else:
                string += "\n"
    if gamestate[X_W]:
        string += "X has won the game."
    elif gamestate[O_W]:
        string += "O has won the game."
    else:
        string+="It is "+gamestate[TURN]*"O"+(not gamestate[TURN])*"X"+"'s turn.\n"
        if gamestate.all(False):
            string += "The first move can be in any square."
        else:
            for i, x in enumerate(gamestate[PREV_MOV:PREV_MOV+9]):
                if x:
                    if (gamestate[X_VIC+i] or gamestate[O_VIC+i] or
                        gamestate[X_LOC+i*9:X_LOC+i*9+9].__or__(gamestate[O_LOC+i*9:O_LOC+i*9+9]).all(True)):
                        string += "The next move can be in any un-won grid with an empty square."
                    else:
                        string += "The next move must be in grid number "+str(i+1)+"."
    return string

def subgrid_winner(gamestate, num, letter):
    subgrid=gamestate[X_LOC+(letter=="O")*81+(num-1)*9:X_LOC+(letter=="O")*81+num*9]
    for win in VICTORIES:
        if subgrid&win == win:
            return True
    return False

def total_winner(gamestate, letter):
    grid=gamestate[X_VIC+(letter=="O")*9:X_VIC+(letter=="O")*9+9]
    for win in VICTORIES:
        if grid&win == win:
            return True
    return False

def similar(gamestate1, gamestate2):
    symmetry_functions=(
        flip_horizontal_axis,
        flip_vertical_axis,
        flip_backslash_axis,
        flip_slash_axis,
        identity,
        rotate_90_degrees,
        rotate_180_degrees,
        rotate_270_degrees
    )
    for f in symmetry_functions:
        if f(gamestate1)==gamestate2:
            return True
    return False

def flip_horizontal_axis(gamestate):
    new_string=''
    for i in [X_LOC,O_LOC]:
        for sub in range(9):
            new_sub_num=sub+(sub<3)*6-(sub>5)*6
            new_sub=gamestate[i+9*new_sub_num:i+9*new_sub_num+9].bin
            for j in range(6,-1,-3):
                new_string+=new_sub[j:j+3]
    for i in range(6,-1,3):
        new_string+=gamestate[PREV_MOV+i:PREV_MOV+i+3].bin
    new_string+=str(int(gamestate[TURN]))
    for i in range(6,-1,3):
        new_string+=gamestate[X_VIC+i:X_VIC+i+3].bin
    for i in range(6,-1,3):
        new_string+=gamestate[O_VIC+i:O_VIC+i+3].bin
    new_string+=str(int(gamestate[X_W]))
    new_string+=str(int(gamestate[O_W]))
    return Bits(bin=new_string)

def flip_vertical_axis(gamestate):
    new_string=''
    for i in [X_LOC,O_LOC]:
        for sub in range(9):
            new_sub=gamestate[i+9*(sub-2*(sub%3)+2):i+9*(sub-2*(sub%3)+3)].bin
            for j in range(9):
                new_string+=new_sub[j+2-2*(j%3)]
    for i in range(9):
        new_string+=str(int(gamestate[PREV_MOV+(i+2-2*(i%3))]))
    new_string+=str(int(gamestate[TURN]))
    for i in range(9):
        new_string+=str(int(gamestate[X_VIC+(i+2-2*(i%3))]))
    for i in range(9):
        new_string+=str(int(gamestate[O_VIC+(i+2-2*(i%3))]))
    new_string+=str(int(gamestate[X_W]))
    new_string+=str(int(gamestate[O_W]))
    return Bits(bin=new_string)

def flip_backslash_axis(gamestate):
    new_string=''
    for x in [X_LOC,O_LOC]:
        for i in range(0,7,3):
            for j in range(3):
                new_sub=gamestate[x+9*(i+j):x+9*(i+j+1)].bin
                for k in range(0,7,3):
                    for l in range(3):
                        new_string+=new_sub[k+l]
    for i in range(0,7,3):
        for j in range(3):
            new_string+=str(int(gamestate[PREV_MOV+i+j]))
    new_string+=str(int(gamestate[TURN]))
    for i in range(0,7,3):
        for j in range(3):
            new_string+=str(int(gamestate[X_VIC+i+j]))
    for i in range(0,7,3):
        for j in range(3):
            new_string+=str(int(gamestate[O_VIC+i+j]))
    new_string+=str(int(gamestate[X_W]))
    new_string+=str(int(gamestate[O_W]))
    return Bits(bin=new_string)

def flip_slash_axis(gamestate):
    new_string=''
    for x in [X_LOC,O_LOC]:
        for i in range(8,5,-1):
            for j in range(0,-7,-3):
                new_sub=gamestate[x+9*(i+j):x+9*(i+j+1)].bin
                for k in range(8,5,-1):
                    for l in range(0,-7,-3):
                        new_string+=new_sub[k+l]
    for i in range(8,5,-1):
        for j in range(0,-7,-3):
            new_string+=str(int(gamestate[PREV_MOV+i+j]))
    new_string+=str(int(gamestate[TURN]))
    for i in range(8,5,-1):
        for j in range(0,-7,-3):
            new_string+=str(int(gamestate[X_VIC+i+j]))
    for i in range(8,5,-1):
        for j in range(0,-7,-3):
            new_string+=str(int(gamestate[O_VIC+i+j]))
    new_string+=str(int(gamestate[X_W]))
    new_string+=str(int(gamestate[O_W]))
    return Bits(bin=new_string)

def identity(gamestate):
    return Bits(bin=gamestate.bin)

def rotate_90_degrees(gamestate):
    new_string=''
    for x in [X_LOC,O_LOC]:
        for i in range(6,9):
            for j in range(0,-7,-3):
                new_sub=gamestate[x+9*(i+j):x+9*(i+j+1)].bin
                for k in range(6,9):
                    for l in range(0,-7,-3):
                        new_string+=new_sub[k+l]
    for i in range(6,9):
        for j in range(0,-7,-3):
            new_string+=str(int(gamestate[PREV_MOV+i+j]))
    new_string+=str(int(gamestate[TURN]))
    for i in range(6,9):
        for j in range(0,-7,-3):
            new_string+=str(int(gamestate[X_VIC+i+j]))
    for i in range(6,9):
        for j in range(0,-7,-3):
            new_string+=str(int(gamestate[O_VIC+i+j]))
    new_string+=str(int(gamestate[X_W]))
    new_string+=str(int(gamestate[O_W]))
    return Bits(bin=new_string)

def rotate_180_degrees(gamestate):
    new_string=''
    for x in [X_LOC,O_LOC]:
        for i in range(8,-1,-1):
            new_sub=gamestate[x+9*i:x+9*(i+1)].bin
            for j in range(8,-1,-1):
                new_string+=new_sub[j]
    for i in range(8,-1,-1):
        new_string+=str(int(gamestate[PREV_MOV+i]))
    new_string+=str(int(gamestate[TURN]))
    for i in range(8,-1,-1):
        new_string+=str(int(gamestate[X_VIC+i]))
    for i in range(8,-1,-1):
        new_string+=str(int(gamestate[O_VIC+i]))
    new_string+=str(int(gamestate[X_W]))
    new_string+=str(int(gamestate[O_W]))
    return Bits(bin=new_string)

def rotate_270_degrees(gamestate):
    new_string=''
    for x in [X_LOC,O_LOC]:
        for i in range(2,-1,-1):
            for j in range(0,7,3):
                new_sub=gamestate[x+9*(i+j):x+9*(i+j+1)].bin
                for k in range(2,-1,-1):
                    for l in range(0,7,3):
                        new_string+=new_sub[k+l]
    for i in range(2,-1,-1):
        for j in range(0,7,3):
            new_string+=str(int(gamestate[PREV_MOV+i+j]))
    new_string+=str(int(gamestate[TURN]))
    for i in range(2,-1,-1):
        for j in range(0,7,3):
            new_string+=str(int(gamestate[X_VIC+i+j]))
    for i in range(2,-1,-1):
        for j in range(0,7,3):
            new_string+=str(int(gamestate[O_VIC+i+j]))
    new_string+=str(int(gamestate[X_W]))
    new_string+=str(int(gamestate[O_W]))
    return Bits(bin=new_string)

if __name__=="__main__":
    game = Bits(192)
    game = make_move(game, (5,5))
    print(gamestate_to_string(game))
    game = make_move(game, (5,1))
    print(gamestate_to_string(game))
    game = make_move(game, (1,3))
    print(gamestate_to_string(game))
    game = make_move(game, (3,2))
    print(gamestate_to_string(game))
    game = make_move(game, (2,5))
    print(gamestate_to_string(game))
    game = make_move(game, (5,2))
    print(gamestate_to_string(game))
    game = make_move(game, (2,2))
    print(gamestate_to_string(game))
    game = make_move(game, (2,4))
    print(gamestate_to_string(game))
    game = make_move(game, (4,5))
    print(gamestate_to_string(game))
    game = make_move(game, (5,3))
    print(gamestate_to_string(game))
    game = make_move(game, (3,5))
    print(gamestate_to_string(game))

    game1 = Bits(192)
    game1 = make_move(game1, (1,1))
    game1 = make_move(game1, (1,5))
    game1 = make_move(game1, (5,1))
    print(gamestate_to_string(game1))
    game2 = Bits(192)
    game2 = make_move(game2, (9,9))
    game2 = make_move(game2, (9,5))
    game2 = make_move(game2, (5,9))
    print(gamestate_to_string(game2))
    print('This should be true:')
    print(similar(game1,game2))
