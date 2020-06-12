import random


class SFilter:
	def __init__(self, L):
		self.Num = []
		self.L = L
		self.M = 2
		random.seed()
		for i in range(L):
			self.Num.append(0.5)
		self.prevValues = []
		for i in range(self.M):
			self.prevValues.append(0)
		return

	def getOutput(self, x):
		# Le aplica una Transferencia de H(z)=1/(1+gz^-M)

		y = []
		for i in range(len(x)):
			y.append(0)
		g = 0.5
		y_tot = self.prevValues

		for n in range(len(x)):
			y[n] = x[n] - g * y_tot[n] - 0.3 * y_tot[n+1]
			y_tot.append(y[n])
		self.prevValues = []
		for i in range(self.M):
			self.prevValues.append(y[len(y) - self.M + i])	#Si tengo y=[y1,y2,y3,y4,...,y10] agarro los ultimos M valores
															#pej, si M = 2 entonces prevValues=[y8,y9,y10]
		return y

	def detCoefs(self):
		return self.Num
