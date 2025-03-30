from openai import OpenAI
import re
client = OpenAI(api_key="sk-ac12WLHENXWSRWiTD299F516A904475d916d255d30Ca328b",base_url="https://api.bltcy.ai/v1")
def extract_code_from_response(response_text):
    match = re.search(r"```(?:python)?\s*(.*?)\s*```", response_text, re.DOTALL)
    return match.group(1).strip() if match else response_text.strip()

def generate_heuristic():
    prompt = """
    Write a Python function named heuristic(customers, demand, capacity).

    The function receives:
      - customers: a list of customer indices (e.g., [1,2,3,4])
      - demand: a list of demand values indexed by customer
      - capacity: maximum capacity for a vehicle

    Global variable distance_matrix is available for distance lookup:
      distance_matrix[i][j] gives the distance between customer i and j
    Global variable coordinates is also available:
      coordinates[i] gives the (x, y) location of customer i

    Requirements:
    - All customers must be visited once and only once
    - Each route must start and end at depot (assume depot index = 0)
    - Vehicle must not exceed capacity
    - Do not redefine distance_matrix or coordinates
    - Do not assume customers have .location or object attributes (they are integers)
    - If using numpy inf or masking, make sure distance_matrix is float
    - Avoid set indexing: use next(iter(myset)) instead of myset[0]
    - demand is a list, use demand[i] (not demand.values())
    - If using float('inf'), ensure it's written correctly and closed with quotes
    - If using clustering, use coordinates[i] as (x, y), not just index
    - When selecting next customer, avoid dead loops: filter candidate list first
    - When using float('inf') as key value, ensure the comparison returns a number, not a dict or boolean
    - Before using min() on candidate list, always check the list is non-empty
    - Avoid calling .fit() on a dict (convert coordinates to np.array of shape (n,2))
    - Ensure all routes begin and end with depot 0
    - Do not modify the function signature. The heuristic function must only accept (customers, demand, capacity)
    - Use global coordinates and distance_matrix when needed
    - Do not use min() over a float value; min() requires an iterable.
    - Do not use customers[i] to access coordinates; use coordinates[i] instead.

    Please avoid:
    - Using only nearest-neighbor greedy strategies
    - Copying previous examples

    Encouraged strategies:
    - Start with customers with high demand
    - Apply clustering (like k-means or grid partitioning)
    - Combine route construction with insertion heuristics
    - Use stochastic/randomized route seeding

    Be creative. Make sure the function is valid and returns complete routes

    Return only valid Python code.
    Return: A list of routes (each route is a list of customer indices starting/ending with 0)
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in heuristic design."},
            {"role": "user", "content": prompt}
        ]
    )
    return extract_code_from_response(response.choices[0].message.content)