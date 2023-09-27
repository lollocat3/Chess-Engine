from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import tensorflow as tf
import numpy as np

def load_data():
	X = np.load('/Users/lorenzo/Desktop/Python/Chess/processed_data/positions_data.npy')
	evals = np.load('/Users/lorenzo/Desktop/Python/Chess/processed_data/evaluation_data.npy')/100
	y = np.zeros((evals.shape[0], 3))
	for i in range(len(evals)):
		if evals[i] > 0.5:
			y[i][0] = 1
		elif evals[i] < -0.5:
			y[i][1] = 1
		else:
			y[i][2] = 1 
	return X, y

model = Sequential()

model.add(Dense(100, input_dim=69, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))

model.compile(optimizer = 'adam', metrics = ['accuracy'], loss='binary_crossentropy')

X, y = load_data()
X_training, X_test = X[:500000, :], X[500000:, :]
y_training, y_test = y[:500000], y[500000:]



model.fit(X_training, y_training, epochs = 1, batch_size = 10)

_, accuracy = model.evaluate(X_test, y_test)

print('Accuracy: %.2f' % (accuracy*100))

