"""
examples/extract_tables.py

Demonstrates how to iterate through HWP tables and extract cell data.
"""
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.api import load
from hwplib.hwp5.core.control import ControlTable

def main():
    filename = "your_document.hwp"
    if not os.path.exists(filename):
        print(f"Please place an HWP file at '{filename}'")
        return

    doc = load(filename)
    
    table_count = 0
    for section in doc.sections:
        for paragraph in section.paragraphs:
            for ctrl in paragraph.controls:
                
                # Check if control is a Table
                if isinstance(ctrl, ControlTable):
                    table_count += 1
                    print(f"\n[Table #{table_count}] Rows: {ctrl.row_count}, Cols: {ctrl.col_count}")
                    
                    for r_idx, row in enumerate(ctrl.rows):
                        row_data = []
                        for cell in row.cells:
                            # Extract text from the cell's paragraphs
                            cell_text = " ".join([p.text for p in cell.paragraphs])
                            row_data.append(cell_text)
                        
                        print(f"  Row {r_idx}: {row_data}")

if __name__ == "__main__":
    main()
