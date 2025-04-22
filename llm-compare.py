import openai
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
            "content": (
                "You are an expert LLM evaluator. "
                "I’m going to give you several separate evaluation reports, "
                "and I’d like you to synthesize them into one coherent comparative analysis. "
                "Highlight each model’s strengths, weaknesses, similarities, and differences."
            ),
        }
    ]

    for idx, eval_text in enumerate(evaluations, start=1):
        messages.append({"role": "user", "content": f"Evaluation #{idx}:\n{eval_text}"})

    messages.append(
        {
            "role": "user",
            "content": ("Now, please produce a comprehensive comparison report based on the above evaluations."),
        }
    )
    # Call OpenAI
    try:
        response = openai.chat.completions.create(model="gpt-4.1", messages=messages, temperature=0.3)
        comparison_output = response.choices[0].message.content
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
