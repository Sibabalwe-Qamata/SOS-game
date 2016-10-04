#TUT 10 Final System Alpha
#Khomotjo Modipa   MDPRAS001
#Sibabalwe Qamata  QMTSIB001
# 11 May 2015

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from GameClient import *

class Thread(QtCore.QThread,GameClient): #define thread
    update_signal = QtCore.pyqtSignal(str) #create  a signal
    
    def __init__(self,l=''):
        QtCore.QThread.__init__(self)
        GameClient.__init__(self)
        self.server = l
        
    def connect(self):
        try: 
            self.connect_to_server(self.server)#takes the IP address that the user entered to the server
        except: return 'no'
        
    def run(self): #run executed when start() method called
        
        try:
            while True:
                msg = self.receive_message()
                if len(msg):
                    self.update_signal.emit(str(msg)) #emit signal
                else: break
        except Exception as e:
            self.update_signal.emit(str(e))    
             
            print('ERROR:' + str(e) + '\n')
            self.log('ERROR:' + str(e) + '\n')        
        self.update_signal.emit(str(msg))        