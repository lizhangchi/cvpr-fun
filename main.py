import os
import json
from datetime import datetime
from funsearch.generator import generate_heuristic
from funsearch.evaluator import evaluate_heuristic, evaluate_routes
from funsearch.data_loader import load_vrp
from funsearch.baseline import baseline_heuristic

if __name__ == '__main__':
    dataset_folder = "data/B"
    os.makedirs("results", exist_ok=True)
    vrp_files = [f for f in os.listdir(dataset_folder) if f.endswith(".vrp")]

    all_results = []

    for filename in vrp_files:
        print(f"\n===== Running on {filename} =====")
        data = load_vrp(os.path.join(dataset_folder, filename))
        customers = list(range(1, len(data['demand'])))
        capacity = data['vehicle_capacities'][0]
        distance_matrix = data['distance_matrix']

        # === 多轮 GPT 搜索 ===
        best_score = float('inf')
        best_code = ""
        NUM_TRIALS = 5

        for i in range(NUM_TRIALS):
            print(f"\n==== Trial {i+1} ====")
            try:
                code = generate_heuristic()
                score = evaluate_heuristic(code, data)
                print(f"Score: {score}")
                if score < best_score:
                    best_score = score
                    best_code = code
                    print("New best found!")
            except Exception as e:
                print(f"Error in Trial {i+1}:", e)

        print("\n==== Best Heuristic Selected ====")
        print(best_code)
        print(f"Final Score: {best_score}")

        # === Baseline ===
        try:
            baseline_routes = baseline_heuristic(customers, data['demand'], capacity, distance_matrix)
            baseline_score = evaluate_routes(baseline_routes, data)
        except Exception as e:
            print("Baseline Evaluation Error:", e)
            baseline_score = float('inf')

        print("\n==== Baseline Score ====")
        print(baseline_score)

        # === 保存结果 ===
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_safe = filename.replace(".vrp", "")
        result = {
            "file": filename,
            "score": best_score,
            "baseline": baseline_score,
            "code": best_code
        }

        try:
            single_path = f"results/{filename_safe}_{timestamp}.json"
            with open(single_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print(f"Saved: {single_path}")
        except Exception as e:
            print("Failed to save result:", e)

        all_results.append(result)


    try:
        summary_path = f"results/summary_{timestamp}.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)
        print(f"\n Summary saved to: {summary_path}")
    except Exception as e:
        print(" Failed to save summary:", e)
