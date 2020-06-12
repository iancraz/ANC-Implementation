from FXLMS import FXLMS


class WienerFilter:
	def __init__(self, N):  # N es el orden del filtro de wiener
		self.N = N
		self.a = []
		self.fxlms = FXLMS(5e-2)
		self.prevValues = []
		for i in range(self.N):
			self.a.append(0)
			self.prevValues.append(0)
		return

	def getOutput(self, x):  # Recibe un input de L cantidad de valores
		L = len(x)
		y = []
		for i in range(len(x)):
			y.append(0)
		x_tot = self.prevValues + x  # x_tot tiene los N valores previos a la entrada guardados
		self.X = x_tot  # Guardo esto para usar en otras funciones
		# Calculo la salida
		# Creo que esto anda bien
		# y(n) = a_0 x(n) + a_1 x(n-1) + ...
		for n in range(len(x)):
			temp = 0
			n_tot = n + self.N
			for i in range(1, len(self.a)):
				if n_tot > i:
					temp = temp + x_tot[n_tot - i] * self.a[i]
			y[n] = self.a[0] * x[n] + temp
		self.prevValues = []
		for i in range(self.N):
			self.prevValues.append(x[L - 1 - self.N + i])

		# Actualizo los valores de los coeficientes
		# Todavia no esta chequeado que esto ande
		signal = []
		for i in range(len(self.prevValues)):
			signal.append(0)

		# for n in range(len(y)):
		# 	for i in range(self.N):
		# 		signal[i] = x_tot[n + self.N - i]
		# 	# Cargo los valores previos para mandar al algoritmo
		# 	# Osea para actualizar los coeficientes en n, necesito
		# 	# x(n), x(n-1), x(n-2), ..., x(n-N), siendo M la cantidad
		# 	# de coeficientes.
		# 	# signal = [x(n), x(n-1), ... , x(n-N)]
		# 	self.updateCoefs(signal, y[n])
		return y

	def updateCoefs(self, signal, error_n):
		# Mando a=[a_0,a_1,a_2,...] y signal=[x(n),x(n-1),...,x(n-N)]
		self.a = self.fxlms.calcNewCoef(self.a, signal, error_n)
		return

	def update(self, error):
		signal = []
		for i in range(len(self.prevValues)):
			signal.append(0)

		for n in range(len(error)):
			for i in range(self.N):
				signal[i] = self.X[n + self.N - i]
			# Cargo los valores previos para mandar al algoritmo
			# Osea para actualizar los coeficientes en n, necesito
			# x(n), x(n-1), x(n-2), ..., x(n-N), siendo M la cantidad
			# de coeficientes.
			# signal = [x(n), x(n-1), ... , x(n-N)]
			self.updateCoefs(signal, error[n])
