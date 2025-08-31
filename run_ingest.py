import sys
import os

# Add the backend directory to the Python path to resolve imports
backend_path = os.path.abspath("SGA-CD-FASTAPI-BACKEND")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Now that the path is set, we can import and run the main function
from app.agents.knowledge_base.ingest_docs import main

if __name__ == "__main__":
    print("Executing ingestion script via wrapper...")
    main()
    print("Wrapper script execution finished.")
