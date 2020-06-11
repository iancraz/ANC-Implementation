import random


class SFilter:
	def __init__(self, L):
		self.Num = []
		self.L = L
		random.seed()
		for i in range(L):
			self.Num.append(random.randint(1, 2))
		return

	def getOutput(self, inp):
		output = []
		for n in range(len(inp)):
			temp = 0
			for i in range(self.L):
				if n >= i:
					temp = temp + self.Num[self.L - i -1] * inp[n - i]
			output.append(temp)
		return output

	def detCoefs(self):
		return self.Num
