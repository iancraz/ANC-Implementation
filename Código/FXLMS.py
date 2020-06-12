class FXLMS:
	def __init__(self, alpha):
		self.alpha = alpha
		return

	def calcNewCoef(self, a_n, signal, error_n):
		a_n1 = []
		if len(a_n) != len(signal):  # Creo que prevCoefs deberia ser de 1+len(signal), CHEQUEAR
			raise NameError('Las longitudes de signal  a_n no coinciden')
		for i in range(len(a_n)):
			a_n1.append(0)

		for i in range(len(a_n)):
			a_n1[i] = a_n[i] + 2 * self.alpha * signal[i] * error_n
		return a_n1
