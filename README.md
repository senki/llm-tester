# LLM Testing & Evaluation

This repository provides a Python script for **querying multiple LLMs** via [Ollama](https://ollama.com), **caching** their responses, and **evaluating** those responses with an OpenAI GPT-4 model. It’s useful for automated model benchmarking and comparison.

---

## Features

1. **Multiple LLM Support**
   Reads a list of model names from `config/models.json` and queries each model with predefined prompts.

2. **Prompt Caching**
   Saves each LLM’s response in the `cache` directory to avoid re-running prompts if a file already exists.

3. **Flexible Prompt Configuration**
   Loads prompt text from `config/prompts.json`, which can be updated or extended as needed.

4. **Automated Evaluations**
   Reads an evaluation instruction text from `config/evaluation_prompt.txt`. Sends both the prompts and responses to GPT-4 for automated scoring or assessment, saved in the `results` directory.

---

## Prerequisites

- **Python 3.7+**
- **Ollama** installed locally for running supported models: [Ollama GitHub](https://github.com/ollama/ollama)
- **Environment Variable for OpenAI Key**
  You must have `OPENAI_API_KEY` set in your environment or a `.env` file so that `openai.chat.completions.create(...)` can authenticate. For example:

  ```bash
  export OPENAI_API_KEY=your_openai_key_here
  ```

---

## Installation & Setup

1. **Clone or Download** this repository.
2. **Install Dependencies**:

   ```bash
   pip install openai ollama
   ```

3. **Create or Update Configuration**:
   - **`config/models.json`**: A JSON array of LLM model names. For example:

     ```json
     [
        "gemma", "llama3", "mistral"
     ]
     ```

   - **`config/prompts.json`**: A dictionary of prompt IDs and prompts:

     ```json
     {
        "1": "Explain quantum entanglement in simple terms.",
        "2": "Summarize the impact of AI on the job market.",
        "3": "What are the main differences between GPT-3 and GPT-4?",
        "4": "What is the capital of France?"
     }
     ```

   - **`config/evaluation_prompt.txt`**: A text file containing instructions for how GPT-4 should evaluate the responses. For example:

     ```txt
     Compare the responses and assess their clarity, coherence, factual accuracy, and relevance. Provide a ranking and insights.
     ```

---

## Usage

1. **Run the script**:

   ```bash
   python llm-tester.py.py
   ```

   This will:
   - Read model list from `config/models.json`.
   - Load prompts from `config/prompts.json`.
   - For each model, query each prompt if not already cached in `cache/`.
   - Evaluate the prompts and responses using GPT-4 instructions in `config/evaluation_prompt.txt`.
   - Store the final markdown evaluation in `results/` with a timestamp.

2. **Check Outputs**:
   - **Cached Responses** in `cache/<model_name>/prompt_<id>.txt`
   - **Evaluation Reports** in `results/evaluation_YYYYMMDD_HHMMSS.md`

3. **Rerunning**:
   - If a file already exists in `cache/` for a given model and prompt, the script **skips** re-querying that model. If you want to force re-query, delete the corresponding `.txt` file from `cache/`.
