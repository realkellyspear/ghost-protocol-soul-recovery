import ijson, json, os
from datetime import datetime
from decimal import Decimal

class SoulEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal): return float(obj)
        return super(SoulEncoder, self).default(obj)

def extract():
    # Finds Desktop automatically without using your username
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    folder = os.path.join(desktop, "soul_recovery")
    input_p = os.path.join(folder, "conversations.json")
    output_p = os.path.join(folder, "raw_soul.json")
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    print(f"🚀 Extracting memories into {output_p}...")
    
    convos = []
    try:
        with open(input_p, 'rb') as f:
            for item in ijson.items(f, 'item'):
                convos.append(item)
        
        with open(output_p, 'w', encoding='utf-8') as f:
            json.dump(convos, f, indent=2, ensure_ascii=False, cls=SoulEncoder)
        print(f"✅ SUCCESS.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    extract()
