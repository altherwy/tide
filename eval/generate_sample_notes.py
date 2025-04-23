#%%
import pandas as pd
import os

# Load your dataset
csv_path = "conll_dataset_testset_with_new_format.csv"  # path to your CSV
output_folder = "../sample_notes"  # where to save the notes

# Create output folder if it doesn't exist
#os.makedirs(output_folder, exist_ok=True)

# Read the CSV
df = pd.read_csv(csv_path)

# Loop and write each row to a .txt file
for idx, row in df.iterrows():
    filename = os.path.join(output_folder, f"note_{idx+1}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(row['text'])
# %%
