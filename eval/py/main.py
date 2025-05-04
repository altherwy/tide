#%%
import convert_to_tide as ct
import extract_annotations_to_jsonl as ea
#%%
def print_results(metrics):
    """
    Print the evaluation metrics in a formatted way.
    
    Args:
        metrics (dict): A dictionary containing precision, recall, and F1-score.
    """
    print("\nEvaluation Metrics:")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1 Score: {metrics['f1_score']:.4f}")
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
# %% calculate metrics
import calculate_metrics as ct
gt_file_path = '../data/conll_ground_truth.jsonl'
pred_file_path = '../data/conll_predictions.jsonl'
tp = ct.calc_tp(gt_file_path, pred_file_path)
gt_total_labels = ct.get_total_labels(gt_file_path)
pred_total_labels = ct.get_total_labels(pred_file_path)
fn = gt_total_labels - tp
fp = pred_total_labels - tp
all_metrics = ct.calculate_metrics(tp, fp, fn)

print_results(all_metrics)

# %%

