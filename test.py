import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams.update({'font.size': 30})

city_name = "Sioux_Falls"
name_test = f"CAP_{city_name}_test_from_scratch_2"
fig, ax = plt.subplots(3, 1, figsize=(30, 30))
fp_nobimodel = f"output/optimization/rgo_results_df_opt_{name_test}.csv"
fp_bimodel = f"output/optimization/rgo_results_df_opt_CAP_Sioux_Falls_BIMODEL_test_from_scratch_2.csv"
df_nobimodel = pd.read_csv(fp_nobimodel)
df_bimodel = pd.read_csv(fp_bimodel)

# Plot primaire
ax[0].plot(df_bimodel["nbr_bike_lanes"], df_bimodel["modal_share_bike"], linewidth=2, label = "Bi model")
ax[0].plot(df_nobimodel["nbr_bike_lanes"], df_nobimodel["modal_share_bike"], linewidth=2, label = "No Bi model")
ax[1].plot(df_bimodel["nbr_bike_lanes"], df_bimodel["flow_of_removed_edge"].iloc[::-1].values, linewidth=2, label = "Bi model")
ax[1].plot(df_nobimodel["nbr_bike_lanes"], df_nobimodel["flow_of_removed_edge"].iloc[::-1].values, linewidth=2, label = "No Bi model")
ax[2].plot(df_bimodel["nbr_bike_lanes"], df_bimodel["average_bi_coef"].values, linewidth=2, label = "Bi model")
ax[2].plot(df_nobimodel["nbr_bike_lanes"], df_nobimodel["average_bi_coef"].values, linewidth=2, label = "No Bi model")

ax[2].set_xlabel("Number of dedicated bike lanes")
ax[0].set_ylabel("Bicycle modal share (%)")
ax[1].set_ylabel("Flow of least used edge")
ax[2].set_ylabel("Average bikeability coefficient")
ax[0].grid(True, alpha=0.3)
ax[1].grid(True, alpha=0.3)
ax[2].grid(True, alpha=0.3)
ax[0].legend(loc="lower right")
ax[1].legend(loc="lower right")
ax[2].legend(loc="lower right")

fig.suptitle("Comparaison of results on Sioux Falls Network, with and without Bikeability Model.")

plt.tight_layout()
plt.savefig(f"output/test_comparaison/comparaison_SF_BIMODEL_NOBIMODEL.png")