import json
import os
import statistics
from collections import defaultdict

if __name__ == "__main__":
    sources = ["Hangout/", "Lib/", "Skype/", "Youtube/", ]
    types = ["RJ45/", "Wifi/"]
    path = "json/"
    compteur = 0
    dict = {}
    for source in sources:
        dict_source = {}
        for type in types:
            liste_par_type = []
            fichiers_json = [pos_json for pos_json in os.listdir(path + source + type) if pos_json.endswith('.json')]
            for fichier_json in fichiers_json:
                compteur += 1
                print(".........................{}.........................".format(fichier_json))
                with open(path + source + type + fichier_json) as fichier:
                    datas = json.load(fichier)
                dict_ip = defaultdict(list)
                for data in datas:
                    pc_taille = []
                    pc_temps = []
                    pc_duree = []
                    web_app_temps = []
                    web_app_taille = []
                    web_app_duree = []
                    n = 0
                    if "ip" in data["_source"]["layers"]:
                        if "ip.src" in data["_source"]["layers"]["ip"]:
                            n += 1
                            ip_src = data["_source"]["layers"]["ip"]["ip.src"]
                            ip_dst = data["_source"]["layers"]["ip"]["ip.dst"]
                            protocole = list(data["_source"]["layers"].keys())[3]
                            if protocole == "udp" or protocole == "tcp":
                                taille = int(data["_source"]["layers"]["ip"]["ip.len"]) - int(
                                    data["_source"]["layers"]["ip"][
                                        "ip.hdr_len"])
                                temps_debut = data["_source"]["layers"][protocole]["Timestamps"][
                                    protocole + ".time_relative"]
                                delta_temps = data["_source"]["layers"]["frame"]["frame.time_delta"]

                                if not ip_src in dict_ip:
                                    dict_ip[ip_src].extend((0, {}, {}, [], [], []))
                                dict_ip[ip_src][0] += 1
                                if not ip_dst in dict_ip[ip_src][1]:
                                    dict_ip.get(ip_src)[1][ip_dst] = 0
                                dict_ip.get(ip_src)[1][ip_dst] += 1
                                if not protocole in dict_ip[ip_src][2]:
                                    dict_ip[ip_src][2][protocole] = 0
                                dict_ip[ip_src][2][protocole] += 1
                                protocole_present = False
                                for dict_protocole, valeur in dict_ip[ip_src][3]:
                                    if protocole == dict_protocole:
                                        ip_present = False
                                        for ip, val in valeur:
                                            if ip == ip_dst:
                                                val.append(taille)
                                                ip_present = True
                                                break
                                        if not ip_present:
                                            valeur.append((ip_dst, [taille]))
                                        protocole_present = True
                                        break
                                if not protocole_present:
                                    dict_ip[ip_src][3].append((protocole, [(ip_dst, [taille])]))
                                protocole_present = False
                                for dict_protocole, valeur in dict_ip[ip_src][5]:
                                    if protocole == dict_protocole:
                                        ip_present = False
                                        for ip, val in valeur:
                                            if ip == ip_dst:
                                                val.append(float(delta_temps))
                                                ip_present = True
                                                break
                                        if not ip_present:
                                            valeur.append((ip_dst, [float(delta_temps)]))
                                        protocole_present = True
                                        break
                                if not protocole_present:
                                    dict_ip[ip_src][5].append((protocole, [(ip_dst, [float(delta_temps)])]))
                                protocole_present = False
                                for dict_protocole, valeur in dict_ip[ip_src][4]:
                                    if protocole == dict_protocole:
                                        ip_present = False
                                        for ip, val in valeur:
                                            if ip == ip_dst:
                                                val.append(float(temps_debut))
                                                ip_present = True
                                                break
                                        if not ip_present:
                                            valeur.append((ip_dst, [float(temps_debut)]))
                                        protocole_present = True
                                        break
                                if not protocole_present:
                                    dict_ip[ip_src][4].append((protocole, [(ip_dst, [float(temps_debut)])]))

                print("Nombre de paquets analysé pour {} : {}".format(fichier_json, n))
                print("Nombre total de paquets pour {} : {}".format(fichier_json, len(datas)))
                print("Sources de paquets pour {} :".format(fichier_json))
                for ip, valeurs in dict_ip.items():
                    liste_ip = []
                    assez_paquets = False
                    print("  /{} : ".format(ip))
                    print("         -destinations : {}".format(valeurs[1]))
                    print("         -protocoles : {}".format(valeurs[2]))
                    for protocole, valeur in valeurs[3]:
                        for ip, val in valeur:
                            if len(val) > 300 or source == "Lib/":
                                assez_paquets = True
                                print("         -Pour les flux de plus de 300 paquets:")
                                print("             ---------INFO TAILLE PAQUETS---------")

                                liste_ip.append(ip)
                                print("                 *nombre de paquets {} en destination de {} : {} ".format(
                                    protocole, ip, len(val)))
                                print(
                                    "                 *taille moyenne paquets {} en destination de {} : {} octets".format(
                                        protocole, ip,
                                        statistics.mean(
                                            val)))
                                if len(val) >= 2:
                                    print(
                                        "                 *variance taille paquets {} en destination de {} : {} octets".format(
                                            protocole, ip,
                                            statistics.variance(
                                                val)))
                                    print(
                                        "                 *écart-type taille paquets {} en destination de {} : {} octets".format(
                                            protocole, ip,
                                            statistics.stdev(
                                                val)))
                                if "192.168." in ip:
                                    web_app_taille.extend(val)
                                else:
                                    pc_taille.extend(val)

                    if not assez_paquets:
                        print("         -Aucun flux supérieur à 300 paquets pour cette source")

                    for protocole, valeur in valeurs[5]:
                        for ip, val in valeur:
                            if len(val) > 500 or source == "Lib/":
                                print("             ---------INFO TEMPS PAQUETS---------")
                                print(
                                    "                 *temps moyen inter-packets {} en destination de {} : {} ms".format(
                                        protocole, ip,
                                        statistics.mean(
                                            val)))
                                if len(val) >= 2:
                                    print(
                                        "                 *variance temps inter-packets {} en destination de {} : {} ms".format(
                                            protocole, ip,
                                            statistics.variance(
                                                val)))
                                    print(
                                        "                 *écart-type temps inter-packets {} en destination de {} : {} ms".format(
                                            protocole, ip,
                                            statistics.stdev(
                                                val)))
                                if "192.168." in ip:
                                    web_app_temps.extend(val)
                                else:
                                    pc_temps.extend(val)


                    for protocole, valeur in valeurs[4]:
                        for ip, val in valeur:
                            if ip in liste_ip:
                                print("             ---------INFO DUREE FLUX---------")
                                print(
                                    "                 *durée du flux {} en destination de {}: {}".format(protocole, ip,
                                                                                                         val[-1]))
                                duree = val[-1]
                                print(duree)
                                if "192.168." in ip:
                                    pc_duree.append(duree)
                                else:
                                    web_app_duree.append(duree)

                donnee_fichier = [pc_taille, pc_temps, pc_duree, web_app_taille, web_app_temps, web_app_duree]
                liste_par_type.append(donnee_fichier)
            taille_pc = []
            temps_pc = []
            duree_pc = []
            taille_web_app = []
            temps_web_app = []
            duree_web_app = []
            for fichier in liste_par_type:
                taille_pc.extend(fichier[0])
                temps_pc.extend(fichier[1])
                duree_pc.extend(fichier[2])
                taille_web_app.extend(fichier[3])
                temps_web_app.extend(fichier[4])
                duree_web_app.extend(fichier[5])
            donnee_type = {"data": {"taille_pc": taille_pc, "temps_pc": temps_pc, "duree_pc": duree_pc,
                                    "taille_web_app": taille_web_app, "temps_web_app": temps_web_app,
                                    "duree_web_app": duree_web_app}}
            dict_source[type] = donnee_type
        dict[source] = dict_source

print("{} fichiers analysés".format(compteur))

with open('output.json', 'w') as file:
    file.write(json.dumps(dict))

