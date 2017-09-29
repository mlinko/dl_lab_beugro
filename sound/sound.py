import pyaudio
import wave
import sys
import os.path
import time
import numpy as np
import pylab

'''
It has turned put my microphone doenst really work, pyaudio
and neither the sounddevice module cannot detect it. 
The ALSA package works neither.

This script can play a .waw file, also could plot it, but it
is very slow. I could not solve the problem properly, but I
really worked with it.

The monitor.html includes a little JS script that refreshes
the output picture of the plots.
'''

CHUNK = 512

def plotSound(data):
	#data = np.fromstring(dataIn, dtype=np.int16)
	pylab.plot(data)
	pylab.title('Sound')
	pylab.grid()
	pylab.axis([0,len(data), -2**16/2, 2**16/2])
	pylab.savefig("kep.png", dpi=50)
	pylab.close('all')

def play_wav(wav_filename, chunk_size=CHUNK):
	'''
	Play (on the attached system sound device) the WAV file
	named wav_filename.
	'''

	try:
		print 'Trying to play file ' + wav_filename
		wf = wave.open(wav_filename, 'rb')
	except IOError as ioe:
		sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
		str(ioe) + '. Skipping.\n')
		return
	except EOFError as eofe:
		sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
		str(eofe) + '. Skipping.\n')
		return

	# Instantiate PyAudio.
	p = pyaudio.PyAudio()

	# Open stream.
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
		channels=wf.getnchannels(),
		rate=wf.getframerate(),
					output=True)

	data = wf.readframes(chunk_size)

	while len(data) > 0:
		data = np.fromstring(data, dtype=np.int16)
		stream.write(data)
		#plotSound(data)
		maxesnp.max(np.abs(data))
		data = wf.readframes(chunk_size)

	# Stop stream.
	stream.stop_stream()
	stream.close()

	# Close PyAudio.
	p.terminate()

def usage():
	prog_name = os.path.basename(sys.argv[0])
	print "Usage: {} filename.wav".format(prog_name)
	print "or: {} -f wav_file_list.txt".format(prog_name)

def main():
	lsa = len(sys.argv)
	if lsa < 2:
		usage()
		sys.exit(1)
	elif lsa == 2:
		play_wav(sys.argv[1])
	else:
		if sys.argv[1] != '-f':
			usage()
			sys.exit(1)
		with open(sys.argv[2]) as wav_list_fil:
			for wav_filename in wav_list_fil:
				# Remove trailing newline.
				if wav_filename[-1] == '\n':
					wav_filename = wav_filename[:-1]
				play_wav(wav_filename)
				time.sleep(3)

if __name__ == '__main__':
	main()

