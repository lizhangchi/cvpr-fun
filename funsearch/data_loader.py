import numpy as np
import re

def load_vrp(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    dimension = 0
    capacity = 0
    node_coord_section = False
    demand_section = False
    depot_section = False
    coordinates = {}
    demand = {}
    depot_index = 0

    for line in lines:
        line = line.strip()
        if line.startswith("DIMENSION"):
            dimension = int(re.findall(r"\d+", line)[0])
        elif line.startswith("CAPACITY"):
            capacity = int(re.findall(r"\d+", line)[0])
        elif line.startswith("NODE_COORD_SECTION"):
            node_coord_section = True
            continue
        elif line.startswith("DEMAND_SECTION"):
            node_coord_section = False
            demand_section = True
            continue
        elif line.startswith("DEPOT_SECTION"):
            demand_section = False
            depot_section = True
            continue
        elif line.startswith("EOF"):
            break

        if node_coord_section:
            parts = list(map(float, line.split()))
            if len(parts) >= 3:
                coordinates[int(parts[0])] = (parts[1], parts[2])
        elif demand_section:
            parts = list(map(int, line.split()))
            if len(parts) == 2:
                demand[parts[0]] = parts[1]
        elif depot_section:
            depot_index = int(line)

    # Build distance matrix
    coords = [coordinates[i] for i in range(1, dimension + 1)]
    distance_matrix = np.zeros((dimension, dimension))
    for i in range(dimension):
        for j in range(dimension):
            distance_matrix[i][j] = np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))

    demand_list = [demand[i] for i in range(1, dimension + 1)]

    return {
        'coordinates': coords,
        'distance_matrix': distance_matrix.tolist(),
        'demand': demand_list,
        "vehicle_capacities": [capacity]
    }

