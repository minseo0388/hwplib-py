"""
examples/basic_usage.py

Demonstrates how to load an HWP file and extract all text.
"""
import sys
import os

# Add src to path if running from repo root
sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.api import load

def main():
    filename = "your_document.hwp"
    
    if not os.path.exists(filename):
        print(f"Please place an HWP file at '{filename}' to run this example.")
        return

    print(f"Loading {filename}...")
    doc = load(filename)
    
    # 1. Check Version
    print(f"HWP Version: {doc.header.version_str}")
    
    # 2. Extract Text
    text = doc.get_text()
    print("-" * 40)
    print(text[:500] + "..." if len(text) > 500 else text)
    print("-" * 40)

if __name__ == "__main__":
    main()
