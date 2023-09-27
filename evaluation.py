import chess
import chess.polyglot
import chess.syzygy
import copy
from piece_dicts import *
from square_control import *
#from bitboards import *
import time
import cProfile
import random
from copy import copy
from termcolor import colored

class ChessState():
    def __init__(self, board_state):
        self.board = board_state
        #self.bitboard = bitboards_to_array(bitboard(self.board))
        self.game_phase = self.get_phase()

    def zobrist_init_hash(self):
        init_hash = [[] for i in range(64)]
        for i in range(64):
            for j in range(12):
                init_hash[i].append(random.randint(0, 2**64))
        return init_hash

    def zobrist_hash(self, init_hash):
        board = self.board
        value_dict = {'P':0, 'R':1, 'B':2, 'N':3, 'Q':4, 'K':5, 'p':6, 'r':7, 'b':8, 'n': 9, 'q':10, 'k':11}
        h = 0
        for i in range(64):
            if board.piece_at(i):
                index = value_dict[board.piece_at(i).symbol()]
                j = init_hash[i][index]
                h = h ^ j
        return h


    def getMoves(self):
        return list(self.board.legal_moves)

    def get_phase(self):
        num_pieces = len(self.board.piece_map())
        if len(self.board.pieces(chess.QUEEN, chess.WHITE)) == 0 and len(self.board.pieces(chess.QUEEN, chess.BLACK)) == 0 and num_pieces > 5:
            return 'endgame'
        elif num_pieces <= 5:
            return 'tablebase'
        return 'middlegame'

    def dtz(self, state):
        with chess.syzygy.open_tablebase("/Users/lorenzo/Documents/3-4-5piecesSyzygy/3-4-5") as tablebase:
            dtz = tablebase.probe_dtz(state.board)
        return dtz

    def wdl(self, state):
        with chess.syzygy.open_tablebase("/Users/lorenzo/Documents/3-4-5piecesSyzygy/3-4-5") as tablebase:
            wdl = tablebase.probe_wdl(state.board)
        return wdl

    def tablebase(self):
        initial_wdl = self.wdl(self)
        if self.isWhitesTurn:
            maximise = True
        else:
            maximise = False
        moves = self.getMoves()
        good_moves = []
        distances = []
        for m in moves:
            res = self.result(m)
            if maximise:
                if self.wdl(res) <= -initial_wdl:
                    good_moves.append(m)
                    distances.append(self.dtz(res))
            elif not maximise:
                if self.wdl(res) >= -initial_wdl:
                    good_moves.append(m)
                    distances.append(self.dtz(res))
        if (maximise and initial_wdl >= 0) or (not maximise and initial_wdl <= 0):
            sorted_moves = [x for (y,x) in sorted(zip(distances,good_moves), key=lambda pair: pair[0], reverse = True)]
        elif (maximise and initial_wdl < 0) or (not maximise and initial_wdl > 0):
            sorted_moves = [x for (y,x) in sorted(zip(distances,good_moves), key=lambda pair: pair[0], reverse = False)]
        return sorted_moves[0]

    def material_eval(self):
        pieces=self.board.piece_map()
        values={
            chess.KING:1000000,
            chess.QUEEN:900,
            chess.ROOK:500,
            chess.BISHOP:330,
            chess.KNIGHT:320,
            chess.PAWN:100
            }
        total=0
        for p in pieces.values():
            multiplier=1
            if p.color==chess.BLACK:
                multiplier=-1
            total+=multiplier*values[p.piece_type]
        return total

    def piece_dict_eval(self):
        arr = self.piece_dicts()
        score = arr[0]-arr[1]+arr[2]-arr[3]+arr[4]-arr[5]+arr[6]-arr[7]+arr[8]-arr[9]+arr[10]-arr[11]
        return score

    def square_control_eval(self):
        num_white = num_squares_controled(self.board, True)
        num_black = num_squares_controled(self.board, False)
        return num_white - num_black

    def center_control_eval(self):
        num_white = center_control(self.board, True)
        num_black = center_control(self.board, False)
        return num_white-num_black

    def center_pawns_eval(self):
        num_white = pawns_center(self.board, True)
        num_black = pawns_center(self.board, False)
        return num_white-num_black

    def evaluate(self):
        #return 1.54*self.material_eval()+1.17*self.piece_dict_eval()  + 27.2*self.square_control_eval() -13.8*self.center_control_eval() -23.5*self.center_pawns_eval()+1.13*10**-4*self.material_eval()**2-3.14*10**-4*self.piece_dict_eval()**2+0.53*self.square_control_eval()**2-1.02*self.center_control_eval()**2+0.89*self.center_pawns_eval()**2
        return 3*self.material_eval()+3*self.piece_dict_eval()  + 2*self.square_control_eval() + 5*self.center_control_eval() +100*self.center_pawns_eval()
    
    def piece_dicts(self):
        #bitboard = self.bitboard
        board = self.board
        white_pawns = white_pawn_table(board)
        black_pawns = black_pawn_table(board)
        white_knights = white_knight_table(board)
        black_knights = black_knight_table(board)
        white_bishop = white_bishop_table(board)
        black_bishop = black_bishop_table(board)
        white_rook = white_rook_table(board)
        black_rook = black_rook_table(board)
        white_queen = white_queen_table(board)
        black_queen = black_queen_table(board)
        white_king = white_king_table(board, self.game_phase)
        black_king = black_king_table(board, self.game_phase)
        return [white_pawns, black_pawns, white_knights, black_knights, white_bishop, black_bishop, white_rook, black_rook, white_queen, black_queen, white_king, black_king]

    def isWhitesTurn(self):
        return self.board.turn

    def result(self,move):
        s=ChessState(copy(self.board))
        s.board.push(move)
        return s

    def print(self):
        print('   a b c d e f g h\n')
        rank=8
        for row in str(self.board).split('\n'):
            print(str(rank)+'  '+row)
            rank-=1

