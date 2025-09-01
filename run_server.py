import sys
import os
import uvicorn

if __name__ == "__main__":
    # Get the absolute path to the directory containing this script (the project root)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the backend directory
    backend_dir = os.path.join(project_root, "Sarita-FASTAPI-BACKEND")

    # Add the backend directory to the Python path to ensure imports work
    sys.path.insert(0, backend_dir)

    # Change the current working directory to the backend directory
    # This is crucial for the app to find relative paths correctly (like app/.env)
    os.chdir(backend_dir)

    # Now, run uvicorn programmatically.
    # It will find 'app.main:app' because we've set the CWD and path.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
