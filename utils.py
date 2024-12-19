import pdfplumber
import torch
from transformers import pipeline
import fitz  # PyMuPDF


# Constants
LLAMA_3_2_1B = "meta-llama/Llama-3.2-1B-Instruct"
LLAMA_3_2_3B = "meta-llama/Llama-3.2-3B-Instruct"
LLAMA_3_1_8B = "meta-llama/Llama-3.1-8B-Instruct"
DEFAULT_MODEL = LLAMA_3_2_1B
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.8
TOP_K = 50
TOP_P = 0.95

def run_prompts_on_text_llm(messages, model_id=DEFAULT_MODEL):
    """
    Runs the generated prompt on the Llama model.
    """
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    outputs = pipe(
        messages,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_k=TOP_K,
        top_p=TOP_P,
        do_sample=True,
    )
    result = outputs[0]["generated_text"][-1]['content']
    return result

def convert_pdf_to_markdown(pdf_file):
    """
    Converts the PDF file to Markdown format while maintaining the order of content (text and tables).
    """
    try:
        markdown_content = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                # Extract text
                text = page.extract_text()
                if text:
                    markdown_content += f"{text}\n\n"

                # Extract tables in sequence
                tables = page.extract_tables()
                for i, table in enumerate(tables, 1):
                    markdown_content += f"**Table {i}:**\n\n"
                    for row in table:
                        row = [cell if cell is not None else '' for cell in row]
                        markdown_content += "| " + " | ".join(row) + " |\n"
                    markdown_content += "|---" * len(table[0]) + "|\n\n"

        return markdown_content
    except Exception as e:
        print(f"Error converting {pdf_file} to Markdown")
        raise e.__class__(str(e)).with_traceback(e.__traceback__)


def convert_pdf_to_html(pdf_file):
    try:
        html_content = ""
        doc = fitz.open(pdf_file)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            html_content += page.get_text("html")
        return html_content
    except Exception as e:
        print(f"Error converting {pdf_file} to HTML: {str(e)}")
        raise e.__class__(str(e)).with_traceback(e.__traceback__)