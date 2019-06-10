# pandas
# numpy
# matplotlib

# Tää ohjelma perustuu kiinteän mittaiseen (350) taulukkoon jossa antennin ja kaapelin gain on jaettu 20Mhz kaistoihin välillä 0 ...7000Mhz
#totetus ei ole kovin Python


import pandas as pd
import matplotlib.pyplot as plt
import AF_C_correlation
import numpy as np
import dBm_mW

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


    fc = meas_info.TEKSTI[7]  # Occupied muutos 10.6.2019 --> käytetään declared arvoa max_value_index:sinä
    for laskuri in range(350):
        vertailtava_taajuus= freq[laskuri]
        if vertailtava_taajuus > float(fc): max_value_index = laskuri-1

    freq_r  = np.round( freq[max_value_index], decimals=3)
    value_r = np.round( values[max_value_index], decimals=2)
    pointer_f = freq[max_value_index]
    pointer_v = values[max_value_index]

"""
Plot..
"""
def piirra():

    raami = plt.figure()
    kuvaaja = raami.add_subplot(1,1,1)
    kuvaaja.plot(freq,values)

    alareuna = values.min()
    ylareuna = values.max()
    occ_oikea = freq[occ_osoitin_oikea]
    occ_vasen = freq[occ_osoitin_vasen]

    occ_kHz = (occ_oikea - occ_vasen)*1000

    kuvaaja.plot([occ_oikea,occ_oikea],[alareuna,ylareuna], 'r')
    kuvaaja.plot([occ_vasen, occ_vasen], [alareuna, ylareuna], 'r')
    kuvaaja.text(0.8,0.90,meas_info.TEKSTI[0],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.8,0.85,('OBW(kHz): '+ str( occ_kHz)),ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.8,0.80,('Center f(MHz):'+str(pointer_f[0])),ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.8,-0.1,meas_info.TEKSTI[3],ha='center', va='center', transform=kuvaaja.transAxes, fontweight='bold')
    kuvaaja.text(0.5,1.05,meas_info.TEKSTI[4],ha='center', va='center', transform=kuvaaja.transAxes,fontweight='bold')
    plt.show()   # tätä ei kutsuta kun ajetaan LabView:stä
    polkuhakemisto_png = str(meas_info.TEKSTI[5]+meas_info.TEKSTI[6]+'.png')
    polkuhakemisto_pdf = str(meas_info.TEKSTI[5] + meas_info.TEKSTI[6] + '.pdf')
    raami.savefig(polkuhakemisto_png)
    raami.savefig(polkuhakemisto_pdf)

def laske_occ_rajat(datacorr_array2):

    global values_mW_int
    global occ_osoitin_oikea
    global occ_osoitin_vasen

    values_temp = datacorr_array2[:,1]
    values_mW_plot =np.array(dBm_mW.dBm_to_mW(values_temp)*100000)
    values_mW = np.array(dBm_mW.dBm_to_mW(values_temp))
    values_mW_int=values_mW_plot.astype(int)
    value_max = values_mW[max_value_index]
    power_total = values_mW.sum()
    power_99= power_total*0.99/2 #  99% tehosta. Koska jäljempänä tarkastellaan tehon puolikasta jaetaan kahdella
    power_cum = 0
    cnt_loop = 0

    while power_cum < power_99:
        occ_osoitin_oikea = max_value_index+cnt_loop
        cnt_loop = cnt_loop+1
        power_cum = power_cum+values_mW[occ_osoitin_oikea]

    occ_osoitin_vasen = max_value_index-cnt_loop
    """
PÄÄOHJELMA
"""

hae_data()  # tämä välittää funktiolle datacorr datan: dataraw globaalina muuttujana
datacorr = AF_C_correlation.AF_C_corr(data_raw)  # kutsutaan modulia AF_C_correlation
laske_max(datacorr) # laskee  mm. signaalin max arvon ja taajuuden. Nämä määritelty globaaleiksi muuttujiksi
laske_occ_rajat(datacorr) # PÄIVITÄ
piirra() #käyttää laske_max arvoja globaalien muuttujien kautta
print('DONE')
