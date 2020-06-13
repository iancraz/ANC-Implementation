import sys
sys.path.insert(1, 'C:/Users/Ian Diaz/Desktop/TP4---Investigacion/Código')
try:
	from Simulation import Simulation
	from PlotTool import PlotTool
	import numpy as np
	import scipy.io.wavfile as wav
	import easygui
except Exception as e:
    print("\nTHERE WAS AN ERROR PROCESSING YOUR REQUEST:", e, file=sys.stderr)
    input("Press Enter to exit...")
import warnings
warnings.filterwarnings("ignore")


def main():
	print("Choose a .wav file to simulate...")
	orden = 10
	fs, x = wav.read(easygui.fileopenbox())
	showEstimation = easygui.ynbox('Do you want to see the S filter estimation?', 'S Filter Estimator', ('Yes', 'No'))
	x = x / 2.0 ** 15  # Normalizo la entrada porque esta como bytes enteros
	if x[0].shape != ():  # Si es estereo solo agarro 1 canal
		x = x.transpose()[0]
	# x = np.array([0.5*np.sin(2*3.142*i * 400/44100.0) for i in range(661500)]) # Si le quiero meter una senoidal perfecta.
	print("Simulation Started")

	sim = Simulation(x, fs, 10)
	sim.approximateS(1, showEstimation=showEstimation)
	en, test = sim.simulate()

	wav.write("out.wav", fs, np.array(en * 2.0 ** 15, dtype='int16'))
	# Ploteo la salida
	plotResults = easygui.ynbox('Do you want to plot the ANC Results?', 'Results', ('Yes', 'No'))
	if plotResults:
		graphics = PlotTool()
		graphics.plot(x, en, fs, test= None)
	print("Output from the ANC out.wav has been created.")
	input("Press Enter to exit...")


if __name__ == "__main__":
	main()
