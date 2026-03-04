import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ASC_bike = -2.5
ASC_car = 0

mu_mode = 1
mu_route = 1

time_path1 = 2000
time_path2 = 3000
time_path3 = 3000

speed_car = 20 / 3.6
speed_bike = 15 / 3.6

beta_time = -0.000235
liste_beta_time = np.arange(start=-0.004,stop=0,step=0.00001)


df_result = pd.DataFrame(columns=["beta_time","proba_path1","proba_path2","proba_path3"])
liste_proba_path1 = []
liste_proba_path2 = []
liste_proba_path3 = []

for beta_time in liste_beta_time:
    utility_path1 = ASC_car+beta_time*time_path1
    utility_path2 = ASC_car+beta_time*time_path2
    utility_path3 = ASC_car+beta_time*time_path3

    exp_path1 = np.exp(mu_mode*utility_path1)
    exp_path2 = np.exp(mu_mode*utility_path2)
    exp_path3 = np.exp(mu_mode*utility_path3)

    proba_path1 = exp_path1/(exp_path1+exp_path2+exp_path3)
    proba_path2 = exp_path2/(exp_path1+exp_path2+exp_path3)
    proba_path3 = exp_path3/(exp_path1+exp_path2+exp_path3)

    liste_proba_path1.append(proba_path1)
    liste_proba_path2.append(proba_path2)
    liste_proba_path3.append(proba_path3)

df_result["beta_time"]=liste_beta_time
df_result["proba_path1"]=liste_proba_path1
df_result["proba_path2"]=liste_proba_path2
df_result["proba_path3"]=liste_proba_path3

df_result.plot.area(x="beta_time", y=["proba_path1", "proba_path2", "proba_path3"])
plt.yticks(np.linspace(0,1,21))
plt.grid(True)
plt.title("Probabilities of each path for different beta time")
plt.show()

beta_time = -0.0025
liste_ASC_bike = np.arange(start=-10,stop=10,step=0.1)


time_car = 3000
time_bike = 3000

df_result = pd.DataFrame(columns=["ASC_bike","proba_car","proba_bike"])
liste_proba_car = []
liste_proba_bike = []

for ASC_bike in liste_ASC_bike:
    utility_car = ASC_car+beta_time*time_car
    utility_bike = ASC_bike+beta_time*time_bike

    exp_car = np.exp(mu_mode*utility_car)
    exp_bike = np.exp(mu_mode*utility_bike)

    proba_car = exp_car/(exp_car+exp_bike)
    proba_bike = exp_bike/(exp_car+exp_bike)

    liste_proba_car.append(proba_car)
    liste_proba_bike.append(proba_bike)

df_result["ASC_bike"]=liste_ASC_bike
df_result["proba_car"]=liste_proba_car
df_result["proba_bike"]=liste_proba_bike

df_result.plot.area(x="ASC_bike", y=["proba_car", "proba_bike"])
plt.yticks(np.linspace(0,1,21))
plt.grid(True)
plt.title(f"Probabilities of each model for different ASC bike (beta_time={beta_time})")
plt.show()

