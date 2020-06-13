import numpy as np


class SFilter:
	def __init__(self):
		self.M = 2
		self.prevValues = np.zeros(self.M)
		return

	def getOutput(self, x):
		# Le aplica una Transferencia de H(z)=1/(1+gz^-M)

		y = np.ndarray(len(x))
		g = 0.5
		y_tot = np.append(self.prevValues, np.ndarray(len(x)))

		for n in range(len(x)):
			y[n] = x[n] - g * y_tot[n] - 0.3 * y_tot[n + 1]
			y_tot[n+self.M] = y[n]
		for i in range(self.M):
			self.prevValues[i] = y[len(y) - self.M + i]
		# Si tengo y=[y1,y2,y3,y4,...,y10] agarro los ultimos M valores
		# pej, si M = 3 entonces prevValues=[y8,y9,y10]
		return y

	def resetPrevValues(self):
		self.prevValues = np.zeros(self.M)
		return