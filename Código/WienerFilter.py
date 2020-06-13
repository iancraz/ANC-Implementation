from FXLMS import FXLMS
import numpy as np


class WienerFilter:
	def __init__(self, N, alpha):  # N es el orden del filtro de wiener
		self.N = N
		self.a = np.zeros(N)
		self.alpha = alpha
		self.fxlms = FXLMS(self.alpha)
		self.prevValues = np.zeros(N)
		self.counter = 0
		self.X = None
		return

	def getOutput(self, x):  # Recibe un input de L cantidad de valores
		L = len(x)
		y = np.ndarray(L)
		x_tot = np.concatenate((self.prevValues, x))  # x_tot tiene los N valores previos a la entrada guardados
		self.X = x_tot  # Guardo esto para usar en otras funciones
		# Calculo la salida
		# Creo que esto anda bien
		# y(n) = (-1)*(a_0 x(n) + a_1 x(n-1) + ...)
		for n in range(L):
			temp = 0
			n_tot = n + self.N
			for i in range(1, len(self.a)):
				if n_tot > i:
					temp = temp - x_tot[n_tot - i] * self.a[i]
			y[n] = - self.a[0] * x[n] + temp
			if y[n] > 2:
				y[n] = 2
			elif y[n] < -2:
				y[n] = -2
		for i in range(self.N):
			self.prevValues[i] = x[L - self.N + i]
		return y

	def updateCoefs(self, signal, error_n):
		# Mando a=[a_0,a_1,a_2,...] y signal=[x(n),x(n-1),...,x(n-N)]
		if self.alpha > 1e-6:
			self.a = self.fxlms.calcNewCoef(self.a, signal, error_n, self.alpha)
		return

	def update(self, error, sfilter=None):
		if sfilter is not None:
			x_tot = sfilter.getOutput(self.X)
		else:
			x_tot = self.X
		signal = np.ndarray(self.N)
		for n in range(len(error)):
			for i in range(self.N):
				signal[i] = x_tot[n + self.N - i]
			# Cargo los valores previos para mandar al algoritmo
			# Osea para actualizar los coeficientes en n, necesito
			# x(n), x(n-1), x(n-2), ..., x(n-N), siendo M la cantidad
			# de coeficientes.
			# signal = [x(n), x(n-1), ... , x(n-N)]
			self.updateCoefs(signal, error[n])
		return

	def updateAlpha(self, decreace):
		if decreace:
			self.alpha = self.alpha / 2.0
		elif self.alpha:
			self.alpha = self.alpha * 2.0
		return

	def resetPrevValues(self):
		self.prevValues = np.zeros(self.N)
		self.X = None
		return
