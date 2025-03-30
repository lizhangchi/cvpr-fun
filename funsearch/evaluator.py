import random
from scipy.cluster.vq import kmeans,vq
import sklearn
from sklearn.cluster import KMeans
import numpy as np

# 重构 evaluator.py 的核心逻辑，分出 evaluate_routes() 和 evaluate_heuristic()

def evaluate_routes(routes, data):
    """通用路线评估函数，用于 baseline 或生成函数返回的 routes"""
    try:
        total_distance = 0
        visited = set()
        for route in routes:
            if not route or route[0] != 0 or route[-1] != 0:
                raise ValueError("Each route must start and end at depot (index 0)")
            for node in route:
                if node is None or not isinstance(node, int):
                    raise ValueError(f"Invalid node in route: {node}")
                if node < 0 or node >= len(data['demand']):
                    raise ValueError(f"Node index out of bounds: {node}")
                if node != 0:
                    if node in visited:
                        raise ValueError(f"Customer {node} visited more than once")
                    visited.add(node)
            load = sum(data['demand'][i] for i in route if i != 0)
            if load > data['vehicle_capacities'][0]:
                return float('inf')
            prev = route[0]
            for node in route[1:]:
                total_distance += data['distance_matrix'][prev][node]
                prev = node
        if len(visited) != len(data['demand']) - 1:
            raise ValueError("Not all customers were visited")
        return total_distance
    except Exception as route_error:
        print("Route Evaluation Error:", route_error)
        return float('inf')


def evaluate_heuristic(heuristic_code, data):
    """对 LLM 生成的启发式代码进行执行与路线评估"""
    import random
    import numpy as np
    import sklearn
    from sklearn.cluster import KMeans
    from scipy.cluster.vq import kmeans, vq

    try:
        code = heuristic_code.encode('ascii', 'ignore').decode()
        global_scope = {
            'random': random,
            'distance_matrix': np.array(data['distance_matrix'], dtype=np.float32),
            'KMeans': KMeans,
            'sklearn': sklearn,
            'np': np,
            'kmeans': kmeans,
            'vq': vq,
            'coordinates': data.get('coordinates', {}),
        }
        local_scope = {}
        exec(code, global_scope, local_scope)
        heuristic = local_scope.get('heuristic')
        if heuristic is None:
            raise ValueError("Heuristic function not defined in the code")
        customers = list(range(1, len(data['demand'])))  # exclude depot 0
        routes = heuristic(customers, data['demand'], data['vehicle_capacities'][0])
        return evaluate_routes(routes, data)
    except Exception as e:
        print("Evaluation Error:", e)
        print("Code was:\n", heuristic_code)
        return float('inf')
