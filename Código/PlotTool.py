import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


class PlotTool:
	def __init__(self):
		return

	def plot(self, x, en, fs, test=None):
		t = np.ndarray(len(x))
		for i in range(len(x)):
			t[i] = 1 / fs * i
		plt.grid(which='both', linewidth=0.1, color='black')
		if test is not None:
			plt.plot(t, test, "r", label="Speaker Signal", linewidth=0.5)
		plt.plot(t, x, 'k', label="Input", linewidth=0.5)
		plt.plot(t, en, "#4d4d4d", label="Output", linewidth=0.5)
		plt.xlabel("Time (s)")
		plt.ylabel("Aplitude (V)")
		plt.xlim(0, t[-1])
		plt.legend()
		plt.show()
