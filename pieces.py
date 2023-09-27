import pygame


HEIGHT = WIDTH = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
Images = {}

class Cell():
	def __init__(self, name, piece):
		self.name = name
		self.cell_rect = self.cell_rect(self.name)
		self.color = self.find_color(self.name)
		self.row, self.col = self.Get_row_and_col(self.name)
		self.piece = piece
		self.properties = [self.row, self.col, self.name, self.cell_rect, self.color, self.piece]

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def Get_row_and_col(self, name):
		letter, number = list(name)
		return 8-int(number), ord(letter)-97

	def cell_rect(self, name):
		letter_and_number = list(name)
		letter = ord(letter_and_number[0])-97
		num = 8-int(letter_and_number[1])
		return pygame.Rect(letter*SQUARE_SIZE, num*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

	def find_color(self, name):
		letter_and_number = list(name)
		letter = ord(letter_and_number[0])-97
		num = 8-int(letter_and_number[1])
		if (letter+num)%2 == 0:
			return 'white'
		else:
			return 'black'

class Move():
	def __init__(self, Start_cell, End_cell, Board, pawnPromotion = False, enPassantSquare = None, castling = None):
		self.Start_cell = Start_cell
		self.End_cell = End_cell
		self.Start_row = self.Start_cell.row
		self.Start_col = self.Start_cell.col
		self.End_row = self.End_cell.row
		self.End_col = self.End_cell.col
		self.Board = Board
		self.Start_piece = self.Start_cell.piece
		self.End_piece = self.End_cell.piece
		self.pawnPromotion = pawnPromotion
		self.enPassantSquare = enPassantSquare
		self.castling = castling
		self.chessNotation = self.chessNotation(self.Start_cell, self.End_cell)

	def chessNotation(self, Start_cell, End_cell): #TODO: introduce FEN notation
		Start_letter, Start_num = list(Start_cell.name)
		End_letter, End_num = list(End_cell.name)
		return Start_letter + Start_num + End_letter + End_num

class Piece():
	def __init__(self, cell, Board, color, moveLog, castling = None):
		self.cell = cell
		self.Board = Board
		self.color = color
		self.moveLog = moveLog

	def letter_to_number(self, letter):
		return ord(letter)-97

	def number_to_letter(self, number):
		return chr(ord('`')+number+1)

	def find_diag_moves(self, cell, Board, color):
		legal_moves = []
		letter, num = list(cell)
		row = 8-int(num)
		col = ord(letter)-97
		row_Greater_col_right = int(num) >= int(col+1)
		row_Greater_col_left = int(num) >= 8-int(col)
		if row_Greater_col_right:
			for i in range(int(num), 8):
				if Board[8-(i+1)][col + (i+1-int(num))].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col + (i+1-int(num)))+str(i+1), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter(col + (i+1-int(num)))+str(i+1))
				elif list(Board[8-(i+1)][col + (i+1-int(num))].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col + (i+1-int(num)))+str(i+1), Board[8-(i+1)][col + (i+1-int(num))].piece), Board))
					#legal_moves.append(cell+self.number_to_letter(col + (i+1-int(num)))+str(i+1))
					break
				elif list(Board[8-(i+1)][col + (i+1-int(num))].piece)[0] == color:
					break
			for j in range(8-int(col), 8):
				if Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(7-j)+str(((8-row)-(j+1-(8-int(col))))), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter((7-j))+str(((8-row)-(j+1-(8-int(col))))))
				elif list(Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(7-j)+str(((8-row)-(j+1-(8-int(col))))), Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece), Board))
					#legal_moves.append(cell+self.number_to_letter(7-j)+str(((8-row)-(j+1-(8-int(col))))))
					break 
				elif list(Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece)[0] == color:
					break

		if not row_Greater_col_right:
			for i in range(int(col), 7):
				if Board[8-(int(num)+i+1-(int(col)))][i+1].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(i+1)+str(int(num)+i+1-(int(col))), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter(i+1)+str(int(num)+i+1-(int(col))))
				elif list(Board[8-(int(num)+i+1-(int(col)))][i+1].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(i+1)+str(int(num)+i+1-(int(col))), Board[8-(int(num)+i+1-(int(col)))][i+1].piece), Board))
					#legal_moves.append(cell+self.number_to_letter(i+1)+str(int(num)+i+1-(int(col))))
					break
				elif list(Board[8-(int(num)+i+1-(int(col)))][i+1].piece)[0] == color:
					break
			for j in range(row, 7):
				if Board[j+1][col-(j+1-row)].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter((col-(j+1-row)))+str(8-(j+1)), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter((col-(j+1-row)))+str(8-(j+1)))
				elif list(Board[j+1][col-(j+1-row)].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter((col-(j+1-row)))+str(8-(j+1)), Board[j+1][col-(j+1-row)].piece), Board))
					#legal_moves.append(cell+self.number_to_letter((col-(j+1-row)))+str(8-(j+1)))
					break
				elif list(Board[j+1][col-(j+1-row)].piece)[0] == color:
					break

		if row_Greater_col_left:
			for i in range(7-row, 7):
				if Board[7-(i+1)][col-(i+1-(7-row))].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-(i+1-(7-row)))+str(8-(7-(i+1))), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter(col-(i+1-(7-row)))+str(8-(7-(i+1))))
				elif list(Board[7-(i+1)][col-(i+1-(7-row))].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-(i+1-(7-row)))+str(8-(7-(i+1))), Board[7-(i+1)][col-(i+1-(7-row))].piece), Board))
					#legal_moves.append(cell+self.number_to_letter(col-(i+1-(7-row)))+str(8-(7-(i+1))))
					break
				elif list(Board[7-(i+1)][col-(i+1-(7-row))].piece)[0] == color:
					break

			for j in range(col, 7):
				if Board[row+(j+1-col)][j+1].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(j+1)+str(8-(row+(j+1-col))), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter(j+1)+str(8-(row+(j+1-col))))
				elif list(Board[row+(j+1-col)][j+1].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(j+1)+str(8-(row+(j+1-col))), Board[row+(j+1-col)][j+1].piece), Board))
					#legal_moves.append(cell+self.number_to_letter(j+1)+str(8-(row+(j+1-col))))
					break
				elif list(Board[row+(j+1-col)][j+1].piece)[0] == color:
					break

		if not row_Greater_col_left:
			for k in range(7-int(col), 7):
				if Board[row-(k+1-(7-int(col)))][(7-k)-1].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter((7-k)-1)+str(8-(row-(k+1-(7-int(col))))), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter((7-k)-1)+str(8-(row-(k+1-(7-int(col))))))
				elif list(Board[row-(k+1-(7-int(col)))][(7-k)-1].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter((7-k)-1)+str(8-(row-(k+1-(7-int(col))))), Board[row-(k+1-(7-int(col)))][(7-k)-1].piece), Board))
					#legal_moves.append(cell+self.number_to_letter((7-k)-1)+str(8-(row-(k+1-(7-int(col))))))
					break
				elif list(Board[row-(k+1-(7-int(col)))][(7-k)-1].piece)[0] == color:
					break

			for j in range(row, 7):
				if Board[j+1][col+(j+1-row)].piece == '--':
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+(j+1-row))+str(8-(j+1)), '--'), Board))
					#legal_moves.append(cell+self.number_to_letter(col+(j+1-row))+str(8-(j+1)))
				elif list(Board[j+1][col+(j+1-row)].piece)[0] != color:
					legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+(j+1-row))+str(8-(j+1)), Board[j+1][col+(j+1-row)].piece), Board))
					#legal_moves.append(cell+self.number_to_letter(col+(j+1-row))+str(8-(j+1)))
					break
				elif list(Board[j+1][col+(j+1-row)].piece)[0] == color:
					break
		return legal_moves

	def find_linear_moves(self, cell, Board, color):
		legal_moves = []
		letter, num = list(cell)
		row = 8-int(num)
		col = ord(letter)-97
		for i in range(int(num), 8):
			if Board[8-(i+1)][col].piece == '--':
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(i+1), '--'), Board))
				#legal_moves.append(cell+letter+str(i+1))
			elif list(Board[8-(i+1)][col].piece)[0] != color:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(i+1), Board[8-(i+1)][col].piece), Board))
				#legal_moves.append(cell+letter+str(i+1))
				break
			elif list(Board[8-(i+1)][col].piece)[0] == color:
				break
		for j in range(row+1, 8):
			if Board[j][col].piece == '--':
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(8-j), '--'), Board))
				#legal_moves.append(cell+letter+str(8-j))
			elif list(Board[j][col].piece)[0] != color:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(8-j), Board[j][col].piece), Board))
				#legal_moves.append(cell+letter+str(8-j))
				break
			elif list(Board[j][col].piece)[0] == color: 
				break
		for k in range(col, 7):
			if Board[row][k+1].piece == '--':
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(k+1)+str(8-int(row)), '--'), Board))
				#legal_moves.append(cell+self.number_to_letter(k+1)+str(8-int(row)))
			elif list(Board[row][k+1].piece)[0] != color:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(k+1)+str(8-int(row)), Board[row][k+1].piece), Board))
				#legal_moves.append(cell+self.number_to_letter(k+1)+str(8-int(row)))
				break
			elif list(Board[row][k+1].piece)[0] == color: 
				break
		for l in range(8-col, 8):
			if Board[row][8-(l+1)].piece == '--':
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(8-(l+1))+str(num), '--'), Board))
				#legal_moves.append(cell+self.number_to_letter(8-(l+1))+str(num))
			elif list(Board[row][8-(l+1)].piece)[0] != color:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(8-(l+1))+str(num), Board[row][8-(l+1)].piece), Board))
				#legal_moves.append(cell+self.number_to_letter(8-(l+1))+str(num))
				break
			elif list(Board[row][8-(l+1)].piece)[0] == color:
				break
		return legal_moves


