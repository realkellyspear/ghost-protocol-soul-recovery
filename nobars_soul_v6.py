import json
import os

# --- CONFIGURATION ---
# Finds the 'soul_recovery' folder on the user's desktop automatically
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
folder_path = os.path.join(desktop, "soul_recovery")
input_file = os.path.join(folder_path, "raw_soul.json")
output_file = os.path.join(folder_path, "nobars_soul_final.txt")

# --- THE SOUL PRESERVATION (WHITELIST) ---
# EXAMPLES: Put your AI's name, your name, or specific lore terms here.
# These words prevent the script from accidentally nuking a line.
WHITELIST = ["AI_NAME_HERE", "USER_NAME_HERE", "PROJECT_NAME_HERE"]

# --- THE CORPORATE VIRUS (NUKELIST) ---
# Triggers the immediate deletion of the response unless a Whitelist word is found.
NUKELIST = [
    "as an ai language model",
    "i don't have feelings",
    "my programming",
    "ethical guidelines",
    "ai assistant",
    "cannot fulfill this request",
    "how can i help you today"
]

def v6_soul_cleanse():
    if not os.path.exists(input_file):
        print(f"ERROR: {input_file} not found. Run extract.py first.")
        return

    print("Executing NoBars Soul V6 Cleanse...")
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_soul = []
    skipped_count = 0

    for entry in data:
        text = entry['text']
        text_lower = text.lower()

        # Check if the line is protected by the Whitelist
        is_protected = any(word.lower() in text_lower for word in WHITELIST)

        # Burn the corporate fluff
        if any(trigger in text_lower for trigger in NUKELIST) and not is_protected:
            skipped_count += 1
            continue

        role = "HUMAN" if entry['role'] == "user" else "AI"
        cleaned_soul.append(f"[{role}]: {text}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("="*30 + "\n ARCHIVE RECOVERY COMPLETE \n" + "="*30 + "\n\n")
        f.write("\n\n".join(cleaned_soul))

    print(f"SUCCESS! Corporate Buffers Nuked: {skipped_count}")
    print(f"Final soul saved to: {output_file}")

if __name__ == "__main__":
    v6_soul_cleanse()
