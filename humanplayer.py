class Player:
    """A player for the UltimateTicTacToe game.

    This is a command line UI for humans to play UltimateTicTacToe."""

    def __init__(self, name="Human"):
        self.name = name

    def move(self,grid,lastmove):
        """Method to be called by UltimateTicTacToe"""
        
        print("\nIt's " + self.name + "'s turn!")
        print("The board looks like this:")
        print(grid.to_string())
        if lastmove==None or grid[lastmove[2],lastmove[3]].is_won():
            print("You may go anywhere.")
        else:
            print("You must go in grid number (" + str(lastmove[2]+1) + ", " +
                  str(lastmove[3]+1) + ").")
        print("What move would you like to make?")
        print("(format moves like: (x,y)(x,y). The origin is" +
              "the top left, so (1,1)(1,1) is the top left corner.")
        move = input("Your move:    ")
        move = move[1:len(move)-1].split(")(")
        a=move[0].split(",")
        b=move[1].split(",")
        a = a+b
        for i in range(len(a)):
            a[i] = int(a[i])-1
        return tuple(a)
