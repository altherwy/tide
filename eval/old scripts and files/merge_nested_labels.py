#%%
import os
import json

# Path to folder containing note_*.txt.json files
annotator_folder = "../output/1744348281291/annotator"  # Replace with actual path

# Function to merge overlapping spans with the same label
def merge_spans(spans):
    if not spans:
        return []
    print(spans)
    # Sort by start index
    spans = sorted(spans, key=lambda x: (x[0], x[1]))
    merged = []

    for span in spans:
        if not merged:
            merged.append(span)
        else:
            last = merged[-1]
            if span[0] <= last[1] and span[2] == last[2]:  # Overlap & same label
                merged[-1] = [min(last[0], span[0]), max(last[1], span[1]), last[2]]
            else:
                merged.append(span)
    return merged

# Process each file
for filename in os.listdir(annotator_folder):
    print(filename)
    if filename.endswith(".txt.json") and filename.startswith("note_"):
        filepath = os.path.join(annotator_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️ Skipping {filename}: JSON decode error → {e}")
            continue

        original_spans = data.get("label", [])
        if not isinstance(original_spans, list):
            original_spans = []

        merged_spans = merge_spans(original_spans)
        data["label"] = merged_spans

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

print("✅ All overlapping spans have been merged.")

# %%
