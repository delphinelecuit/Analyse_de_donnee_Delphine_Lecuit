#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats

# C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
# Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
# Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

# Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(nom):
    with open(nom, "r", encoding="utf-8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu 
# print(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))
# #./data/ pour que python sache où est le fichier par rapport à main.py. Le fichier est dans le dossier data.

# Question 1 : Théorie de l'échantillonnage (intervalles de fluctuation)
# L'échantillonnage se base sur la répétitivité.
print("Question 1")
## Travail données echantillonnage 100 
donnees_100 = ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv")
Pour_100 = []
for x in donnees_100["Pour"]:
    Pour_100.append(x)
Contre_100 = []
for x in donnees_100["Contre"]:
    Contre_100.append(x)
Sans_op_100 = []
for x in donnees_100["Sans opinion"]:
    Sans_op_100.append(x)
moy_pour_100 = round(sum(Pour_100) / len(Pour_100))
moy_contre_100 = round(sum(Contre_100) / len(Contre_100))
moy_sans_op_100 = round(sum(Sans_op_100) / len(Sans_op_100))
print("Moyenne POUR, 100 échantillons :", moy_pour_100)
print("Moyenne CONTRE, 100 échantillons :", moy_contre_100)
print("Moyenne SANS OPINION, 100 échantillons :", moy_sans_op_100)
## calcul fréquences
somme_moy = moy_pour_100 + moy_contre_100 + moy_sans_op_100
fq_pour_100 = round((moy_pour_100 / somme_moy),2)
fq_contre_100 = round((moy_contre_100 / somme_moy),2)
fq_sans_op_100 = round((moy_sans_op_100 / somme_moy),2)
print("Fréquence POUR, 100 échantillons :", fq_pour_100)
print("Fréquence CONTRE, 100 échantillons :", fq_contre_100)
print("Fréquence SANS OPINION, 100 échantillons :", fq_sans_op_100)
## Idem population réelle
donnees_Pop_tot = ouvrirUnFichier("./data/Echantillonnage-Population-reelle.csv")
Pour_tot = 852
Contre_tot = 911
Sans_op_tot = 422
## Frequences population réelle
somme_tot = Pour_tot + Contre_tot + Sans_op_tot
fq_pour = round((Pour_tot / somme_tot),2)
fq_contre = round((Contre_tot / somme_tot),2)
fq_sans_op = round((Sans_op_tot / somme_tot),2)
print("Fréquence POUR, population réelle:", fq_pour)
print("Fréquence CONTRE, population réelle:", fq_contre)
print("Fréquence SANS OPINION, population réelle:", fq_sans_op)
## Intervalles de fluctuation
n = 1000
zc = 1.96
def intervalle_fluc(p, n, zc):
    borne = zc * math.sqrt((p * (1 - p)) / n)
    return (p - borne, p + borne)
## création des variables p sans arrondis
p_POUR = Pour_tot / somme_tot
p_CONTRE = Contre_tot / somme_tot
p_SANS_OP = Sans_op_tot / somme_tot
## intervalles de fluctuation "bruts"
bas_pour, haut_pour = intervalle_fluc(p_POUR, n, zc)
bas_contre, haut_contre = intervalle_fluc(p_CONTRE, n, zc)
bas_sans_op, haut_sans_op = intervalle_fluc(p_SANS_OP, n, zc)
## intervalles de fluctuation arrondis
print("Intervalle de fluctuation POUR :", "[", round(bas_pour, 2), "; ", round(haut_pour, 2), "]")
print("Intervalle de fluctuation CONTRE :", "[", round(bas_contre, 2), "; ", round(haut_contre, 2), "]")
print("Intervalle de fluctuation SANS OPINION :", "[", round(bas_sans_op, 2), "; ", round(haut_sans_op, 2), "]")
# # print("Résultat sur le calcul d'un intervalle de fluctuation")

# Question 2 : Théorie de l'estimation (intervalles de confiance)
# L'estimation se base sur l'effectif.
print("Question 2")
echant_1 = list(donnees_100.iloc[0])
fq_POUR_1 = (echant_1[0] / sum(echant_1))
fq_CONTRE_1 = (echant_1[1] / sum(echant_1))
fq_SANS_OP_1 = (echant_1[2] / sum(echant_1))
print("Echantillon 1", echant_1)
print("Fréquence POUR, échantillon 1 :", fq_POUR_1)
print("Fréquence CONTRE, échantillon 1 :", fq_CONTRE_1)
print("Fréquence SANS OPINION, échantillon 1 :", fq_SANS_OP_1)
## Intervalles de confiance
bas_POUR_1, haut_POUR_1 = intervalle_fluc(fq_POUR_1, sum(echant_1), zc)
bas_CONTRE_1, haut_CONTRE_1 = intervalle_fluc(fq_CONTRE_1, sum(echant_1), zc)
bas_SANS_OP_1, haut_SANS_OP_1 = intervalle_fluc(fq_SANS_OP_1, sum(echant_1), zc)
print("Intervalle de confiance POUR :", "[", round(bas_POUR_1, 2), "; ", round(haut_POUR_1, 2), "]")
print("Intervalle de confiance CONTRE :", "[", round(bas_CONTRE_1, 2), "; ", round(haut_CONTRE_1, 2), "]")
print("Intervalle de confiance SANS OPINION :", "[", round(bas_SANS_OP_1, 2), "; ", round(haut_SANS_OP_1, 2), "]")

# print("Résultat sur le calcul d'un intervalle de confiance")

# Question 3 : Théorie de la décision (tests d'hypothèse)
# La décision se base sur la notion de risques alpha et bêta.
# Comme à la séance précédente, l'ensemble des tests se trouve au lien : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Question 3")
test_1 = ouvrirUnFichier("./data/Loi-normale-Test-1.csv")
test_2 = ouvrirUnFichier("./data/Loi-normale-Test-2.csv")
# print(test_1.head())
# print(test_1.columns)
# print(test_2.head())
# print(test_2.columns)
resultat_1 = scipy.stats.shapiro(test_1["Test"])
resultat_2 = scipy.stats.shapiro(test_2["Test"])
print("Shapiro Test 1 :", resultat_1)
print("Shapiro Test 2 :", resultat_2)
print("p-value Test 1 :", resultat_1[1])
print("p-value Test 2 :", resultat_2[1])
# print("Théorie de la décision")

# # Question bonus
# print("Question bonus")
