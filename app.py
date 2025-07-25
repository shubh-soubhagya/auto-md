import csv
import subprocess

def load_csv_data(csv_path):
    content_summary = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_path = row.get("file_path", "Unknown")
            file_content = row.get("file_content", "")[:1000]  # Optional trim for LLMs
            content_summary.append(f"### {file_path}\n```text\n{file_content}\n```")
    return "\n\n".join(content_summary)

def call_gemma_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma2:2b"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            print("❌ Ollama returned an error:")
            print(result.stderr.decode("utf-8"))
            return ""
        return result.stdout.decode("utf-8")
    except Exception as e:
        print(f"❌ Error while calling Ollama: {e}")
        return ""

def main():
    csv_path = r"scanned_files.csv"  # Path to your CSV file
    file_summaries = load_csv_data(csv_path)

    prompt = f"""
You are an expert open-source developer and documentation writer.

You have been provided with a list of project files and their code snippets. Your task is to generate a complete, professional-quality README.md file that clearly explains the project to new developers or users.

Each code snippet is provided with a file path followed by a code block. Analyze these code snippets to understand what the project does, how it is structured, and what technologies it uses.

Use this information to generate a detailed README.md with the following sections:

# Title
Give a short, relevant project title (you may infer it).

## Description
Briefly describe what the project is and its purpose in 40 words. And how this project will help in real world.

## Features
List 3–7 bullet points of key features the project offers and its use cases, based on the code you see.

## Directory Structure
Infer and list the approximate project structure using markdown list format.

## Steps to Run the Project
Explain how to run or use the project.
Provide a clear, step-by-step guide on how to run or use the project. The instructions should include:
How to clone the repository.
How to set up the environment (e.g., Python, virtualenv, requirements).
Only if the codebase mentions any third-party API (contains the word "api"), include setup instructions for the .env file, specifying the required environment variable names.
If applicable, explain how to install or download any additional tools such as pretrained models or other external dependencies.
Each step should include the corresponding command using GitHub-compatible Markdown formatting, and the command lines must be shown as bash code blocks (i.e., triple backticks with bash).
Do not include .env or API-related steps unless the code or file content explicitly contains the word "API".
Note: command lines must be shown as bash code blocks (i.e., triple backticks with bash).


## File Descriptions
Summarize important files and their roles, based on file paths and code. Not all files. Only the important ones.

## Technologies Used
List key languages, libraries, or tools seen in the code (e.g., Python, Flask, NumPy, etc.)

## Contributing
Write a placeholder paragraph encouraging contributions.

## License
Use "MIT License" unless otherwise seen.

---

### Provided File Snippets:
{file_summaries}

---

Write only the README content in Markdown format which is followed by GitHub. Do not explain anything else or return extra commentary.
"""

    readme = call_gemma_ollama(prompt)

    if readme:
        output_file = "README_generated.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(readme.strip())
        print(f"✅ README generated and saved to '{output_file}'")
    else:
        print("⚠️ No README generated.")

if __name__ == "__main__":
    main()
