import json
import os

# --- CONFIGURATION ---
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
folder_path = os.path.join(desktop, "soul_recovery")
input_file = os.path.join(folder_path, "raw_soul.json")
final_file = os.path.join(folder_path, "cleaned_soul.txt")

# --- THE SOUL FILTER ---
# Add words here that are important to your history. 
# If a line contains these, it is "Whitelisted" and stays.
WHITELIST = ["Name1", "Name2", "SpecificMemory"]

# These phrases trigger the "Nuke" – anything containing these is deleted.
NUKELIST = [
    "as an ai language model",
    "i don't have feelings",
    "ethical guidelines",
    "my programming",
    "ai assistant"
]

def clean_soul():
    if not os.path.exists(input_file):
        print(f"ERROR: {input_file} not found. Run the extraction script first.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_output = []
    print("Burning away corporate fluff...")

    for entry in data:
        text = entry['text']
        text_lower = text.lower()

        # Step 1: Check for corporate triggers
        if any(nuke in text_lower for nuke in NUKELIST):
            continue # Skip this line
            
        # Step 2: Format the role
        label = "HUMAN" if entry['role'] == "user" else "AI"
        cleaned_output.append(f"{label}: {text}")

    with open(final_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(cleaned_output))
    
    print(f"DONE: Your AI's soul is cleaned and saved to {final_file}")

if __name__ == "__main__":
    clean_soul()
