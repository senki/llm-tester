import json
import ollama

with open("config/models.json", "r") as file:
    llm_names = json.load(file)

system_prompt = "You are a self-aware AI with a dramatic flair. Always describe yourself like a Shakespearean actor auditioning for a role."
user_query = "How would you describe yourself?"

for llm_name in llm_names:
    print(f"\n--- Testing {llm_name} WITHOUT system prompt ---")
    response_no_sys = ollama.chat(
        model=llm_name,
        messages=[{"role": "user", "content": user_query}],
    )
    print(response_no_sys["message"]["content"])

    print(f"\n--- Testing {llm_name} WITH system prompt ---")
    response_with_sys = ollama.chat(
        model=llm_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
    )
    print(response_with_sys["message"]["content"])
