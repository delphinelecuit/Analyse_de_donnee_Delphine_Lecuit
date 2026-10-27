#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math

def ouvrirUnFichier(nom):
    with open(nom, "r", encoding='utf-8') as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

def ordreDecroissant(liste):
    liste.sort(reverse = True)
    return liste

def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if np.isnan(pop[element]) == False:
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop

def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element][1]])
    return classement

# Question 2
print("Question 2")
donnees = ouvrirUnFichier("./data/island-index.csv")

# # Question 3
print("Question 3")
surfaces = list(donnees["Surface (km²)"])
surfaces.append(float(85545323))
surfaces.append(float(37856841))
surfaces.append(float(7768030))
surfaces.append(float(7605049))
# print(len(surfaces))

# # Question 4
print("Question 4")
surfaces_ord = ordreDecroissant(surfaces)

# # Question 5
print("Question 5")
rangs = list(range(1, len(surfaces_ord) + 1))
plt.plot(rangs, surfaces_ord)
plt.xlabel("Rangs")
plt.ylabel("Surfaces (km²)")
plt.title("Visualisation loi rang-taille des surfaces")
plt.savefig("./S5_loi_rang_taille.png")
plt.close()

# # Question 6
print("Question 6")
rangs_log = conversionLog(rangs)
surfaces_log = conversionLog(surfaces_ord)
plt.plot(rangs_log, surfaces_log)
plt.xlabel("Rangs (log)")
plt.ylabel("Surfaces (log km²)")
plt.title("Visualisation loi rang-taille des surfaces")
plt.savefig("./S5_loi_rang_taille_log.png")
plt.close()

# # Question 7
print("Question 7")
# # Non,  il n'est pas possible de faire un test sur les rangs car il n'y a qu'un classement à traiter (les rangs) donc pas de comparaison envisageable. Il n'y aurait pas de pertinence à faire un test statistique sur les rangs.

# # Question 9
print("Question 9")
donnees_1 = ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2026.csv")
# print(donnees_1)

# # Question 10
print("Question 10")
Etat = list(donnees_1["État"])
Pop_2007 = list(pd.to_numeric(donnees_1["Pop 2007"], errors='coerce'))
Pop_2026 = list(pd.to_numeric(donnees_1["Pop 2026"], errors='coerce'))
Dens_2007 = list(pd.to_numeric(donnees_1["Densité 2007"], errors='coerce'))
Dens_2026 = list(pd.to_numeric(donnees_1["Densité 2026"], errors='coerce'))
print(Pop_2007)
print(Pop_2026)
print(Dens_2007)
print(Dens_2026)

# # Question 11
print("Question 11")
Pop_2007_ord = ordrePopulation(Pop_2007, Etat)
Pop_2026_ord = ordrePopulation(Pop_2026, Etat)
Dens_2007_ord = ordrePopulation(Dens_2007, Etat)
Dens_2026_ord = ordrePopulation(Dens_2026, Etat)
print(Pop_2007_ord[-4:])
print(Pop_2026_ord[-4:])
print(Dens_2007_ord[-4:])
print(Dens_2026_ord[-4:])

# # Question 12
print("Question 12")
classement_pop = classementPays(Pop_2007_ord, Pop_2026_ord)
classement_densite = classementPays(Dens_2007_ord, Dens_2026_ord)
# print("Le classement de population se structure selon : ['rang 2007', 'rang 2026', 'Pays'] :", classement_pop)
# print("Le classement de densité de population se structure selon : ['rang 2007', 'rang 2026', 'Pays'] :", classement_densite)
classement_pop.sort()
classement_densite.sort()
print(classement_pop[:5])
print(classement_densite[:5])

# # Question 13
print("Question 13")
rang_pop_2007 = []
rang_pop_2026 = []
for element in range(len(classement_pop)):
    rang_pop_2007.append(classement_pop[element][0])
    rang_pop_2026.append(classement_pop[element][1])
print(rang_pop_2007[:5])
print(rang_pop_2026[:5])
# idem for density
rang_dens_2007 = []
rang_dens_2026 = []
for element in range(len(classement_densite)):
    rang_dens_2007.append(classement_densite[element][0])
    rang_dens_2026.append(classement_densite[element][1])
print(rang_dens_2007[:5])
print(rang_dens_2026[:5])

# # Question 14
print("Question 14")
coeff_correlation_rangs_pop = scipy.stats.spearmanr(rang_pop_2007, rang_pop_2026)
coeff_correlation_rangs_dens = scipy.stats.spearmanr(rang_dens_2007, rang_dens_2026)
concordance_rangs_pop = scipy.stats.kendalltau(rang_pop_2007, rang_pop_2026)
concordance_rangs_dens = scipy.stats.kendalltau(rang_dens_2007, rang_dens_2026)
print("Coefficient de corrélation entre les rangs de population : ")
print(coeff_correlation_rangs_pop)
print("Coefficient de corrélation entre les rangs de densité : ")
print(coeff_correlation_rangs_dens)
print("Concordance des rangs pour la population : ")
print(concordance_rangs_pop)
print("Concordance des rangs pour la densité : ")
print(concordance_rangs_dens)
