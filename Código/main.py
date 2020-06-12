from WienerFilter import WienerFilter
from SFilter import SFilter
import numpy as np
import matplotlib.pyplot as plt
import librosa


def main():
	fs = 44100
	x_n, fs = librosa.load("test3.wav", sr=fs)
	y_n = []
	# for i in range(100000):
	#	x_n.append(np.sin(2 * 3.1419 *10* i /44e3))
	wfilter = WienerFilter(10)
	sfilter = SFilter(10)
	for i in range(int(len(x_n) / 10)):
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
	librosa.output.write_wav("out.wav", np.asarray(y_n), fs)
	plt.plot(x_n)
	plt.plot(y_n)
	plt.show()


if __name__ == "__main__":
	main()
