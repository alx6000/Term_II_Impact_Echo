#!/usr/bin/env python
# coding: utf-8

# In[1]:


from math import log
import matplotlib.mlab as mlab
import numpy
from tangible import ast, scales
from tangible.backends.openscad import OpenScadBackend
from tangible.shapes.bars import BarsND
import wave
import nfft


# In[2]:


inPath = r'C:\Users\varva\Desktop/leos.wav'


# In[6]:


outPath = r'C:\Users\varva\Desktop\leos2.scad'


# In[7]:


loggishness = 0.00000000000004


# In[8]:


nfft = 2**18
padto = nfft/(2**13)

padto = int (padto)

def main():

  print ("Reading and analyzing file...")
  spectrum, freqs = ReadAndAnalyze(inPath)

  print (len(freqs))
  print (len(spectrum[0]))


  print ("Scaling logarithmically (kinda)...")
  for i, s in enumerate(spectrum):
    spectrum[i] = list(map(loggish, s))

  print ("Generating linear scale...")
  scale = scales.linear(domain=[spectrum.min(), spectrum.max()],
                        codomain=[1, 10])

  print ("Normalizing spectrum data...")
  datapoints = list(map(lambda x:list(map(scale, x)), spectrum))

  print ("Trimming spectrum data post-normalization...")
  for i, x in enumerate(datapoints):
    for j, v in enumerate(x):
        if v > 9:
          datapoints[i][j] = 9

  print ("Generating bars...")
  bars = BarsND(datapoints,
                bar_width=1,
                bar_depth=1)

  print ("Rendering...")
  code = bars.render(backend=OpenScadBackend)

  print ("Saving to file...")
  with open(outPath, "w") as f:
      f.write(code)

def loggish(v):
  v = float(v)
  L = loggishness
  return L * (log(v) - v) + v

def ReadAndAnalyze(f):
    wav = wave.open(f, 'r')
    frames = wav.readframes(-1)
    sound_info = numpy.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    specdata = mlab.specgram(sound_info,
                             NFFT=nfft,
                             pad_to=padto,
                             Fs=frame_rate)
    spectrum = specdata[0]
    freqs = specdata[1]
    return spectrum, freqs

if __name__ == "__main__":
  main()


# In[ ]:




