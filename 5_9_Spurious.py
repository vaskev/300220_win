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

    freq_to_7_15 = freq[freq < rajat.loc['7_15','freq']]  # rajataan mukaan vain ne datapisteet jotka ovat OC:n ulkopuolella
    values_to_7_15 = values[freq < rajat.loc['7_15','freq']]
    freq_from_7_25 = freq[freq > rajat.loc['7_25','freq']]
    values_from_7_25 = values[freq > rajat.loc['7_25','freq']]

    kuvaaja.plot(freq_to_7_15, values_to_7_15, 'b')
    kuvaaja.plot(freq_from_7_25, values_from_7_25, 'b')
    #kuvaaja.plot(freq,values,'c')

    if meas_info.TEKSTI[9] == 1:              # valitaan käytetäänkö Rx vai tx rajoja
                    rx_vai_tx = 'dBm_tx'
    else:
                    rx_vai_tx = 'dBm_rx'

    print (rx_vai_tx)


    # 0.009 ... 0.150 MHz   säteilevä mittaus alaraja 25MHz jossa mitataan RBW = 10kHz
    kuvaaja.plot( [rajat.loc['7_10','freq'], rajat.loc['47-','freq'] ] ,
                  [rajat.loc['7_10','dBm_tx'], rajat.loc['47-','dBm_tx'] ]
                  ,'r')

    # 47 ...74 MHz
    kuvaaja.plot([rajat.loc['47+', 'freq'], rajat.loc['74-', 'freq']],
                 [rajat.loc['47+', 'dBm_tx'], rajat.loc['74-', 'dBm_tx']]
                 , 'r')

    # 74 ...87.5 MHz
    kuvaaja.plot([rajat.loc['74+', 'freq'], rajat.loc['87.5-', 'freq']],
                 [rajat.loc['74+', 'dBm_tx'], rajat.loc['87.5-', 'dBm_tx']]
                 , 'r')

    # 87.5 ...118 MHz
    kuvaaja.plot([rajat.loc['87.5+', 'freq'], rajat.loc['118-', 'freq']],
                 [rajat.loc['87.5+', 'dBm_tx'], rajat.loc['118-', 'dBm_tx']]
                 , 'r')

    # 118 ... 174 MHz
    kuvaaja.plot([rajat.loc['118+', 'freq'], rajat.loc['174-', 'freq']],
                 [rajat.loc['118+', 'dBm_tx'], rajat.loc['174-', 'dBm_tx']]
                 , 'r')

    # 174 ... 230 MHz
    kuvaaja.plot([rajat.loc['174+', 'freq'], rajat.loc['230-', 'freq']],
                 [rajat.loc['174+', 'dBm_tx'], rajat.loc['230-', 'dBm_tx']]
                 , 'r')

    # 230 ... 470 MHz
    kuvaaja.plot([rajat.loc['230+', 'freq'], rajat.loc['470-', 'freq']],
                 [rajat.loc['230+', 'dBm_tx'], rajat.loc['470-', 'dBm_tx']]
                 , 'r')

    # 470 ... 790 MHz
    kuvaaja.plot([rajat.loc['470+', 'freq'], rajat.loc['790-', 'freq']],
                 [rajat.loc['470+', 'dBm_tx'], rajat.loc['790-', 'dBm_tx']]
                 , 'r')


    # 470 ... 790 MHz
    kuvaaja.plot([rajat.loc['470+', 'freq'], rajat.loc['790-', 'freq']],
                 [rajat.loc['470+', 'dBm_tx'], rajat.loc['790-', 'dBm_tx']]
                 , 'r')

    # 790 ... 7_13 MHz

    kuvaaja.plot([rajat.loc['790+', 'freq'], rajat.loc['7_13', 'freq']],
                 [rajat.loc['790+', 'dBm_tx'], rajat.loc['7_13', 'dBm_tx']]
                 , 'k')


    # 7_13 ... 7_14
    kuvaaja.plot([rajat.loc['7_13', 'freq'], rajat.loc['7_14', 'freq']],
                 [rajat.loc['7_13', 'dBm_tx'], rajat.loc['7_14', 'dBm_tx']]
                 , 'k')

    # 7_14 ... 7_15
    kuvaaja.plot([rajat.loc['7_14', 'freq'], rajat.loc['7_15', 'freq']],
                 [rajat.loc['7_14', 'dBm_tx'], rajat.loc['7_15', 'dBm_tx']]
                 , 'k')

    # 7_25 ... 7_24
    kuvaaja.plot([rajat.loc['7_25', 'freq'], rajat.loc['7_24', 'freq']],
                 [rajat.loc['7_25', 'dBm_tx'], rajat.loc['7_24', 'dBm_tx']]
                 , 'k')

    # 7_24 ... 7_23
    kuvaaja.plot([rajat.loc['7_24', 'freq'], rajat.loc['7_23', 'freq']],
                 [rajat.loc['7_24', 'dBm_tx'], rajat.loc['7_23', 'dBm_tx']]
                 , 'k')

    # 7_23 ... 7_22
    kuvaaja.plot([rajat.loc['7_23', 'freq'], rajat.loc['7_22', 'freq']],
                 [rajat.loc['7_23', 'dBm_tx'], rajat.loc['7_22', 'dBm_tx']]
                 , 'k')



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

    rajat_rakenne_init = { 'freq':[1.001,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],   # Python hauskaa 1.001 tai muuten taulukko tyyppiä int
                           'dBm_tx':[-1.001,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],
                           'dBm_rx':[-1.001,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]}

    rajat=pd.DataFrame(rajat_rakenne_init,index=['7_10','7_11','7_12',
                                                 '47-','74-','87.5-','118-','174-','230-','470-','790-',
                                                 '47+','74+','87.5+','118+','174+','230+','470+','790+',
                                                 '7_13','7_14','7_15','7_25','7_24','7_23','7_22','7_20',
                                                 'm','n','p',
                                                 'OCW','fc','F_low_OFB','F_high_OFB'])

    OCW = float(meas_info.TEKSTI[7])*0.001   # muunnos kHz --> MHz Operation Channel Width
    #fc = (pointer_f[0])  # fc =keskitaajuus
    fc = float(meas_info.TEKSTI[10]) # Spurious käyttää keskitaajuutena declared arvoa. EI datasta laskettua

    print(fc)

    F_low_OFB = fc - OCW / 2   # keskitaajuus - OCW /2
    F_high_OFB = fc + OCW / 2   # keskitaajuus + OCW /2

