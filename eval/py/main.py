#%%
import convert_to_tide as ct
import extract_annotations_to_jsonl as ea
#%%
original_dataset = '../data/ontonotes_dataset.csv'
output_dataset = '../data/ontonotes_ground_truth.jsonl'
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
# %% calculate metrics MASKED
import calculate_metrics as ct
gt_file_path = '../data/conll_ground_truth.jsonl'
pred_file_path = '../data/conll_predictions.jsonl'
tp = ct.calc_tp(gt_file_path, pred_file_path)
gt_total_labels = ct.get_total_labels(gt_file_path)
pred_total_labels = ct.get_total_labels(pred_file_path)
fn = gt_total_labels - tp
fp = pred_total_labels - tp
all_metrics_masked = ct.calculate_metrics(tp, fp, fn)
# write the results to a file
with open("../data/conll_metrics_masked.txt", "w") as f:
    f.write(f"True positives: {tp}\n")
    f.write(f"Total labels in ground truth: {gt_total_labels}\n")
    f.write(f"Total labels in prediction: {pred_total_labels}\n")
    f.write(f"False negatives: {fn}\n")
    f.write(f"False positives: {fp}\n")
    f.write(f"Precision: {all_metrics_masked['precision']:.4f}\n")
    f.write(f"Recall: {all_metrics_masked['recall']:.4f}\n")
    f.write(f"F1 Score: {all_metrics_masked['f1_score']:.4f}\n")
f.close()
# %% calculate metrics of each label
import calculate_metrics_by_label as cml
gt_file_path = '../data/conll_ground_truth.jsonl'
pred_file_path = '../data/conll_predictions.jsonl'
labels = ['PERSON','ZIP_CODE','PHONE_NUMBER','NRP','Medical_ID','LOCATION','EMAIL_ADDRESS','DATE','MENTION']
for label in labels:
    tp = cml.calc_tp(gt_file_path, pred_file_path, label)
    gt_total_labels = cml.get_total_labels(gt_file_path, label)
    pred_total_labels = cml.get_total_labels(pred_file_path, label)
    fn = gt_total_labels - tp
    fp = pred_total_labels - tp
    all_metrics = cml.calculate_metrics(tp, fp, fn)
    # write the results to a file
    with open(f"../data/conll_metrics_{label}.txt", "w") as f:
        f.write(f"True positives: {tp}\n")
        f.write(f"Total labels in ground truth: {gt_total_labels}\n")
        f.write(f"Total labels in prediction: {pred_total_labels}\n")
        f.write(f"False negatives: {fn}\n")
        f.write(f"False positives: {fp}\n")
        f.write(f"Precision: {all_metrics['precision']:.4f}\n")
        f.write(f"Recall: {all_metrics['recall']:.4f}\n")
        f.write(f"F1 Score: {all_metrics['f1_score']:.4f}\n")
    f.close()


# %%
