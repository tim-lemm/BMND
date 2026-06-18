from PIL import Image
import glob
import re

scenario = "CAP_2_corner_2_4000_bi2"
main_folder = f"output/optimization/images/{scenario}/"
folder = main_folder + "network/*.png"

files = glob.glob(folder)

def extraire_numero(nom_fichier):
    match = re.search(r"networks_budget_(\d+)", nom_fichier)
    return int(match.group(1)) if match else 0

files = sorted(files, key=extraire_numero)

images = [Image.open(f) for f in files]

images[0].save(main_folder + f"{scenario}.gif", save_all=True, append_images=images[1:], duration=500, loop=0)