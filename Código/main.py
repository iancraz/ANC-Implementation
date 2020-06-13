from Simulation import Simulation
from PlotTool import PlotTool
import numpy as np
import time
import scipy.io.wavfile as wav


def main():
	orden = 10
	fs, x = wav.read("test3.wav")
	x = x / 2.0 ** 15  # Normalizo la entrada porque esta como bytes enteros
	# x = np.array([0.5*np.sin(2*3.142*i * 400/44100.0) for i in range(661500)])
	print("File length: ", len(x))

	print("Simulation Started")
	start_time = time.time()

	sim = Simulation(x, fs, 10)
	en, test = sim.simulate()
	
	end_time = (time.time() - start_time)
	print("Simulation Time: ", end_time, "seconds")
	print("File time length: ", len(x) / 44.1e3, "seconds")

	wav.write("out.wav", fs, np.array(en * 2.0 ** 15, dtype='int16'))
	wav.write("inp.wav", fs, np.array(x * 2.0 ** 15, dtype='int16'))

	# Ploteo la salida
	graphics = PlotTool()
	graphics.plot(x, en, fs)


if __name__ == "__main__":
	main()
