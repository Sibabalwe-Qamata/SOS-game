#CSC1011H Tutorial 8
#Student_1 = Khomotjo_Modipa(MDPRAS001)
#Student_2 = Sibabalwe_Qamata(QMTSIB001)

import random
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPalette, QBrush, QPixmap
#from SOSTextClient import SOSTextClient
from Thread import *
from GameClient import *
import os

skipDisplay = True  #handles the display of the moves played
message = ""


#Run the server before the GUI pops up
os.startfile('"SOSGameServer.bat"')


class MainWindow(QtGui.QMainWindow):
    
    def __init__( self):
        
        QtGui.QMainWindow.__init__ (self)            
        self.setWindowTitle("TenElevenGamezSOS")
        self.setWindowIcon (QtGui.QIcon ("sos.png"))
        
        self.SOS_board = GameWidget (self)
        self.setCentralWidget (self.SOS_board)

        instructions = QtGui.QAction ("Instructions", self)
        instructions.setShortcut ("Ctrl + I")
        instructions.setStatusTip ("How to play the game")
        
        version = QtGui.QAction ("version", self)
        version.setStatusTip ("Version 0.1")
        
        about = QtGui.QAction ("about", self)
        about.setStatusTip ("About Ten Eleven Gamez,programmers,OS version,Copyright and etc")
        
        #method for the user to turn on the sound
        sound_on = QtGui.QAction ("sound on", self)
        sound_on.setShortcut ("Ctrl + Y")
        sound_on.setStatusTip ("sound on")
        
        #method for the user to turn off the sound
        sound_off = QtGui.QAction ("sound off", self)
        sound_off.setShortcut ("Ctrl + K")
        sound_off.setStatusTip ("sound off")
        
        #method for the user to change a background colour
        color = QtGui.QAction ("Change backgroud color", self)
        color.setStatusTip ("choose background color")
        
        self.statusBar()

        menubar = self.menuBar()
    
        #menu for help
        help_menu = menubar.addMenu ("&Help")
        help_menu.addAction (instructions)
        help_menu.addAction (version)
        help_menu.addAction (about)
        
        
        self.connect(instructions, QtCore.SIGNAL("triggered()"), self.showAboutBox)
        self.connect(version, QtCore.SIGNAL("triggered()"), self.gameVersion)
        self.connect(about,QtCore.SIGNAL("triggered()"), self.aboutGame)
        
        
    def showAboutBox(self):
        QtGui.QMessageBox.information(self, self.tr("Instructions"),
                                self.tr("1. You are presented with a 4x4 grid, below. \n"+
                       "2. Each block has a position number, from 0 to 15. \n"+
                       "3. To play in a block, simply enter the corresponding position number\n"+"    and a character in the Play-Choice section. \n"+
                       "4. The person who plays first is randomly assigned."))
        
    def gameVersion(self):
        QtGui.QMessageBox.information(self, self.tr("version"),
                                self.tr("The version of this (SOS GAME) is version 0.0.1\n"
                                        "created by Ten Eleven GameZ."))
        
    def aboutGame(self):
        QtGui.QMessageBox.information(self, self.tr("about"),
                                self.tr("Company name: Ten Eleven Gamez CC\n"
                                        "Product     : SOSGame\n"
                                        "Version     : 0.0.1\n"
                                        "Release Date: 17 May 2015\n"
                                        "Supported OS: Windows vista,windows 7 and windows 8\n"
                                        "Memory      : 15kilobytes\n"
                                        "Copyright   : 2014 - 2015"))
        
class GameWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle('TenElevenGamezSOS')      #window Title
        self.setWindowIcon (QtGui.QIcon ("sos.png"))  #window icon
        
        #set Bold font for Group Box Titles
        font = QtGui.QFont('Arial',13,QtGui.QFont.Bold)        
            
        
        #set_picture
        self.pixmap1 = QtGui.QPixmap('images/transparent_text_effect.png')
        self.pic_label = QtGui.QLabel()
        self.pic_label.setPixmap(self.pixmap1) 
        
        self.decor = QtGui.QPixmap('images/simple_sos.png')
        self.decor_label = QtGui.QLabel()
        self.decor_label.setPixmap(self.decor)
        
        self.decor = QtGui.QPixmap('images/simple_sos.png')
        self.decor_label2 = QtGui.QLabel()
        self.decor_label2.setPixmap(self.decor)        

        #Edit_Boxes
        self.position_edit = QtGui.QLineEdit(self)
        self.position_edit.setPlaceholderText("Enter Position Number(0-15)")
        self.server_edit = QtGui.QLineEdit(self)  #edit box for the IP address of the server
        self.server_edit.setPlaceholderText("Enter Clients IP")
        
        #comboBox
        self.character_combox = QtGui.QComboBox()
        self.list_colour = ['S','O']
        self.character_combox.addItems(self.list_colour)
        
        #Variables for Shape of the player and scores
        self.current_player = None
        self.shape_player1 = None
        self.shape_player2 = None        
        
        self.score_player1 = 0
        self.score_player2 = 0        
        
        #labels
        self.heading = QtGui.QLabel("SOS Game") # Window title
        self.server_label = QtGui.QLabel("Server:")
        self.server_label.setFont(font)
        self.heading.setFont(QtGui.QFont('Forte',30))
        
        self.score = QtGui.QLabel("Score:")
        self.game_board = QtGui.QLabel("Game Board")
        self.message = QtGui.QLabel("Message")
        
        self.position = QtGui.QLabel("Position  :")
        self.character = QtGui.QLabel("Character:")
        self.blank = QtGui.QLabel(" "*130)
        self.blank2 = QtGui.QLabel(" "*100)
        self.s = QtGui.QLabel("S:")
        self.o = QtGui.QLabel("O:")
        
        self.display_Message = QtGui.QTextBrowser()
        self.display_Message.setText("SOS GAME")
        self.display_Message.setMinimumSize(100,200) 
        self.display_Message.setMaximumSize(500,500)
        
        self.display_Board = QtGui.QTextBrowser()
        self.display_Board.setPlainText("")   #Display_Grid/Board
        
        self.display_Scores1 = QtGui.QTextBrowser()   #score board for player 1
        self.display_Scores1.setText("Player 0 \n"
                                     "Score: 0")
        self.turn = 'disconnected' # Checks the turn
        
        self.display_Scores2 = QtGui.QTextBrowser()   #score board for player 2
        self.display_Scores2.setMinimumSize(100,200) 
        self.display_Scores2.setMaximumSize(500,20) 
        self.display_Scores2.setText("Player 1 \n"
                                     "Score: 0")
        
        #Buttons
        self.connect_button = QtGui.QPushButton('Connect')
        self.connect_button.setFont(font)
        self.new_game_button = QtGui.QPushButton('New Game')
        self.exit = QtGui.QPushButton('Exit')
        self.submit_button = QtGui.QPushButton('Send Move')
        
        #checkBox
        self.character1 = QtGui.QCheckBox()
        self.character2 = QtGui.QCheckBox() 
        
        #Board_Pictures
        
        self.zero = QtGui.QPixmap('images/zero_109x109.png')
        self.pic_zero = QtGui.QLabel()
        self.pic_zero.setPixmap(self.zero) 
        
        self.one = QtGui.QPixmap('images/one_109x109.png')
        self.pic_one = QtGui.QLabel()
        self.pic_one.setPixmap(self.one)
        
        self.two = QtGui.QPixmap('images/two_109x109.png')
        self.pic_two = QtGui.QLabel()
        self.pic_two.setPixmap(self.two)
        
        self.three = QtGui.QPixmap('images/three_109x109.png')
        self.pic_three = QtGui.QLabel()
        self.pic_three.setPixmap(self.three)
        
        self.four = QtGui.QPixmap('images/four_109x109.png')
        self.pic_four = QtGui.QLabel()
        self.pic_four.setPixmap(self.four)
        
        self.five = QtGui.QPixmap('images/five_109x109.png')
        self.pic_five = QtGui.QLabel()
        self.pic_five.setPixmap(self.five)
        
        self.six = QtGui.QPixmap('images/six_109x109.png')
        self.pic_six = QtGui.QLabel()
        self.pic_six.setPixmap(self.six)
        
        self.seven = QtGui.QPixmap('images/seven_109x109.png')
        self.pic_seven = QtGui.QLabel()
        self.pic_seven.setPixmap(self.seven)
        
        self.eight = QtGui.QPixmap('images/eight_109x109.png')
        self.pic_eight = QtGui.QLabel()
        self.pic_eight.setPixmap(self.eight)
        
        self.nine = QtGui.QPixmap('images/nine_109x109.png')
        self.pic_nine = QtGui.QLabel()
        self.pic_nine.setPixmap(self.nine)
        
        self.ten = QtGui.QPixmap('images/ten_109x109.png')
        self.pic_ten = QtGui.QLabel()
        self.pic_ten.setPixmap(self.ten)
        
        self.eleven = QtGui.QPixmap('images/eleven_109x109.png')
        self.pic_eleven = QtGui.QLabel()
        self.pic_eleven.setPixmap(self.eleven)
        
        self.twelve = QtGui.QPixmap('images/twelve_109x109.png')
        self.pic_twelve = QtGui.QLabel()
        self.pic_twelve.setPixmap(self.twelve)        
        
        self.thirteen = QtGui.QPixmap('images/thirteen_109x109.png')
        self.pic_thirteen = QtGui.QLabel()
        self.pic_thirteen.setPixmap(self.thirteen)
        
        self.fourteen = QtGui.QPixmap('images/fourteen_109x109.png')
        self.pic_fourteen = QtGui.QLabel()
        self.pic_fourteen.setPixmap(self.fourteen)
        
        self.fifteen = QtGui.QPixmap('images/fifteen_109x109.png')
        self.pic_fifteen = QtGui.QLabel()
        self.pic_fifteen.setPixmap(self.fifteen)        
        
        #Style
    
        #display for scores
        groupBox =QtGui.QGroupBox("Scores")
        gridA = QtGui.QGridLayout()
        gridA.addWidget(self.display_Scores1,0,0,5,10)
        gridA.addWidget(self.display_Scores2,1,0,5,10)
        gridA_Widget= QtGui.QGroupBox("Scores")
        gridA_Widget.setFont(font)
        gridA_Widget.setLayout(gridA) 
        
        #display for the board
        groupBox =QtGui.QGroupBox("Board")
        gridB = QtGui.QGridLayout()
        gridB.addWidget(self.pic_zero,0,0)
        gridB.addWidget(self.pic_one,0,1)
        gridB.addWidget(self.pic_two,0,2)
        gridB.addWidget(self.pic_three,0,3)
        
        gridB.addWidget(self.pic_four,1,0)
        gridB.addWidget(self.pic_five,1,1)
        gridB.addWidget(self.pic_six,1,2)
        gridB.addWidget(self.pic_seven,1,3)
        
        gridB.addWidget(self.pic_eight,2,0)
        gridB.addWidget(self.pic_nine,2,1)
        gridB.addWidget(self.pic_ten,2,2)
        gridB.addWidget(self.pic_eleven,2,3)
        
        gridB.addWidget(self.pic_twelve,3,0)
        gridB.addWidget(self.pic_thirteen,3,1)
        gridB.addWidget(self.pic_fourteen,3,2)
        gridB.addWidget(self.pic_fifteen,3,3)
        
        gridB_Widget= QtGui.QGroupBox("Game-Board")
        gridB_Widget.setFont(font)
        gridB_Widget.setLayout(gridB) 
    
        #display for the messages
        
        groupBox =QtGui.QGroupBox("Messages")
        gridC = QtGui.QGridLayout()
        gridC.addWidget(self.display_Message,3,3,5,10)
        gridC_Widget= QtGui.QGroupBox("Messages")
        gridC_Widget.setFont(font)
        gridC_Widget.setLayout(gridC)        
        
        #Grid_Layout_Play-Choice/)
        grid1 = QtGui.QGridLayout()
        
        grid1.addWidget(self.position,0,0)
        grid1.addWidget(self.position_edit,0,1)
        grid1.addWidget(self.character,0,2)
        grid1.addWidget(self.character_combox,0,3)
        grid1.addWidget(self.submit_button,0,4)
        grid1.addWidget(self.blank2,0,5)


        grid1_widget = QtGui.QGroupBox("Play-Choice")
        grid1_widget.setFont(font)
        grid1_widget.setLayout(grid1)
        
        #grid1_widget.setPalette(QtGui.QPalette(QtGui.QColor('skyBlue')))
        #grid1_widget.setAutoFillBackground(True)        
        
        #Grid_Layout_New_Game/Exit_Button
        Grid_new = QtGui.QGridLayout()
        
        Grid_new.addWidget(self.new_game_button,0,0)
        Grid_new.addWidget(self.exit,0,1)
        Grid_new_exit = QtGui.QGroupBox("New-Game/Exit")
        Grid_new_exit.setFont(font)
        Grid_new_exit.setLayout(Grid_new)
        
        #Layaut_Section
        
        #Horizontal_layout_HEADING/Server_Section
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.decor_label)
        hbox1.addStretch(5)
        hbox1.addWidget(self.pic_label)
        hbox1.addStretch(5)
        hbox1.addWidget(self.decor_label2)
        hbox1.addStretch(5)
        hbox1_widget = QtGui.QWidget()
        hbox1_widget.setLayout(hbox1)
        
        #Horizontal_layout_HEADING_Section
        hbox = QtGui.QHBoxLayout()
        
        hbox.addWidget(self.server_label)
        hbox.addWidget(self.server_edit)
        hbox.addWidget(self.connect_button)
        hbox.addWidget(self.blank)
        #hbox.addWidget(self.disconnect_button)
       
        hbox_widget = QtGui.QWidget()
        hbox_widget.setLayout(hbox)
        
        #Horizontal layout for Displays
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(gridA_Widget)   #grid for the scores
        hbox3.addWidget(gridB_Widget)   #Grid for the scores
        hbox3.addWidget(gridC_Widget)   #Grid for the messages
        hbox3_widget = QtGui.QWidget()  #Create the widget for all of them
        hbox3_widget.setLayout(hbox3)      
        
        #Horizontal_bottom
        hbox4 = QtGui.QHBoxLayout()
        
        hbox4.addWidget(grid1_widget)
        hbox4.addWidget(Grid_new_exit)
        grid_widget = QtGui.QWidget()
        grid_widget.setLayout(hbox4)           
        
        #Combined_Layout
        vbox = QtGui.QVBoxLayout()
        
        vbox.addWidget(hbox1_widget)  #display Heading
        vbox.addWidget(hbox_widget)   #display the server things
        vbox.addWidget(hbox3_widget)
        vbox.addWidget(grid_widget)
        
        self.setLayout(vbox) 
        
        self.setPalette(QtGui.QPalette(QtGui.QColor("skyBlue")))
        self.setAutoFillBackground(True)
        
        #backgroundColor and picture
        self.picture = QtGui.QPalette(self)
        self.picture.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap('images/o7nZzK2.jpg')))   
        self.setPalette(self.picture)        
      
        #Buttons_Connections/Events_Handling
        self.connect(self.exit,QtCore.SIGNAL('clicked()'), self.Close_Button)
        self.connect(self.new_game_button,QtCore.SIGNAL('clicked()'), self.NewGame)
        self.connect(self.submit_button,QtCore.SIGNAL('clicked()'), self.SendMove)
        #self.connect(self.submit_button,QtCore.SIGNAL('clicked()'), self.Update_Board)
        
        #Buttons_Handling
        self.connect_button.clicked.connect(self.Connection)    #Connect button Signal
        #self.submit_button = cmds.button(command = partial(my_button_on_click_handler, arg1, arg2))      #Send Move to the server button
        
        
        self.loopthread = Thread()   #creating the thread
        
        #connecting signals to slots
        self.loopthread.update_signal.connect(self.handle_message) 
        
        
    def input_move(self):    #get user input
        self.chosen_character = str(self.character_combox.currentText())
        self.chosen_position = self.position_edit.displayText()
        return  self.chosen_position + ","+ self.chosen_character
    
    
    def SendMove(self):  #handles player move
        self.input_move()
        self.move = self.input_move()
        self.chosen_character = self.character_combox.currentText()
        self.chosen_position1 = int(self.position_edit.displayText())         
        
        self.loopthread.send_message(self.move)  #send user inputs to the server
        
        #if self.chosen_character == "O":
            #self.pic = 'images/long-o-sound_109x109.jpg'
            #self.pixmap = QtGui.QPixmap(self.pic)

        #elif self.chosen_character == "S":
            #self.pic = 'images/blueS_109x109.jpg'
            #self.pixmap = QtGui.QPixmap(self.pic)    
            
        #if self.chosen_position1 == 0:       
            #self.pic_zero.setPixmap(self.pixmap)
        
        #elif self.chosen_position1 == 1:
            #self.pic_one.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 2:
            #self.pic_two.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 3:
            #self.pic_three.setPixmap(self.pixmap)
    
        #elif self.chosen_position1 == 4:
            #self.pic_four.setPixmap(self.pixmap)
        
        #elif self.chosen_position1 == 5:
            #self.pic_five.setPixmap(self.pixmap)
        
        #elif self.chosen_position1 == 6:
            #self.pic_six.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 7:
            #self.pic_seven.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 8:
            #self.pic_eight.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 9:
            #self.pic_nine.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 10:
            #self.pic_ten.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 11:
            #self.pic_eleven.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 12:
            #self.pic_twelve.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 13:
            #self.pic_thirteen.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 14:
            #self.pic_fourteen.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 15:
            #self.pic_fifteen.setPixmap(self.pixmap)         
  
        self.position_edit.setText("")  #clear text edit box
        #self.loopthread.send_message()  #indicate to the server that position chosen
        return self.chosen_character, self.chosen_position1
        
    #def Update_Board(self):
        
        #self.input_move()
        #self.chosen_character = self.character_combox.currentText()
        #self.chosen_position1 = int(self.chosen_position)        
        
        #if self.chosen_character == "O":
            #self.pic = 'images/long-o-sound_109x109.jpg'
            #self.pixmap = QtGui.QPixmap(self.pic)

        #elif self.chosen_character == "S":
            #self.pic = 'images/blueS_109x109.jpg'
            #self.pixmap = QtGui.QPixmap(self.pic)    
            
        #if self.chosen_position1 == 0:       
            #self.pic_zero.setPixmap(self.pixmap)
        
        #elif self.chosen_position1 == 1:
            #self.pic_one.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 2:
            #self.pic_two.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 3:
            #self.pic_three.setPixmap(self.pixmap)
    
        #elif self.chosen_position1 == 4:
            #self.pic_four.setPixmap(self.pixmap)
        
        #elif self.chosen_position1 == 5:
            #self.pic_five.setPixmap(self.pixmap)
        
        #elif self.chosen_position1 == 6:
            #self.pic_six.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 7:
            #self.pic_seven.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 8:
            #self.pic_eight.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 9:
            #self.pic_nine.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 10:
            #self.pic_ten.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 11:
            #self.pic_eleven.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 12:
            #self.pic_twelve.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 13:
            #self.pic_thirteen.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 14:
            #self.pic_fourteen.setPixmap(self.pixmap)
            
        #elif self.chosen_position1 == 15:
            #self.pic_fifteen.setPixmap(self.pixmap)        
    
        
        
    def Clear_Board(self): #change each individual button's Pixmap to blank image 
        self.pic_zero.setPixmap(self.zero)
        self.pic_one.setPixmap(self.one)
        self.pic_two.setPixmap(self.two)
        self.pic_three.setPixmap(self.three)
        self.pic_four.setPixmap(self.four)
        self.pic_five.setPixmap(self.five)
        self.pic_six.setPixmap(self.six)
        self.pic_seven.setPixmap(self.seven)
        self.pic_eight.setPixmap(self.eight)
        self.pic_nine.setPixmap(self.nine)
        self.pic_ten.setPixmap(self.ten)
        self.pic_eleven.setPixmap(self.eleven)
        self.pic_twelve.setPixmap(self.twelve)
        self.pic_thirteen.setPixmap(self.thirteen)
        self.pic_fourteen.setPixmap(self.fourteen)
        self.pic_fifteen.setPixmap(self.fifteen)
      
    def NewGame(self):
        
        self.display_Message.setText("New Game Started \n"
                                     "You are Player1\n "
                                     "Play your move")
        self.Clear_Board()  #Run function to clear board
        self.window.close()  #Close the pop-up box
        self.loopthread.send_message('y') #Start a new game        
 
        
    def Connection(self):
        
        self.display_Message.setText("Server Connected \n"
                                     "New Game Started")
        
        self.loopthread.server = self.server_edit.displayText()    #Obtain the text from sever
    
        if self.loopthread.connect() == 'no':  #Check that server connection is correct
            self.display_Message.append('Error connecting to server!')
        else:
            self.display_Message.append('Please Wait for opponent to join the game... \n')
            self.turn = 'connected'
            self.loopthread.start()   #thread starts after conneting
            
        self.server_edit.setText("")
            
    def handle_message(self,msg):
        #self.board = self.Update_Board()
        #self.move = self.input_move()
        #self.chosen_character = self.character_combox.currentText()
        #self.chosen_position1 = self.chosen_position
        
          
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
       
             # "New game" handler
        if (self.msgType == "new game"):
              
            # Stores char obtained from the separated message
            self.char = self.msgList [1]
            
            # Information dialog
            self.display_Message.append("You are player "+self.char+".")
            #self.display_Scores1.setText("Player "+str(self.score1))
            #self.display_Scores2.setText("Player "+msg[1])
            
            return (self.msgType, self.char)
            

          # "Your move" handler
        if (self.msgType == "your move"):
            # Input prompt
            self.display_Message.append("Your move \n")                
            # Sends move to the "GameServer"
            
            return (self.msgType)
        
            # "Opponent's move" handler
            # If the opponent's move is invalid then it doesn't display the board again
            # Otherwise, it does 
            
        if (self.msgType == "opponents move" and skipDisplay == False):
            
              
            return (self.msgType)
            
        elif (self.msgType == "opponents move"):
              
            self.display_Message.append ("\nIt's the opponent's move, please wait...")
            skipDisplay = False
            
            return (self.msgType)
        
      
           # "Valid move" handler
        if (self.msgType == "valid move"):
          
            skipDisplay == True
            
            # Stores the character, position, score1 and score2 played from the separated message
            self.char = self.msgList [2]
            self.position1 = self.msgList [1]
            self.score1 = self.msgList[3]
            self.score2 = self.msgList[4]
        
            # Information dialog
            self.display_Message.append ("\n\"" + self.char + "\" was played in position " + self.position1)
            self.display_Scores1.setText("Player 0 \nScore: "+str(self.score1))
            self.display_Scores2.setText("Player 1 \nScore: "+str(self.score2))
            
            self.input_move()
            self.move = self.input_move()
            self.chosen_character = self.character_combox.currentText()
            self.chosen_position1 = int(self.position_edit.displayText()) 
            
            if self.chosen_character == "O":
                self.pic = 'images/long-o-sound_109x109.jpg'
                self.pixmap = QtGui.QPixmap(self.pic)
    
            elif self.chosen_character == "S":
                self.pic = 'images/blueS_109x109.jpg'
                self.pixmap = QtGui.QPixmap(self.pic)    
                
            if self.chosen_position1 == 0:       
                self.pic_zero.setPixmap(self.pixmap)
            
            elif self.chosen_position1 == 1:
                self.pic_one.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 2:
                self.pic_two.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 3:
                self.pic_three.setPixmap(self.pixmap)
        
            elif self.chosen_position1 == 4:
                self.pic_four.setPixmap(self.pixmap)
            
            elif self.chosen_position1 == 5:
                self.pic_five.setPixmap(self.pixmap)
            
            elif self.chosen_position1 == 6:
                self.pic_six.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 7:
                self.pic_seven.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 8:
                self.pic_eight.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 9:
                self.pic_nine.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 10:
                self.pic_ten.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 11:
                self.pic_eleven.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 12:
                self.pic_twelve.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 13:
                self.pic_thirteen.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 14:
                self.pic_fourteen.setPixmap(self.pixmap)
                
            elif self.chosen_position1 == 15:
                self.pic_fifteen.setPixmap(self.pixmap)         
      
            #self.position_edit.setText("")          
            
            #self.pic_eleven.setPixmap(self.pixmap)
            #self.board
           
            # Updates the board at the positioned played with the player's char
            #self.board [int (self.position)] = self.char
            
            return (self.msgType, self.char, self.position1)
         
             # Invalid move" handler
        if (self.msgType == "invalid move"):
              
          # Information dialog
            self.display_Message.append ("\nThat move is invalid. Please retry.")
                
            return (self.msgType)
            
                     # "Game over" handler
        if (self.msgType == "game over"):
              
            # Stores winning char from the separated message
            self.winShape = self.msgList [1]
            
            # Checks whether the game is a tie or not and displays the 
            # appropriate message
            if (self.winShape == "T"):
              
                  # Information dialog
                self.display_Message.append("\nGame over. The Game is a draw (Tie game).")
                self.display_Message.append("score")
                self.display_Message.append("Player 0: "+str(self.score1))
                self.display_Message.append("Player 1: "+str(self.score2))
                #self.pic_eleven.setPixmap(self.pixmap)
               
                
                return (self.msgType, self.winShape)
            else:
            
                # Information dialog
                self.display_Message.append ("\nGame over. The winner is Player \"" + self.winShape + "\"")
                self.display_Scores1.append("Player 0: "+str(self.score1))
                self.display_Scores2.append("Player 1: "+str(self.score2)) 
                #self.pic_eleven.setPixmap(self.pixmap)
            
                return (self.msgType, self.winShape)
        
      # "Play again" handler
        if (self.msgType == "play again"):
            end = QtGui.QMessageBox.question(self, 'Message',"Game over. Do you want to play again?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if end == QtGui.QMessageBox.Yes:
                self.loopthread.send_message("y")
            else:
                self.loopthread.send_message("n")                  
                
            return (self.msgType)
          
        
          
    def Close_Button(self):#the function for the close button
              
        confirm = QtGui.QMessageBox.question (self, 'Message',
                  "Are you sure you want to Exit the game?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      
        if (confirm == QtGui.QMessageBox.Yes):
            self.loopthread.send_message('n') #Indicate to server that player has left
            sys.exit ()
              
        else:
            pass          
                       
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    game_widget = MainWindow()   #create GameWidget object
    game_widget.show()
    sys.exit(app.exec_())
    
main()