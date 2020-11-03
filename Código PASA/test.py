import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from tqdm import tqdm
import scipy.io.wavfile as wav

np.random.seed(616)

class VSNLMS:
	def __init__(self, mu, mu_max, mu_min, m0, m1, alpha, delta=0.0):
		"""
		Funcion de inicialización del algoritmo VSNLMS
		@:param mu: Coeficiente de ajuste de paso inicial
		@:param mu_max: Maximo valor del coeficiente de paso (Los coeficientes se van ajustando a medida que se hacen
		iteraciones por el algoritmo VS-LMS)
		@:param mu_min: Mínimo valor del coeficiente de paso
		@:param m0_per: Cantidad de valores de gradiente que deben cambiar de signo para que se ajuste el mu. Esta cantidad
		viene dada porcentualmente del valor de N
		@:param m1_per: Cantidad de valores de gradiente que deben mantener signo para que se ajuste el mu. Esta cantidad
		viene dada porcentualmente del valor de N
		@:param alpha: parametro de ajuste del mu
		@:param delta: delta del algoritmo NLMS, esta puesto para asegurar que en el caso de que el denominador sea nulo no
		explote.
		"""
		self.mu = mu
		self.count_mu_values = 0
		self.mu_max = mu_max
		self.mu_min = mu_min
		self.alpha = alpha
		self.m0 = m0
		self.m1 = m1
		self.prev_sign = 0
		self.delta = delta
		self.prev_grad = []
		return

	def calcNewCoef(self, a_n, signal, error):
		"""
		Funcion que dados unos coeficientes previos, los actualiza correspondientemente
		:param a_n: Coeficientes a actualizar
		:param signal: Vector de señal de entrada
		:param error: Valor del error para actualizar los coeficientes
		:return: Vector de coeficientes actualizados formateados de la misma manera que a_n
		"""
		grad = np.array(signal) * error
		if len(self.prev_grad) != 0:
			if np.sum(np.sign(grad) != self.prev_grad) > self.m0 and self.mu > self.mu_min:
				self.mu /= self.alpha
			elif np.sum(np.sign(grad) == self.prev_grad) > self.m1 and self.mu < self.mu_max:
				self.mu *= self.alpha
		self.prev_grad = np.sign(grad)
		return a_n + self.mu * grad / (np.dot(signal, signal) + self.delta)  # NLMS

	def getMu(self):
		"""
		Funcion para obtener el mu actual del algoritmo
		:return: mu actual.
		"""
		return self.mu

