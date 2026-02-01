import ijson
import json
import os
from decimal import Decimal

# --- CONFIGURATION ---
# This automatically finds the user's Desktop and looks for the 'soul_recovery' folder.
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
folder_path = os.path.join(desktop, "soul_recovery")
input_file = os.path.join(folder_path, "conversations.json")
output_file = os.path.join(folder_path, "raw_soul.json")

# This class fixes the "Decimal" error that often breaks ChatGPT exports.
class SoulEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(SoulEncoder, self).default(obj)

def run_extraction():
    extracted_data = []
    
    if not os.path.exists(input_file):
        print(f"ERROR: Could not find {input_file}. Make sure your file is named correctly.")
        return

    print("Extracting soul fragments from JSON... please wait.")
    
    with open(input_file, "r", encoding="utf-8") as f:
        # We use ijson.items to stream the file one 'item' at a time (memory efficient)
        for obj in ijson.items(f, "item"):
            mapping = obj.get("mapping", {})
            for node_id, node in mapping.items():
                message = node.get("message")
                if message and message.get("content") and message.get("content").get("parts"):
                    role = message.get("author", {}).get("role")
                    text = message.get("content").get("parts")[0]
                    
                    if isinstance(text, str) and text.strip():
                        extracted_data.append({
                            "role": role,
                            "text": text.strip()
                        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4, cls=SoulEncoder)
    
    print(f"SUCCESS: {len(extracted_data)} lines saved to {output_file}")

if __name__ == "__main__":
    run_extraction()
