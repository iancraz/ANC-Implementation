from WienerFilter import WienerFilter
from SFilter import SFilter
from PFilter import PFilter
import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm

class Simulation:
	def __init__(self,input,fs,order):
		self.x = input
		self.fs = fs
		self.orden = order
		self.en = np.ndarray(len(self.x))
		self.wfilter = WienerFilter(self.orden)
		self.sfilter = SFilter(self.orden)
		self.pfilter = PFilter()
		return

	def simulate(self):
		test = np.ndarray(len(self.x))
		error = np.ndarray(self.orden)
		inp = np.ndarray(self.orden)
		for i in tqdm(range(int(len(self.x) / self.orden))):
			# for i in range(int(len(x_n) / 10)):
			for u in range(self.orden):
				inp[u] = self.x[u + (i * self.orden)]

			# La interconexión de modulos la hago como en la figura 16.6 de la pag. 556 del libro Farhang
			xprim = self.sfilter.getOutput(inp)
			yn = self.wfilter.getOutput(xprim)
			dn = self.pfilter.getOutput(inp)
			error = dn + yn
			for u in range(len(inp)):
				self.en[u + i * self.orden] = error[u]
			test[u + i * self.orden] = yn[u]
			self.wfilter.update(error)
		return self.en, test
