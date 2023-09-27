import numpy as np
import chess

def bitboards_to_array(bb: np.ndarray) -> np.ndarray:
    bb = np.asarray(bb, dtype=np.uint64)[:, np.newaxis]
    s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
    b = (bb >> s).astype(np.uint8)
    b = np.unpackbits(b, bitorder="little")
    return b.reshape(-1, 64)

def bitboard(board):
	black, white = board.occupied_co
	bitboards = np.array([
    black & board.pawns,
    black & board.knights,
    black & board.bishops,
    black & board.rooks,
    black & board.queens,
    black & board.kings,
    white & board.pawns,
    white & board.knights,
    white & board.bishops,
    white & board.rooks,
    white & board.queens,
    white & board.kings,
	], dtype=np.uint64)
	return bitboards