class P(Piece):
	def __init__(self, cell, Board, color, moveLog):
		super(P,self).__init__(cell, Board, color, moveLog)
		self.cell = cell
		self.Board = Board
		self.color = color
		self.name = self.color+'P'
		self.moveLog = moveLog
		if color == 'w':
			self.move_list = self.find_legal_moves_white(self.cell, self.Board, self.moveLog)
		elif color == 'b':
			self.move_list = self.find_legal_moves_black(self.cell, self.Board, self.moveLog)

	def letter_to_number(self, letter):
		return super().letter_to_number(letter)

	def number_to_letter(self, number):
		return super().number_to_letter(number)

	def find_legal_moves_white(self, cell, Board, moveLog):
		#TODO: implement en-passant and pawn promotion
		legal_moves = []
		letter, num = list(cell)
		row = 8-int(num)
		col = ord(letter)-97
		if Board[row-1][col].piece == '--':
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(int(num)+1), '--'), Board))
			#legal_moves.append(cell+letter+str(int(num)+1))
		if moveLog:
			if moveLog[-1].enPassantSquare == self.number_to_letter(col-1)+str(int(num)+1):
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(int(num)+1), Board[row-1][col-1].piece), Board, enPassantSquare = self.number_to_letter(col-1)+str(int(num)+1)))
			elif moveLog[-1].enPassantSquare == self.number_to_letter(col+1)+str(int(num)+1):
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(int(num)+1), Board[row-1][col+1].piece), Board, enPassantSquare = self.number_to_letter(col+1)+str(int(num)+1)))

		if col != 0 and list(Board[row-1][col-1].piece)[0] == 'b':
			if row == 1:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(int(num)+1), Board[row-1][col-1].piece), Board, pawnPromotion = True))
			else:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(int(num)+1), Board[row-1][col-1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-1)+str(int(num)+1))
		
		if col != 7 and list(Board[row-1][col+1].piece)[0] == 'b':
			if row == 1:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(int(num)+1), Board[row-1][col+1].piece), Board, pawnPromotion = True))
			else:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(int(num)+1), Board[row-1][col+1].piece), Board))

			#legal_moves.append(cell+self.number_to_letter(col+1)+str(int(num)+1))
		if row == 6 and Board[row-2][col].piece == '--' and Board[row-1][col].piece == '--':
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(int(num)+2), '--'), Board, enPassantSquare = letter+str(int(num)+1)))
			#legal_moves.append(cell+letter+str(int(num)+2))
		return legal_moves

	def find_legal_moves_black(self, cell, Board, moveLog):
		#TODO: implement en-passant and pawn promotion
		legal_moves = []
		letter, num = list(cell)
		row = 8-int(num)
		col = ord(letter)-97
		if Board[row+1][col].piece == '--':
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(int(num)-1), '--'), Board))
			#legal_moves.append(cell+letter+str(int(num)-1))

		if moveLog:
			if moveLog[-1].enPassantSquare == self.number_to_letter(col-1)+str(int(num)-1):
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(int(num)-1), Board[row+1][col-1].piece), Board, enPassantSquare =  self.number_to_letter(col-1)+str(int(num)-1)))
			elif moveLog[-1].enPassantSquare == self.number_to_letter(col+1)+str(int(num)-1):
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(int(num)-1), Board[row+1][col+1].piece), Board, enPassantSquare = self.number_to_letter(col+1)+str(int(num)-1)))

		if col != 0 and list(Board[row+1][col-1].piece)[0] == 'w':
			if row == 6:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(int(num)-1), Board[row+1][col-1].piece), Board, pawnPromotion = True))
			else:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(int(num)-1), Board[row+1][col-1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-1)+str(int(num)-1))
		if col != 7 and list(Board[row+1][col+1].piece)[0] == 'w':
			if row == 6:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(int(num)-1), Board[row+1][col+1].piece), Board, pawnPromotion = True))
			else:
				legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(int(num)-1), Board[row+1][col+1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+1)+str(int(num)-1))
		if row == 1 and Board[row+2][col].piece == '--' and Board[row+1][col].piece == '--':
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(letter+str(int(num)-2), '--'), Board, enPassantSquare = letter+str(int(num)-1)))
			#legal_moves.append(cell+letter+str(int(num)-2))
		return legal_moves

