from openai import OpenAI
import re
client = OpenAI(api_key="sk-ac12WLHENXWSRWiTD299F516A904475d916d255d30Ca328b",base_url="https://api.bltcy.ai/v1")
def extract_code_from_response(response_text):
    match = re.search(r"```(?:python)?\s*(.*?)\s*```", response_text, re.DOTALL)
    return match.group(1).strip() if match else response_text.strip()

def mutate_heuristic(original_code):
    prompt = f"""
    Improve or redesign the following Python heuristic function for capacitated vehicle routing.
    You can explore strategies like:
    - distance-based sorting
    - nearest-neighbor construction
    - randomized assignment
    - clustering approaches

    Assume distance_matrix is available as a global variable.
    Return only clean Python code.
    {original_code}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a heuristic optimization expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return extract_code_from_response(response.choices[0].message.content)