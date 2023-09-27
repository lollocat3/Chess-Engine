from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import tensorflow as tf
import numpy as np
from tqdm import tqdm
from fen_to_bitboard import score

def load_data():
	X = np.load('/Users/lorenzo/Desktop/Python/Chess/processed_data/positions_data.npy')
	evals = np.load('/Users/lorenzo/Desktop/Python/Chess/processed_data/evaluation_data.npy')/100
	y = np.zeros((evals.shape[0], 2))
	for i in range(len(evals)):
		if evals[i] > 0:
			y[i][0] = 1
		elif evals[i] < 0:
			y[i][1] = 1
	for row in tqdm(X):
		elem = list(row)
		scor = score(elem)
		if elem[64] == 1:
			np.append(row, scor)
		else:
			np.append(row, -scor)
	return X, y

model = Sequential()

model.add(Dense(100, input_dim=69, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(2, activation='softmax'))

model.compile(optimizer = 'adam', metrics = ['accuracy'], loss='binary_crossentropy')

X, y = load_data()
X_training, X_test = X[:500000, :], X[500000:, :]
y_training, y_test = y[:500000], y[500000:]



model.fit(X_training, y_training, epochs = 3, batch_size = 10)

_, accuracy = model.evaluate(X_test, y_test)

print('Accuracy: %.2f' % (accuracy*100))

model.save('model_no_draws')

