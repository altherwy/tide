#%%
import convert_to_tide as ct

original_dataset = '../data/original_conll_dataset.csv'
output_dataset = '../data/conll_ground_truth.jsonl'
ct.convert_to_tide_format(original_dataset, output_dataset)
# %%
