import os
import re

# ==================== CONFIGURATION ====================
# Path to YOUR MOD'S copied history/buildings folder
mod_buildings_path = "C:/Users/themc/Documents/Paradox Interactive/Victoria 3/mod/Earth Mod/common/history/buildings"

TAG = "UNE"  # Replace with your country's 3-letter code
# ========================================================

print("Forcing full building financial ownership transfer... Please wait.")

count = 0
for root, dirs, files in os.walk(mod_buildings_path):
    for filename in files:
        if filename.endswith(".txt"):
            file_path = os.path.join(root, filename)
            
            with open(file_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
            
            # STEP 1: Re-route where the building physically exists (State owner)
            content = re.sub(r'region_state:[A-Z]{3}', f'region_state:{TAG}', content)
            
            # STEP 2: Forcefully seize financial equity/ownership block
            # This turns country = "c:GBR" or country = "c:RUS" into country = "c:FRA"
            content = re.sub(r'country\s*=\s*"c:[A-Z]{3}"', f'country = "c:{TAG}"', content)
            
            with open(file_path, "w", encoding="utf-8-sig") as f:
                f.write(content)
            count += 1

print(f"Successfully nationalized and re-routed buildings in {count} files to c:{TAG}!")