# Lasketaan taajuusalueiden reunapisteiden apuarvot
    rajat.at['OCW', 'freq'] = OCW
    rajat.at['fc', 'freq'] = fc
    rajat.at['F_low_OFB', 'freq'] = F_low_OFB
    rajat.at['F_high_OFB', 'freq'] = F_high_OFB

    m = OCW * 10
    if m < 0.5:
        m = 0.5   # ehto max 500kHz
    rajat.at['m','freq'] = m
    
    n = OCW * 4
    if n < 0.1:
        n = 0.1   # ehto max 100kHz
    rajat.at['n', 'freq'] = n
    
    p = OCW * 2.5
    rajat.at['p', 'freq'] = p
    
    
#300220-1 Figure 7 Lasketaan taajuusalueiden reunapisteiden arvot
    rajat.at['7_10', 'freq'] = 0.009
    rajat.at['7_11', 'freq'] = 0.0150
    rajat.at['7_12', 'freq'] = 30
    rajat.at['7_13', 'freq'] = fc - m
    rajat.at['7_14', 'freq'] = fc - n
    rajat.at['7_15', 'freq'] = fc - p
    rajat.at['7_25', 'freq'] = fc + p
    rajat.at['7_24', 'freq'] = fc + n
    rajat.at['7_23', 'freq'] = fc + m
    rajat.at['7_22', 'freq'] = 1000
    # 7_21 ei olemassa katso application note
    rajat.at['7_20', 'freq'] = 3000

    rajat.at['47-', 'freq'] = 47
    rajat.at['74-', 'freq'] = 74
    rajat.at['87.5-', 'freq'] = 87.5
    rajat.at['118-', 'freq'] = 118
    rajat.at['174-', 'freq'] = 174
    rajat.at['230-', 'freq'] = 230
    rajat.at['470-', 'freq'] = 470
    rajat.at['790-', 'freq'] = 790

    rajat.at['47+', 'freq'] = 47
    rajat.at['74+', 'freq'] = 74
    rajat.at['87.5+', 'freq'] = 87.5
    rajat.at['118+', 'freq'] = 118
    rajat.at['174+', 'freq'] = 174
    rajat.at['230+', 'freq'] = 230
    rajat.at['470+', 'freq'] = 470
    rajat.at['790+', 'freq'] = 790

    #rajat.at['5_10', 'freq'] = freq[0]  # datan ensimmäinen piste
    #rajat.at['5_20', 'freq'] = freq[556] #datan viimeinen piste

