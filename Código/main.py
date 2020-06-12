from WienerFilter import WienerFilter
from SFilter import SFilter
from PFilter import PFilter
import numpy as np
import matplotlib.pyplot as plt
import librosa


def main():
	fs = 44100
	x_n, fs = librosa.load("test3.wav", sr=fs)
	en = []
	wfilter = WienerFilter(10)
	sfilter = SFilter(10)
	pfilter = PFilter()
	for i in range(int(len(x_n) / 10)):
		inp = []
		for u in range(10):
			inp.append(x_n[u + i * 10])
		# La interconexión de modulos la hago como en la figura 16.6 de la pag. 556 del libro Farhang
		xprim = sfilter.getOutput(inp)
		yn = wfilter.getOutput(xprim)
		dn = pfilter.getOutput(inp)
		error = []
		for u in range(len(inp)):
			error.append(dn[u] - yn[u])
			en.append(error[u])
		wfilter.update(error)

	# Ploteo la salida
	librosa.output.write_wav("out.wav", np.asarray(en), fs)
	plt.plot(x_n)
	plt.plot(en)
	plt.show()
	print(wfilter.a)


if __name__ == "__main__":
	main()
