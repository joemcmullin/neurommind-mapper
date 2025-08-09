import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
from neurommind_mapper.main import main

if __name__ == "__main__":
    main()