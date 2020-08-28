from board import *
import humanplayer

class SmallGrid(Board):
    """This is a small, or regular tic tac toe grid.

    It extends the Board class of the python board module.
    https://pypi.org/project/board/
    """

    def __init__(self):
        #the gris is always 3x3
        super().__init__((3,3))

    def to_string(self):
        """Returns a string of the tic tac toe small grid."""
        
        string = ""
        for i in range(3):
            for j in range(3):
                if self[i,j]==Empty:
                    string += " |"
                else:
                    string += self[i,j]
                    string += "|"
            string = string[0:len(string)-1]
            if i!=2:
                string += "\n-+-+-\n"
        return string

    def is_won(self):
        """returns a boolean indicating whether anyone has won this grid."""
        
        return not not(self.winner())
        
    def winner(self):
        """returns the winner of this grid, or 0 if it has not been won."""
        
        if self[0,0]!=Empty:
            if (self[0,1]!=Empty) and (self[0,2]!=Empty):
                if (self[0,0]==self[0,1]) and (self[0,0]==self[0,2]):
                    return self[0,0]
            if (self[1,0]!=Empty) and (self[2,0]!=Empty):
                if (self[0,0]==self[1,0]) and (self[0,0]==self[2,0]):
                    return self[0,0]
            if (self[1,1]!=Empty) and (self[2,2]!=Empty):
                if (self[0,0]==self[1,1]) and (self[0,0]==self[2,2]):
                    return self[0,0]
        if self[1,1]!=Empty:
            if (self[1,0]!=Empty) and (self[1,2]!=Empty):
                if (self[1,0]==self[1,1]) and (self[1,0]==self[1,2]):
                    return self[1,1]
            if (self[0,1]!=Empty) and (self[2,1]!=Empty):
                if (self[0,1]==self[1,1]) and (self[0,1]==self[2,1]):
                    return self[1,1]
            if (self[0,2]!=Empty) and (self[2,0]!=Empty):
                if (self[1,1]==self[0,2]) and (self[1,1]==self[2,0]):
                    return self[1,1]
        if self[2,2]!=Empty:
            if (self[2,0]!=Empty) and (self[2,1]!=Empty):
                if (self[2,0]==self[2,1]) and (self[2,0]==self[2,2]):
                    return self[2,2]
            if (self[0,2]!=Empty) and (self[1,2]!=Empty):
                if (self[0,2]==self[2,2]) and (self[1,2]==self[2,2]):
                    return self[2,2]
        return 0

class LargeGrid(Board):
    """This is a large, or ultimate tic tac toe grid.

    It extends the Board class of the python board module.
    https://pypi.org/project/board/
    """

    def __init__(self):
        super().__init__((3,3))
        #always a 3x3 grid of SmallGrids
        for i in range(3):
            for j in range(3):
                self[i, j] = SmallGrid()

    def to_string(self):
        """Returns a string of the ultimate tic tac toe grid."""
        
        string = ""
        for i in range(9):
            for j in range(9):
                if self[int(i/3), int(j/3)][i%3, j%3]==Empty:
                    string += " "
                else:
                    string += self[int(i/3), int(j/3)][i%3, j%3]
                if (j+1)%3:
                    string += "|"
                else:
                    if (j+1)%9:
                        string += "\u25AE"
            if (i+1)%9 and not (i+1)%3:
                string += "\n" + ("\u25AC"*17)
            elif i!=8:
                string += "\n" + ("-+-+-\u25AE"*2) + "-+-+-"
            if (i+1)%9:
                string += "\n"
        return string

    def is_won(self):
        """returns a boolean indicating whether anyone has won the game."""
        
        return not not(self.winner())

    def winner(self):
        """returns the winner of the game, or 0 if nobody has won"""
        
        if self[0,0].is_won():
            if (self[0,1].is_won()) and (self[0,2].is_won()):
                if (self[0,0].winner()==self[0,1].winner()) and (self[0,0].winner()==self[0,2].winner()):
                    return self[0,0].winner()
            if (self[1,0].is_won()) and (self[2,0].is_won()):
                if (self[0,0].winner()==self[1,0].winner()) and (self[0,0].winner()==self[2,0].winner()):
                    return self[0,0].winner()
            if (self[1,1].is_won()) and (self[2,2].is_won()):
                if (self[0,0].winner()==self[1,1].winner()) and (self[0,0].winner()==self[2,2].winner()):
                    return self[0,0].winner()
        if self[1,1].is_won():
            if (self[1,0].is_won()) and (self[1,2].is_won()):
                if (self[1,0].winner()==self[1,1].winner()) and (self[1,0].winner()==self[1,2].winner()):
                    return self[1,1].winner()
            if (self[0,1].is_won()) and (self[2,1].is_won()):
                if (self[0,1].winner()==self[1,1].winner()) and (self[0,1].winner()==self[2,1].winner()):
                    return self[1,1].winner()
            if (self[0,2].is_won()) and (self[2,0].is_won()):
                if (self[1,1].winner()==self[0,2],winner()) and (self[1,1].winner()==self[2,0].winner()):
                    return self[1,1].winner()
        if self[2,2].is_won():
            if (self[2,0].is_won()) and (self[2,1].is_won()):
                if (self[2,0].winner()==self[2,1].winner()) and (self[2,0].winner()==self[2,2].winner()):
                    return self[2,2].winner()
            if (self[0,2].is_won()) and (self[1,2].is_won()):
                if (self[0,2].winner()==self[2,2].winner()) and (self[1,2].winner()==self[2,2].winner()):
                    return self[2,2].winner()
        return 0

