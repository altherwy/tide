#%%
import convert_to_tide as ct
import extract_annotations_to_jsonl as ea
#%%
original_dataset = '../data/original_conll_dataset.csv'
output_dataset = '../data/conll_ground_truth.jsonl'
ct.convert_to_tide_format(original_dataset, output_dataset)
# %%
# export each line in the jsonl file to a separate .txt file
import generate_input_txt as git
output_dir = '../data/sample_notes'
git.split_jsonl_to_txt(output_dataset, output_dir)
# %% Generate prediction file
annotation_files_path = '../../output/conll/annotator'
output_path = '../data/conll_predictions.jsonl'
ea.extract_annotations_to_jsonl(annotation_files_path, output_path)
# %% calculate tp
import calculate_tp as ct
gt_file_path = '../data/conll_ground_truth.jsonl'
pred_file_path = '../data/conll_predictions.jsonl'
tp = ct.calc_tp(gt_file_path, pred_file_path)
# %%
