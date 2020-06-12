from WienerFilter import WienerFilter
from SFilter import SFilter
from PFilter import PFilter
import numpy as np
import matplotlib.pyplot as plt
import librosa
import time
from tqdm import tqdm


def main():
	print("Simulation Started")
	start_time = time.time()
	fs = 44100
	orden = 10
	x, fs = librosa.load("test3.wav", sr=fs)
	# x = np.array([0.5*np.sin(2*3.142*i/44100.0) for i in range(661500)])
	print("File length: ", len(x))
	t = np.zeros(len(x))
	for i in tqdm(range(len(x))):
		t[i] = 1 / 44.1e3 * i
	en = np.ndarray(len(x))
	wfilter = WienerFilter(orden)
	sfilter = SFilter(orden)
	pfilter = PFilter()
	error = np.ndarray(orden)
	inp = np.ndarray(orden)
	for i in tqdm(range(int(len(x) / orden))):
		# for i in range(int(len(x_n) / 10)):
		for u in range(orden):
			inp[u] = x[u + (i * orden)]
		# La interconexión de modulos la hago como en la figura 16.6 de la pag. 556 del libro Farhang
		xprim = sfilter.getOutput(inp)
		yn = wfilter.getOutput(xprim)
		dn = pfilter.getOutput(inp)
		error = dn + yn
		for u in range(len(inp)):
			en[u + i * orden] = error[u]
		wfilter.update(error)
	end_time = (time.time() - start_time)
	print("Simulation Time: ", end_time, "seconds")
	print("File time length: ", len(x)/44.1e3)
	# Ploteo la salida
	librosa.output.write_wav("out.wav", en, fs)
	plt.grid(which='both')
	plt.plot(t, x, 'k', label="Input")
	plt.plot(t, en, 'r', label="Output")
	plt.xlabel("Time (s)")
	plt.ylabel("Aplitude (V)")
	plt.xlim(0, 15)
	plt.ylim(-1, 1)
	plt.legend()
	plt.show()


if __name__ == "__main__":
	main()
