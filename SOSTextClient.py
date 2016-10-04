#CSC1011H Tutorial 7 - Text-based Client
#Khomotjo Modipa - MDPRAS001
#Sibabalwe Qamata - QMTSIB001

from GameClient import *
from GameServer import *
skipDisplay = True  #handles the display of the moves played
message = ""

class SOSTextClient(GameClient):

    def __init__(self):
        GameClient.__init__(self)
        self.board = [' '] * BOARD_SIZE
        self.char= None  #variable to handle the characters
        
    def clear_board(self):
        self.board = [' '] * BOARD_SIZE
        
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter position(0-15):') + ',' +input('enter char(S,O):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):
        
        print ("+---------------+")
        print ("| " + self.board [0] + " | " + self.board [1] + " | " + self.board [2]+" | "+self.board[3]+" |")
        print ("|---+---+---+---|")
        print ("| " + self.board [4] + " | " + self.board [5] + " | " + self.board [6]+" | "+self.board[7]+" |")
        print ("|---+---+---+---|")
        print ("| " + self.board [8] + " | " + self.board [9] + " | " + self.board [10]+" | "+self.board[11]+" |")
        print ("|---+---+---+---|")
        print ("| " + self.board [12] + " | " + self.board [13] + " | " + self.board [14]+" | "+self.board[15]+" |") 
        print ("+---------------+")
        
    def handle_message(self,msg):
        
        global message
             # Calls the skipDisplay variable
        global skipDisplay
             
             # Splits the recieved message into separate strings
        self.msgList = msg.split (",")
             
             # Stores the message description
        self.msgType = self.msgList [0]
        message = self.msgList [0]
             # "for" loop used to iterate through all message descriptions
             # "break" is used to exit the loop if the condition is true
        for i in range (0, 16):
             
                 # "New game" handler
            if (self.msgType == "new game"):
                
                # Stores char obtained from the separated message
                self.char = self.msgList [1]
                
                # Information dialog
                print ("\nA new game has started. You are Player " + self.char)
                
                # Displays the instructions
                print ("\n ***Instructions*** ")
                print("")
                print ("1. You are presented with a 4x4 grid, below. \n"+
                       "2. Each block has a position number, from 0 to 15. \n"+
                       "3. To play in a block, simply enter the corresponding position number. \n"+
                       "4. The person who plays first is randomly assigned.")
                
                return (self.msgType, self.char)
            

            # "Your move" handler
            if (self.msgType == "your move"):
                
                print ()
                
                # Allows user to see the board before making a move
                self.display_board()
                
                # Input prompt
                print ("\nIt's your move.")
                self.move = self.input_move(textedit,combobox)
                
                # Sends move to the "GameServer"
                self.send_message (self.move)
                
                return (self.msgType)
            
                # "Opponent's move" handler
                # If the opponent's move is invalid then it doesn't display the board again
                # Otherwise, it does
            if (self.msgType == "opponents move" and skipDisplay == False):
                
                return (self.msgType)
            
            elif (self.msgType == "opponents move"):
                
                print()
                
                # Allows user to see the board while waiting for the opponent to
                # move
                self.display_board ()
            
                print ("\nIt's the opponent's move, please wait...")
                
                skipDisplay = False
                
                return (self.msgType)
            
                 # "Valid move" handler
            if (self.msgType == "valid move"):
                
                skipDisplay == True
                
                # Stores the character, position, score1 and score2 played from the separated message
                self.char = self.msgList [2]
                self.position = self.msgList [1]
                self.score1 = self.msgList[3]
                self.score2 = self.msgList[4]
            
                # Information dialog
                print ("\n\"" + self.char + "\" was played in position " + self.position)
                print("Player 0:",self.score1)
                print("Player 1:",self.score2)
                
                # Updates the board at the positioned played with the player's char
                self.board [int (self.position)] = self.char
                
                return (self.msgType, self.char, self.position)
             
                 # Invalid move" handler
            if (self.msgType == "invalid move"):
                
                # Information dialog
                print ("\nThat move is invalid. Please retry.")
                
                return (self.msgType)
            
                 # "Game over" handler
            if (self.msgType == "game over"):
                
                # Stores winning char from the separated message
                self.winShape = self.msgList [1]
                
                # Checks whether the game is a tie or not and displays the 
                # appropriate message
                if (self.winShape == "T"):
                    
                    # Displays the board for user to check final result
                    self.display_board()
                    
                    # Information dialog
                    print ("\nGame over. The Game is a draw (Tie game).")
                    print("score")
                    print("Player 0:",self.score1)
                    print("Player 1:",self.score2)                
                    
                    
                    return (self.msgType, self.winShape)
                else:
                    
                    # Displays the board for user to check final result
                    self.display_board ()
                    
                    # Information dialog
                    print ("\nGame over. The winner is Player \"" + self.winShape + "\"")
                    print("Player 0:",self.score1)
                    print("Player 1:",self.score2)                
                
                    return (self.msgType, self.winShape)
        
        # "Play again" handler
            if (self.msgType == "play again"):
            
                print ()
                
                # "while" loop ensures that user enters either "y" or "n"
                while True:
                    
                    # Input prompt
                    self.play = self.input_play_again ()
                
                    # Checks if input is valid
                    if not (self.play.upper() == "Y" or self.play.upper() == "N"):
                    
                        # Information dialog
                        print ("\nInvalid coice. Please try again.")
                    
                    else:
                        
                        #Clears the board for the new game
                        if (self.play == "y"):
                            self.clear_board ()
                        
                        else:
                            pass
                        
                        # Sends choice to "GameServer"
                        self.send_message (self.play.lower ())
                        
                        # Exits loop
                        break
                
                return (self.msgType)
            
            if (self.msgType == "play again"):
                
                # Information dialog
                self.play_again = self.input_play_again()
            
                # Sends move to the "GameServer"
                self.send_message (self.play_again)                
                 
                return (self.msgType)
    
        
       
    def play_loop(self):
        try:
            while True:
                msg = self.receive_message()
                if len(msg): self.handle_message(msg)
                else: break
        except Exception as e:
            print('ERROR:' + str(e) + '\n')
            self.log('ERROR:' + str(e) + '\n')
            
def main():
    stc = SOSTextClient()
    while True:
        try:
            stc.connect_to_server(stc.input_server())
            break
        except Exception as e:
            print('Error connecting to server!\nERROR:' + str(e) + '\n')
            self.log('Error connecting to server!\nERROR:' + str(e) + '\n')
            
    stc.play_loop()
    input('Press enter to exit.')
        
main()