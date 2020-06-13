from WienerFilter import WienerFilter
from SFilter import SFilter
from PFilter import PFilter
import numpy as np
from PlotTool import PlotTool
from tqdm import tqdm


class Simulation:
	def __init__(self, inp, fs, order):
		self.x = inp
		self.fs = fs
		self.orden = order
		self.en = np.ndarray(len(self.x))
		self.wfilter = WienerFilter(self.orden, 1e-1)
		self.sfilter = SFilter(self.orden)
		self.pfilter = PFilter()
		self.sApproxFiler = WienerFilter(self.orden, 1e-3)
		return

	def simulate(self):
		test = np.ndarray(len(self.x))
		inp = np.ndarray(self.orden)
		print("Simulating ANC...")
		for i in tqdm(range(int(len(self.x) / self.orden))):
			# for i in range(int(len(x_n) / 10)):
			for u in range(self.orden):
				inp[u] = self.x[u + (i * self.orden)]
			xp = self.wfilter.getOutput(inp)
			yn = self.sfilter.getOutput(xp)
			dn = self.pfilter.getOutput(inp)
			error = dn + yn
			for u in range(len(inp)):
				self.en[u + i * self.orden] = error[u]
				test[u + i * self.orden] = xp[u]
			self.wfilter.update(error, self.sApproxFiler)
		print("Finished Simulating ANC...")
		return self.en, test

	def approximateS(self, estimationTime, showEstimation=False):
		approximationTime = int(44.1e3 * estimationTime)
		x = np.array([0.5 * np.sin(2 * 3.142 * i * 400 / 44100.0) for i in range(approximationTime)])
		print("Estimating S Filter...")
		test = np.ndarray(len(x))

		inp = np.ndarray(self.orden)
		for i in tqdm(range(int(len(x) / self.orden))):
			for u in range(self.orden):
				inp[u] = x[u + (i * self.orden)]
			dn = self.sfilter.getOutput(inp)
			y = self.sApproxFiler.getOutput(inp)
			e = dn + y
			for u in range(len(inp)):
				test[u + i * self.orden] = e[u]
			self.sApproxFiler.update(e)
		print("Finished Estimating")
		# print("Filter Parameters: ", self.sApproxFiler.a)
		if showEstimation:
			plot = PlotTool()
			plot.plot(x, test, 44.1e3)

		self.sApproxFiler.a = (-1)* self.sApproxFiler.a
		# Quito la inversión ya que necesito una copia exacta de S, no una invertida
		return
