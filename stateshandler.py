import os
import re

# ==================== CONFIGURATION ====================
# Path to your Victoria 3 installation folder map data
vanilla_map_path = "C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/map_data/state_regions"

# Path directly to your mod's history file (the script will create/overwrite it)
mod_output_path = "C:/Users/themc/Documents/Paradox Interactive/Victoria 3/mod/Earth Mod/common/history/states/00_states.txt"

TAG = "UNE"  # Replace with your country's 3-letter code
# ========================================================

# Ensure the output directory exists
os.makedirs(os.path.dirname(mod_output_path), exist_ok=True)

print("Parsing game files and writing directly to mod file... Please wait.")

with open(mod_output_path, "w", encoding="utf-8-sig") as out_file:
    out_file.write("STATES = {\n")

    for filename in os.listdir(vanilla_map_path):
        if filename.endswith(".txt"):
            with open(os.path.join(vanilla_map_path, filename), "r", encoding="utf-8-sig") as f:
                content = f.read()
                
                # Remove comments to avoid tracking fake braces
                content = re.sub(r'#.*', '', content)
                
                pos = 0
                while True:
                    match = re.search(r'(STATE_[A-Z0-9_]+)\s*=\s*\{', content[pos:])
                    if not match:
                        break
                    
                    state_name = match.group(1)
                    start_idx = pos + match.end()
                    
                    # Track bracket depth to grab the nested structure safely
                    depth = 1
                    end_idx = start_idx
                    while depth > 0 and end_idx < len(content):
                        if content[end_idx] == '{':
                            depth += 1
                        elif content[end_idx] == '}':
                            depth -= 1
                        end_idx += 1
                    
                    block_body = content[start_idx:end_idx-1]
                    pos = end_idx  # Move forward
                    
                    # Filter out sea/lake zones
                    if "sea = yes" in block_body or "lake = yes" in block_body:
                        continue
                    
                    # Extract the province list block
                    province_match = re.search(r'provinces\s*=\s*\{\s*([^}]+)\}', block_body)
                    if province_match:
                        raw_provinces = province_match.group(1).replace('"', '')
                        provinces_list = " ".join(raw_provinces.split())
                        
                        # Write directly to the target file
                        out_file.write(f"    s:{state_name} = {{\n")
                        out_file.write(f"        create_state = {{\n")
                        out_file.write(f"            country = c:{TAG}\n")
                        out_file.write(f"            owned_provinces = {{ {provinces_list} }}\n")
                        out_file.write(f"        }}\n")
                        out_file.write(f"    }}\n")

    out_file.write("}\n")

print(f"Successfully generated and wrote all states directly to: {mod_output_path}")
