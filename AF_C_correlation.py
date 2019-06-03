import pandas as pd
import math
import dBm_mW
def AF_C_corr(data_rawAF):

    r = 3 # 3m mittapaikka
    AF_taulukko = pd.read_csv('C:/Projektit/300220/Python/300220_analysis/AF_table.csv', delimiter=';')  # taulukko jossa antenna / cable gain
    dataRaw_arr = data_rawAF.values # tälle pandas varoitus että käytä pandas.DataFrame.to_numpy .values sijaan


    dataCorr_osoittaja = 0  # käytetään osoittimena kun kasataan arvokorjattu taulukko uudestaan
    for slot in range(350):  # tää olettaa että AF taulukossa 350 osaa. Ei kovin Python toteutus
        freq_low = AF_taulukko.FREQ[slot] # antenna / cable gain on jaettu osiin slot joille jokaiselle lasketaan korjaus
        freq_high = AF_taulukko.FREQ[slot+1] # tämä on slotin ylätaajuus
        AFC_tekija = AF_taulukko.dBi[slot]
        dataCorr_arr = dataRaw_arr  #  luodaan uusi array jossa korvataan mitattu data korjatulla datalla
        for line in dataRaw_arr:
           if freq_low <= line[0] <= freq_high:  # line[0] viittaa taajuuteen line[1] on taasen mitattu arvo

               power_tmp_dBm = line[1]
               power_tmp_dBuV =power_tmp_dBm+107+AFC_tekija # kaava P+107dB

               tekija_1 = pow(10, (power_tmp_dBuV / 20) - 6)
               #print('1= ' + str(tekija_1))
               tekija_2 = pow(tekija_1, 2)
               #print('2= ' + str(tekija_2))
               tekija_3 = tekija_2 * 9
               #print('3= ' + str(tekija_3))
               tekija_4 = tekija_3 / (30 * 1.64)
               tekija_5 = tekija_4 / 0.001
               calc = math.log10(tekija_5) * 10

               #received_power_W = pow(10, power_tmp_dBuV) / 1000
               #print('received_power_W = ' + str(received_power_W))
               #beacon_W = 4 * 3.14 * pow(r, 2) * received_power_W
               #print('beacon W = ' + str(beacon_W))
               #beacon_dBm = 10 * math.log10(1000 * beacon_W)
               #print('beacon dBm = ' + str(beacon_dBm))


               #power_tmp_dBm = line[1]/10  # datapisteen teho
               #print(power_tmp_dBm)
               #received_power_W = math.pow(10, power_tmp_dBuV)/1000   # muunnetaan dBm --> W
               #beacon_W = 4 * 3.14 * math.pow(r, 2) * received_power_W # 3m mittapaikka, muunnetaan lähettimen tehoksi
               #print(beacon_W)
               #beacon_dBm = 10 * math.log10(1000 * beacon_W) # muunnetaan W --> dBm
               #print(beacon_dBm)
               #print(' ')

               dataCorr_arr[dataCorr_osoittaja] = [line[0], calc]
               #dataCorr_arr[dataCorr_osoittaja] = [line[0], line[1] +107 + AFC_tekija]
               #dataCorr_arr[dataCorr_osoittaja] = [line[0], line[1]]
               dataCorr_osoittaja = dataCorr_osoittaja+1

    assert isinstance(dataCorr_arr, object)  # PyCharm automaattilisäys
    return dataCorr_arr


