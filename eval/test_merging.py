#%%
import csv
from collections import defaultdict
import json

# Read and group labels by file
grouped = defaultdict(list)
with open('conll_predictions.jsonl', 'r') as infile:
    for line in infile:
        data = json.loads(line)
        file_name = data['id']
        label = data['label']  # Assuming labels are already in the right format in JSON
        grouped[file_name].append(label)

grouped

#%%
# Process each file's labels
processed_data = []
for file_name, labels in grouped.items():
    # Sort by start (ascending) and end (descending)
    labels_sorted = sorted(labels, key=lambda x: (x[0], -x[1]))
    
    
    kept_labels = []
    for label in labels_sorted:
        l_start, l_end, _ = label
        # Check if contained in any kept label
        contained = any(k_start <= l_start and l_end <= k_end 
                        for (k_start, k_end, _) in kept_labels)
        if not contained:
            kept_labels.append(label)
    
    # Sort kept labels naturally
    kept_labels = sorted(kept_labels, key=lambda x: (x[0], x[1]))
    
    processed_data.append({
        'label': str(kept_labels),
        'file': file_name,
        'total_labels': len(kept_labels)
    })
#%%
# Write output CSV
with open('filtered_labels.csv', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['label', 'file', 'total_labels'])
    writer.writeheader()
    writer.writerows(processed_data)

#%%

    
# %%
