#%%
import convert_to_tide as ct

#%%
original_dataset = '../data/original_conll_dataset.csv'
output_dataset = '../data/conll_ground_truth.jsonl'
ct.convert_to_tide_format(original_dataset, output_dataset)
# %%
# export each line in the jsonl file to a separate .txt file
import generate_input_txt as git
output_dir = '../data/sample_notes'
git.split_jsonl_to_txt(output_dataset, output_dir)
# %%

# %%
