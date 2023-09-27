import pygame
import sys
from pieces import Piece, P, R, B, Q, N, K, Move, Cell
#import numpy as np
import time
from copy import deepcopy
import cProfile

HEIGHT = WIDTH = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
Images = {}

class Standard_Board():

	def __init__(self):
		self.Board = [
			[Cell('a8', 'bR'), Cell('b8','bN'), Cell('c8', 'bB'), Cell('d8','bQ'), Cell('e8','bK'), Cell('f8','bB'), Cell('g8','bN'), Cell('h8','bR')],
			[Cell('a7', 'bP'), Cell('b7','bP'), Cell('c7', 'bP'), Cell('d7','bP'), Cell('e7','bP'), Cell('f7','bP'), Cell('g7','bP'), Cell('h7','bP')],
			[Cell('a6', '--'), Cell('b6','--'), Cell('c6', '--'), Cell('d6','--'), Cell('e6','--'), Cell('f6','--'), Cell('g6','--'), Cell('h6','--')],
			[Cell('a5', '--'), Cell('b5','--'), Cell('c5', '--'), Cell('d5','--'), Cell('e5','--'), Cell('f5','--'), Cell('g5','--'), Cell('h5','--')],
			[Cell('a4', '--'), Cell('b4','--'), Cell('c4', '--'), Cell('d4','--'), Cell('e4','--'), Cell('f4','--'), Cell('g4','--'), Cell('h4','--')],
			[Cell('a3', '--'), Cell('b3','--'), Cell('c3', '--'), Cell('d3','--'), Cell('e3','--'), Cell('f3','--'), Cell('g3','--'), Cell('h3','--')],
			[Cell('a2', 'wP'), Cell('b2','wP'), Cell('c2', 'wP'), Cell('d2','wP'), Cell('e2','wP'), Cell('f2','wP'), Cell('g2','wP'), Cell('h2','wP')],
			[Cell('a1', 'wR'), Cell('b1','wN'), Cell('c1', 'wB'), Cell('d1','wQ'), Cell('e1','wK'), Cell('f1','wB'), Cell('g1','wN'), Cell('h1','wR')],
		]
		self.WhiteToMove = True
		self.MoveLog = []
		self.BoardLog = []
		self.castling = [[True, True, True, True]]

	def check_two_boards(self, board, other):
		for i in range(0, DIMENSION):
			for j in range(0, DIMENSION):
				if board[i][j] != other[i][j]:
					return False
		return True

	def MakeMove(self, move, Board, background = False):
		Start_row = move.Start_row
		Start_col = move.Start_col
		End_row = move.End_row
		End_col = move.End_col
		if move.pawnPromotion and not move.castling:
			Board[Start_row][Start_col].piece = '--'
			Board[End_row][End_col].piece = list(move.Start_piece)[0]+'Q'
		elif not move.pawnPromotion and not move.castling:
			Board[Start_row][Start_col].piece = '--'
			Board[End_row][End_col].piece = move.Start_piece
		#print(move.enPassantSquare)
		if move.enPassantSquare == move.End_cell.name:
			if list(move.Start_piece)[0] == 'w':
				Board[Start_row][Start_col].piece = '--'
				Board[End_row][End_col].piece = move.Start_piece
				Board[End_row+1][End_col].piece = '--'
			elif list(move.Start_piece)[0] == 'b':
				Board[Start_row][Start_col].piece = '--'
				Board[End_row][End_col].piece = move.Start_piece
				Board[End_row-1][End_col].piece = '--'
		if move.castling != None:
			if move.castling == 1:
				Board[Start_row][Start_col].piece = '--'
				Board[End_row][End_col].piece = 'wK'
				Board[Start_row][Start_col+3].piece = '--'
				Board[Start_row][Start_col+1].piece = 'wR'
			elif move.castling == 2:
				Board[Start_row][Start_col].piece = '--'
				Board[End_row][End_col].piece = 'wK'
				Board[Start_row][Start_col-3].piece = '--'
				Board[Start_row][Start_col-4].piece = '--'
				Board[Start_row][Start_col-1].piece = 'wR'
			elif move.castling == 3:
				Board[Start_row][Start_col].piece = '--'
				Board[End_row][End_col].piece = 'bK'
				Board[Start_row][Start_col+3].piece = '--'
				Board[Start_row][Start_col+1].piece = 'bR'
			elif move.castling == 4:
				Board[Start_row][Start_col].piece = '--'
				Board[End_row][End_col].piece = 'bK'
				Board[Start_row][Start_col-3].piece = '--'
				Board[Start_row][Start_col-4].piece = '--'
				Board[Start_row][Start_col-1].piece = 'bR'

		if not background:
			self.MoveLog.append(move)
		#self.BoardLog.append(Board)
		self.WhiteToMove = not self.WhiteToMove
		return Board

	def UndoMove(self, MoveLog, Board, castling, manual = False):
		if MoveLog:
			last_move = MoveLog.pop(-1)
			Start_row = last_move.Start_row
			Start_col = last_move.Start_col
			End_row = last_move.End_row
			End_col = last_move.End_col
			End_piece = last_move.End_piece
			Start_piece = last_move.Start_piece
			if MoveLog:
				if MoveLog[-1].enPassantSquare == last_move.End_cell.name and list(last_move.Start_piece)[1] == 'P':
					if list(last_move.Start_piece)[0] == 'w':
						Board[End_row][End_col].piece = '--'
						#print(End_piece)
						Board[Start_row][Start_col].piece = Start_piece
						Board[End_row+1][End_col].piece = 'bP'
					elif list(last_move.Start_piece)[0] == 'b':
						#print('true')
						Board[End_row][End_col].piece = End_piece
						Board[Start_row][Start_col].piece = Start_piece
						Board[End_row-1][End_col].piece = 'wP'
				if last_move.castling:
					if last_move.castling == 1:
						Board[7][7].piece = 'wR'
						Board[7][5].piece = '--'
					elif last_move.castling == 2:
						Board[7][0].piece = 'wR'
						Board[7][3].piece = '--'
					elif last_move.castling == 3:
						Board[0][7].piece = 'bR'
						Board[0][5].piece = '--'
					elif last_move.castling == 4:
						Board[0][0].piece = 'bR'
						Board[0][3].piece = '--'
			Board[End_row][End_col].piece = End_piece
			Board[Start_row][Start_col].piece = Start_piece
			if self.BoardLog:
				del self.BoardLog[-1]
			self.WhiteToMove = not self.WhiteToMove
			if manual and castling:
				del castling[-1]
		return Board

	def termination(self, board, valid_moves, moveLog):

		#3-fold repetition
		equal_states = False
		length = len(board.BoardLog)
		for i in range(0, length):
			for j in range(0, length):
				for k in range(0, length):
					if i != j and i != k and j != k:
						if self.check_two_boards(board.BoardLog[i], board.BoardLog[j]) and self.check_two_boards(board.BoardLog[i], board.BoardLog[k]):
							equal_states = True
		if equal_states:
			return 'three fold'

		#checking for checkmate and stalemate
		legal_moves = []
		for elem in valid_moves:
			board.Board = board.MakeMove(elem, board.Board)
			for row in board.Board:
				for cell in row:
					if cell.piece == list(elem.Start_cell.piece)[0]+'K':
						king_cell = cell
						king = K(cell.name, board.Board, list(cell.piece)[0], moveLog)
						checks = king.find_checks(cell.name, board.Board, list(cell.piece)[0])
						if not checks:
							legal_moves.append(elem)
			board.Board = board.UndoMove(moveLog, board.Board, board.castling)
		if not legal_moves:
			if king.find_checks(king_cell.name, board.Board, list(cell.piece)[0]):
				return 'checkmate'
			elif not king.find_checks(king_cell.name, board.Board, list(cell.piece)[0]):
				return 'stalemate'





	def load_pieces(self):
		Pieces = ['bQ', 'bK', 'bB', 'bN', 'bR',
				  'bP', 'wP', 'wQ', 'wK', 'wB', 'wN', 'wR']
		for piece in Pieces:
			Images[piece] = pygame.transform.scale(pygame.image.load(
				"/Users/lorenzo/Desktop/Python/Chess/pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
		return Images

	def draw_board(self, dim, SQUARE_SIZE, window):
		colors = [(240, 217, 182), (181, 136, 99)]
		for r in range(dim):
			for c in range(dim):
				color = colors[(r + c) % 2]
				pygame.draw.rect(window, color, pygame.Rect(
					r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

	def draw_pieces(self, dim, window, Images, board):
		for row in range(dim):
			for col in range(dim):
				if board.Board[row][col].piece != '--':
					window.blit(Images[board.Board[row][col].piece], board.Board[row][col].cell_rect)

def concatenate_no_np(arr):
	final = []
	for elem in arr:
		for move in elem:
			final.append(move)
	return final


def main():
	window = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	FPS = 30
	board = Standard_Board()
	Images = board.load_pieces()
	red = False
	game_has_ended = False
	pause = 5*FPS
	pause_check = FPS
	pygame.font.init()
	font = pygame.font.Font(None, 70)


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					for row in board.Board:
						for cell in row:
							rect = cell.cell_rect
							if rect.collidepoint(event.pos):
								Start_cell = cell

				valid_moves = []
				valid_moves_objects = []
				
				if board.WhiteToMove:
					for row in board.Board:
						for cell in row:
							if list(cell.piece)[0] == 'w':
								if cell.piece == 'wK':
									piece = K(cell.name, board.Board, list(cell.piece)[0], board.MoveLog, board.castling[-1])
									valid_moves.append(piece.move_list)
								else:
									klass = globals()[list(cell.piece)[1]]
									piece = klass(cell.name, board.Board, list(cell.piece)[0], board.MoveLog)
									valid_moves.append(piece.move_list)
					valid_moves = concatenate_no_np(valid_moves)
				elif not board.WhiteToMove:
					for row in board.Board:
						for cell in row:
							if list(cell.piece)[0] == 'b':
								if cell.piece == 'bK':
									piece = K(cell.name, board.Board, list(cell.piece)[0], board.MoveLog, board.castling[-1])
									valid_moves.append(piece.move_list)
								else:
									klass = globals()[list(cell.piece)[1]]
									piece = klass(cell.name, board.Board, list(cell.piece)[0], board.MoveLog)
									valid_moves.append(piece.move_list)
					valid_moves = concatenate_no_np(valid_moves)
		
				
				
				

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					already_found = False
					previous_castling = board.castling[-1].copy()
					move_played = False
					for row in board.Board:
						for cell in row:
							if cell.cell_rect.collidepoint(event.pos):
								End_cell = cell
								move = Move(Start_cell, End_cell, board.Board)
								for elem in valid_moves:
									if elem.chessNotation == move.chessNotation:
										move_played = True
										board.Board = board.MakeMove(elem, board.Board)
										for row in board.Board:
											for cell in row:
												if not already_found:
													if cell.piece == list(elem.Start_cell.piece)[0]+'K':
														king = K(cell.name, board.Board, list(cell.piece)[0], board.MoveLog, board.castling[-1])
														checks = king.find_checks(cell.name, board.Board, list(cell.piece)[0])
														if checks:
															if not game_has_ended:
																print('this move' + ' ('+elem.chessNotation+') '+'is illegal as it leaves the king in check')
															board.Board = board.UndoMove(board.MoveLog, board.Board, board.castling)
															move_played = False
															red = not red
															already_found = not already_found
															for row in board.Board:
																for cell in row:
																	if cell.piece == list(elem.Start_cell.piece)[0]+'K':
																		new_king = K(cell.name, board.Board, list(cell.piece)[0], board.MoveLog, board.castling[-1])
										if move_played:
											if (elem.Start_piece == 'wK' or (elem.Start_piece == 'wR' and elem.Start_cell.name == 'h1')):
												previous_castling[0] = False
											if (elem.Start_piece == 'wK' or (elem.Start_piece == 'wR' and elem.Start_cell.name == 'a1')):
												previous_castling[1] = False
											if (elem.Start_piece == 'bK' or (elem.Start_piece == 'bR' and elem.Start_cell.name == 'h8')):
												previous_castling[2] = False
											if (elem.Start_piece == 'bK' or (elem.Start_piece == 'bR' and elem.Start_cell.name == 'a8')):
												previous_castling[3] = False
											board.castling.append(previous_castling)

					board_state_copy = deepcopy(board.Board)
					if move_played:
						board.BoardLog.append(board_state_copy)			
					board_copy = deepcopy(board)
					valid_moves_copy = []
					if board_copy.WhiteToMove:
						for row in board_copy.Board:
							for cell in row:
								if list(cell.piece)[0] == 'w':
									klass = globals()[list(cell.piece)[1]]
									piece = klass(cell.name, board_copy.Board, list(cell.piece)[0], board_copy.MoveLog)
									valid_moves_copy.append(piece.move_list)
						valid_moves_copy = concatenate_no_np(valid_moves_copy)
				
					elif not board_copy.WhiteToMove:
						for row in board_copy.Board:
							for cell in row:
								if list(cell.piece)[0] == 'b':
									klass = globals()[list(cell.piece)[1]]
									piece = klass(cell.name, board_copy.Board, list(cell.piece)[0], board_copy.MoveLog)
									valid_moves_copy.append(piece.move_list)
						valid_moves_copy = concatenate_no_np(valid_moves_copy)

					if board.termination(board_copy, valid_moves_copy, board_copy.MoveLog):
						game_has_ended = True
						end_event = board.termination(board_copy, valid_moves_copy, board_copy.MoveLog)
						
														

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					board.Board = board.UndoMove(board.MoveLog, board.Board, board.castling, manual = True)
				elif event.key == pygame.K_r:
					board = Standard_Board()

		window.fill(pygame.Color('white'))
		board.draw_board(DIMENSION, SQUARE_SIZE, window)
		board.draw_pieces(DIMENSION, window, Images, board)
		pygame.display.update()
		#clock.tick(FPS)
		if not game_has_ended:
			if red:
				if pause_check > 0:
					pause_check -= 1
					s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE), pygame.SRCALPHA)
					s.fill((255, 0, 0,128))
					window.blit(s, ((new_king.col) * SQUARE_SIZE, (new_king.row) * SQUARE_SIZE))
					pygame.display.update()
				else:
					red = not red
					pause_check = FPS
			else:
				pygame.display.update()
				clock.tick(FPS)
		else:
			if pause > 0:
				pause -= 1
				if end_event == 'checkmate':
					textsurface = font.render('Checkmate!', False, (0, 0, 0))
					window.blit(textsurface,(WIDTH//2-130,HEIGHT//2-20))
					pygame.display.update()
				elif end_event == 'stalemate':
					textsurface = font.render('Stalemate!', False, (0, 0, 0))
					window.blit(textsurface,(WIDTH//2-130,HEIGHT//2-20))
					pygame.display.update()
				elif end_event == 'three fold':
					textsurface = font.render('Draw by repetition!', False, (0, 0, 0))
					window.blit(textsurface,(WIDTH//2-210,HEIGHT//2-20))
					pygame.display.update()
			else:
				board = Standard_Board()
				game_has_ended = not game_has_ended
				pause = 5*FPS

#cProfile.run('main()')
main()
