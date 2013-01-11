= python qam encoder/decoder =

A test to explore QAM-encoded data over audio. To use:

    python send.py  # will write test.bin with 44100 samples / second data
    python receive.py  # will decode the file test.bin

Dependencies:

 - python-pyaudio
 - python-matplotlib (for graphing the symbol diagram on receive)

Todo:

 - carrier synchronization/recovery (very important!)
 - receive.py using a microphone
 - real world testing, not just random noise :)
 - encoding of data for forward error correction
    - and data masking to spread out the symbols used
 - filter sent signal to clean up spiky data
 - 16 bit samples