def shallow_search(state):
    moves = state.getMoves()
    values = []
    for m in moves:        
        values.append(state.result(m).evaluate())
    sorted_moves = [x for (y,x) in sorted(zip(values,moves), key=lambda pair: pair[0], reverse = True)]
    return sorted_moves

def alphabeta(state, depth, alpha, beta, total, init_hash, trans_dict, transpositions, ordered_moves, first = False, time_limit = 30, time_elapsed = 0):
    value = None
    if first:
        moves = ordered_moves
    else:
        moves = state.getMoves()
    if depth==0 or len(state.getMoves())==0:
        try:
            precomputed_eval = trans_dict[state.zobrist_hash(init_hash)]
            transpositions += 1
            return (precomputed_eval, None)
        except:
            pass
        total += 1
        evaluation = state.evaluate()
        trans_dict[state.zobrist_hash(init_hash)] = evaluation
        return (evaluation, None)
    if state.isWhitesTurn():
        value=float("-inf")
        for m in moves:
            childScore=alphabeta(state.result(m), depth-1, alpha, beta, total, init_hash, trans_dict, transpositions, ordered_moves, first = False)[0]
            if childScore>value:
                value=childScore
                nextMove=m
            alpha = max(alpha, value)
            if alpha >= beta:
                break #β cut-off
        return (value,nextMove)
    else:
        value=float("inf")
        for m in moves:
            childScore=alphabeta(state.result(m), depth-1, alpha, beta, total, init_hash, trans_dict, transpositions, ordered_moves, first = False)[0]
            if childScore<value:
                value=childScore
                nextMove=m
            beta = min(beta, value)
            if alpha >= beta:
                break #α cut-off
        return (value,nextMove)



def main():
    i = 0
    while True:
        if i % 2 == 0:
            if i == 0:
                state= ChessState(chess.Board('r1bqkb1r/pp1ppppp/5n2/8/2PQ4/8/PP2PPPP/RNB1KB1R w KQkq - 1 6'))
            total = 0
            transpositions = 0
            trans_dict = {}
            init_hash = state.zobrist_init_hash()
            moves = shallow_search(state)
            opening_book = chess.polyglot.MemoryMappedReader('/Users/lorenzo/Documents/performance.bin')
            t = time.time()
            try:
                computer_move = opening_book.choice(state.board).move
                state = state.result(computer_move)
                print(colored('still theory!', 'red'))
            except:
                if state.get_phase() == 'tablebase':
                    computer_move = state.tablebase()
                    state = state.result(computer_move)
                else:
                    computer_move = alphabeta(state,4,float("-inf"),float("inf"), total, init_hash, trans_dict, transpositions, moves, first = True)[1]
                    state = state.result(computer_move)
            state.print()
            #print(colored(str(total)+" nodes examined", 'yellow'))
            #print(colored(str(transpositions)+' transpositions', 'green'))
            print(colored('the computer played: '+ str(computer_move), 'yellow'))
            print(colored('the search took ' +str(float(round(time.time()-t, 3))) + ' seconds', 'blue'))
            i+=1
        elif i % 2 == 1:
            player_move = str(input('your move? ')) 
            if player_move == 'exit':
                break
            player_move = chess.Move.from_uci(player_move)            
            while not state.board.is_legal(player_move):
                print(colored('invalid move!', 'red'))
                player_move = chess.Move.from_uci(str(input('your move? ')))
            state.board.push(player_move)
            if state.board.is_game_over():
                print(colored('THE GAME IS OVER!', 'red'))
                break
            i+=1


if __name__ == '__main__':
    #cProfile.run('main()')
    main()


