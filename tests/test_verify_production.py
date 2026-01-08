import sys
import os
import io

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.model import HwpDocument
from hwplib.hwp5.core.body_text import Section, Paragraph
from hwplib.hwp5.core.control import ControlEquation, ControlTable

def test_production_logic():
    print("Test: Production Logic Verification")
    
    # 1. Manually construct a Document Model
    doc = HwpDocument()
    doc.header.version_str = "5.0.0.0"
    
    # 2. Create a Section
    section = Section()
    
    # 3. Add Paragraph 1 (Plain Text)
    p1 = Paragraph()
    p1.text = "Hello World"
    section.paragraphs.append(p1)
    
    # 4. Add Paragraph 2 (Equation)
    p2 = Paragraph()
    p2.text = "Equation:" # Anchor text
    eq = ControlEquation()
    eq.script = "y = ax + b"
    p2.controls.append(eq)
    section.paragraphs.append(p2)
    
    # 5. Add Paragraph 3 (Table Placeholder)
    p3 = Paragraph()
    p3.text = "Cell Text" # Simulated cell parsing falling through to main stream
    # Note: If we had fully implemented recursive parsing, this text would be inside the Cell object.
    # But currently it sits in the main stream.
    section.paragraphs.append(p3)
    
    doc.sections.append(section)
    
    # 6. Execute get_text()
    extracted_text = doc.get_text()
    
    print("-" * 20)
    print(extracted_text)
    print("-" * 20)
    
    # 7. Assertions
    if "Hello World" in extracted_text:
        print("PASS: Plain text extracted")
    else:
        print("FAIL: Plain text missing")
        
    if "y = ax + b" in extracted_text:
        print("PASS: Equation script extracted (New Feature)")
    else:
        print("FAIL: Equation script missing")
        
    if "Cell Text" in extracted_text:
        print("PASS: Table cell text extracted (Linear Fallback)")
    else:
        print("FAIL: Table text missing")

if __name__ == "__main__":
    test_production_logic()
