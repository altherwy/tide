import json
import os

def split_jsonl_to_txt(jsonl_file: str, output_dir: str):
    """
    Splits a JSONL file into multiple .txt files, each containing the text from one line of the JSONL file.
    To be placed inside the sample_notes folder.

    Args:
        jsonl_file (str): Path to the input JSONL file.
        output_dir (str): Directory where the .txt files will be saved.
    """
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            text = data['text']
            with open(os.path.join(output_dir, f'note_{i+1}.txt'), 'w', encoding='utf-8') as out_f:
                out_f.write(text)

if __name__ == "__main__":
    # Example usage
    output_dataset = '../data/conll_ground_truth.jsonl'
    split_jsonl_to_txt(output_dataset, '../data/sample_notes')