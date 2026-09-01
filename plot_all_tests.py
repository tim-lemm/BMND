import os
import matplotlib

matplotlib.use("TkAgg")
from PIL import Image
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd

# Style global
plt.rcParams.update({"font.size": 11})

# Dictionnaire de correspondance Coef / Notes
from config import COEF_NOTE_MAPS

# Paramètres
list_ASC_bike = [-2]
beta_time = -0.001
list_coef_map_num = list(range(1, 30))
city_name = "Sioux_Falls"
horodatage = "2026-08-27_14-16-45"
ASC_bike = list_ASC_bike[0]

# 1. Chargement préalable des données
data_dict = {}
for coef in list_coef_map_num:
    name_test = f"CAP_{city_name}_test_{beta_time}_{ASC_bike}_bi_{coef}"
    filename = f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv"
    if os.path.exists(filename):
        data_dict[coef] = pd.read_csv(filename)

if not data_dict:
    raise FileNotFoundError("Aucun fichier CSV de données n'a été trouvé.")

available_coefs = list_coef_map_num

# 2. Layout GridSpec : 3 Graphiques à gauche, Image (haut droite) + Tableau (bas droite)
fig = plt.figure(figsize=(18, 12))
gs = gridspec.GridSpec(
    4,
    2,
    width_ratios=[1, 1.2],
    left=0.06,
    right=0.98,
    top=0.93,
    bottom=0.06,
    wspace=0.25,
    hspace=0.25,
)

ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[1, 0], sharex=ax0)
ax2 = fig.add_subplot(gs[2, 0], sharex=ax0)
axes_metrics = [ax0, ax1, ax2]

ax_img = fig.add_subplot(gs[0:3, 1])  # 2 premiers tiers à droite
ax_img.axis("off")

ax_table = fig.add_subplot(gs[3, 1])  # Dernier tiers à droite pour le tableau
ax_table.axis("off")

fig.suptitle(f"Test parametres for {city_name}", fontsize=14, fontweight="bold")

# 3. Tracé des courbes et métriques
lines_dict = {}  # { coef: [line_ax0, line_ax1, line_ax2] }
metrics = ["modal_share_bike", "average_bi_coef", "flow_of_removed_edge"]
labels_y = [
    "Bicycle modal share (%)",
    "Average Bikeability coef",
    "Flow of removed edge",
]

for coef, df in data_dict.items():
    l0 = ax0.plot(
        df["nbr_bike_lanes"], df["modal_share_bike"], label=f"Coef {coef}"
    )[0]
    l1 = ax1.plot(
        df["nbr_bike_lanes"], df["average_bi_coef"], label=f"Coef {coef}"
    )[0]
    l2 = ax2.plot(
        df["nbr_bike_lanes"], df["flow_of_removed_edge"], label=f"Coef {coef}"
    )[0]
    lines_dict[coef] = [l0, l1, l2]

for idx, ax in enumerate(axes_metrics):
    ax.set_ylabel(labels_y[idx])
    ax.grid(True, alpha=0.3)

axes_metrics[2].set_xlabel("Number of dedicated bike lanes")

# 4. Lignes verticales rouges synchronisées
vlines = [
    ax.axvline(x=1, color="red", linestyle="--", alpha=0.8, zorder=15)
    for ax in axes_metrics
]

# 5. Infobulles (Annotations) pour chaque axe
annots = []
for ax in axes_metrics:
    an = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(15, 15),
        textcoords="offset points",
        bbox=dict(
            boxstyle="round,pad=0.5", fc="white", lw=1.5, alpha=0.9
        ),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=0"
        ),
        zorder=20,
    )
    an.set_visible(False)
    annots.append(an)

# 6. Image initiale
initial_coef = 1
initial_i = 1


def get_image_path(nbr_lanes, coef):
    return f"output/optimization/test_parametres/{horodatage}/images/CAP_{city_name}_test_{beta_time}_{ASC_bike}_bi_{coef}/network/networks_budget_{nbr_lanes}_CAP_{city_name}_test_{beta_time}_{ASC_bike}_bi_{coef}.png"


path_init = get_image_path(initial_i, initial_coef)
img_data = (
    Image.open(path_init)
    if os.path.exists(path_init)
    else Image.new("RGB", (400, 400), color="gray")
)
img_display = ax_img.imshow(img_data)
ax_img.set_title(
    f"Network (Budget: {initial_i}, Bi Model: {initial_coef})", fontsize=11
)

