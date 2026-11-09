import os
import re

# Path to YOUR MOD'S copied history/pops folder
# (Make sure you copy the vanilla common/history/pops/ files into your mod folder first!)
mod_pops_path = "C:/Users/themc/Documents/Paradox Interactive/Victoria 3/mod/Earth Mod/common/history/pops"
YOUR_TAG = "UNE"

for root, dirs, files in os.walk(mod_pops_path):
    for filename in files:
        if filename.endswith(".txt"):
            file_path = os.path.join(root, filename)
            with open(file_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
            
            # This regex replaces things like region_state:GBR or region_state:PRU with region_state:FRA
            modified_content = re.sub(r'region_state:[A-Z]{3}', f'region_state:{YOUR_TAG}', content)
            
            with open(file_path, "w", encoding="utf-8-sig") as f:
                f.write(modified_content)

print("Successfully re-routed all native populations to your country tag!")
