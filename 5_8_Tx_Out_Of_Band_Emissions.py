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


    x_5_arvot= rajat.loc[:'5_20','freq']
    y_5_arvot=rajat.loc[:'5_20','dBm']
    kuvaaja.plot(x_5_arvot,y_5_arvot,'r') # 300220-1 Figure 5

    kuvaaja.plot([rajat.loc['6_10','freq'],rajat.loc['6_11','freq']],
                 [rajat.loc['6_10','dBm' ],rajat.loc['6_11','dBm' ]],'b') # 300220-1 Figure 6
    kuvaaja.plot([rajat.loc['6_21','freq'],rajat.loc['6_20','freq']],
                 [rajat.loc['6_21','dBm' ],rajat.loc['6_20','dBm' ]],'b') # 300220-1 Figure 6

    teksti = str(freq_r)+"MHz "+str(value_r)+' dBm'
    #kuvaaja.annotate(teksti,
     #                xy=(pointer_f,pointer_v  ),
      #               xytext = (pointer_f +0.1 ,pointer_v +0.1),
       #              arrowprops=dict(arrowstyle="->",connectionstyle="arc,angleA=0,armA=10,rad=0")
        #             )
    kuvaaja.text(0.8,0.90,meas_info.TEKSTI[0],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.8,0.85,meas_info.TEKSTI[1],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.8,0.80,meas_info.TEKSTI[2],ha='center', va='center', transform=kuvaaja.transAxes)
    kuvaaja.text(0.8,-0.1,meas_info.TEKSTI[3],ha='center', va='center', transform=kuvaaja.transAxes, fontweight='bold')
    kuvaaja.text(0.5,1.05,meas_info.TEKSTI[4],ha='center', va='center', transform=kuvaaja.transAxes,fontweight='bold')
    plt.show()   # tätä ei kutsuta kun ajetaan LabView:stä
    polkuhakemisto_png = str(meas_info.TEKSTI[5]+meas_info.TEKSTI[6]+'.png')
    polkuhakemisto_pdf = str(meas_info.TEKSTI[5] + meas_info.TEKSTI[6] + '.pdf')
    raami.savefig(polkuhakemisto_png)
    raami.savefig(polkuhakemisto_pdf)


def laske_rajat():
    global rajat

    rajat_rakenne_init = { 'freq':[1.001,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],   # Python hauskaa 1.001 tai muuten taulukko tyyppiä int
                           'dBm':[-40.001,-40,-30,-30,-40,-40,-20,-20,-30,-40,-40,-30,-20,-20,-40,-40,-40,-40]}

    rajat=pd.DataFrame(rajat_rakenne_init,index=['5_10','5_11','5_12','5_22','5_21','5_20',
                                                 '6_10','6_11','6_12','6_13','6_23','6_22','6_21','6_20',
                                                 'OCW','fc','F_low_OFB','F_high_OFB'])

    OCW = float(meas_info.TEKSTI[7])*0.001   # muunnos kHz --> MHz Operation Channel Width
    fc = (pointer_f[0])  # fc =keskitaajuus
    F_low_OFB = fc - OCW / 2   # keskitaajuus - OCW /2
    F_high_OFB = fc + OCW / 2   # keskitaajuus + OCW /2

# 300220-1 Figure 5 Lasketaan taajuusalueiden reunapisteiden apuarvot
    rajat.at['OCW', 'freq'] = OCW
    rajat.at['fc', 'freq'] = fc
    rajat.at['F_low_OFB', 'freq'] = F_low_OFB
    rajat.at['F_high_OFB', 'freq'] = F_high_OFB

#300220-1 Figure 5 Lasketaan taajuusalueiden reunapisteiden arvot
    rajat.at['5_11', 'freq'] = fc - 2.5 * OCW
    rajat.at['5_21', 'freq'] = fc + 2.5 * OCW
    rajat.at['5_12', 'freq'] = fc - 0.5 * OCW
    rajat.at['5_22', 'freq'] = fc + 0.5 * OCW
    rajat.at['5_10', 'freq'] = freq[0]
    rajat.at['5_20', 'freq'] = freq[556]

# 300220-1 Figure 5 Asetaan taajuusalueiden reunapisteiden dBm arvot
    rajat.at['5_11', 'dBm'] = -36
    rajat.at['5_21', 'dBm'] = -36
    rajat.at['5_12', 'dBm'] = 0
    rajat.at['5_22', 'dBm'] = 0
    rajat.at['5_10', 'dBm'] = -36
    rajat.at['5_20', 'dBm'] = -36

# 300220-1 Figure 6 Asetaan taajuusalueiden reunapisteiden arvot
    rajat.at['6_11', 'freq'] = F_low_OFB -0.4  # 0.4 = 400kHz
    rajat.at['6_12', 'freq'] = F_low_OFB - 0.2  # 0.4 = 200kHz
    rajat.at['6_13', 'freq'] = F_low_OFB
    rajat.at['6_21', 'freq'] = F_high_OFB +0.4  # 0.4 = 400kHz
    rajat.at['6_22', 'freq'] = F_high_OFB + 0.2  # 0.4 = 200kHz
    rajat.at['6_23', 'freq'] = F_high_OFB
    rajat.at['6_10', 'freq'] = freq[0]
    rajat.at['6_20', 'freq'] = freq[556]

# 300220-1 Figure 6 Asetaan taajuusalueiden reunapisteiden dBm arvot
    rajat.at['6_11', 'dBm'] = -36
    rajat.at['6_12', 'dBm'] = -36
    rajat.at['6_13', 'dBm'] = 0
    rajat.at['6_21', 'dBm'] = -36
    rajat.at['6_22', 'dBm'] = -36
    rajat.at['6_23', 'dBm'] = 0
    rajat.at['6_10', 'dBm'] = -36
    rajat.at['6_20', 'dBm'] = -36



    rajat.to_csv(tyohakemisto + "/5_8_OutOfBandrajat.txt", sep=';')

"""
PÄÄOHJELMA
"""

hae_data()  # tämä välittää funktiolle datacorr datan: dataraw globaalina muuttujana
datacorr = AF_C_correlation.AF_C_corr(data_raw)  # kutsutaan modulia AF_C_correlation
laske_max(datacorr) # laskee  mm. signaalin max arvon ja taajuuden. Nämä määritelty globaaleiksi muuttujiksi
laske_rajat()#
piirra() #käyttää laske_max arvoja globaalien muuttujien kautta
#debug_tiedosto()

print('DONE')
