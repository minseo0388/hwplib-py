import struct
import io
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.body_text import Section
from hwplib.hwp5.core.defs import HwpTag
from hwplib.hwp5.core.control import ControlLine, ControlRect, ControlEllipse, ControlParser

def create_mock_record(tag, content=b''):
    size = len(content)
    header_val = (tag & 0x3FF) | (0 << 10) | (size & 0xFFF) << 20
    return struct.pack('<I', header_val) + content

def test_shape_parsing():
    print("Test: Shape Parsing Integration")
    
    # 1. ParaHeader
    p_header = struct.pack('<IIHBBHHI', 3, 0, 1, 0, 0, 0, 0, 0)
    
    # 2. Control Keys (Reversed)
    # 'lin ' -> ' nil'
    # 'rec ' -> ' cer'
    lin = b' nil'
    rec = b' cer'
    
    # 3. Shape Records (Empty content for now)
    dummy_content = b'\x00' * 4
    
    data = b''
    data += create_mock_record(HwpTag.HWPTAG_PARA_HEADER, p_header)
    
    # Line
    data += create_mock_record(HwpTag.HWPTAG_CTRL_HEADER, lin)
    data += create_mock_record(HwpTag.HWPTAG_SHAPE_COMPONENT_LINE, dummy_content)
    
    # Rect
    data += create_mock_record(HwpTag.HWPTAG_CTRL_HEADER, rec)
    data += create_mock_record(HwpTag.HWPTAG_SHAPE_COMPONENT_RECTANGLE, dummy_content)
    
    stream = io.BytesIO(data)
    section = Section()
    section.parse(stream)
    
    para = section.paragraphs[0]
    print(f"  Controls found: {len(para.controls)}")
    
    found_line = False
    found_rect = False
    
    for ctrl in para.controls:
        print(f"    - Found {type(ctrl).__name__} (ID: {ctrl.ctrl_id})")
        if isinstance(ctrl, ControlLine): found_line = True
        if isinstance(ctrl, ControlRect): found_rect = True
        
    if found_line and found_rect:
        print("  SUCCESS: Both Line and Rect parsed")
    else:
        print(f"  FAILED: Missing objects (Line={found_line}, Rect={found_rect})")

if __name__ == "__main__":
    test_shape_parsing()
