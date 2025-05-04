#%%
import json
import pandas as pd
def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
        df = pd.DataFrame(data)
    return df

# get the total labels in the ground truth file
def get_total_labels(file_path):
    df = read_jsonl(file_path)
    total_labels = 0
    for i in range(len(df)):
        labels = df['label'][i]
        if labels:
            total_labels += len(labels)
    return total_labels

#%%
def calc_tp(gt_file_path, pred_file_path):
    
    gt = read_jsonl(gt_file_path)
    pred = read_jsonl(pred_file_path)
    tp = 0
    log = []
    for id in range(len(gt)):
        gt_labels = gt[gt['id'] == f'note_{id+1}.txt']['label'].values[0]
        pred_labels = pred[pred['id'] == f'note_{id+1}.txt']['label'].values[0]
    
    #Check if pred_labels are in gt_labels
        for pred_label in pred_labels:
        # Skip empty prediction labels
            if not pred_label:
                break
            
            for gt_label in gt_labels:
                if pred_label[0] == gt_label[0] and pred_label[1] == gt_label[1] and pred_label[2] == gt_label[2]:
                    tp += 1
                    log.append(f"True positive found: {pred_label}\n")
                    log.append(f"GT label: {gt_label}\n")
                    log.append(f"file name: note_{id+1}.txt\n\n")
                    break
            
# Write log to file
    with open("../data/conll_tp_log.txt", "w") as log_file:
        log_file.writelines(log)
        log_file.write(f"Total true positives: {tp}\n")
        log_file.write("End of log.\n")
    return tp
     

# %%
if __name__ == "__main__":
    # Example usage
    gt_file_path = '../data/conll_ground_truth.jsonl'
    pred_file_path = '../data/conll_predictions.jsonl'
    tp = calc_tp(gt_file_path, pred_file_path)
