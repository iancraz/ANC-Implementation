class SFilter:
	def __init__(self, L):
		self.M = 2
		self.prevValues = [0 for i in range(self.M)]
		return

	def getOutput(self, x):
		# Le aplica una Transferencia de H(z)=1/(1+gz^-M)

		y = [0 for i in x]
		g = 0.5
		y_tot = self.prevValues

		for n in range(len(x)):
			y[n] = x[n] - g * y_tot[n] - 0.3 * y_tot[n + 1]
			y_tot.append(y[n])
		self.prevValues = []
		for i in range(self.M):
			self.prevValues.append(y[len(y) - self.M + i])
		# Si tengo y=[y1,y2,y3,y4,...,y10] agarro los ultimos M valores
		# pej, si M = 2 entonces prevValues=[y8,y9,y10]
		return y
