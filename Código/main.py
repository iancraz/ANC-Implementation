from WienerFilter import WienerFilter
from SFilter import SFilter
import numpy as np


def main():

	x_n = []
	for i in range(10):
		x_n.append(np.sin(2 * 3.1419 * 10 * i))
	wfilter = WienerFilter(10)
	sfilter = SFilter(10)
	for i in range(100):
		inp = []
		for u in range(10):
			inp.append(x_n[u + i * 10])
		outWiener = wfilter.getOutput(inp)
		outS = sfilter.getOutput(outWiener)
		out = []
		for u in range(len(inp)):
			out.append(outS[u] + inp[u])
		wfilter.updateCoefs(inp, out)


if __name__ == "__main__":
	main()