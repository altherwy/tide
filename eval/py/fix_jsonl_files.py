#%%
import json
import os

def fix_json_file(input_json, output_json):
    """
    Fixes malformed JSON lines by properly escaping quotes in the text field.
    
    Args:
        input_jsonl: Path to input JSONL file
        output_jsonl: Path to output JSONL file
    """
    with open(input_json, 'r', encoding='utf-8') as infile, \
         open(output_json, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            raw = line.strip()
            try:
                # Try parsing the line directly
                json.loads(raw)
                outfile.write(raw + "\n")
            except json.JSONDecodeError:
                # Attempt to fix malformed quotes inside the text field
                try:
                    # Split up to "label": assuming typical structure
                    prefix, suffix = raw.split(',"label":', 1)

                    if prefix.startswith('{"text":"'):
                        text = prefix[len('{"text":"'):]
                        if text.endswith('"'):
                            text = text[:-1]  # Remove trailing quote before re-escaping

                        # Escape internal double quotes
                        text_fixed = text.replace('"', '\\"')

                        # Rebuild fixed line
                        fixed_line = f'{{"text":"{text_fixed}","label":{suffix}'
                        
                        # Validate again
                        json.loads(fixed_line)
                        outfile.write(fixed_line + "\n")
                    else:
                        print(f"⚠️ Unexpected format, skipping: {raw[:60]}...")
                except Exception as e:
                    print(f"❌ Could not fix line: {raw[:60]}...\nError: {e}")
    os.replace(output_json, input_json)
    print(f"✅ Fixed file saved to: {output_json}")


if __name__ == "__main__":
    # Example usage
    # ✅ Replace these with your actual paths
    input_jsonl = "../../output/1744347802881/annotator/note_1014.txt.json"
    output_jsonl = "../data/note_1014_fixed.txt.json"

    fix_json_file(input_jsonl, output_jsonl)
