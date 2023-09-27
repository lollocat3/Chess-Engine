import pygame
import sys
import time
import cProfile
import math
import chess
from copy import deepcopy
import time
from termcolor import colored
from evaluation import ChessState, shallow_search, alphabeta
from halo import Halo 
import signal
from chess import engine

HEIGHT = WIDTH = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
Images = {}

class Standard_Board():
	def __init__(self):
		self.board = chess.Board()
		self.boardLog = []
		self.col_dict = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

	def cell_rect(self, number):
		col = number % 8
		row = 7- math.floor(number/8)
		return pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

	def handler(self, signum, frame):
		raise Exception("over time limit")

	def engine_move(self):
		engin = engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
		m = engin.play(self.board, engine.Limit(time=0.1)).move
		return m

	def computer_move(self):
		state = ChessState(self.board)
		total = 0
		transpositions = 0
		trans_dict = {}
		init_hash = state.zobrist_init_hash()
		moves = shallow_search(state)
		opening_book = chess.polyglot.MemoryMappedReader('/Users/lorenzo/Documents/performance.bin')
		table = False
		theory = False
		try:
			m = opening_book.choice(state.board).move
			theory = True
		except:
			if state.get_phase() == 'tablebase':
				m = state.tablebase()
				table = True
			else:
				try:
					signal.signal(signal.SIGALRM, self.handler)
					signal.alarm(30)
					m = alphabeta(state,4,float("-inf"),float("inf"), total, init_hash, trans_dict, transpositions, moves, first = True)[1]
					signal.alarm(0)
				except Exception:
					m = self.engine_move()
		return m, theory, table

	def undoMove(self):
		try:
			self.board = self.boardLog.pop()
		except:
			return

	def termination(self):
		if self.board.is_checkmate():
			return 'checkmate'
		elif self.board.is_stalemate():
			return 'stalemate'
		elif self.board.is_insufficient_material():
			return 'insufficient'
		elif self.board.can_claim_fifty_moves():
			return 'fifty moves'
		elif self.board.can_claim_threefold_repetition():
			return 'threefold'
		else:
			return None

	def load_pieces(self):
		Pieces = ['q', 'k', 'b', 'n', 'r',
				  'p', 'P', 'Q', 'K', 'B', 'N', 'R']
		pieces_for_imgs = ['bQ', 'bK', 'bB', 'bN', 'bR', 'bP', 'wP', 'wQ', 'wK', 'wB', 'wN', 'wR']
		for i in range(12):
			piece = Pieces[i]
			piece_img = pieces_for_imgs[i]
			Images[piece] = pygame.transform.scale(pygame.image.load(
				"/Users/lorenzo/Desktop/Python/Chess/pieces/" + piece_img + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
		return Images

	def draw_board(self, dim, SQUARE_SIZE, window):
		colors = [(240, 217, 182), (181, 136, 99)]
		for r in range(dim):
			for c in range(dim):
				color = colors[(r + c) % 2]
				pygame.draw.rect(window, color, pygame.Rect(
					r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

	def draw_pieces(self, dim, window, Images, Board):
		for i in range(64):
			if Board.board.piece_at(i) != None:
				window.blit(Images[Board.board.piece_at(i).symbol()], self.cell_rect(i))

def main():
	game_has_ended = False
	window = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	FPS = 60
	Board = Standard_Board()
	Images = Board.load_pieces()
	red = False
	game_has_ended = False
	pause = 5*FPS
	pause_check = FPS
	pygame.font.init()
	font = pygame.font.Font(None, 70)
	surfaces = [font.render('Checkmate!', False, (0, 0, 0)), font.render('Stalemate!', False, (0, 0, 0)), font.render('Draw by repetition!', False, (0, 0, 0)),
	font.render('insufficient material!!', False, (0, 0, 0)), font.render('fifty move draw!', False, (0, 0, 0))]

	while True:
		if Board.termination():
				end_event = Board.termination()
				game_has_ended = True
		if game_has_ended:
			if pause > 0:
				pause -= 1
				if end_event == 'checkmate':
					textsurface = surfaces[0]
					window.blit(textsurface,(WIDTH//2-130,HEIGHT//2-20))
					pygame.display.update()
					clock.tick(FPS)
				elif end_event == 'stalemate':
					textsurface = surfaces[1]
					window.blit(textsurface,(WIDTH//2-130,HEIGHT//2-20))
					pygame.display.update()
					clock.tick(FPS)
				elif end_event == 'threefold':
					textsurface = surfaces[2]
					window.blit(textsurface,(WIDTH//2-210,HEIGHT//2-20))
					pygame.display.update()
					clock.tick(FPS)
				elif end_event == 'insufficient':
					textsurface = surfaces[3]
					window.blit(textsurface,(WIDTH//2-220,HEIGHT//2-20))
					pygame.display.update()
					clock.tick(FPS)
				elif end_event == 'fifty moves':
					textsurface = surfaces[4]
					window.blit(textsurface,(WIDTH//2-210,HEIGHT//2-20))
					pygame.display.update()
					clock.tick(FPS)
			else:
				Board.board = chess.Board()
				game_has_ended = not game_has_ended
				pause = 5*FPS
		
		if not Board.board.turn:
			t = time.time()
			spinner = Halo(text='Thinking...', spinner='boxBounce')
			spinner.start()
			move, theory, table = Board.computer_move()
			spinner.stop()
			#board_copy = deepcopy(Board.board)
			#Board.boardLog.append(board_copy)
			Board.board.push(move)
			search_time = time.time()-t
			if theory:
				print(colored('still theory!', 'red'))
			elif table:
				print(colored('endgame tablebase!', 'red'))
			print(colored('the computer played: '+ str(move), 'yellow'))
			print(colored('the search took ' +str(float(round(time.time()-t, 3))) + ' seconds', 'blue'))
			print('-----------------------')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if Board.board.turn:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						x, y = event.pos
						row = math.floor(y/64)
						col = math.floor(x/64)
						square = (7-row)*8+col
						starting_square = Board.col_dict[col]+ str(8-row)
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						x, y = event.pos
						row = math.floor(y/64)
						col = math.floor(x/64)
						ending_square = Board.col_dict[col]+ str(8-row)
						if ending_square != starting_square:
							try:
								piece = Board.board.piece_at(square).symbol()
								move = chess.Move.from_uci(starting_square+ending_square)
								if (piece == 'p' and row == 7) or (piece == 'P' and row == 0):
									move = chess.Move.from_uci(starting_square+ending_square+'q')
							except:
								move = chess.Move.from_uci(starting_square+ending_square)
							is_legal = Board.board.is_legal(move)
							if is_legal:
								board_copy = deepcopy(Board.board)
								Board.boardLog.append(board_copy)
								Board.board.push(move)

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						Board.undoMove()
					elif event.key == pygame.K_r:
						Board.board = chess.Board()
						Board.board.boardLog = []

		window.fill(pygame.Color('white'))
		Board.draw_board(DIMENSION, SQUARE_SIZE, window)
		Board.draw_pieces(DIMENSION, window, Images, Board)
		pygame.display.update()

		
		

main()
