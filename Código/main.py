from WienerFilter import WienerFilter
from SFilter import SFilter
import numpy as np
import matplotlib.pyplot as plt


def main():
	x_n = []
	y_n = []
	for i in range(100000):
		x_n.append(np.sin(2 * 3.1419* 100 * i /44e3))
	wfilter = WienerFilter(10)
	sfilter = SFilter(10)
	for i in range(10000):
		inp = []
		for u in range(10):
			inp.append(x_n[u + i * 10])
		outWiener = wfilter.getOutput(inp)
		outS = sfilter.getOutput(outWiener)
		error = []
		for u in range(len(inp)):
			error.append(inp[u] - outS[u])
			y_n.append(error[u])
		wfilter.update(error)

	# Ploteo la salida

	plt.plot(x_n)
	plt.plot(y_n)
	plt.show()


if __name__ == "__main__":
	main()
