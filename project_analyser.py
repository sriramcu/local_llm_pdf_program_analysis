import os
import argparse
from datetime import datetime
from utils import run_prompts_on_text_llm
import time

def generate_folder_structure(root_folder):
    """
    Generates a text-based tree representation of the folder structure.
    """
    folder_structure = []
    for root, dirs, files in os.walk(root_folder):
        level = root.replace(root_folder, '').count(os.sep)
        indent = ' ' * 4 * level
        folder_structure.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            folder_structure.append(f"{sub_indent}{f}")
    return "\n".join(folder_structure)


def generate_project_prompt(root_folder) -> list[dict]:
    """
    Creates a prompt for analyzing the structural and content details of a coding project.
    """
    messages = []

    # System prompt
    system_prompt = (
        "You are a highly intelligent assistant. Your task is to analyze the structure and contents of a coding project."
        " Each filename is provided by the user (in the format 'Filename:<filepath>'), followed by its contents."
        " Examine the project and explain how it works. "
        " Your initial response should be concise (no more than 300 words)."
    )
    messages.append({"role": "system", "content": system_prompt})

    # Folder structure
    folder_structure = generate_folder_structure(root_folder)
    messages.append({
        "role": "user",
        "content": f"### Folder Structure of '{root_folder}':\n\n{folder_structure}"
    })

    # File contents
    for root, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except Exception as e:
                file_content = f"Could not read file due to error: {str(e)}"

            messages.append({
                "role": "user",
                "content": f"### Filename: {os.path.relpath(file_path, root_folder)}\n\nContents:\n\n{file_content}"
            })

    return messages


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze coding projects and generate a summary.")
    parser.add_argument(
        '--project_folder', type=str, required=True, help="Path to the folder containing the coding project."
    )
    parser.add_argument(
        '--suffix', type=str, default=None, help="Suffix for the output file. If blank, will use a timestamp."
    )
    parser.add_argument(
        '--interactive', action='store_true', help="Enter an interactive loop for further inputs after initial analysis."
    )
    return parser.parse_args()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    args = parse_args()

    print("Generating project analysis prompt...")
    messages = generate_project_prompt(args.project_folder)

    start_time = time.time()
    print("Prompt generated. Running the analysis...")
    model_output = run_prompts_on_text_llm(messages)

    print("Model Output:\n")
    print(model_output)

    # Save the results
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    if args.suffix:
        suffix = args.suffix.strip()
        if suffix.endswith("*"):
            suffix = suffix[:-1] + "_" + timestamp
    else:
        suffix = timestamp
        
    os.makedirs("model_outputs", exist_ok=True)
    output_filepath = os.path.join("model_outputs", f"project_analysis_{suffix}.txt")

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write("Prompts:\n")
        for message in messages:
            f.write(f"{message['role']}:\n{message['content']}\n\n")
        f.write("\nModel Output:\n\n")
        f.write(model_output)
        
    print(f"\nPrompt response completed in {round(time.time() - start_time, 2)} seconds.")

    print(f"Output saved to '{output_filepath}'")
    # Interactive loop for additional inputs
    if args.interactive:
        print("Entering interactive mode. Type 'exit' to quit.")
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                print("Exiting interactive mode.")
                break

            # Append user input to messages
            messages.append({"role": "user", "content": user_input})

            # Get model response
            new_output = run_prompts_on_text_llm(messages)
            print(f"Assistant: {new_output}")

            # Append assistant response for continuity
            messages.append({"role": "assistant", "content": new_output})


if __name__ == "__main__":
    main()
