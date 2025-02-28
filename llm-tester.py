import json
import ollama
import os
from datetime import datetime


def load_prompts(prompt_file):
    with open(prompt_file, "r") as file:
        return json.load(file)


def query_ollama(llm_name, prompt):
    response = ollama.chat(model=llm_name, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()


def safe_filename(llm_name, prompt_id, cache_dir):
    llm_safe_name = llm_name.replace(":", "-")
    output_path = os.path.join(cache_dir, llm_safe_name)
    os.makedirs(output_path, exist_ok=True)
    return os.path.join(output_path, f"prompt_{prompt_id}.txt")


def save_response(llm_name, prompt_id, response, cache_dir):
    filename = safe_filename(llm_name, prompt_id, cache_dir)
    with open(filename, "w") as file:
        file.write(response)
    return filename


def evaluate_with_chatgpt(responses, evaluation_prompt, prompt_file):
    prompts = load_prompts(prompt_file)
    messages = [{"role": "system", "content": evaluation_prompt}]
    for id, response in responses.items():
        prompt = prompts[id]
        messages.append({"role": "user", "content": f"Prompt {id}:\n{prompt}"})
        messages.append({"role": "user", "content": f"Response to prompt {id}:\n{response}"})

    # Debug output messages
    # print(messages)

    return query_ollama("deepseek-r1", messages)


def save_evaluation(llm_name, evaluation, result_dir):
    os.makedirs(result_dir, exist_ok=True)
    filename = os.path.join(result_dir, f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(filename, "w") as file:
        file.write(f"# Evaluation for {llm_name}\n\n")
        file.write(evaluation)
        file.write("\n")
    return filename


def main(prompt_file, evaluate_file, llm_names, cache_dir, result_dir):
    prompts = load_prompts(prompt_file)

    with open(evaluate_file, "r") as file:
        evaluation_prompt = file.read()

    for llm_name in llm_names:
        responses = {}
        for prompt_id, prompt in prompts.items():
            filename = safe_filename(llm_name, prompt_id, cache_dir)
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                print(f"Skipping {llm_name} for prompt {prompt_id}, response already exists.")
                with open(filename, "r") as file:
                    responses[prompt_id] = file.read()
                continue

            print(f"Querying {llm_name} with prompt {prompt_id}...")
            response = query_ollama(llm_name, prompt)
            save_response(llm_name, prompt_id, response, cache_dir)
            responses[prompt_id] = response

        print(f"Evaluating {llm_name} responses...")
        evaluation = evaluate_with_chatgpt(responses, evaluation_prompt, prompt_file)
        eval_filename = save_evaluation(llm_name, evaluation, result_dir)
        print(f"Evaluation saved to: {eval_filename}")


if __name__ == "__main__":
    prompt_path = "config/prompts.json"
    evaluate_path = "config/evaluation_prompt.txt"
    with open("config/models.json", "r") as file:
        llm_list = json.load(file)
    cache_dir = "cache"
    result_dir = "results"
    main(prompt_path, evaluate_path, llm_list, cache_dir, result_dir)
