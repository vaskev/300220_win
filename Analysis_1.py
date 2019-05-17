# pandas
# numpy
# matplotlib

# Tää ohjelma perustuu kiinteän mittaiseen (350) taulukkoon jossa antennin ja kaapelin gain on jaettu 20Mhz kaistoihin välillä 0 ...7000Mhz
#totetus ei ole kovin Python


import pandas as pd
import matplotlib.pyplot as plt
import AF_C_correlation
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
def laske_max(datacorr_array):
    global freq_r
    global value_r
    global pointer_f
    global pointer_v
    global freq
    global values
    global max_value_index

    freq = datacorr_array[:,0]
    values = datacorr_array[:,1]

    dataRaw_temp = pd.DataFrame(values)
    max_value_index = dataRaw_temp.idxmax(0)
    freq_r  = np.round( freq[max_value_index[0]], decimals=3)
    value_r = np.round( values[max_value_index[0]], decimals=2)
    pointer_f = freq[max_value_index]
    pointer_v = values[max_value_index]

"""
Plot..
"""
def piirra():

    raami = plt.figure()
    kuvaaja = raami.add_subplot(1,1,1)
    kuvaaja.plot(freq,values)
    teksti = str(freq_r)+"MHz "+str(value_r)+' dBi'
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
    #plt.show()   # tätä ei kutsuta kun ajetaan LabView:stä


    polkuhakemisto_png = str(meas_info.TEKSTI[5]+meas_info.TEKSTI[6]+'.png')
    polkuhakemisto_pdf = str(meas_info.TEKSTI[5] + meas_info.TEKSTI[6] + '.pdf')
    raami.savefig(polkuhakemisto_png)
    raami.savefig(polkuhakemisto_pdf)

"""
PÄÄOHJELMA
"""

hae_data()  # tämä välittää funktiolle datacorr datan: dataraw globaalina muuttujana
datacorr = AF_C_correlation.AF_C_corr(data_raw)  # kutsutaan modulia AF_C_correlation
laske_max(datacorr) # laskee  mm. signaalin max arvon ja taajuuden. Nämä määritelty globaaleiksi muuttujiksi
piirra() #käyttää laske_max arvoja globaalien muuttujien kautta
#debug_tiedosto()

print('DONE')
