import math, sys, binascii
from pylab import scatter, show

samplerate = 44100

twopi = math.pi * 2.0
freq = samplerate / 8000.0
ampl = 100.0
symbolrate = samplerate / 1000
buflen = 1024

stream = open('test.bin','rb')
counter = 0
zcounter = 0 # zero-crossing-counter, to sync the phase
psample = 128
lowpassI = 0.0
lowpassQ = 0.0

hexDecode = ""

scatterI = []
scatterQ = []
lowpassSamples = (freq / (symbolrate * 2.0))

for c in stream.read():
	counter += 1
	sample = ord(c)
	#if psample < 128 and sample >= 128:
	#	zcounter = counter # reset zero-crossing detector
#		print "reset zcounter",zcounter
	I = ((sample-128)/100.0) * (math.cos(twopi * ((counter - zcounter) / freq)))
	Q = ((sample-128)/100.0) * (math.sin(twopi * ((counter - zcounter) / freq)))
	lowpassI = (lowpassI * (1 - lowpassSamples)) + lowpassSamples * (I * 2)
	lowpassQ = (lowpassQ * (1 - lowpassSamples)) + lowpassSamples * (Q * 2)
	#print "%05d" % counter, "%03d" % sample, "%0.4f" % I, "%0.4f" % lowpass, " "*int(sample/7),"*"
	psample = sample
	if (counter + 5) % symbolrate  == 0:
		# time to reconstruct!
		guessI = (lowpassI + 0.75) * 2
		guessQ = (lowpassQ + 0.75) * 2
		guessSymbol = round(guessQ) * 4 + round(guessI)
		scatterI.append(guessI)
		scatterQ.append(guessQ)
		print "%d: I: %.04f (%d)  Q: %.04f (%d)  %x" % (counter, lowpassI, guessI, lowpassQ, guessQ, guessSymbol)
		hexDecode += "%.01x" % guessSymbol
print hexDecode

print binascii.unhexlify(hexDecode)

scatter(scatterI,scatterQ,marker='o')

show()
