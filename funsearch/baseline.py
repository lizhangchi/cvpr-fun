def baseline_heuristic(customers, demand, capacity, distance_matrix):
    routes = []
    unvisited = set(customers)
    
    while unvisited:
        route = [0]  # Start from depot
        current_capacity = 0
        current_location = 0

        while True:
            candidates = [c for c in unvisited if current_capacity + demand[c] <= capacity]
            if not candidates:
                break

            # Select the nearest customer
            next_customer = min(candidates, key=lambda x: distance_matrix[current_location][x])
            route.append(next_customer)
            current_capacity += demand[next_customer]
            unvisited.remove(next_customer)
            current_location = next_customer

        route.append(0)  # Return to depot
        routes.append(route)

    return routes

