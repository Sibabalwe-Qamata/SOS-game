# DO NOT MODIFY THIS FILE

from GameServer import *
from random import *

class SOSGameServer(GameServer):
    
    def __init__(self):
        GameServer.__init__(self)
        self.triples = [[0,1,2],[1,2,3],[4,5,6],[5,6,7],[8,9,10],[9,10,11],[12,13,14],[13,14,15], #horizontals
                        [0,4,8],[4,8,12],[1,5,9],[5,9,13],[2,6,10],[6,10,14],[3,7,11],[7,11,15], #verticals
                        [2,5,8],[3,6,9],[6,9,12],[7,10,13],[4,9,14],[0,5,10],[5,10,15],[1,6,11]] #diagonals

    def is_move_valid(self,i,c):
        return i.isdigit() and 0 <= int(i) < BOARD_SIZE and self.board[int(i)] == ' ' and len(c) == 1 and c in 'SO'
    
    def is_board_full(self):
        return ' ' not in self.board
        
    def update_score(self,pos):
        updated = False
        for triple in self.triples:
            if pos in triple:
                pattern = self.board[triple[0]]+self.board[triple[1]]+self.board[triple[2]]
                if pattern == 'SOS':
                    self.scores[self.current_player] += 1
                    updated = True
        if updated: return True
        else: return False

    def play_loop(self):
        while True:
            try:
                self.output('*** SOS GAME SERVER STARTED ***')
                self.accept_clients()
                while True:
                    self.board = [' '] * BOARD_SIZE
                    self.current_player = randint(0,1)
                    self.scores = [0,0]
                    self.winner = None
                    self.send_message(self.current_player,'new game,' + str(self.current_player))
                    self.send_message(self.current_player ^ 1,'new game,' + str(self.current_player ^ 1))
                    while not self.is_board_full():
                        self.send_message(self.current_player,'your move')
                        self.send_message(self.current_player ^ 1,'opponents move')
                        move_position,move_char = tuple(self.receive_message(self.current_player).split(','))
                        move_position = move_position.strip()
                        move_char = move_char.strip()
                        if not self.is_move_valid(move_position,move_char):
                            self.send_message(self.current_player,'invalid move')
                        else:
                            move_position = int(move_position)
                            self.board[move_position] = move_char
                            score_updated = self.update_score(move_position)
                            valid_move_str = 'valid move,' + str(move_position) + ',' + str(move_char) + ',' + str(self.scores[0]) + ',' + str(self.scores[1])
                            self.send_message(self.current_player, valid_move_str)
                            self.send_message(self.current_player ^ 1, valid_move_str)
                            if not score_updated: 
                                self.current_player = self.current_player ^ 1
                    
                    if self.scores[0] == self.scores[1]:
                        self.winner = 'T'
                    elif self.scores[0] > self.scores[1]:
                        self.winner = '0'
                    else:
                        self.winner = '1'
                    self.send_message(self.current_player,'game over,' + self.winner + ',' + str(self.scores[0]) + ',' + str(self.scores[1]))
                    self.send_message(self.current_player ^ 1,'game over,' + self.winner + ',' + str(self.scores[0]) + ',' + str(self.scores[1]))
                    
                    self.send_message(self.current_player,'play again')
                    self.send_message(self.current_player ^ 1,'play again')
                    
                    play_again_current = self.receive_message(self.current_player)[0].lower()
                    play_again_opponent = self.receive_message(self.current_player ^ 1)[0].lower()
                    if play_again_current != 'y' or play_again_opponent != 'y': 
                        self.send_message(self.current_player,'exit game')
                        self.send_message(self.current_player ^ 1,'exit game')
                        self.close_clients()
                        break
            except Exception as e:
                self.output('ERROR:' + str(e) + '\n\nGame Server is being restarted.\n')
                
def main():
    sgs = SOSGameServer()
    sgs.play_loop()

main()