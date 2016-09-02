#Name: Tuan Anh Huynh
#CS 121 Assignment 10 AI Connect-4
#Dr. Lang

from Tkinter import *
import random

diameter = 50
spacing = 10
gutter = 50

class Board:
 
  def __init__( self, width, height ): 
    self.width = width 
    self.height = height 
    self.data = [] # this will be the board 
    
    for row in range( height ): 
      boardRow = [] 
      for col in range( width ): 
        boardRow += [' '] 
      self.data += [boardRow] 
    return

  def __repr__(self): 
    #print out rows & cols 
    s = '' # the string to return 
    for row in range( self.height ): 
      s += '|' # add the spacer character 
      for col in range( self.width ): 
        s += self.data[row][col] + '|' 
      s += '\n' 
    #print out separator 
    s += '--'*self.width + '-\n' 
    # print out indices of each column 
    # using mod if greater than 9, 
    # for spacing issues 
    for col in range( self.width):
        s += ' ' + str( col % 9)
    s += '\n'
    
    return s # return it 

  def allowsMove(self,col):
    move = True
    if col < 0 or col >= self.width:
      move = False        
    if move:    
      if self.data[0][col] != ' ':
        move = False
    return move
      
  def addMove(self, col, ox):
    if self.allowsMove(col):
      for row in range (self.height):
        if self.data[row][col] != ' ':
          self.data[row-1][col] = ox
          return row-1
      self.data[self.height-1][col] = ox
      return self.height-1  
  
  def clear(self): # clear board
    for row in range(self.height):
      for col in range (self.width):
        self.data[row][col] = ' '
  
  def delMove(self, col): # delete a 'XO' in a colum
    undeleted = True
    for row in range(self.height):
      if self.data[row][col] != ' ' and undeleted:
        self.data[row][col] = ' '
        undeleted = False
      

  def setBoard( self, moveString) :
    
    nextCh = 'X'
    for colString in moveString:
      col = int(colString)
      if 0 <= col <= self.width:
        self.addMove(col, nextCh)
      if nextCh == 'X':
        nextCh = 'O'
      else:
        nextCh = 'X'
    return 
    
  def isFull(self): #return True if the board is full, otherwise False
    full = True
    for row in range(self.height):
      for col in range(self.width):
        if self.data[row][col] == ' ':
          full = False
    return full
  
  def winsFor( self,ox ):
    win = False
    #check vertical wins
    for row in range( 0,self.height ):
      for col in range( 0,self.width-3 ):
        if self.data[row][col] == ox and \
           self.data[row][col+1] == ox and \
           self.data[row][col+2] == ox and \
           self.data[row][col+3] == ox:
          win = True
    
    #check horizotal wins           
    for col in range( 0,self.width):
      for row in range( 0,self.height-3 ):
        if self.data[row][col] == ox and \
           self.data[row+1][col] == ox and \
           self.data[row+2][col] == ox and \
           self.data[row+3][col] == ox:
          win = True
    
    #check NW - SE wins             
    for row in range( 0,self.height-3 ):
      for col in range( 3,self.width ):
        if self.data[row][col] == ox and \
           self.data[row+1][col-1] == ox and \
           self.data[row+2][col-2] == ox and \
           self.data[row+3][col-3] == ox:
          win = True
    
    #check NE - SW wins        
    for row in range( 0,self.height-3):
      for col in range( 0,self.width-3 ):
        if self.data[row][col] == ox and \
           self.data[row+1][col+1] == ox and \
           self.data[row+2][col+2] == ox and \
           self.data[row+3][col+3] == ox:
          win = True
    return win 
  
  def Input(self, ox): # call a help function for hostGame to ask player's move
    while True:
      play = raw_input("input the number of colum:  ")
      play = int(play)
      if self.allowsMove(play):
        return play
      
  def hostGame(self):
    print self
    print "please input a valid number of colum"
    while True:
      play = self.Input('X')
      self.addMove(play, 'X')
      print self
      if self.winsFor('X'):
        print "X player wins -- Congratulations!!!"
        break
      play = self.Input('O')
      self.addMove(play, 'O')
      print self
      if self.winsFor('O'):
        print "O player has won -- Congratulations!!!"
        break
      if self.isFull():
        print "it is a tie, play again!!!"
        break
  
  def quit(self):
    self.window.destroy()
  
  def restart(self):
    for row in range (self.height):
      for col in range(self.width):
        self.data[row][col] = ' '
        self.gui(row,col,"white")
        self.ignoreEvents = False
    self.postMessage("Make Your Move")    
    print ("Make Your Move")
     
 
  def postMessage(self,Message):
    if self.message != None:
      self.draw.delete(self.message)
    self.message = self.draw.create_text(diameter/2, \
                                         self.gutter + diameter/2, \
                                         text=Message,anchor="w", font="Courier 20")
    self.window.update()                                     
  
  def gui(self,row,col,color):
    c = self.circles[row][col]
    self.draw.itemconfig(c,fill=color)
    
  def mouse(self,event):
    if self.ignoreEvents:
      self.window.bell()
      return
    print(event.x," ",event.y)
    col = (event.x - spacing/2) / (diameter + spacing)
    if self.allowsMove(col):
      row = self.addMove(col,'X')
      self.gui(row,col,"red")
      if self.winsFor('X'):
        self.postMessage("You won")
        self.ignoreEvents = True
        return
      elif self.isFull():
        self.postMessage("Tie")
        self.ignoreEvents = True
        return
      self.postMessage("Thinking....")
      col = self.player.nextMove(self)
      row = self.addMove(col,"O")
      self.gui(row,col,"black")
      if self.winsFor('O'):
        self.postMessage("You Lost")
        self.ignoreEvents = True
        return
      elif self.isFull():
        self.postMessage("Tie")
        self.ignoreEvents = True
        return
      self.postMessage("Your Move...")
      self.ignoreEvents = False
    else:
      self.window.bell()
      return
  
  def attachGUI(self,window,player):
    self.ignoreEvents = True
    self.player = player
    self.window = window
    self.frame = Frame(window)
    self.message = None
    self.frame.pack()
    self.qButton = Button(self.frame,text="Quit",fg="black", \
                          command=self.quit)
    self.qButton.pack(side=RIGHT)
    self.newButton = Button(self.frame,text="Restart",fg="black", \
                            command=self.restart)
    self.newButton.pack(side=LEFT)
    w = self.width * (diameter + spacing) + spacing
    h = self.height * (diameter + spacing) + spacing + gutter
    self.draw = Canvas(window, width = w, height = h, bg="green",borderwidth=0, \
                       highlightbackground="black",highlightthickness=2)
    self.draw.bind("<Button-1>",self.mouse)
    self.draw.pack()
    self.circles = []
    delta = diameter + spacing
    y = spacing
    for row in range(self.height):
      boardRow = []
      x = spacing #+ (diameter/2)
      for col in range(self.width):
        c = self.draw.create_oval(x, y, x+diameter, y+diameter, \
                                  fill="white")
        boardRow += [c]
        x += delta
      self.circles += [boardRow]
      y += delta
    self.gutter = y
    self.postMessage("Make your move")
    self.ignoreEvents = False
    
  #add a new mothod called PlayGameWith for aiPlayer
  def playGameWith(self,aiPlayer):
    print self 
    while True:
      play = self.Input('X')
      self.addMove(play, 'X')
      print self
      if self.winsFor( 'X' ):
        print "You have won -- Congratulations!!!"
        break
      oMove = aiPlayer.nextMove( self ) #get the move
      self.addMove(oMove, 'O')    #make the move where self is the board object      
      print self
      if self.winsFor( 'O' ):
        print "Computer has won"
        break
      if self.isFull():
        print "The game is tie"
        break     

