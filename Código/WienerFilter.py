from FXLMS import FXLMS
import random


#
# class WienerFilter:
# 	def __init__(self, N):
# 		self.N = N
# 		self.fxlms = FXLMS(1e-3, N)
# 		self.a = []
# 		self.prevValues = []
# 		random.seed()
# 		for n in range(N):
# 			if n != N - 1:
# 				self.a.append(0)
# 			else:
# 				self.a.append(0)
# 			self.prevValues.append(0)
# 		return
#
# 	def getOutput(self, inp):
# 		output = []
# 		totalInp = self.prevValues + inp
# 		for n in range(len(inp)):
# 			temp = 0
# 			for i in range(1, self.N):
# 				temp = temp + self.a[i] * totalInp[self.N-i]
# 			output.append(self.a[0] * inp[n] + temp)
# 		self.prevValues = []
# 		for i in range(self.N):
# 			self.prevValues.append(inp[i])
# 		return output
#
# 	def updateCoefs(self, signal, error):
# 		self.a = self.fxlms.calcNewCoef(self.a, signal, error)
# 		return

class WienerFilter:
	def __init__(self, N):  # N es el orden del filtro de wiener
		self.N = N
		self.a = []
		self.prevValues = []
		for i in range(self.N):
			self.a.append(0)
			self.prevValues.append(0)
		return

	def getOutput(self, x):  # Recibe un input de L cantidad de valores
		L = len(x)
		y = []
		x_tot = self.prevValues + x
		for n in range(len(x)):
			temp = 0
			for i in range(1, len(self.a) - 1):
				temp = temp + x_tot[n - i] * self.a[i]
			y[n] = self.a[0] * x[n] + temp
		self.prevValues = []
		for i in range(self.N):
			self.prevValues.append(x[L - 1 - self.N + i])
		return y

	def updateCoefs(self, signal, error):
		return
