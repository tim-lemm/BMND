def convert_to_eaquilibrae_od_matrix(od_matrix):
    od_long = od_matrix.stack().reset_index()
    od_long.columns = ["origin", "destination", "demand"]
    return od_long


def convert_from_aequilibrae_od_matrix(od_long):
    od_matrix = od_long.pivot(index="origin", columns="destination", values="demand")
    od_matrix.index.name = None
    od_matrix.columns.name = None
    return od_matrix