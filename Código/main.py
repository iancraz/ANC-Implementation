from WienerFilter import WienerFilter
from SFilter import SFilter
from PFilter import PFilter
import numpy as np
import matplotlib.pyplot as plt
import librosa
import time
from tqdm import tqdm


def main():
	fs = 44100
	x_n, fs = librosa.load("test3.wav", sr=fs)
	en = np.ndarray(len(x_n))
	wfilter = WienerFilter(10)
	sfilter = SFilter(10)
	pfilter = PFilter()
	for i in tqdm(range(int(len(x_n) / 10))):
		inp = np.ndarray(10)
		for u in range(10):
			inp[u] = x_n[u + i * 10]
		# La interconexión de modulos la hago como en la figura 16.6 de la pag. 556 del libro Farhang
		xprim = sfilter.getOutput(inp)
		yn = wfilter.getOutput(xprim)
		dn = pfilter.getOutput(inp)
		error = np.ndarray(len(inp))
		for u in range(len(inp)):
			error[u] = dn[u] + yn[u]
			en[u + i * 10] = error[u]
		wfilter.update(error)

	# Ploteo la salida
	librosa.output.write_wav("out.wav", en, fs)


	plt.plot(x_n)
	plt.plot(en)
	plt.show()
	# print(wfilter.a)


if __name__ == "__main__":
	print("Simulation Started")
	start_time = time.time()
	main()
	end_time = (time.time() - start_time)
	print("Simulation Time: ", end_time, "seconds")
	print("Finished Simulating")
