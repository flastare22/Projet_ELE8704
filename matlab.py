import json
import pickle
import statistics

import numpy
import scipy.io

if __name__ == "__main__":
    sources = ["Youtube/", "Lib/", "Hangout/", "Skype/"]
    types = ["Wifi/", "RJ45/"]
    liste_moy_taille = []
    liste_nbr_paquets = []
    liste_var_delai = []
    liste_moy_trans = []
    liste_moy_debit = []
    liste_delay = {}

    path = "output.json"
    with open(path) as fichier:
        datas = json.load(fichier)

    compteur = 0
    for type in types:

        liste_taille_pc = []
        liste_paquets_pc = []
        liste_delai_pc = []
        liste_trans_pc = []
        liste_debit_pc = []
        liste_taille_web = []
        liste_paquets_web = []
        liste_delai_web = []
        liste_trans_web = []
        liste_debit_web = []

        for source in sources:
            if not (source == "Skype/" and type == "RJ45/"):

                taille_moy_pc = statistics.mean(datas[source][type]["data"]["taille_pc"])
                nbr_paquets_pc = len(datas[source][type]["data"]["taille_pc"])
                delai_var_pc = statistics.variance(datas[source][type]["data"]["temps_pc"])
                trans_moy_pc = statistics.mean(datas[source][type]["data"]["duree_pc"])
                debit_moy_pc = nbr_paquets_pc*taille_moy_pc/trans_moy_pc

                liste_taille_pc.append(taille_moy_pc)
                liste_paquets_pc.append(nbr_paquets_pc)
                liste_delai_pc.append(delai_var_pc)
                liste_trans_pc.append(trans_moy_pc)
                liste_debit_pc.append(debit_moy_pc)

                liste_delay[source] = datas[source][type]["data"]["temps_pc"]

                taille_moy_web = statistics.mean(datas[source][type]["data"]["taille_web_app"])
                nbr_paquets_web = len(datas[source][type]["data"]["taille_web_app"])
                delai_var_web = statistics.variance(datas[source][type]["data"]["temps_web_app"])
                trans_moy_web = statistics.mean(datas[source][type]["data"]["duree_web_app"])
                debit_moy_web = nbr_paquets_web * taille_moy_web / trans_moy_web

                liste_taille_web.append(taille_moy_web)
                liste_paquets_web.append(nbr_paquets_web)
                liste_delai_web.append(delai_var_web)
                liste_trans_web.append(trans_moy_web)
                liste_debit_web.append(debit_moy_web)

                compteur += 1
            else :
                liste_taille_web.append(0)
                liste_paquets_web.append(0)
                liste_delai_web.append(0)
                liste_trans_web.append(0)
                liste_debit_web.append(0)

                liste_taille_pc.append(0)
                liste_paquets_pc.append(0)
                liste_delai_pc.append(0)
                liste_trans_pc.append(0)
                liste_debit_pc.append(0)

        vecteur_taille = numpy.array(liste_taille_pc)
        vecteur_paquets = numpy.array(liste_paquets_pc)
        vecteur_delai = numpy.array(liste_delai_pc)
        vecteur_trans = numpy.array(liste_trans_pc)
        vecteur_debit = numpy.array(liste_debit_pc)

        liste_moy_taille.append(vecteur_taille)
        liste_nbr_paquets.append(vecteur_paquets)
        liste_var_delai.append(vecteur_delai)
        liste_moy_trans.append(vecteur_trans)
        liste_moy_debit.append(vecteur_debit)

        vecteur_taille = numpy.array(liste_taille_web)
        vecteur_paquets = numpy.array(liste_paquets_web)
        vecteur_delai = numpy.array(liste_delai_web)
        vecteur_trans = numpy.array(liste_trans_web)
        vecteur_debit = numpy.array(liste_debit_web)

        liste_moy_taille.append(vecteur_taille)
        liste_nbr_paquets.append(vecteur_paquets)
        liste_var_delai.append(vecteur_delai)
        liste_moy_trans.append(vecteur_trans)
        liste_moy_debit.append(vecteur_debit)


    matlab_avg_size = numpy.asarray(liste_moy_taille)
    print(matlab_avg_size)
    scipy.io.savemat('matlab/matlab_avg_size.mat', mdict={'matlab_avg_size': matlab_avg_size})
    matlab_nbr_pakets = numpy.asarray(liste_nbr_paquets)
    print(matlab_nbr_pakets)
    scipy.io.savemat('matlab/matlab_nbr_pakets.mat', mdict={'matlab_nbr_pakets': matlab_nbr_pakets})
    matlab_var_delai = numpy.asarray(liste_var_delai)
    print(matlab_var_delai)
    scipy.io.savemat('matlab/matlab_var_delai.mat', mdict={'matlab_var_delai': matlab_var_delai})
    matlab_avg_trans_time = numpy.asarray(liste_moy_trans)
    print(matlab_avg_trans_time)
    scipy.io.savemat('matlab/ matlab_avg_trans_time.mat', mdict={' matlab_avg_trans_time':  matlab_avg_trans_time})
    matlab_avg_data_rate = numpy.asarray(liste_moy_debit)
    print(matlab_avg_data_rate)
    scipy.io.savemat('matlab/matlab_avg_data_rate.mat', mdict={'matlab_avg_data_rate': matlab_avg_size})

    with open('delay.pickle', 'wb') as handle:
        pickle.dump(liste_delay, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('delay.json', 'w') as file:
        file.write(json.dumps(liste_delay))

