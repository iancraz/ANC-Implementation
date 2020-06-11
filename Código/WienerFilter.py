import FXLMS
import random


class WienerFilter:
	def __init__(self, N):
		self.N = N
		self.fxlms = FXLMS(0.5, N)
		self.a = []
		random.seed()
		for n in range(N):
			self.a.append(random.randint(-1, 1))
		return

	def getOutput(self, inp):
		output = []
		for n in range(len(inp)):
			temp = 0
			for i in range(self.N):
				if n > i:
					temp = temp - output[n - i - 1] * self.a[self.N - i - 1]
			output.append((-inp[n] + temp) / self.a[self.N])
		return output

	def updateCoefs(self, signal, error):
		self.a = self.fxlms.calcNewCoef(self.a, signal, error)
		return
