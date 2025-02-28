import ollama
import os
import sys
from datetime import datetime


def main():
    results_dir = "results"

    if not os.path.isdir(results_dir):
        print(f"Error: Directory not found: {results_dir}")
        sys.exit(1)

    # Collect all evaluations from the results folder
    evaluations = []
    for file_name in os.listdir(results_dir):
        if file_name.startswith("evaluation_") and file_name.endswith(".md"):
            file_path = os.path.join(results_dir, file_name)
            with open(file_path, "r") as eval_file:
                content = eval_file.read().strip()
                evaluations.append((file_name, content))

    if not evaluations:
        print("No evaluation files found.")
        sys.exit(0)

    # Prepare messages
    messages = [
        {
            "role": "system",
            "content": "Compare and contrast the tested LLMs based on the evaluations provided. Determine the overall winner.",
        }
    ]

    for filename, content in evaluations:
        messages.append({"role": "user", "content": f"Evaluation file: {filename}\n---\n{content}"})

    # Call OpenAI
    try:
        response = ollama.chat(model="deepseek-r1", messages=[{"role": "user", "content": messages}])
        comparison_output = response["message"]["content"].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

    # Save combined comparison
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(results_dir, f"comparison_{timestamp}.md")
    with open(output_file, "w") as f:
        f.write("# Overall LLM Comparison\n\n")
        f.write(comparison_output)

    print(f"Comparison summary saved to: {output_file}")


if __name__ == "__main__":
    main()
