import os
import sys

print(f"Current Working Directory: {os.getcwd()}")
print(f"Absolute path of script: {os.path.abspath(__file__)}")
print(f"sys.path: {sys.path}")
