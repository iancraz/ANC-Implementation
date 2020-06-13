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
		self.sfilter = SFilter()
		self.pfilter = PFilter()
		self.sApproxFiler = WienerFilter(self.orden, 1e-3)
		return

	def simulate(self):
		test = np.ndarray(len(self.x))
		print("Simulating ANC...")
		for i in tqdm(range(int(len(self.x) / self.orden))):
			inp = self.x[self.orden * i: self.orden * i + self.orden]

			xp = self.wfilter.getOutput(inp)
			yn = self.sfilter.getOutput(xp)
			dn = self.pfilter.getOutput(inp)
			error = dn + yn

			self.en[self.orden * i: self.orden * i + self.orden] = error
			test[self.orden * i: self.orden * i + self.orden] = xp
			self.wfilter.update(error, self.sApproxFiler)
		print("Finished Simulating ANC...")
		return self.en, test

	def approximateS(self, estimationTime, showEstimation=False):
		approximationTime = int(44.1e3 * estimationTime)
		x = np.array([0.5 * np.sin(2 * 3.142 * i * 400 / 44100.0) for i in range(approximationTime)])
		print("Estimating S Filter...")
		test = np.ndarray(len(x))
		for i in tqdm(range(int(len(x) / self.orden))):
			inp = x[self.orden * i: self.orden * i + self.orden]
			dn = self.sfilter.getOutput(inp)
			y = self.sApproxFiler.getOutput((-1) * inp)
			e = dn + y
			test[self.orden * i: self.orden * i + self.orden] = e
			self.sApproxFiler.update(e)
		print("Finished Estimating Filter")
		# print("Filter Parameters: ", self.sApproxFiler.a)
		if showEstimation:
			plot = PlotTool()
			plot.plot(x, test, 44.1e3)
		self.sApproxFiler.resetPrevValues()
		self.sfilter.resetPrevValues()
		return
