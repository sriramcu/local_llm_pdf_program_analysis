# Local Privacy-Preserving Analysis of Coding Projects with LLMs

This project allows developers to analyze coding projects locally while maintaining data privacy. It is ideal for those who need to gain insights into another team's codebase without exposing sensitive information.

## Models Used

1. meta-llama/Llama-3.2-1B-Instruct
2. meta-llama/Llama-3.2-3B-Instruct
3. meta-llama/Llama-3.1-8B-Instruct

## Project Overview

The project consists of two main scripts:

1. **`project_analyser.py`**: Examines the structural and content aspects of coding projects.
2. **`pdfs_similarity.py`**: Compares the structure and content of multiple PDF files and converts them to markdown format.

Both scripts leverage a text-generation model (`meta-llama`) to process data and generate insights. The entire process is conducted offline, ensuring the privacy and security of your data. System prompts are predefined in the code, and user prompts are generated for each file individually.

## Setup Instructions

1. Create a HuggingFace account and obtain an access token. Save this token for later use.
2. Install CUDA 12.1, CUDNN 9.3, PyTorch '2.4.1+cu121', and transformers 4.47.0, and ensure you're using Python 3.10.
3. Run `pip install -r requirements.txt` to install necessary dependencies.
4. Execute `pip install huggingface_hub` to enable logging in from the terminal or command prompt.
5. Log into your HuggingFace account via the terminal or command prompt by executing `huggingface-cli login` and providing your access token.
6. In `utils.py`, select your `DEFAULT_MODEL` from the available options. Note that other models have not been tested but may work.
7. Request access to the gated repository on HuggingFace based on your chosen `DEFAULT_MODEL` by submitting your details.

## Usage Instructions

### 1. Analyzing a Coding Project

To analyze a coding project, execute the following command:

```bash
python project_analyser.py
```

### Command Line Options

```
usage: project_analyser.py [-h] --project_folder PROJECT_FOLDER [--suffix SUFFIX]
```

#### Options

- `-h`, `--help`  
  Display help information and exit.

- `--project_folder PROJECT_FOLDER`  
  Specify the path to the folder containing the coding project.

- `--suffix SUFFIX`  
  Define a suffix for the output file that stores the analysis results. If omitted, a timestamp will be used.

- `--interactive`  
  Engage in an interactive loop for additional inputs after the initial analysis.

---

### 2. Analyzing PDFs

To analyze PDFs, use the following command:

```bash
python pdfs_similarity.py
```

In this case, the system instruction is to find structural similarities between multiple PDF files by converting them to markdown/HTML format. You may change the system instruction in this python file in case you want to do something else with the PDFs, such as summarizing them.

### Command Line Options

```
usage: pdfs_similarity.py [-h] [--pdf_folder PDF_FOLDER] [--suffix SUFFIX] [--output_format {markdown,html}] [--interactive]
```

#### Options

- `-h`, `--help`  
  Display help information and exit.

- `--pdf_folder PDF_FOLDER`  
  Specify the path to the folder containing input PDF files.

- `--suffix SUFFIX`  
  Define a suffix for the output file that stores the analysis results. If omitted, a timestamp will be used. The output file does not store analysis from interactive mode.

- `--output_format {markdown,html}`  
  Choose the format for extracting PDF content to be used in user prompts. Options include:
  - `markdown`
  - `html`

- `--interactive`  
  Engage in an interactive loop for additional inputs after the initial analysis. Type "exit" to quit.

---

### 3. Utility Scripts

`generate_readymade_prompt.py` and `pdf_to_markdown.py` are utility scripts that can be used to generate prompts for analysis for both the above usecases and to convert PDFs to markdown format, respectively, in case your PC is not powerful enough and you have access to a proprietary Generative AI service.

---

