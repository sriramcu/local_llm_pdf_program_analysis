import os
import time
import json
import argparse
from datetime import datetime
from utils import run_prompts_on_text_llm, convert_pdf_to_markdown, convert_pdf_to_html



def generate_combined_prompt(pdf_files, output_format="markdown") -> list[dict]:
    """
    Generates a structured messages prompt for text-based analysis.
    Dynamically adjusts based on the chosen output format (Markdown or HTML).
    """
    messages = []

    # Set system-level instruction based on output format
    if output_format == "markdown":
        system_prompt = (
            "You are a highly intelligent assistant. Your task is to analyze the structural similarities between "
            f"{len(pdf_files)} PDF files. Each filename is provided by the user (in the format 'Filename:<filename.pdf>'), "
            "followed by its extracted content converted to Markdown format. Analyze the text, tables, and any structural similarities explicitly, "
            "without introducing unrelated filenames or content. Your response should be no more than 300 words, in English."
        )
    elif output_format == "html":
        system_prompt = (
            "You are a highly intelligent assistant. Your task is to analyze the structural similarities between "
            f"{len(pdf_files)} PDF files. Each filename is provided by the user (in the format 'Filename:<filename.pdf>'), "
            "followed by its extracted content converted to HTML format. Analyze the text, tables, and any structural similarities explicitly, "
            "without introducing unrelated filenames or content. Your response should be no more than 300 words, in English."
        )
    else:
        raise ValueError("Invalid output format specified. Choose 'markdown' or 'html'.")

    # Add system-level instruction
    messages.append({
        "role": "system",
        "content": system_prompt
    })

    # Add user-level input for each PDF
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")

        if output_format == "markdown":
            file_content = convert_pdf_to_markdown(pdf_file)
        elif output_format == "html":
            file_content = convert_pdf_to_html(pdf_file)

        # Append user message for this file
        messages.append({
            "role": "user",
            "content": {
                "type": "text",
                "text": f"### Filename: {os.path.basename(pdf_file)}\n\nContents:\n\n{file_content}"
            }
        })

    return messages


def parse_args():
    parser = argparse.ArgumentParser(description="Process input PDFs and generate model output.")
    parser.add_argument(
        '--pdf_folder', type=str, default="input_pdfs", help="Path to the folder containing input PDFs"
    )
    parser.add_argument(
        '--suffix', type=str, default=None, help="Suffix for the output file. If blank, will use a timestamp."
    )
    parser.add_argument(
        '--output_format', type=str, default="markdown", choices=["markdown", "html"],
        help="Format for PDF content extraction. Options: 'markdown' or 'html'."
    )
    parser.add_argument(
        '--interactive', action='store_true', help="Enter an interactive loop for further inputs after initial analysis."
    )
    return parser.parse_args()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    args = parse_args()

    # List of PDF filenames from the provided folder
    pdf_files = [os.path.join(args.pdf_folder, f) for f in os.listdir(args.pdf_folder) if f.endswith('.pdf')]

    # Generate the combined prompt
    print("Generating prompt...")
    messages = generate_combined_prompt(pdf_files, output_format=args.output_format)

    print("Combined prompt generated. Running the prompt on the model...")

    start_time = time.time()
    model_output = run_prompts_on_text_llm(messages)

    print("Model Output:\n")
    print(model_output)

    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

    # Determine suffix: if provided, use it; otherwise, use a timestamp
    if args.suffix:
        suffix = args.suffix.strip()
        if suffix.endswith("*"):
            suffix = suffix[:-1] + "_" + timestamp
    else:
        suffix = timestamp

    # Save the results
    os.makedirs("model_outputs", exist_ok=True)
    model_output_filepath = os.path.join("model_outputs", f"model_output_{suffix}.txt")
    with open(model_output_filepath, "w", encoding="utf-8") as f:
        f.write("Prompts:\n")
        json.dump(messages, f, indent=4, ensure_ascii=False)
        f.write("\n\nModel Output:\n\n" + model_output)

    print(f"\nPrompt response completed in {round(time.time() - start_time, 2)} seconds.")
    print(f"Output saved to '{model_output_filepath}'")

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
