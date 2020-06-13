import numpy as np


class FXLMS:
	def __init__(self, alpha):
		self.alpha = alpha
		return

	def calcNewCoef(self, a_n, signal, error_n, alpha):
		self.alpha = alpha
		return a_n + 2 * self.alpha * signal * error_n
