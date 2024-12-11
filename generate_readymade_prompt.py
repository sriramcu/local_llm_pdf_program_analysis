import argparse
import os
from pdfs_similarity import generate_combined_prompt as generate_pdf_prompt
from project_analyser import generate_project_prompt

def main():
    parser = argparse.ArgumentParser(description="Generate a readymade prompt for analysis.")
    parser.add_argument(
        '--mode', 
        type=str, 
        required=True, 
        choices=['pdf_similarity', 'project_analysis'], 
        help="Specify the mode: 'pdf_similarity' or 'project_analysis'."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help="Path to the input folder (for PDFs or project files)."
    )
    parser.add_argument(
        '--output_format', 
        type=str, 
        default="markdown", 
        choices=["markdown", "html"], 
        help="Format for PDF content extraction (applicable only for PDF similarity)."
    )

    args = parser.parse_args()

    if args.mode == 'pdf_similarity':
        # Validate PDF folder
        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            print(f"Error: The provided path '{args.path}' does not exist or is not a folder.")
            return

        pdf_files = [os.path.join(args.path, f) for f in os.listdir(args.path) if f.endswith('.pdf')]
        if not pdf_files:
            print(f"Error: No PDF files found in the provided folder '{args.path}'.")
            return

        # Generate the prompt for PDF similarity
        print("Generating prompt for PDF similarity...")
        prompt = generate_pdf_prompt(pdf_files, output_format=args.output_format)
    
    elif args.mode == 'project_analysis':
        # Validate project folder
        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            print(f"Error: The provided path '{args.path}' does not exist or is not a folder.")
            return

        # Generate the prompt for project analysis
        print("Generating prompt for project analysis...")
        prompt = generate_project_prompt(args.path)

    # Print the prompt
    print("\n--- BEGIN PROMPT ---\n")
    for message in prompt:
        print(f"{message['role'].upper()}:")
        print(message['content'])
        print("\n---\n")
    print("--- END PROMPT ---\n")

if __name__ == "__main__":
    main()