class AdaptativeFilter:
	def __init__(self, N, mu=1e-3, mu_max=1.1, mu_min=1e-9, m0_per=0.9, m1_per=0.9, alpha=10, delta=0.0):
		"""
		Funcion de inicializacion del filtro adaptativo
		@:param N: Es el orden del filtro
		@:param mu: Coeficiente de ajuste de paso inicial
		@:param mu_max: Maximo valor del coeficiente de paso (Los coeficientes se van ajustando a medida que se hacen
		iteraciones por el algoritmo VS-LMS)
		@:param mu_min: Mínimo valor del coeficiente de paso
		@:param m0_per: Cantidad de valores de gradiente que deben cambiar de signo para que se ajuste el mu. Esta cantidad
		viene dada porcentualmente del valor de N
		@:param m1_per: Cantidad de valores de gradiente que deben mantener signo para que se ajuste el mu. Esta cantidad
		viene dada porcentualmente del valor de N
		@:param alpha: parametro de ajuste del mu
		@:param delta: delta del algoritmo NLMS, esta puesto para asegurar que en el caso de que el denominador sea nulo no
		explote.
		"""
		self.N = N
		self.w = np.random.randn(N)
		self.mu = mu
		m0 = m0_per * N
		m1 = m1_per * N
		self.vsnlms = VSNLMS(self.mu, mu_max, mu_min, m0, m1, alpha, delta)
		self.inp_signal = list(np.zeros(N))
		self.err = 1
		return

	def fit(self, input, desired):
		"""
		Funcion que actualiza los pesos de un filtro adaptativo para que se ajusten a la respuesta deseada.
		@:param input: Vector de entrada al filtro adaptativo
		@:param desired: Vector de señal deseada del filtro adaptativo.
		"""
		self.inp_signal = list(np.zeros(self.N))
		self.err = 1
		for x, d in tqdm(zip(input, desired)):
			self.inp_signal.append(x)
			self.inp_signal.pop(0)
			self.err = d - np.dot(self.inp_signal, self.w)  # Esta definido de esta manera
			self.updateLMS()
		return

	def getFilterParameters(self):
		"""
		Función que devuelve los parámetros del filtro adaptativo
		@:return Los coeficientes del filtro
		"""
		return np.flip(self.w)

	def updateLMS(self):
		"""
		Función que actualiza los coeficientes del filtro adaptativo, utiliza los vectores self.inp_signal, sel.w, y el valor
		self.err
		"""
		self.w = self.vsnlms.calcNewCoef(self.w, self.inp_signal, self.err)
		return

	def getMu(self):
		"""
		Devuelve el Mu actual del filtro adaptativo
		@:return mu Actual
		"""
		return self.vsnlms.getMu()

	def applyFilterSame(self, input):
		"""
		Aplica el filtro adaptativo obtenido a un vector de entrada
		@:param input: vector de entrada para aplicar el filtro. (IMPORTANTE: No actualiza self.inp_signal)
		@:return Vector de salida del filtro.
		"""
		return signal.convolve(input, np.flip(self.w), mode="same")  # No esta chequeado que vaya el modo same

	def applyFilterFull(self, input):
		"""
		Aplica el filtro adaptativo obtenido a un vector de entrada
		@:param input: vector de entrada para aplicar el filtro. (IMPORTANTE: No actualiza self.inp_signal)
		@:return Vector de salida del filtro.
		"""
		return signal.convolve(input, np.flip(self.w), mode="full")  # No esta chequeado que vaya el modo same

	def resetInput(self):
		"""
		Función que borra los datos de self.inp_signal y los setea todos en cero
		"""
		self.inp_signal = list(np.zeros(self.N))
		return

	def applyFilterToTap(self, tap):
		"""
		Funcion que aplica el filtro adaptativo a un solo tap de entrada, utiliza los valores previos guardados en self.inp_signal
		y actualiza ese vector (IMPORTATNE: Actualiza los valores de self.inp_signal)
		@:param tap: Valor del tap de entrada a aplicar el filtro
		@:return Valor de salida del filtro adaptativo
		"""
		self.inp_signal.append(tap)
		self.inp_signal.pop(0)
		temp = self.applyFilterFull(self.inp_signal)
		temp2 = temp[self.N - 1]
		return temp2

	def fitFilterWithErrorTap(self, input_vector, e_tap):
		"""
		Funcion que actualiza los valores de los coeficientes del filtro adaptativo dado un tap de señal de error.
		(IMPORTANTE: La señal self.inp_signal debe estar previamente actualizada al tap de entrada correspondiente a e_tap).
		@:param input_vector: Vector de entrada al filtro para actualizar los coeficientes
		@:param e_tap: Es un tap de la señal de error medida.
		"""
		self.err = e_tap
		self.w = self.vsnlms.calcNewCoef(self.w, input_vector, self.err)
		return

	def fitFilterWithDesired(self,d_tap):
		"""
		Funcion que actualiza los coeficientes del filtro con un tap actual de la señal deseada
		(IMPORTANTE: self.inp_signal debe estar previamente cargada con el tap de entrada actual).
		:param d_tap: tap de la señal deseada
		"""
		self.err = d - np.dot(self.inp_signal, self.w)
		self.updateLMS()
		return

	def setInputVector(self, input):
		"""
		Funcion que setea el input vector desde afuera.
		:param input: Vector de input para actualizar el filtro adaptativo
		"""
		if len(input) != self.N:
			raise Exception(f"No coinciden el tamaño del filtro {self.N} con el input vector metido {len(input)}")
		self.inp_signal = input
		return

