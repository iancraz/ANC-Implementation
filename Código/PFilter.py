import numpy as np


class PFilter:
	# Se supone que es un Filtro FIR, por lo tanto, tiene una transferencia
	#	H(z)= Pol(z^-1)
	def __init__(self):
		self.order = 4  # Orden del polinomio de la H
		self.prevValues = np.zeros(self.order)
		return

	def getOutput(self, x):
		x_tot = np.concatenate((self.prevValues, x))
		y = np.zeros(len(x))
		for m in range(len(y)):
			n = m + len(self.prevValues)
			y[m] = x_tot[n] + 0.5 * x_tot[n - 1] + 0.25 * x_tot[n - 2] + 0.125 * x_tot[n - 3] + 0.01 * x_tot[n - 4]
		for i in range(self.order):
			self.prevValues[i] = x[len(x) - self.order + i]
		return y

	def resetPrevValues(self):
		self.prevValues = np.zeros(self.order)
		return
