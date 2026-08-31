import pandas as pd
import numpy as np
def parameter (name_parameter = "all"):
    parameter_dict = {
        #mode choice
                      'ASC_bike':-1.5,
                      'ASC_car':0,
                      'mu_mode':1,
                    # 'beta_time':-0.000235, #for toy network
                    # 'beta_time':-0.00005,
                    # 'beta_time':-0.0000075,
                    # 'beta_time':-0.0000005,
                     'beta_time':-0.00005,
                      'max_iter_mode_choice':5,
        #traffic assignement
                      'ta_due_algorithm':'bfw',
                      'ta_sto_algorithm': 'bfsle',
                      'max_iter_ta':500,
                      'tolerance':1e-4,
                      'max_route':3

    }
    if name_parameter == "all":
        return parameter_dict
    else:
        return parameter_dict[name_parameter]

# Coefficient for Bikeability model

_grille_trafic = pd.DataFrame(
    {
        "<6000": [0.4, 0.2, 0.0, 0.0, 0.0],
        "6000-7000": [0.5, 0.4, 0.2, 0.0, 0.0],
        "7000-8000": [0.75, 0.5, 0.4, 0.2, 0.0],
        ">8000": [1.0, 0.75, 0.5, 0.4, 0.0],
    },
    index=[1, 2, 3, 4, 5],
)
_grille_trafic.index.name = "note"
_grille_trafic.columns.name = "flow_car_cat"

TRAFIC_MAPPER = _grille_trafic.unstack()

# Bins et labels
TRAFIC_BINS = [-np.inf, 6000, 7000, 8000, np.inf]
TRAFIC_LABELS = ["<6000", "6000-7000", "7000-8000", ">8000"]

# Dictionnaires de coefficients
COEF_NOTE_MAPS = {
    1: {5: 0.5, 4: 0.75, 3: 1.0, 2: 1.25, 1: 1.5},
    2: {5: 0.75, 4: 1.0, 3: 1.25, 2: 1.75, 1: 2.0},
    3: {5: 1.0, 4: 1.25, 3: 1.5, 2: 1.75, 1: 2.0},
    4: {5: 0.8, 4: 1.0, 3: 1.5, 2: 1.75, 1: 2.0},
    5: {5: 1.0, 4: 1.25, 3: 1.5, 2: 2.0, 1: 2.5},
    6: {5: 1.0, 4: 1.5, 3: 2.0, 2: 2.5, 1: 3.0},
    7: {5: 1.0, 4: 1.75, 3: 2.5, 2: 3.25, 1: 4.0},
    8: {5: 1.0, 4: 2.0, 3: 3.0, 2: 4.0, 1: 5.0},
    9: {5: 1.0, 4: 1.5, 3: 3.0, 2: 6.0, 1: 12.0},
    10: {5: 0.5, 4: 1.0, 3: 3.0, 2: 6.0, 1: 12.0},
    11: {5: 0.5, 4: 0.75, 3: 1.0, 2: 12.0, 1: 24.0},
    12: {5: 0.5, 4: 1.0, 3: 2.0, 2: 3.0, 1: 4.0},
    13: {5: 0.5, 4: 1.0, 3: 3.0, 2: 5.0, 1: 7.0},
    14: {5: 0.2, 4: 0.8, 3: 2.0, 2: 4.0, 1: 6.0},
    15: {5: 0.5, 4: 1.0, 3: 2.0, 2: 4.0, 1: 8.0},
    16: {5: 0.1, 4: 0.2, 3: 0.5, 2: 1.0, 1: 2.0},
    17: {5: 0.1, 4: 1.0, 3: 2.0, 2: 8.0, 1: 15.0},
    18: {5: 0.2, 4: 0.5, 3: 1.0, 2: 3.0, 1: 6.0},
    19: {5: 0.2, 4: 0.3, 3: 1.0, 2: 3.0, 1: 6.0},
    20: {5: 0.2, 4: 0.4, 3: 1.0, 2: 3.0, 1: 6.0},
    21: {5: 0.2, 4: 0.6, 3: 1.0, 2: 3.0, 1: 6.0},
    22: {5: 0.2, 4: 0.75, 3: 1.0, 2: 3.0, 1: 6.0},
    23: {5: 0.2, 4: 0.9, 3: 1.0, 2: 3.0, 1: 6.0}
}