# 300220-1 Figure 7 Asetaan taajuusalueiden reunapisteiden dBm arvot Tx
    rajat.at['7_10', 'dBm_tx'] = -36
    rajat.at['7_11', 'dBm_tx'] = -54
    rajat.at['7_12', 'dBm_tx'] = -54
    rajat.at['7_13', 'dBm_tx'] = -36
    rajat.at['7_14', 'dBm_tx'] = -36
    rajat.at['7_15', 'dBm_tx'] = -36
    rajat.at['7_25', 'dBm_tx'] = -36
    rajat.at['7_24', 'dBm_tx'] = -36
    rajat.at['7_23', 'dBm_tx'] = -36
    rajat.at['7_22', 'dBm_tx'] = -36
    # 7_21 ei olemassa katso application note
    rajat.at['7_20', 'dBm_tx'] = -30

    rajat.at['47-', 'dBm_tx'] = -36
    rajat.at['74-', 'dBm_tx'] = -54
    rajat.at['87.5-', 'dBm_tx'] = -36
    rajat.at['118-', 'dBm_tx'] = -54
    rajat.at['174-', 'dBm_tx'] = -36
    rajat.at['230-', 'dBm_tx'] = -54
    rajat.at['470-', 'dBm_tx'] = -36
    rajat.at['790-', 'dBm_tx'] = -54

    rajat.at['47+', 'dBm_tx']   = -54
    rajat.at['74+', 'dBm_tx'] = -36
    rajat.at['87.5+', 'dBm_tx'] = -54
    rajat.at['118+', 'dBm_tx'] = -36
    rajat.at['174+', 'dBm_tx'] = -54
    rajat.at['230+', 'dBm_tx'] = -36
    rajat.at['470+', 'dBm_tx'] = -54
    rajat.at['790+', 'dBm_tx'] = -36

    # 300220-1 Figure 7 Asetaan taajuusalueiden reunapisteiden dBm arvot Rx

    rajat.at['7_10', 'dBm_rx'] = -57
    rajat.at['7_11', 'dBm_rx'] = -57
    rajat.at['7_12', 'dBm_rx'] = -57
    rajat.at['7_13', 'dBm_rx'] = -57
    rajat.at['7_14', 'dBm_rx'] = -57
    rajat.at['7_15', 'dBm_rx'] = -57
    rajat.at['7_25', 'dBm_rx'] = -57
    rajat.at['7_24', 'dBm_rx'] = -57
    rajat.at['7_23', 'dBm_rx'] = -57
    rajat.at['7_22', 'dBm_rx'] = -57
    # 7_21 ei olemassa katso application note
    rajat.at['7_20', 'dBm_rx'] = -57

    rajat.at['47-', 'dBm_rx'] = -57
    rajat.at['74-', 'dBm_rx'] = -57
    rajat.at['87.5-', 'dBm_rx'] = -57
    rajat.at['118-', 'dBm_rx'] = -57
    rajat.at['174-', 'dBm_rx'] = -57
    rajat.at['230-', 'dBm_rx'] = -57
    rajat.at['470-', 'dBm_rx'] = -57
    rajat.at['790-', 'dBm_rx'] = -57

    rajat.at['47+', 'dBm_rx'] = -57
    rajat.at['74+', 'dBm_rx'] = -57
    rajat.at['87.5+', 'dBm_rx'] = -57
    rajat.at['118+', 'dBm_rx'] = -57
    rajat.at['174+', 'dBm_rx'] = -57
    rajat.at['230+', 'dBm_rx'] = -57
    rajat.at['470+', 'dBm_rx'] = -57
    rajat.at['790+', 'dBm_rx'] = -57

    rajat.to_csv(tyohakemisto + "/5_9_SpuriousRajat.txt", sep=';')

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
