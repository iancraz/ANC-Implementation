from WienerFilter import WienerFilter
from SFilter import SFilter
from PFilter import PFilter
import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import scipy.io.wavfile as wav


def main():
	print("Simulation Started")
	start_time = time.time()
	orden = 10
	fs, x = wav.read("test3.wav")

	x = x / 2.0**15		# Normalizo la entrada porque esta como bytes enteros
	#x = np.array([0.5*np.sin(2*3.142*i * 400/44100.0) for i in range(661500)])
	print("File length: ", len(x))


	t = np.ndarray(len(x))
	for i in tqdm(range(len(x))):
		t[i] = 1 / fs * i
	en = np.ndarray(len(x))
	#test = np.ndarray(len(x))
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
			#test[u + i * orden] = yn[u]
		wfilter.update(error)


	end_time = (time.time() - start_time)
	print("Simulation Time: ", end_time, "seconds")
	print("File time length: ", len(x) / 44.1e3, "seconds")


	# Ploteo la salida
	wav.write("out.wav",fs,np.array(en * 2.0**15, dtype= 'int16'))
	wav.write("inp.wav", fs, np.array(x * 2.0 ** 15, dtype='int16'))
	plt.grid(which='both')
	plt.plot(t, x, 'k', label="Input")
	plt.plot(t, en, 'r', label="Output")
	#plt.plot(t, test, 'g', label="Test Probe")
	plt.xlabel("Time (s)")
	plt.ylabel("Aplitude (V)")
	plt.xlim(0, 15)
	plt.ylim(-1, 1)
	plt.legend()
	plt.show()


if __name__ == "__main__":
	main()
