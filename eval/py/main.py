#%%
import convert_to_tide as ct

original_dataset = '../data/original_conll_dataset.csv'
output_dataset = '../data/conll_ground_truth.jsonl'
ct.convert_to_tide_format(original_dataset, output_dataset)
# %%
# export each line in the jsonl file to a separate .txt file
import generate_input_txt as git
output_dir = '../data/sample_notes'
git.split_jsonl_to_txt(output_dataset, output_dir)
# %%
import os
import json
annotation_files_path = '../../output/1744348281291/annotator'
# sort the files by name
annotation_files = sorted([f for f in os.listdir(annotation_files_path) if f.endswith('.txt.json')])
# read the first file to get the keys
texts = []
labels = []
ids = []
for annotation_file in annotation_files:
    with open(os.path.join(annotation_files_path, annotation_file), 'r', encoding='utf-8') as f:
        data = json.load(f)
        keys = data.keys()
        texts.append(data.get('text', ''))
        # escape single and double quotes in the text
        texts[-1] = texts[-1].replace("'", "\\'").replace('"', '\\"')
        labels.append(data.get('label', ''))
        ids.append(data.get('id', ''))

            
import pandas as pd
df = pd.DataFrame({'text': texts, 'label': labels, 'id': ids})
df.to_json('1744348281291.jsonl', orient='records', lines=True)
# %%
