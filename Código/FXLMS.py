class FXLMS:
	def __init__(self, alpha, N):
		self.alpha = alpha
		self.N = N
		return

	def calcNewCoef(self, prevCoefs, signal, error):
		newCoefs = []
		if len(prevCoefs) != len(signal) or len(signal) != len(
				error):  # Creo que prevCoefs deberia ser de 1+len(signal), CHEQUEAR
			raise NameError('Las longitudes de signal, error y prevCoefs no coinciden')
		for i in range(len(prevCoefs)):
			newCoefs.append(prevCoefs[i] + self.alpha * 2 * error[i] * signal[i])
		return newCoefs
