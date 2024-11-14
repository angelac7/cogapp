import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.modern_interface import ModernCogniCore

def main():
    try:
        app = ModernCogniCore()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()