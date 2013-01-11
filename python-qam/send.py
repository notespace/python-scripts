import pyaudio
import time
import sys
import math 
import random
import binascii

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

counter = 0

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    return (data, pyaudio.paContinue)

samplerate = 44100

stream = p.open(format=p.get_format_from_width(1),
                channels=1,
                rate=samplerate,
                output=True)

fstream = open('test.bin','wb')

twopi = math.pi * 2.0
freq = samplerate / 8000.0
ampl = 100.0
symbolrate = samplerate / 1000
buflen = 1024

noise = 20 # how much noise

# an initial carrier to sync with, 0.5 second
data = ""
#for i in xrange(samplerate/2):
#	data += chr(128 + int(math.sin(twopi * (counter % freq) / freq) * ampl))
#	counter += 1
#	if len(data) == buflen:
#		stream.write(data)
#		data = ""	
#stream.write(data)

counter = 0

dataToSend = binascii.hexlify("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce aliquet, dolor in consequat malesuada, libero eros suscipit urna, placerat varius augue mauris nec dui. Sed quam mauris, blandit convallis hendrerit vitae, iaculis sit amet sem. Integer vel dolor vitae magna tincidunt adipiscing in at nunc. Vivamus pharetra nibh ac metus vulputate tincidunt. In quis tristique nunc. Integer at est nec nisl feugiat dictum sit amet vehicula dui. Nam dignissim nibh quis nibh adipiscing molestie. Aenean ut ultricies sapien. Nulla ultrices justo id nulla sollicitudin aliquet. In auctor vestibulum mauris eget aliquet. Sed commodo felis tempus nisi convallis tincidunt.

Donec porttitor congue tellus, eget imperdiet ante vestibulum sed. Sed a ligula ligula, vitae volutpat felis. Ut varius dui eget dui pellentesque vitae fermentum sapien euismod. Fusce id laoreet nulla. Sed ut venenatis arcu. Sed nisl nulla, posuere nec rhoncus in, viverra vel ante. In sollicitudin consequat metus nec blandit. Pellentesque faucibus malesuada ipsum et rutrum. Phasellus tincidunt sodales molestie. Donec gravida ullamcorper ante, bibendum laoreet sapien iaculis eu. Aliquam id lectus nec neque mattis condimentum.

Morbi orci elit, mollis eu tincidunt nec, ultricies ut nunc. Aenean porta, justo et auctor molestie, nunc risus ultricies mauris, id sodales dolor ipsum nec metus. Morbi ultrices diam eget ligula vehicula laoreet. Sed sed adipiscing lorem. Mauris auctor condimentum lacus vitae ultrices. Fusce vel tellus eu eros varius auctor eget et mauris. Donec mi libero, sodales id mattis in, semper ac justo. Praesent hendrerit felis eget elit ultrices pellentesque pulvinar purus ultricies. Morbi fringilla arcu nec ligula pellentesque vitae tincidunt ipsum consequat.

Donec lacus ligula, hendrerit ut lacinia in, suscipit eu risus. Cras interdum egestas ligula, sed condimentum leo egestas nec. Quisque eget nisi et enim volutpat pulvinar vel vel velit. Phasellus sagittis pharetra mauris, ac mattis libero pulvinar a. Curabitur sem turpis, adipiscing a gravida a, rutrum vitae felis. Suspendisse in cursus mauris. Duis neque quam, mattis a ultrices ac, viverra scelerisque urna. Vestibulum bibendum molestie justo, ac consequat enim laoreet ac. Suspendisse et dolor tortor, auctor feugiat massa. Nunc sodales nisi sit amet nibh varius eget dapibus mi scelerisque.

Mauris luctus laoreet justo nec vulputate. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Proin accumsan mi eu velit bibendum vel semper risus volutpat. Curabitur rutrum posuere neque, posuere cursus metus vehicula at. Nulla vitae ligula urna. Nullam vestibulum congue odio, ac placerat metus hendrerit sit amet. Fusce bibendum fermentum mollis.

Generated 5 paragraphs, 401 words, 2733 bytes of Lorem Ipsum
""")

data = ""
for c in dataToSend:
#for c in "010203000102030000":
	val = int(c,16)
	sendA = (val // 4) / 2.0 - 0.75
	sendB = (val % 4) / 2.0 - 0.75
	print val, sendA, sendB
	for i in xrange(symbolrate):
		counter += 1
		sample = min(max(128 + int(sendA * math.sin(twopi * (counter % freq) / freq) * ampl) + int(sendB * math.cos(twopi * (counter % freq) / freq) * ampl) + random.randrange(-noise,noise),0),255)
		data += chr(sample)
		if len(data) == buflen:
			stream.write(data)
			fstream.write(data)
			data = ""
if len(data) > 0:
	stream.write(data)
	fstream.write(data)
# stop stream (6)
stream.stop_stream()
stream.close()

fstream.close()
# close PyAudio (7)
p.terminate()