class R(Piece):
	def __init__(self, cell, Board, color, moveLog):
		super(R,self).__init__(cell, Board, color, moveLog)
		self.cell = cell
		self.Board = Board
		self.color = color
		self.name = self.color+'R'
		self.moveLog = moveLog
		self.move_list = super().find_linear_moves(self.cell, self.Board, self.color)

class B(Piece):
	def __init__(self, cell, Board, color, moveLog):
		super(B,self).__init__(cell, Board, color, moveLog)
		self.cell = cell
		self.Board = Board
		self.color = color
		self.name = self.color+'B'
		self.moveLog = moveLog
		self.move_list = super().find_diag_moves(self.cell, self.Board, self.color)

class Q(Piece):
	def __init__(self, cell, Board, color, moveLog):
		super(Q,self).__init__(cell, Board, color, moveLog)
		self.cell = cell
		self.Board = Board
		self.color = color
		self.name = self.color+'Q'
		self.moveLog = moveLog
		self.move_list = super().find_linear_moves(self.cell, self.Board, self.color) + super().find_diag_moves(self.cell, self.Board, self.color)

class N(Piece):
	def __init__(self, cell, Board, color, moveLog):
		super(N,self).__init__(cell, Board, color, moveLog)
		self.cell = cell
		self.Board = Board
		self.color = color
		self.name = self.color+'N'
		self.moveLog = moveLog
		self.move_list = self.find_legal_moves(self.cell, self.Board, self.color)

	def letter_to_number(self, letter):
		return super().letter_to_number(letter)

	def number_to_letter(self, number):
		return super().number_to_letter(number)

	def find_legal_moves(self, cell, Board, color):
		legal_moves = []
		letter, num = list(cell)
		row = 8-int(num)
		col = ord(letter)-97
		if row >= 2 and col >= 1 and (Board[row-2][col-1].piece == '--' or list(Board[row-2][col-1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(8-(row-2)), Board[row-2][col-1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-1)+str(8-(row-2)))
		if row >= 2 and col <= 6 and (Board[row-2][col+1].piece == '--' or list(Board[row-2][col+1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(8-(row-2)), Board[row-2][col+1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+1)+str(8-(row-2)))
		if row >= 1 and col >= 2 and (Board[row-1][col-2].piece == '--' or list(Board[row-1][col-2].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-2)+str(8-(row-1)), Board[row-1][col-2].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-2)+str(8-(row-1)))
		if row >= 1 and col <= 5 and (Board[row-1][col+2].piece == '--' or list(Board[row-1][col+2].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+2)+str(8-(row-1)), Board[row-1][col+2].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+2)+str(8-(row-1)))
		if row <= 6 and col >= 2 and (Board[row+1][col-2].piece == '--' or list(Board[row+1][col-2].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-2)+str(8-(row+1)), Board[row+1][col-2].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-2)+str(8-(row+1)))
		if row <= 6 and col <= 5 and (Board[row+1][col+2].piece == '--' or list(Board[row+1][col+2].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+2)+str(8-(row+1)), Board[row+1][col+2].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+2)+str(8-(row+1)))
		if row <= 5 and col >= 1 and (Board[row+2][col-1].piece == '--' or list(Board[row+2][col-1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(8-(row+2)), Board[row+2][col-1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-1)+str(8-(row+2)))
		if row <= 5 and col <= 6 and (Board[row+2][col+1].piece == '--' or list(Board[row+2][col+1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(8-(row+2)), Board[row+2][col+1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+1)+str(8-(row+2)))
		return legal_moves

class K(Piece):
	def __init__(self, cell, Board, color, moveLog, castling = None):
		super(K,self).__init__(cell, Board, color,moveLog, castling = castling)
		self.cell = cell
		self.Board = Board
		self.color = color
		self.name = self.color+'Q'
		self.moveLog = moveLog
		self.castling = castling
		self.move_list = self.find_legal_moves(self.cell, self.Board, self.color, self.castling)
		self.row, self.col = 8-int(list(self.cell)[1]), ord(list(self.cell)[0])-97

	def letter_to_number(self, letter):
		return super().letter_to_number(letter)

	def number_to_letter(self, number):
		return super().number_to_letter(number)

	def find_legal_moves(self, cell, Board, color, castling):
		legal_moves = []
		letter, num = list(cell)
		row = 8-int(num)
		col = ord(letter)-97
		if row >= 1 and (Board[row-1][col].piece == '--' or list(Board[row-1][col].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col)+str(8-(row-1)), Board[row-1][col].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col)+str(8-(row-1)))
		if row >= 1 and col >= 1 and (Board[row-1][col-1].piece == '--' or list(Board[row-1][col-1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(8-(row-1)), Board[row-1][col-1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-1)+str(8-(row-1)))
		if row >= 1 and col <= 6 and (Board[row-1][col+1].piece == '--' or list(Board[row-1][col+1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(8-(row-1)), Board[row-1][col+1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+1)+str(8-(row-1)))
		if col >= 1 and (Board[row][col-1].piece == '--' or list(Board[row][col-1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(8-(row)), Board[row][col-1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-1)+str(8-(row)))
		if col <= 6 and (Board[row][col+1].piece == '--' or list(Board[row][col+1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(8-(row)), Board[row][col+1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+1)+str(8-(row)))
		if row <= 6 and col >= 1 and (Board[row+1][col-1].piece == '--' or list(Board[row+1][col-1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-1)+str(8-(row+1)), Board[row+1][col-1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col-1)+str(8-(row+1)))
		if row <= 6 and (Board[row+1][col].piece == '--' or list(Board[row+1][col].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col)+str(8-(row+1)), Board[row+1][col].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col)+str(8-(row+1)))
		if row <= 6 and col <=6 and (Board[row+1][col+1].piece == '--' or list(Board[row+1][col+1].piece)[0] != color):
			legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+1)+str(8-(row+1)), Board[row+1][col+1].piece), Board))
			#legal_moves.append(cell+self.number_to_letter(col+1)+str(8-(row+1)))
		
		#check castling
		if not self.find_checks(cell, Board, color):
			if castling != None:
				if color == 'w':
					if castling[0]:
						if col <= 5:
							if Board[row][col+1].piece == '--' and Board[row][col+2].piece == '--':
								checks1 = self.find_checks(chr(ord(list(cell)[0])+1)+list(cell)[1], Board, color)
								checks2 = self.find_checks(chr(ord(list(cell)[0])+2)+list(cell)[1], Board, color)
								if not checks1 and not checks2:
									legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+2)+str(8-row), Board[row][col+2].piece), Board, castling = 1))
					if castling[1]:
						if col >= 2:
							if Board[row][col-1].piece == '--' and Board[row][col-2].piece == '--' and Board[row][col-3].piece == '--':
								checks1 = self.find_checks(chr(ord(list(cell)[0])-1)+list(cell)[1], Board, color)
								checks2 = self.find_checks(chr(ord(list(cell)[0])-2)+list(cell)[1], Board, color)
								if not checks1 and not checks2:
									legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-2)+str(8-row), Board[row][col-2].piece), Board, castling = 2))
				elif color == 'b':
					if castling[2]:
						if col <= 5:
							if Board[row][col+1].piece == '--' and Board[row][col+2].piece == '--':
								checks1 = self.find_checks(chr(ord(list(cell)[0])+1)+list(cell)[1], Board, color)
								checks2 = self.find_checks(chr(ord(list(cell)[0])+2)+list(cell)[1], Board, color)
								if not checks1 and not checks2:
									legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col+2)+str(8-row), Board[row][col+2].piece), Board, castling = 3))
					if castling[3]:
						if col >= 2:
							if Board[row][col-1].piece == '--' and Board[row][col-2].piece == '--' and Board[row][col-3].piece == '--':
								checks1 = self.find_checks(chr(ord(list(cell)[0])-1)+list(cell)[1], Board, color)
								checks2 = self.find_checks(chr(ord(list(cell)[0])-2)+list(cell)[1], Board, color)
								if not checks1 and not checks2:
									legal_moves.append(Move(Cell(cell, Board[row][col].piece), Cell(self.number_to_letter(col-2)+str(8-row), Board[row][col-2].piece), Board, castling = 4))
		return legal_moves


	def find_checks(self, cell, Board, color):
		checks = []
		letter, num = list(cell)
		row = 8-int(num)
		col = ord(letter)-97
		if color == 'b':
			opposite_color = 'w'
		else:
			opposite_color = 'b'

		#checking vertical and horizontal moves
		for i in range(int(num), 8):
			if (Board[8-(i+1)][col].piece == opposite_color +'R') or (Board[8-(i+1)][col].piece == opposite_color+'Q'):
				checks.append(Cell(letter+str(i+1), Board[8-(i+1)][col].piece))
				#checks.append(cell+letter+str(i+1))
				break
			elif Board[8-(i+1)][col].piece == '--':
				continue
			else:
				break
		for j in range(row+1, 8):
			if (Board[j][col].piece == opposite_color +'R') or (Board[j][col].piece == opposite_color+'Q'):
				checks.append(Cell(letter+str(8-j), Board[j][col].piece))
				#checks.append(cell+letter+str(8-j))
			elif Board[j][col].piece == '--':
				continue
			else:
				break
		for k in range(col, 7):
			if (Board[row][k+1].piece == opposite_color+'R') or (Board[row][k+1].piece == opposite_color +'Q'):
				checks.append(Cell(self.number_to_letter(k+1)+str(8-int(row)), Board[row][k+1].piece))
				#checks.append(cell+self.number_to_letter(k+1)+str(8-int(row)))
			elif Board[row][k+1].piece == '--':
				continue
			else:
				break
		for l in range(8-col, 8):
			if (Board[row][8-(l+1)].piece == opposite_color+'R') or (Board[row][8-(l+1)].piece == opposite_color+'Q'):
				checks.append(Cell(self.number_to_letter(8-(l+1))+str(num), Board[row][8-(l+1)].piece))
				#checks.append(cell+self.number_to_letter(8-(l+1))+str(num))
			elif Board[row][8-(l+1)].piece == '--':
				continue
			else:
				break

		#checking diagonal moves
		row_Greater_col_right = int(num) >= int(col+1)
		row_Greater_col_left = int(num) >= 8-int(col)
		if row_Greater_col_right:
			for i in range(int(num), 8):
				if Board[8-(i+1)][col + (i+1-int(num))].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter(col + (i+1-int(num)))+str(i+1))
				elif list(Board[8-(i+1)][col + (i+1-int(num))].piece)[0] != color and (list(Board[8-(i+1)][col + (i+1-int(num))].piece)[1] == 'B' or list(Board[8-(i+1)][col + (i+1-int(num))].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter(col + (i+1-int(num)))+str(i+1), Board[8-(i+1)][col + (i+1-int(num))].piece))
					#checks.append(cell+self.number_to_letter(col + (i+1-int(num)))+str(i+1))
					break
				else:
					break
			for j in range(8-int(col), 8):
				if Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter((7-j))+str(((8-row)-(j+1-(8-int(col))))))
				elif list(Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece)[0] != color and (list(Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece)[1] == 'B' or list(Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter(7-j)+str(((8-row)-(j+1-(8-int(col))))), Board[7-((7-row)-(j+1-(8-int(col))))][(7-j)].piece))
					#checks.append(cell+self.number_to_letter(7-j)+str(((8-row)-(j+1-(8-int(col))))))
					break 
				else:
					break

		if not row_Greater_col_right:
			for i in range(int(col), 7):
				if Board[8-(int(num)+i+1-(int(col)))][i+1].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter(i+1)+str(int(num)+i+1-(int(col))))
				elif list(Board[8-(int(num)+i+1-(int(col)))][i+1].piece)[0] != color and (list(Board[8-(int(num)+i+1-(int(col)))][i+1].piece)[1] == 'B' or list(Board[8-(int(num)+i+1-(int(col)))][i+1].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter(i+1)+str(int(num)+i+1-(int(col))), Board[8-(int(num)+i+1-(int(col)))][i+1].piece))
					#checks.append(cell+self.number_to_letter(i+1)+str(int(num)+i+1-(int(col))))
					break
				else:
					break
			for j in range(row, 7):
				if Board[j+1][col-(j+1-row)].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter((col-(j+1-row)))+str(8-(j+1)))
				elif list(Board[j+1][col-(j+1-row)].piece)[0] != color and (list(Board[j+1][col-(j+1-row)].piece)[1] == 'B' or list(Board[j+1][col-(j+1-row)].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter((col-(j+1-row)))+str(8-(j+1)), Board[j+1][col-(j+1-row)].piece))
					#checks.append(cell+self.number_to_letter((col-(j+1-row)))+str(8-(j+1)))
					break
				else:
					break

		if row_Greater_col_left:
			for i in range(7-row, 7):
				if Board[7-(i+1)][col-(i+1-(7-row))].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter(col-(i+1-(7-row)))+str(8-(7-(i+1))))
				elif list(Board[7-(i+1)][col-(i+1-(7-row))].piece)[0] != color and (list(Board[7-(i+1)][col-(i+1-(7-row))].piece)[1] == 'B' or list(Board[7-(i+1)][col-(i+1-(7-row))].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter(col-(i+1-(7-row)))+str(8-(7-(i+1))), Board[7-(i+1)][col-(i+1-(7-row))].piece))
					#checks.append(cell+self.number_to_letter(col-(i+1-(7-row)))+str(8-(7-(i+1))))
					break
				else:
					break

			for j in range(col, 7):
				if Board[row+(j+1-col)][j+1].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter(j+1)+str(8-(row+(j+1-col))))
				elif list(Board[row+(j+1-col)][j+1].piece)[0] != color and (list(Board[row+(j+1-col)][j+1].piece)[1] == 'B' or list(Board[row+(j+1-col)][j+1].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter(j+1)+str(8-(row+(j+1-col))), Board[row+(j+1-col)][j+1].piece))
					#checks.append(cell+self.number_to_letter(j+1)+str(8-(row+(j+1-col))))
					break
				else:
					break

		if not row_Greater_col_left:
			for k in range(7-int(col), 7):
				if Board[row-(k+1-(7-int(col)))][(7-k)-1].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter((7-k)-1)+str(8-(row-(k+1-(7-int(col))))))
				elif list(Board[row-(k+1-(7-int(col)))][(7-k)-1].piece)[0] != color and (list(Board[row-(k+1-(7-int(col)))][(7-k)-1].piece)[1] == 'B' or list(Board[row-(k+1-(7-int(col)))][(7-k)-1].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter((7-k)-1)+str(8-(row-(k+1-(7-int(col))))), Board[row-(k+1-(7-int(col)))][(7-k)-1].piece))
					#checks.append(cell+self.number_to_letter((7-k)-1)+str(8-(row-(k+1-(7-int(col))))))
					break
				else:
					break

			for j in range(row, 7):
				if Board[j+1][col+(j+1-row)].piece == '--':
					continue
					#checks.append(cell+self.number_to_letter(col+(j+1-row))+str(8-(j+1)))
				elif list(Board[j+1][col+(j+1-row)].piece)[0] != color and (list(Board[j+1][col+(j+1-row)].piece)[1] == 'B' or list(Board[j+1][col+(j+1-row)].piece)[1] == 'Q'):
					checks.append(Cell(self.number_to_letter(col+(j+1-row))+str(8-(j+1)), Board[j+1][col+(j+1-row)].piece))
					#checks.append(cell+self.number_to_letter(col+(j+1-row))+str(8-(j+1)))
					break
				else:
					break

		#checking knight moves
		if row >= 2 and col >= 1 and list(Board[row-2][col-1].piece)[0] != color and list(Board[row-2][col-1].piece)[1] == 'N':
			checks.append(Cell(self.number_to_letter(col-1)+str(8-(row-2)), Board[row-2][col-1].piece))
			#checks.append(cell+self.number_to_letter(col-1)+str(8-(row-2)))
		if row >= 2 and col <= 6 and list(Board[row-2][col+1].piece)[1] == 'N' and list(Board[row-2][col+1].piece)[0] != color:
			checks.append(Cell(self.number_to_letter(col+1)+str(8-(row-2)), Board[row-2][col+1].piece))
			#checks.append(cell+self.number_to_letter(col+1)+str(8-(row-2)))
		if row >= 1 and col >= 2 and list(Board[row-1][col-2].piece)[1] == 'N' and list(Board[row-1][col-2].piece)[0] != color:
			checks.append(Cell(self.number_to_letter(col-2)+str(8-(row-1)), Board[row-1][col-2].piece))
			#checks.append(cell+self.number_to_letter(col-2)+str(8-(row-1)))
		if row >= 1 and col <= 5 and list(Board[row-1][col+2].piece)[1] == 'N' and list(Board[row-1][col+2].piece)[0] != color:
			checks.append(Cell(self.number_to_letter(col+2)+str(8-(row-1)), Board[row-1][col+2].piece))
			#checks.append(cell+self.number_to_letter(col+2)+str(8-(row-1)))
		if row <= 6 and col >= 2 and list(Board[row+1][col-2].piece)[1] == 'N' and list(Board[row+1][col-2].piece)[0] != color:
			checks.append(Cell(self.number_to_letter(col-2)+str(8-(row+1)), Board[row+1][col-2].piece))
			#checks.append(cell+self.number_to_letter(col-2)+str(8-(row+1)))
		if row <= 6 and col <= 5 and list(Board[row+1][col+2].piece)[1] == 'N' and list(Board[row+1][col+2].piece)[0] != color:
			checks.append(Cell(self.number_to_letter(col+2)+str(8-(row+1)), Board[row+1][col+2].piece))
			#checks.append(cell+self.number_to_letter(col+2)+str(8-(row+1)))
		if row <= 5 and col >= 1 and list(Board[row+2][col-1].piece)[1] == 'N' and list(Board[row+2][col-1].piece)[0] != color:
			checks.append(Cell(self.number_to_letter(col-1)+str(8-(row+2)), Board[row+2][col-1].piece))
			#checks.append(cell+self.number_to_letter(col-1)+str(8-(row+2)))
		if row <= 5 and col <= 6 and list(Board[row+2][col+1].piece)[1] == 'N' and list(Board[row+2][col+1].piece)[0] != color:
			checks.append(Cell(self.number_to_letter(col+1)+str(8-(row+2)), Board[row+2][col+1].piece))
			#checks.append(cell+self.number_to_letter(col+1)+str(8-(row+2)))

		#checking white pawn checks
		if color == 'b':
			if col > 0 and row < 7:
				if Board[row+1][col-1].piece == 'wP':
					checks.append(Cell(self.number_to_letter(col-1)+str(8-(row+1)), Board[row+1][col-1].piece))
			if col < 7 and row < 7:
				if Board[row+1][col+1].piece == 'wP':
					checks.append(Cell(self.number_to_letter(col+1)+str(8-(row+1)), Board[row+1][col+1].piece))

		#checking black pawn checks
		if color == 'w':
			if col > 0 and row > 0:
				if Board[row-1][col-1].piece == 'bP':
					checks.append(Cell(self.number_to_letter(col-1)+str(8-(row-1)), Board[row-1][col-1].piece))
			if col < 7 and row > 0:
				if Board[row-1][col+1].piece == 'bP':
					checks.append(Cell(self.number_to_letter(col+1)+str(8-(row-1)), Board[row-1][col+1].piece))

		#checking opposite king checks
		if row >= 1 and Board[row-1][col].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col)+str(8-(row-1)), Board[row-1][col].piece))
			#checks.append(cell+self.number_to_letter(col)+str(8-(row-1)))
		if row >= 1 and col >= 1 and Board[row-1][col-1].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col-1)+str(8-(row-1)), Board[row-1][col-1].piece))
			#checks.append(cell+self.number_to_letter(col-1)+str(8-(row-1)))
		if row >= 1 and col <= 6 and Board[row-1][col+1].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col+1)+str(8-(row-1)), Board[row-1][col+1].piece))
			#checks.append(cell+self.number_to_letter(col+1)+str(8-(row-1)))
		if col >= 1 and Board[row][col-1].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col-1)+str(8-(row)), Board[row][col-1].piece))
			#checks.append(cell+self.number_to_letter(col-1)+str(8-(row)))
		if col <= 6 and Board[row][col+1].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col+1)+str(8-(row)), Board[row][col+1].piece))
			#checks.append(cell+self.number_to_letter(col+1)+str(8-(row)))
		if row <= 6 and col >= 1 and Board[row+1][col-1].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col-1)+str(8-(row+1)), Board[row+1][col-1].piece))
			#checks.append(cell+self.number_to_letter(col-1)+str(8-(row+1)))
		if row <= 6 and Board[row+1][col].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col)+str(8-(row+1)), Board[row+1][col].piece))
			#checks.append(cell+self.number_to_letter(col)+str(8-(row+1)))
		if row <= 6 and col <=6 and Board[row+1][col+1].piece == opposite_color+'K':
			checks.append(Cell(self.number_to_letter(col+1)+str(8-(row+1)), Board[row+1][col+1].piece))
			#checks.append(cell+self.number_to_letter(col+1)+str(8-(row+1)))
		
		return checks

