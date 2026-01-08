import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.control import ControlTable, ControlPicture, ControlEquation, ControlParser

def test_control_instantiation():
    print("Test: Control Instantiation")
    
    # Table
    tbl = ControlTable()
    print(f"  Table ID: '{tbl.ctrl_id}'")
    if tbl.ctrl_id == 'tbl':
        print("    SUCCESS: Table ID")
    else:
        print("    FAILED: Table ID")

    # Picture
    pic = ControlPicture()
    print(f"  Picture ID: '{pic.ctrl_id}'")
    if pic.ctrl_id == 'pic':
        print("    SUCCESS: Picture ID")
    else:
        print("    FAILED: Picture ID")

    # Equation
    eq = ControlEquation()
    print(f"  Equation ID: '{eq.ctrl_id}'")
    if eq.ctrl_id == 'eq ': # Note the space
        print("    SUCCESS: Equation ID")
    else:
        print("    FAILED: Equation ID")

def test_control_header_parsing():
    print("Test: Control Header Parsing")
    # 'tbl ' in binary (reversed) -> ' lbt' ?
    # Standard usually 4 chars.
    # Let's verify what we extract.
    # If binary is b'tbl ', decode ascii -> 'tbl ', reverse -> ' lbt'.
    # If binary is reversed 0x206c6274 -> b' lbt', decode -> ' lbt', reverse -> 'tbl '
    # Logic in control.py: data[:4].decode()[::-1]
    
    # Case 1: Stored as ' lbt' (Little Endian integer 0x74626C20)
    data = b' lbt' 
    parsed = ControlParser.parse_header(data)
    print(f"  Input ' lbt' -> Parsed '{parsed}'")
    if parsed == 'tbl ':
        print("    SUCCESS: Parsed 'tbl '")
    else:
        print(f"    FAILED: Expected 'tbl ', got '{parsed}'")

if __name__ == "__main__":
    test_control_instantiation()
    test_control_header_parsing()
