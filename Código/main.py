from Simulation import Simulation
from PlotTool import PlotTool
import numpy as np
import scipy.io.wavfile as wav
import easygui


def main():
	orden = 10
	fs, x = wav.read(easygui.fileopenbox())
	x = x / 2.0 ** 15  # Normalizo la entrada porque esta como bytes enteros
	#x = np.array([0.5*np.sin(2*3.142*i * 400/44100.0) for i in range(661500)])
	print("Simulation Started")

	sim = Simulation(x, fs, 10)
	sim.approximateS(1, showEstimation=False)  # 10 Segundos para estimar S
	en, test = sim.simulate()

	wav.write("out.wav", fs, np.array(en * 2.0 ** 15, dtype='int16'))
	wav.write("inp.wav", fs, np.array(x * 2.0 ** 15, dtype='int16'))

	# Ploteo la salida
	graphics = PlotTool()
	graphics.plot(x, en, fs)


if __name__ == "__main__":
	main()
