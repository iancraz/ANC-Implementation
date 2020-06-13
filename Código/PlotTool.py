import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


class PlotTool:
	def __init__(self):
		return

	def plot(self, x, en, fs, test= None):
		t = np.ndarray(len(x))
		for i in tqdm(range(len(x))):
			t[i] = 1 / fs * i
		plt.grid(which='both')
		plt.plot(t, x, 'k', label="Input")
		plt.plot(t, en, 'r', label="Output")
		if test != None:
			plt.plot(t, test, 'g', label="Test Probe")
		plt.xlabel("Time (s)")
		plt.ylabel("Aplitude (V)")
		plt.legend()
		plt.show()