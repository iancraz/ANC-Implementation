from WienerFilter import WienerFilter
from SFilter import SFilter
import numpy as np
import matplotlib.pyplot as plt


def main():
	x_n = []
	y_n = []
	for i in range(100000):
		x_n.append(np.sin(2 * 3.1419 * 1000 * i))
	wfilter = WienerFilter(10)
	sfilter = SFilter(10)
	for i in range(10000):
		inp = []
		for u in range(10):
			inp.append(x_n[u + i * 10])
		outWiener = wfilter.getOutput(inp)
		outS = sfilter.getOutput(outWiener)
		xprim = sfilter.getOutput(inp)
		out = []
		for u in range(len(inp)):
			out.append(inp[u] + outWiener[u])
			y_n.append(out[u])
			wfilter.updateCoefs(inp[u], out[u])
	print("hola")
	plt.plot(x_n)
	test = []
	for i in range(len(x_n)):
		test.append(x_n[i]-y_n[i])
	#plt.plot(test)
	plt.plot(y_n)
	plt.show()


if __name__ == "__main__":
	main()
