import chess

def num_squares_controled(board, whiteToMove):
	if whiteToMove:
		color = chess.WHITE
	else:
		color = chess.BLACK
	total = 0
	for i in range(64):
		attacked = board.is_attacked_by(color, i)
		if attacked:
			total += 1
	return total

def center_control(board, whiteToMove):
	if whiteToMove:
		color = chess.WHITE
	else:
		color = chess.BLACK
	total = 0
	center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
	for square in center_squares:
		if len(list(board.attackers(color, square))) > 0:
			total += len(list(board.attackers(color, square)))
	return total

def pawns_center(board, whiteToMove):
	center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
	total = 0
	if whiteToMove:
		for square in center_squares:
			try:
				if board.piece_at(square).symbol() == 'P':
					total += 1
			except:
				continue
	else:
		for square in center_squares:
			try:
				if board.piece_at(square).symbol() == 'p':
					total += 1
			except:
				continue
	return total