class UltimateTicTacToe:
    """Class for Ultimate Tic Tac Toe games.

    Each player passed as an argument to the constructor must have a #move()
    method. It should accept a LargeGrid and a list of the form [x,y,x,y]
    containing the last move as input. It should output a new move in the form
    (x,y,x,y) such that the first x and y are the zero-indexed row and column
    of the grid to play in and the second are the zero-indexed row and column
    of the spot to move in.
    """

    def __init__(self, player0, player1):
        self.grid = LargeGrid() #main grid
        self.player0 = player0 #player 1
        self.player1 = player1 #player 2
        self.lastmove = None

    def make_move(self,player_num):
        """This method asks a particular player for a move.

        This method calls the #move() method from a player to find out
        where player number player_num would like to move."""
        
        if player_num:
            while True:
                a,b,c,d = self.player1.move(self.grid,self.lastmove)
                if self.move(a,b,c,d,'O'):
                    self.lastmove = [a,b,c,d]
                    break
        else:
            while True:
                a,b,c,d = self.player0.move(self.grid,self.lastmove)
                if self.move(a,b,c,d,'X'):
                    self.lastmove = [a,b,c,d]
                    break

    def move(self,a,b,c,d,m):
        """This method puts character m in position (a,b)(c,d)."""
        
        if self.check_legal_move(a,b,c,d):
            self.grid[a,b][c,d] = m
            return True
        else:
            print("You can't move here! Try again")
            return False

    def check_legal_move(self,a,b,c,d):
        """This method indicates whether a desired move is legal.

        UltimateTicTacToe#move() only works if this returns True."""
        
        if self.grid[a,b][c,d]!=Empty:
            return False
        if (self.lastmove!=None and not self.grid[self.lastmove[2],self.lastmove[3]].is_won()) and not (a==self.lastmove[2] and b==self.lastmove[3]):
            return False
        return True

    def check_small_win(self,a,b):
        """Check grid number (a,b) to see if someone has won it. Returns boolean."""
        
        if self.grid[a,b].is_won():
            self.grid[a,b].populate(self.grid[a,b].winner()*9)
            return self.grid[a,b].winner()
        return False

    def check_large_win(self):
        """Check to see if someone has won the game. Returns boolean."""
        
        if self.grid.is_won():
            return self.grid.winner()
        return False

    def start(self):
        """Starts the main loop of the game.

        Threads should call this function. Returns the final grid and the winner."""
        
        turn = 0
        while not self.grid.is_won():
            self.make_move(turn) #move
            self.check_small_win(self.lastmove[0], self.lastmove[1]) #check winner
            turn = (turn+1)%2 #increment move
        print("Congratulations! " + self.grid.winner() + " has won!")
        return (self.grid, self.grid.winner())

if __name__=="__main__":
    player1 = humanplayer.Player(input("Player 1 name:   "))
    player2 = humanplayer.Player(input("Player 2 name:   "))
    game = UltimateTicTacToe(player1, player2)
    print(game.grid.to_string())
    game.start()
