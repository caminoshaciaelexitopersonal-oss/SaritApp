import uvicorn
import sys
import os

if __name__ == "__main__":
    # This script is located inside Sarita-FASTAPI-BACKEND.
    # We need to add the sibling directory Sarita-DB.git to the path.
    db_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Sarita-DB.git'))
    if db_repo_path not in sys.path:
        sys.path.insert(0, db_repo_path)

    # By running this script, the Current Working Directory is Sarita-FASTAPI-BACKEND.
    # Pydantic in app/core/config.py should find the .env file at 'app/.env'.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
