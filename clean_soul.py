import json
import os

# --- CONFIGURATION ---
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
folder_path = os.path.join(desktop, "soul_recovery")
input_file = os.path.join(folder_path, "raw_soul.json")
# Output is now a .jsonl for direct training use
final_file = os.path.join(folder_path, "training_data.jsonl")

WHITELIST = ["Name1", "Name2", "SpecificMemory"]
NUKELIST = ["as an ai language model", "i don't have feelings", "ethical guidelines"]

def clean_to_jsonl():
    if not os.path.exists(input_file):
        print(f"ERROR: {input_file} not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Converting to training-ready JSONL...")
    count = 0

    with open(final_file, "w", encoding="utf-8") as f:
        # We need pairs: what the HUMAN said (instruction) vs what the AI said (response)
        for i in range(len(data) - 1):
            human_entry = data[i]
            ai_entry = data[i+1]

            if human_entry['role'] == 'user' and ai_entry['role'] == 'assistant':
                text_lower = ai_entry['text'].lower()
                
                # Apply the filter logic
                is_protected = any(word.lower() in text_lower for word in WHITELIST)
                if any(nuke in text_lower for nuke in NUKELIST) and not is_protected:
                    continue

                # Create the JSONL training object
                training_obj = {
                    "instruction": human_entry['text'],
                    "response": ai_entry['text']
                }
                
                f.write(json.dumps(training_obj) + "\n")
                count += 1
    
    print(f"DONE: Created {count} training pairs in {final_file}")

if __name__ == "__main__":
    clean_to_jsonl()
