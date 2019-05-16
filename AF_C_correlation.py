import pandas as pd

def AF_C_corr(data_rawAF):

    AF_taulukko = pd.read_csv('AF_table.csv', delimiter=';')  # taulukko jossa antenna / cable gain
    dataRaw_arr = data_rawAF.values # tälle pandas varoitus että käytä pandas.DataFrame.to_numpy .values sijaan


    dataCorr_osoittaja = 0  # käytetään osoittimena kun kasataan arvokorjattu taulukko uudestaan
    for slot in range(350):  # tää olettaa että AF taulukossa 350 osaa. Ei kovin Python toteutus
        freq_low = AF_taulukko.FREQ[slot] # antenna / cable gain on jaettu osiin slot joille jokaiselle lasketaan korjaus
        freq_high = AF_taulukko.FREQ[slot+1] # tämä on slotin ylätaajuus
        gain_tekija = AF_taulukko.dBi[slot]
        dataCorr_arr = dataRaw_arr  #  luodaan uusi array jossa korvataan mitattu data korjatulla datalla
        for line in dataRaw_arr:
           if freq_low <= line[0] <= freq_high:  # line[0] viittaa taajuuteen line[1] on taasen mitattu arvo
               #print(slot)
               #print('LOW '+ str(freq_low))
               #print('line '+str(line[0]))
               #print('dBi '+str(gain_tekija))
               #print('korjattu '+ str(line[1]+gain_tekija))
               #print('HIGH '+str(freq_high))
               #print (dataCorr_osoittaja)
               #print('  ')
               dataCorr_arr[dataCorr_osoittaja] = [line[0],line[1]+gain_tekija]
               dataCorr_osoittaja = dataCorr_osoittaja+1

    assert isinstance(dataCorr_arr, object)  # PyCharm automaattilisäys
    return dataCorr_arr


