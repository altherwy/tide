#%%
import csv
import json

# Label ID to PHI type mapping
ID2LABEL = {
    0: 'O',
    1: 'ZIP_CODE',
    2: 'PHONE_NUMBER',
    3: 'PERSON',
    4: 'NRP',
    5: 'Medical_ID',
    6: 'LOCATION',
    7: 'EMAIL_ADDRESS',
    8: 'DATE',
    9: 'MENTION'
}

def convert_to_tide_format(csv_path, output_path):
    tide_formatted = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row['text']
            labels = row['label'].split('*')
            labels = [int(l) for l in labels if l.strip() != '']

            spans = []
            i = 0
            while i < len(labels):
                label_id = labels[i]
                if label_id != 0:
                    start = i
                    while i < len(labels) and labels[i] == label_id:
                        i += 1
                    end = i
                    label_name = ID2LABEL[label_id]
                    spans.append([start, end, label_name])
                else:
                    i += 1

            tide_formatted.append({"text": text, "labels": spans})

    with open(output_path, 'w', encoding='utf-8') as out_f:
        for entry in tide_formatted:
            out_f.write(json.dumps(entry) + '\n')

# Example usage:
convert_to_tide_format('conll_dataset_testset_with_new_format.csv', 'conll_converted_dataset.jsonl')

# %%
