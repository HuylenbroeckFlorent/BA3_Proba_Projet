'''
	Pour quantifier la qualité d'un traitement d'images pour reconnaître des empreintes digitales, 
	il est courant de mesurer le temps CPU pour reconnaître les empreintes d'une certaine base de données. 
	Trois nouveaux types d'algorithmes ont été testés en ajoutant une part de bruit à ces images de 
	référence. la part de bruit est exprimée en échelle relative (%).  Les résultats ont été repris 
	ci-dessous en détaillant la fraction de détection efficace(%) en fonction du bruit.
	Pouvez-vous en déduire qu'il existe un meilleur algorithme ?
	Justifier votre réponse.
'''
from __future__ import division
import math
import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import norm, kstest, ttest_ind
import copy


alpha=0.05
Dna=1.34
Falpha_2=1.39 # for df1=100 and df2=100
student=1.96

noise_percentage=[]
algorithme_1=[]
algorithme_2=[]
algorithme_3=[]

size=0

def read_data(path):
	global noise_percentage ,algorithme_1 ,algorithme_2 ,algorithme_3
	with open(path,'r') as file:
		content=file.readlines()
		file.close()

	for line in content:
		line=line.split()
		if(int(line[0]) not in noise_percentage):
			algorithme_1.append([])
			algorithme_2.append([])
			algorithme_3.append([])
			noise_percentage.append(int(line[0]))
		k=len(noise_percentage)-1
		algorithme_1[k].append(float(line[1]))
		algorithme_2[k].append(float(line[2]))
		algorithme_3[k].append(float(line[3]))
		
def plot(algo,name):
	for i in range(len(noise_percentage)):
		x_histo=np.arange(min(algo[i]), max(algo[i]))
		x_norm=np.linspace(min(algo[i]), max(algo[i]), len(algo[i]))
		plt.hist(algo[i], bins=x_histo, density=True, align='mid', label='noise = '+str(noise_percentage[i]))
		plt.title(name)
		plt.plot(x_norm, norm.pdf(x_norm,np.mean(algo[i]), np.std(algo[i])), color='r', label='normale')
		plt.legend()
	plt.show()

# Returns a normalized copy of parameter array
def normalize(array):
	array_copy=copy.deepcopy(array)
	avg=np.mean(array_copy)
	sd=np.std(array_copy)
	return [(elem-avg)/sd for elem in array_copy]

def ks_test(array):
	D_statistic, p_value=kstest(normalize(array), 'norm')
	return D_statistic<Dna

def variance_test(array_1, array_2):
	T=(np.var(array_1)/np.var(array_2))
	return T<Falpha_2

def mean_test(array_1, array_2):
	Z=(np.mean(array_1)-np.mean(array_2))/math.sqrt(((np.var(array_1)/100)+(np.var(array_2)/100)))
	return abs(Z)>student

def array_compare_mean(array_1, array_2):
	if np.mean(array_1)<np.mean(array_2):
		return -1
	elif np.mean(array_1)==np.mean(array_2):
		return 0
	else:
		return 1

def algo_compare(algo_1, algo_2):
	compare=0
	for i in range(len(noise_percentage)):
		#print(i)
		if ks_test(algo_1[i]) and ks_test(algo_2[i]):
			#print("passe ici")
			if variance_test(algo_1[i],algo_2[i]):
				#print("passe la")
				if not mean_test(algo_1[i],algo_2[i]):
					#print("teste ca : ",array_compare_mean(algo_1[i],algo_2[i]))
					compare+=array_compare_mean(algo_1[i],algo_2[i])
			else:
				#print("passe plutot ici, resultat : ",array_compare_mean(algo_1[i],algo_2[i]))
				compare+=array_compare_mean(algo_1[i],algo_2[i])
	return compare

		
def main():
	read_data('./QI8_donnee.dat')
	print(algo_compare(normalize(algorithme_1),normalize(algorithme_2)))
	print(algo_compare(normalize(algorithme_3),normalize(algorithme_2)))
	print(algo_compare(normalize(algorithme_1),normalize(algorithme_3)))

	#plot(algorithme_1, "Algorithme 1")
	#plot(algorithme_2, "Algorithme 2")
	#plot(algorithme_3, "Algorithme 3")

main()