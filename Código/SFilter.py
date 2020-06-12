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
		y = []
		for i in range(len(x)):
			y.append(0)
		g = 0.5
		x_tot = self.prevValues + x

		for n in range(len(x)):
			y[n] = x[n] + g * x_tot[0]
		self.prevValues = x
		return y

	def detCoefs(self):
		return self.Num
