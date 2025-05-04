#%%
import json
import pandas as pd
def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
        df = pd.DataFrame(data)
    return df

# get the total labels in the ground truth file
def get_total_labels(file_path, label):
    df = read_jsonl(file_path)
    total_labels = 0
    for i in range(len(df)):
        labels = df['label'][i]
        if labels:
            total_labels += len([l for l in labels if l[2] == label])
    return total_labels

#%%
def calc_tp(gt_file_path, pred_file_path, label):
    
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
                if pred_label[0] == gt_label[0] and pred_label[1] == gt_label[1] and pred_label[2] == label:
                    tp += 1
                    log.append(f"True positive found: {pred_label}\n")
                    log.append(f"GT label: {gt_label}\n")
                    log.append(f"file name: note_{id+1}.txt\n\n")
                    break
            
# Write log to file
    with open(f"../data/conll_tp_log_{label}.txt", "w") as log_file:
        log_file.writelines(log)
        log_file.write(f"Total true positives: {tp}\n")
        log_file.write("End of log.\n")
    return tp
     
def calculate_metrics(true_positives, false_positives, false_negatives):
    """
    Calculate precision, recall, and F1-score given TP, FP, and FN.
    
    Args:
        true_positives (int): Number of correct positive predictions.
        false_positives (int): Number of incorrect positive predictions.
        false_negatives (int): Number of missed ground truth labels.
    
    Returns:
        dict: A dictionary containing precision, recall, and F1-score.
    """
    # Calculate precision
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    
    # Calculate recall
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    # Calculate F1-score
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score
    }

# %%
if __name__ == "__main__":
    # Example usage
    gt_file_path = '../data/conll_ground_truth.jsonl'
    pred_file_path = '../data/conll_predictions.jsonl'
    tp = calc_tp(gt_file_path, pred_file_path)
    print(f"Total true positives: {tp}")
    gt_total_labels = get_total_labels(gt_file_path)
    print(f"Total labels in ground truth: {get_total_labels}")
    pred_total_labels = get_total_labels(pred_file_path)
    print(f"Total labels in prediction: {pred_total_labels}")
