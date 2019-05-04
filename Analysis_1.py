# cycler	0.10.0	0.10.0
# kiwisolver	1.1.0	1.1.0
# matplotlib	3.0.3	3.0.3
# numpy	1.16.3	1.16.3
# pandas	0.24.2	0.24.2
# pip	10.0.1	19.1
# pyparsing	2.4.0	2.4.0
# python-dateutil	2.8.0	2.8.0
# pytz	2019.1	2019.1
# setuptools	39.1.0	41.0.1
# six	1.12.0	1.12.0
#

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tyohakemisto = 'c:/300220_data/'

"""
Haetaan data 
"""

def hae_data():

    global data_raw
    global meas_info

    data_raw_read = pd.read_csv(tyohakemisto+'data.txt', delimiter=';')
    meas_info = pd.read_csv(tyohakemisto+'meas_info.txt', delimiter=';')
    data_raw =data_raw_read.iloc[0:557,0:2]


"""
Debug tiedosto jos tarvitaan 
"""
def debug_tiedosto():

    dataRaw_pandas=pd.DataFrame(dataRaw_arr)
    dataRaw_pandas.to_csv(tyohakemisto+"/data_from_calc.txt", sep=';')

"""
Haetaan max piikin arvo 
"""
def laske_max():
    global dataRaw_arr
    global freq
    global values
    global freq_r
    global value_r
    global pointer_f
    global pointer_v
    global max_value_index

    dataRaw_arr = data_raw.values
    max_value_index= data_raw.idxmax(0)  # tää hakee piikin arvon data_raw:sta eikä dataRaw_arr:sta. En muista miksi
    freq =dataRaw_arr[:,0]
    values=dataRaw_arr[:,1]




    pointer_f = freq[max_value_index[1]]
    pointer_v = values[max_value_index[1]]
    freq_r  = round ( freq  [max_value_index[1]] , 2)
    value_r = round ( values[max_value_index[1]] , 2)

"""
Plot..
"""
def piirra():

    raami = plt.figure()
    kuvaaja = raami.add_subplot(1,1,1)
    kuvaaja.plot(freq,values)
    teksti = str(freq_r)+"MHz ,"+str(value_r)
    kuvaaja.annotate(teksti,
                     xy=(pointer_f,pointer_v  ),
                     xytext = (pointer_f +5 ,pointer_v +5),
                     arrowprops=dict(arrowstyle="->",connectionstyle="arc,angleA=45,armA=10,rad=10")
                     )
    kuvaaja.text(0.9,0.90,meas_info.TEKSTI[0],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.9,0.85,meas_info.TEKSTI[1],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.9,0.80,meas_info.TEKSTI[2],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.9,0.75,meas_info.TEKSTI[3],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.5,-0.1,meas_info.TEKSTI[4],ha='center', va='center', transform=kuvaaja.transAxes)
    plt.show()



"""
PÄÄOHJELMA
"""


hae_data()
laske_max()
piirra()
debug_tiedosto()

print('DONE')