class Player:
    def __init__(self, checker, ply):
            self.checker = checker
            self.ply = ply
            
    def nextMove(self,board):
        scores = self.scoresFor(board,self.checker,self.ply)
        best = max(scores)
        bestmoves = []
        for m in scores:
            if m[0] == best[0]:
                bestmoves += [m]
        moves = random.choice(bestmoves)
        print (moves,bestmoves)
        return moves[1]
            
    def scoresFor(self,board,ox,depth):
        scoresList = []
        for col in range(board.width):
          if board.allowsMove(col):
            board.addMove(col, ox)
            if board.winsFor(ox):
              scoresList += [[100.0,col]]
            elif depth < 1:
              scoresList += [[50.0,col]]
            else:
              if ox == 'X':
                opponent = 'O'
              else:
                opponent = 'X'
              oppList = self.scoresFor(board,opponent,depth-1)
              bestOpp = max(oppList)
              OppScore = 100.0 - bestOpp[0]
              scoresList+= [[OppScore,col]]
            board.delMove(col)
          else:
            scoresList += [[-1.0,col]]
        return scoresList      
      
def play(size,ply):
  b = Board(9,8)
  p = Player ('O',ply)
  window = Tk()
  window.title("Connect 4 GUI")
  b.attachGUI(window, p)
  window.mainloop()
  
play(1,4)
