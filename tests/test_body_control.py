import struct
import io
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.body_text import Section
from hwplib.hwp5.core.defs import HwpTag
from hwplib.hwp5.core.control import ControlTable

def create_mock_record(tag, content=b''):
    size = len(content)
    header_val = (tag & 0x3FF) | (0 << 10) | (size & 0xFFF) << 20
    return struct.pack('<I', header_val) + content

def test_control_parse():
    print("Test: Control Parsing Integration")
    
    # 1. ParaHeader
    p_header = struct.pack('<IIHBBHHI', 3, 0, 1, 0, 0, 0, 0, 0)
    
    # 2. Control Header: 'tbl ' reversed -> ' lbt'
    # b' lbt'
    c_header = b' lbt'
    
    # 3. Table Record (Dummy content)
    t_prop = b'\x00' * 10
    
    data = b''
    data += create_mock_record(HwpTag.HWPTAG_PARA_HEADER, p_header)
    data += create_mock_record(HwpTag.HWPTAG_CTRL_HEADER, c_header)
    data += create_mock_record(HwpTag.HWPTAG_TABLE, t_prop)
    
    stream = io.BytesIO(data)
    section = Section()
    section.parse(stream)
    
    para = section.paragraphs[0]
    print(f"  Paragraph Control Count: {len(para.controls)}")
    
    if len(para.controls) == 1:
        ctrl = para.controls[0]
        print(f"  Control Type: {type(ctrl).__name__}")
        print(f"  Control ID: '{ctrl.ctrl_id}'")
        
        if isinstance(ctrl, ControlTable) and ctrl.ctrl_id == 'tbl':
            print("  SUCCESS: Control Identified and Object Created")
        else:
            print("  FAILED: Type Mismatch")
    else:
        print("  FAILED: Control not attached")

if __name__ == "__main__":
    test_control_parse()
