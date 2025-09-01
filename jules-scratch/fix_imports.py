import os
import re

def fix_imports_in_endpoints():
    endpoints_dir = "Sarita-FASTAPI-BACKEND/app/api/v1/endpoints/"
    if not os.path.isdir(endpoints_dir):
        print(f"Error: Directory not found at {endpoints_dir}")
        return

    print(f"Scanning directory: {endpoints_dir}")
    for filename in os.listdir(endpoints_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(endpoints_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    lines = f.readlines()

                new_lines = []
                modified = False
                for line in lines:
                    # Look for the problematic pattern
                    if "from app import" in line and "models" in line:
                        modified = True
                        print(f"Found problematic import in {filename}: {line.strip()}")

                        # Extract modules other than 'models'
                        parts = line.replace("from app import", "").strip().split(',')
                        other_modules = [p.strip() for p in parts if "models" not in p and p.strip()]

                        # Create new import statements
                        if other_modules:
                            new_lines.append(f"from app import {', '.join(other_modules)}\n")
                        new_lines.append("import models\n")
                        print(f"  -> Replacing with: from app import {', '.join(other_modules)} / import models")
                    else:
                        new_lines.append(line)

                if modified:
                    with open(filepath, 'w') as f:
                        f.writelines(new_lines)
                    print(f"  -> Patched {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    fix_imports_in_endpoints()
