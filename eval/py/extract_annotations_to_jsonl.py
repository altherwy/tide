import fix_jsonl_files as fj
import os
import json
import pandas as pd
def extract_annotations_to_jsonl(annotation_files_path, output_path):
    """
    Extract annotations from JSON files and save them to a JSONL file.
    
    Args:
        annotation_files_path: Path to directory containing annotation files
        output_path: Path where the JSONL file will be saved
    """
    # sort the files by name
    annotation_files = sorted([f for f in os.listdir(annotation_files_path) if f.endswith('.txt.json')])
    
    texts = []
    labels = []
    ids = []
    
    for annotation_file in annotation_files:
        file_path = os.path.join(annotation_files_path, annotation_file)
        temp_file_path = os.path.join(annotation_files_path, 'temp.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            print(f"Reading file: {annotation_file}")
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                f.close()
                fj.fix_json_file(file_path, temp_file_path)
                # open the file again after fixing it
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            keys = data.keys()
            texts.append(data.get('text', ''))
            # escape single and double quotes in the text
            texts[-1] = texts[-1].replace("'", "\\'").replace('"', '\\"')
            labels.append(data.get('label', ''))
            ids.append(data.get('id', ''))
    
    
    df = pd.DataFrame({'text': texts, 'label': labels, 'id': ids})
    df.to_json(output_path, orient='records', lines=True)

if __name__ == "__main__":
    # Example usage
    annotation_files_path = '../../output/1744347802881 copy/annotator'
    output_path = '../data/conll_predictions.jsonl'
    extract_annotations_to_jsonl(annotation_files_path, output_path)