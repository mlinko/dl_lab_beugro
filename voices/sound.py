import numpy as np
import pyaudio
import datetime
import pylab
import wave

CHUNK = 1024
RATE = 44100

'''
This script can classify the input voice. It is not solved with neural network,
but later I would like to work on it a little more.
'''

def plotSound(data, spectre, freq):
	t1 = datetime.datetime.now()
	#data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
	pylab.plot(data)
	pylab.title(t1)
	pylab.grid()
	pylab.axis([0,len(data), -2**16/2, 2**16/2])
	pylab.savefig("kep.png", dpi=50)
	pylab.close('all')

	data_fft = abs(np.fft.fft(data).real)
	data_fft = data_fft[:int(len(data_fft))]
	pylab.plot(data_fft)
	pylab.title(t1)
	pylab.grid()
	pylab.axis(freq, spectre)
	pylab.savefig("kep2.png", dpi=50)
	pylab.close('all')
	print(t1)


def main():
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer = CHUNK)

	#df = wave.open('output.waw')

	#stream = p.open(format=pyaudio.get_format_from_width( wf.getsampwidth()),
	#                channels=wf.getnchannels(),
	#		rate=wf.getframerate(),
	#		input=True, frames_per_buffer = CHUNK)
	
	#stream = sd.InputStream(channels=1,samplerate=RATE,blocksize=CHUNK,dtype=np.int16)
	#stream.start()

	try:
		while True:
			#plotSound(stream)
			data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
			peak = np.average(np.abs(data))*2
			#absfft = np.abs(scipy.fftpack.fft(subdata))
			spectre = abs(np.fft.fft(data))
			freq = np.fft.fftfreq(data.size, 1.0/RATE)
			mask = freq>0
			spectre = spectre[mask]
			freq = freq[mask]
			maxfreq = freq[spectre == max(spectre) ]
			if peak <= 1500:
				volume = 'Whispering'
			else:
				volume = 'Talking   '
			if maxfreq < 336:
				voiceHeight = 'Low   '
			elif maxfreq < 987:
				voiceHeight = 'Normal'
			else:
				voiceHeight = 'High  '
			bars = "#" * int(50*peak/2**16)
			print( "%s,\t%s"%( volume, voiceHeight))
			#print( "%05d  \t\t %s"%( peak, bars, volume))
			#print(maxfreq, '\t', peak)
	except KeyboardInterrupt:
#		plotSound(data, spectre, freq)
		stream.close()
		print('Program has terminated succesfully')

if __name__ == '__main__':
	main()

