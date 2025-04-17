#%%
import os
import json

def calculate_tp(prediction_folder, ground_truth_file):
    # Load ground truth lines
    with open(ground_truth_file, 'r', encoding='utf-8') as f:
        ground_truth = [json.loads(line) for line in f]

    # Sort prediction files by index (e.g., note_1.txt.json -> 1)
    pred_files = sorted(
        [f for f in os.listdir(prediction_folder) if f.startswith("note_") and f.endswith(".txt.json")],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )
    tp = 0
    log_entries = []
    for idx, pred_file in enumerate(pred_files):
        pred_path = os.path.join(prediction_folder, pred_file)
        with open(pred_path, 'r', encoding='utf-8') as f:
            try:
                pred = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {pred_file}")
    
        try:
            for p_label in pred.get('label', []):
                # check if the label is in the ground truth
                if idx < len(ground_truth) and 'labels' in ground_truth[idx]:
                    for gt_label in ground_truth[idx]['labels']:
                        if p_label[0] == gt_label[0] and p_label[1] == gt_label[1] and p_label[2] == gt_label[2]:
                            # Add match log entry
                            log_entries.append(f"Match found: {p_label} in {pred_file} matches {gt_label} in ground truth\n")
                            tp += 1
                            break
                    else:
                        # Add no-match log entry
                        log_entries.append(f"No match found for {p_label} in {pred_file}\n")
                else:
                    log_entries.append(f"Warning: No ground truth labels available for {pred_file}\n")
        except Exception as e:
            log_entries.append(f"Error processing {pred_file}: {str(e)}\n")
            print(f"Error processing {pred_file}: {str(e)}")

        print(f"Processed {pred_file}, total correct: {tp}")
        # Add processing status log entry
        log_entries.append(f"Processed {pred_file}, total correct so far: {tp}\n")

    # Write all log entries to file at once
    with open("match_log.txt", "a") as log_file:
        log_file.writelines(log_entries)
    
    return pred_files, ground_truth, tp


def calculate_tp_by_label(prediction_folder, ground_truth_file, label):
    # Load ground truth lines
    with open(ground_truth_file, 'r', encoding='utf-8') as f:
        ground_truth = [json.loads(line) for line in f]

    # Sort prediction files by index (e.g., note_1.txt.json -> 1)
    pred_files = sorted(
        [f for f in os.listdir(prediction_folder) if f.startswith("note_") and f.endswith(".txt.json")],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )
    tp = 0
    log_entries = []
    for idx, pred_file in enumerate(pred_files):
        pred_path = os.path.join(prediction_folder, pred_file)
        with open(pred_path, 'r', encoding='utf-8') as f:
            try:
                pred = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {pred_file}")
                continue
    
        try:
            for p_label in pred.get('label', []):
                # check if the label is in the ground truth
                if idx < len(ground_truth) and 'label' in ground_truth[idx]:
                    for gt_label in ground_truth[idx]['label']:
                        if p_label[0] == gt_label[0] and p_label[1] == gt_label[1] and p_label[2] == label:
                            # Add match log entry
                            log_entries.append(f"Match found: {p_label} in {pred_file} matches {gt_label} in ground truth\n")
                            tp += 1
                            break
                    else:
                        # Add no-match log entry
                        log_entries.append(f"No match found for {p_label} in {pred_file}\n")
                else:
                    log_entries.append(f"Warning: No ground truth labels available for {pred_file}\n")
        except Exception as e:
            log_entries.append(f"Error processing {pred_file}: {str(e)}\n")
            print(f"Error processing {pred_file}: {str(e)}")

        print(f"Processed {pred_file}, total correct: {tp}")
        # Add processing status log entry
        log_entries.append(f"Processed {pred_file}, total correct so far: {tp}\n")

    # Write all log entries to file at once
    with open("match_log.txt", "a") as log_file:
        log_file.writelines(log_entries)
    
    return pred_files, ground_truth, tp

# get the total number of labels in the prediction files
def get_total_pred_labels(folder, files):
    total_labels = 0
    for file in files:
        pred_path = os.path.join(folder, file)
        with open(pred_path, 'r', encoding='utf-8') as f:
            pred = json.load(f)
        try:
            if len(pred['label'][0]) == 3:
                total_labels += len(pred['label'])
                print(f"File: {file}, Total labels: {total_labels}")
        except IndexError as e:
            print(f"Error in file {file}: {e}")
            continue    
    return total_labels

# get the total number of labels in the prediction files
def get_total_pred_labels_by_label(folder, files, label):
    total_labels = 0
    for file in files:
        pred_path = os.path.join(folder, file)
        with open(pred_path, 'r', encoding='utf-8') as f:
            pred = json.load(f)
        try:
            for p_label in pred['label']:
                # check if the label is in the ground truth
                if len(p_label) == 3 and p_label[2] == label:
                    total_labels += 1
                print(f"File: {file}, Total labels: {total_labels}")
        except IndexError as e:
            print(f"Error in file {file}: {e}")
            continue    
    return total_labels




def get_total_gt_labels(ground_truth):
    total_labels = 0
    for idx, gt in enumerate(ground_truth):
        print(idx)
        try:
            if len(gt['label'][0]) == 3:
                total_labels += len(gt['label'])
        except IndexError as e:
            print(f"Error in file {idx}: {e}")
            continue

    return total_labels

def get_total_gt_labels_by_label(ground_truth, label):
    total_labels = 0
    for idx, gt in enumerate(ground_truth):
        try:
            for g_label in gt['label']:
                # check if the label is in the ground truth
                if len(g_label) == 3 and g_label[2] == label:
                    total_labels += 1
                
        except IndexError as e:
            print(f"Error in file {idx}: {e}")
            continue

    return total_labels

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

# Main function for evaluation
def main(labels):
    prediction_folder = "../output/1744348281291/annotator"  # Replace with the folder containing note_*.txt.json files
    ground_truth_file = "conll_converted_dataset.jsonl"  # Replace with actual path
    
    print("Calculating true positives...")
    pred_files, ground_truth, tp = calculate_tp(prediction_folder, ground_truth_file)
    
    print("Counting predicted labels...")
    total_pred_label = get_total_pred_labels(prediction_folder, pred_files)
    
    print("Counting ground truth labels...")
    total_ground_truth_label = get_total_gt_labels(ground_truth)
    
    # Calculate false negatives and false positives
    fn = total_ground_truth_label - tp
    fp = total_pred_label - tp
    
    print(f"\nSummary:")
    print(f"True Positives: {tp}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    
    # Calculate and print metrics
    metrics = calculate_metrics(tp, fp, fn)
    print("\nMetrics:")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1 Score: {metrics['f1_score']:.4f}")
    
    return metrics

# Execute if script is run directly
if __name__ == "__main__":
    conll_labels = ['NAME','LOCATION']
    main()
