import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.api import load
from hwplib.hwp5.core.model import HwpDocument

def test_api_structure():
    print("Test: API Structure")
    
    doc = HwpDocument()
    print(f"  Initialized HwpDocument: {doc}")
    
    if hasattr(doc, 'get_text'):
        print("  SUCCESS: doc.get_text() exists")
    else:
        print("  FAILED: doc.get_text() missing")

    if callable(load):
        print("  SUCCESS: load() function exists")
    else:
        print("  FAILED: load() is not callable")

if __name__ == "__main__":
    test_api_structure()