# 7. Sliders (Indexés sur les coefs disponibles)
ax_slider_i = plt.axes([0.15, 0.08, 0.7, 0.035])
ax_slider_coef = plt.axes([0.15, 0.04, 0.7, 0.035])

slider_i = Slider(
    ax_slider_i, "Budget (Number of bike lanes)", 1, 75, valinit=initial_i, valstep=1
)
slider_coef = Slider(
    ax_slider_coef,
    "Bi Model",
    1,
    29,
    valinit=1,
    valstep=1,
)


# Function d'affichage du tableau des coefficients
def display_table(selected_coef):
    ax_table.clear()
    ax_table.axis("off")

    notes_map = COEF_NOTE_MAPS.get(selected_coef, {})
    if notes_map:
        headers = ["Note", "5", "4", "3", "2", "1"]
        weights = [
            f"{notes_map.get(k, '-'):.2f}" for k in [5, 4, 3, 2, 1]
        ]
        cell_text = [weights]

        tbl = ax_table.table(
            cellText=cell_text,
            colLabels=headers[1:],
            rowLabels=["Coef"],
            loc="center",
            cellLoc="center",
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        tbl.scale(1.0, 1.0)
        ax_table.set_title(
            f"Coef mapping for Bi Model {selected_coef}",
            fontsize=11,
            pad=10,
        )


# 8. Fonction globale de mise à jour (via sliders)
def update(val=None):
    nbr_lanes = int(slider_i.val)
    idx_coef = int(slider_coef.val)
    selected_coef = available_coefs[idx_coef - 1]

    # A. Mise à jour des lignes verticales rouges
    for line in vlines:
        line.set_xdata([nbr_lanes, nbr_lanes])

    # B. Mise en valeur de la courbe sélectionnée
    for coef, lines in lines_dict.items():
        is_selected = coef == selected_coef
        for line in lines:
            line.set_linewidth(3.5 if is_selected else 1.2)
            line.set_alpha(1.0 if is_selected else 0.25)
            line.set_zorder(10 if is_selected else 2)

    # C. Mise à jour de l'image
    img_path = get_image_path(nbr_lanes, selected_coef)
    if os.path.exists(img_path):
        img_display.set_data(Image.open(img_path))
        ax_img.set_title(
            f"Network (Budget: {nbr_lanes}, Bi Model: {selected_coef})",
            fontsize=11,
        )
    else:
        ax_img.set_title(
            f"Image introuvable : Budget {nbr_lanes}, Bi Model {selected_coef}",
            color="red",
            fontsize=10,
        )

    # D. Mise à jour du tableau
    display_table(selected_coef)

    fig.canvas.draw_idle()


# 9. Événement : Survol pour afficher l'infobulle
def on_move(event):
    for an in annots:
        an.set_visible(False)

    if (
        event.inaxes in axes_metrics
        and event.xdata is not None
        and event.ydata is not None
    ):
        idx = axes_metrics.index(event.inaxes)
        nbr_lanes = int(round(event.xdata))

        idx_coef = int(slider_coef.val)
        selected_coef = available_coefs[idx_coef - 1]
        df = data_dict.get(selected_coef)

        if df is not None:
            row = df[df["nbr_bike_lanes"] == nbr_lanes]
            if not row.empty:
                col_name = metrics[idx]
                val = row[col_name].values[0]

                curr_annot = annots[idx]
                curr_annot.set_text(f"{val:.4f}")
                curr_annot.xy = (nbr_lanes, val)
                curr_annot.set_visible(True)
                fig.canvas.draw_idle()
                return

    fig.canvas.draw_idle()


# 10. Événement : Clic pour déplacer le slider i
def on_click(event):
    if event.inaxes in axes_metrics and event.xdata is not None:
        nbr_lanes = int(round(event.xdata))
        slider_i.set_val(nbr_lanes)


# Connexion des événements
slider_i.on_changed(update)
slider_coef.on_changed(update)
fig.canvas.mpl_connect("button_press_event", on_click)
fig.canvas.mpl_connect("motion_notify_event", on_move)

# Initialisation du style des courbes et du tableau au lancement
update()

plt.show()