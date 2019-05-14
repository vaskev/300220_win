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

# Tää ohjelma perustuu kiinteän mittaiseen (350) taulukkoon jossa antennin ja kaapelin gain on jaettu 20Mhz kaistoihin välillä 0 ...7000Mhz
#totetus ei ole kovin Python


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
1. Lasketaan antenni yms korjaukset
2. Haetaan max piikin arvo ja kohta 
"""
def laske_max():
    global dataRaw_arr
    dataCorr_arr = np.full([1000,2],-1.00)
    #dataCorr_arr = np.array(1000,2,'f')
    global freq
    global values
    global freq_r
    global value_r
    global pointer_f
    global pointer_v
    global max_value_index

    AF_taulukko = pd.read_csv('AF_table.csv', delimiter=';')  # taulukko jossa antenna / cable gain
    dataRaw_arr = data_raw.values # tälle pandas varoitus että käytä pandas.DataFrame.to_numpy .values sijaan

    max_value_index= data_raw.idxmax(0)  # KORJAA OSOITTAMAAN korjattua taulukkoa


    for slot in range(350):  # tää olettaa että AF taulukossa 350 osaa. Ei kovin Python toteutus
        freq_low = AF_taulukko.FREQ[slot] # antenna / cable gain on jaettu osiin slot joille jokaiselle lasketaan korjaus
        freq_high = AF_taulukko.FREQ[slot+1] # tämä on slotin ylätaajuus
        gain_tekija = AF_taulukko.dBi[slot]
        dataCorr_osoittaja =0       # käytetään osoittimena kun kasataan arvokorjattu taulukko uudestaan
        for line in dataRaw_arr:
           if freq_low <= line[0] <= freq_high:  # line[0] viittaa taajuuteen line[1] on taasen mitattu arvo
               #print(slot)
               #print('LOW '+ str(freq_low))
               #print('line '+str(line))
               #print('dBi '+str(gain_tekija))
               #print('korjattu '+ str(line[1]+gain_tekija))
               #print('HIGH '+str(freq_high))
               #print('  ')
               dataCorr_arr[dataCorr_osoittaja] = [line[0],line[1]+gain_tekija]
               dataCorr_osoittaja = dataCorr_osoittaja+1

    #print(dataCorr_arr)
    freq = dataCorr_arr[:,0]
    values = dataCorr_arr[:,1]
    dataCorr_pandas=pd.DataFrame(dataCorr_arr)
    dataCorr_pandas.to_csv(tyohakemisto+"/dataCorr.txt", sep=';')

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
#debug_tiedosto()

print('DONE')