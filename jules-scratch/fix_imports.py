import os
import re

def fix_imports_in_dir(directory_to_fix):
    if not os.path.isdir(directory_to_fix):
        print(f"Error: Directory not found at {directory_to_fix}")
        return

    print(f"Scanning directory: {directory_to_fix}")
    for filename in os.listdir(directory_to_fix):
        if filename.endswith(".py"):
            filepath = os.path.join(directory_to_fix, filename)
            try:
                with open(filepath, 'r') as f:
                    lines = f.readlines()

                new_lines = []
                modified = False
                # Fix relative imports of models
                for line in lines:
                    if line.strip().startswith("from ..models"):
                        modified = True
                        new_line = line.replace("from ..models", "from models")
                        new_lines.append(new_line)
                        print(f"Found in {filename}: {line.strip()} -> {new_line.strip()}")
                    else:
                        new_lines.append(line)

                if modified:
                    with open(filepath, 'w') as f:
                        f.writelines(new_lines)
                    print(f"  -> Patched {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Fix the crud directory in the new backend_principal
    crud_dir = "sarita/backend_principal/app/crud"
    fix_imports_in_dir(crud_dir)

    # Also fix the endpoints just in case
    endpoints_dir = "sarita/backend_principal/app/api/v1/endpoints"
    # In endpoints, the error was `from app import models`, which is more complex.
    # I will stick to manual fixing for endpoints as it's only a few files.
    print("\\nManual check might be needed for endpoints directory.")
