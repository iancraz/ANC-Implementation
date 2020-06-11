from FXLMS import FXLMS
import random


class WienerFilter:
	def __init__(self, N):
		self.N = N
		self.fxlms = FXLMS(1e-3, N)
		self.a = []
		random.seed()
		for n in range(N):
			if n != N-1:
				self.a.append(0)
			else:
				self.a.append(10)
		return

	def getOutput(self, inp):
		output = []
		for n in range(len(inp)):
			temp = 0
			for i in range(self.N):
				if n > i:
					temp = temp - output[n - i - 1] * self.a[self.N - i - 1]
			output.append((-inp[n] + temp) / self.a[self.N-1])
		return output

	def updateCoefs(self, signal, error):
		self.a = self.fxlms.calcNewCoef(self.a, signal, error)
		return
