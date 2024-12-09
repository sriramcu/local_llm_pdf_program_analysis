# Coding Project Analyzer and PDF Similarity Using local LLMs

Local LLM inference for analysing multiple PDF files and coding projects in any programming language.

## Models Used

1. meta-llama/Llama-3.2-1B-Instruct
2. meta-llama/Llama-3.2-3B-Instruct
3. meta-llama/Llama-3.1-8B-Instruct


## Overview
This project includes two programs:
1. **`pdfs_similarity.py`**: Analyzes the structural and content similarities between multiple PDF files.
2. **`project_analyser.py`**: Analyzes the structure and content of coding projects.

Both programs use a text-generation model (`meta-llama`) to process input data and generate insights. This project uses only LLM inference. The inference is completely offline, without any API keys required, thereby ensuring privacy and security.

System prompt is hard-coded in the code. User prompts are created one at a time for each PDF/program file.


## Setup Instructions


1. Sign up for a HuggingFace account and setup an access token. Save this token for later use. 
2. Setup CUDA 12.1, CUDNN 9.3, PyTorch '2.4.1+cu121', transformers 4.47.0, use Python 3.10.
3. `pip install -r requirements.txt`
4. `pip install huggingface_hub` for logging in via the terminal/cmd.
5. Login to your HuggingFace account in your terminal/cmd where you are running the program, by running `huggingface-cli login` and enter your access token saved earlier. 
6. Go to `utils.py` and choose your `DEFAULT_MODEL` from the options given. Other models are not tested but may work. 
7. Based on the `DEFAULT_MODEL` selected, request access to the gated repo on the Huggingface portal, by filling in your details.


## How to Use

### 1. Analyze PDFs

```bash
python pdfs_similarity.py
```

### Command Line Options

```
usage: pdfs_similarity.py [-h] [--pdf_folder PDF_FOLDER] [--suffix SUFFIX] [--output_format {markdown,html}] [--interactive]
```

### Options

- `-h`, `--help`  
  Show the help message and exit.

- `--pdf_folder PDF_FOLDER`  
  Path to the folder containing input PDFs.

- `--suffix SUFFIX`  
  Suffix for the output file which stores the analysis. If not provided, a timestamp will be used. Output file will not store analysis from the interactive mode.

- `--output_format {markdown,html}`  
  Format for PDF content extraction, to be used in the user prompts. You can choose between:
  - `markdown`
  - `html`

- `--interactive`  
  Enter an interactive loop for further inputs after the initial analysis, type "exit" to quit.

---


### 2. Analyse Coding Project


```bash
python project_analyser.py
```

### Command Line Options

```
usage: project_analyser.py [-h] --project_folder PROJECT_FOLDER [--suffix SUFFIX]
```

### Options

- `-h`, `--help`  
  Show the help message and exit.

- `--project_folder PROJECT_FOLDER`  
  Path to the folder containing the coding project.

- `--suffix SUFFIX`  
  Suffix for the output file which stores the analysis. If not provided, a timestamp will be used.

- `--interactive`  
  Enter an interactive loop for further inputs after the initial analysis.

---