class Filter:
	def __init__(self,coefs):
		"""
		Funcion para inicializar el filtro con una lista de coeficientes dada
		:param coefs: Coeficientes del filtro a inicializar deben estar dados de la siguiente manera:
			[w0,w1,w2,w3,..wN]
		"""
		self.coefs = coefs
		return

	def applyFilter(self, input):
		"""
		Funcion para aplicar el filtro a una señal de entrada dada
		:param input: Vector de señal de entrada, con el valor mas reciente ubicado a derecha, y el valor mas viejo a
		izquierda.
		:return: Vector de la señal de salida, filtrada.
		"""
		return signal.convolve(input, self.coefs, mode="full")

	def getFilterLen(self):
		"""
		Funcion que devuelve la cantidad de parámetros del filtro.
		:return:
		"""
		return len(self.coefs)

	def getCoefs(self):
		"""
		Funcion que devuelve una lista con los coeficientes del filtro.
		:return: Lista con los coeficientes del filtro.
		"""
		return self.coefs



filter_size = 30
# Defino el filtro S2
#s2 = Filter(np.random.rand(50))
#s2 = Filter([1,0.5,0.5,0.5])
t = np.linspace(0,-10,6)
signs = np.array([(-1)**n for n in range(6)])
temp = np.power(np.e,t)*signs
temp /= np.sum(temp)
s2 = Filter(temp)
# Defino el filtro P
#p = Filter(np.random.rand(50))
#p = Filter([1,0.4,0.3,0.2])
t = np.linspace(0,-10,30)
signs = np.array([(-1)**n for n in range(30)])
temp = np.power(np.e,t)*signs
temp /= np.sum(temp)
p = Filter(temp)
# Estimo el filtro S2
# 1ro Envio al parlante Ruido Blanco gaussiano y mido cuando me mide el error mic

muestras = 100000
wgn = np.random.randn(muestras)
#error_mic = apply_filter(wgn, s2)
error_mic = s2.applyFilter(wgn)

s2_estimation = AdaptativeFilter(filter_size, 1e-2, 1, 1e-20, 1, 1, 10, 1e-5)
# Obtengo la estimacion del filtro S2
s2_estimation.fit(wgn, error_mic)
# Se puede observar que se estrima perfectamente bien
print(s2.getCoefs()[0:4])
print(s2_estimation.getFilterParameters()[0:4])

# Defino la entrada a mi sistema para suprimir
epoch = filter_size
fs = 48000
time = 1
muestras = time * fs
epochs = muestras // epoch

#x = np.random.randn(muestras)
#t = np.linspace(0, 1, 100000)
#x = np.sin(2*np.pi*5*t)
fs, x = wav.read("./factoryfan.wav")
x = x / np.max(np.abs(x))

# Creo el filtro adaptativo
adapt_filter = AdaptativeFilter(filter_size,mu=1e-2, mu_max=1e-1, mu_min=1e-10, m0_per=1, m1_per=1, alpha=1.1, delta=1e-15)
# Filtro la entrada por P
#desired = apply_filter(x, p)
desired = p.applyFilter(x)
x_prim = s2_estimation.applyFilterFull(x)

w_out = list(np.zeros(filter_size))
xp_vector = list(np.zeros(filter_size))

error = []
y = []

for i in tqdm(range(len(x))):
	inp = x[i]
	d = desired[i]
	xp = x_prim[i]
	xp_vector.append(xp)
	xp_vector.pop(0)

	w_out.append(adapt_filter.applyFilterToTap(inp))
	w_out.pop(0)

	#temp = apply_filter(w_out, s2)
	temp = s2.applyFilter(w_out)
	y_n = temp[filter_size - 1]
	error_mic = d + y_n
	if i <= 48000*7:
		adapt_filter.fitFilterWithErrorTap(xp_vector, -error_mic)
	error.append(error_mic)
	y.append(y_n)

print("El mu final fue de: ", adapt_filter.getMu())
print("Los coeficientes del filtro son: ", adapt_filter.getFilterParameters())
plt.plot(-1*desired[0:len(y)])
plt.plot(y)
plt.show()

plt.plot(x)
plt.plot(error)
plt.show()

#espectro = np.fft.fft(error)
#frecuencia = np.fft.fftfreq(len(error),d= 1/fs)
#plt.semilogx(frecuencia,espectro)


wav.write("out.wav", fs, np.array(np.array(error) * 2.0 ** 15, dtype='int16'))
