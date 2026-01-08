import struct
import io
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.body_text import Section
from hwplib.hwp5.core.defs import HwpTag

def create_mock_record(tag, content=b''):
    size = len(content)
    header_val = (tag & 0x3FF) | (0 << 10) | (size & 0xFFF) << 20
    return struct.pack('<I', header_val) + content

def test_section_parse():
    print("Test: Section Parsing")
    
    # 1. ParaHeader (Mock content 20 bytes)
    # text_len=5, mask=0, para_shape=1, style=0, divide=0, char_count=0, range_count=0, inst_id=0
    # struct.unpack('<IIHBBHHI', data[:20])
    p_header = struct.pack('<IIHBBHHI', 5, 0, 1, 0, 0, 0, 0, 0)
    
    # 2. ParaText "Hello" in UTF-16LE
    p_text = "Hello".encode('utf-16le')
    
    # 3. CharShape: Pos=0, Id=1 (8 bytes)
    p_char = struct.pack('<II', 0, 1)
    
    data = b''
    data += create_mock_record(HwpTag.HWPTAG_PARA_HEADER, p_header)
    data += create_mock_record(HwpTag.HWPTAG_PARA_TEXT, p_text)
    data += create_mock_record(HwpTag.HWPTAG_PARA_CHAR_SHAPE, p_char)
    
    stream = io.BytesIO(data)
    section = Section()
    section.parse(stream)
    
    print(f"  Paragraphs: {len(section.paragraphs)}")
    
    if len(section.paragraphs) == 1:
        para = section.paragraphs[0]
        print(f"  Text: '{para.text}'")
        print(f"  CharShapes: {len(para.char_shape_pointers)}")
        
        if para.text == "Hello" and len(para.char_shape_pointers) == 1:
            print("  SUCCESS")
        else:
            print("  FAILED: Content Validation")
    else:
        print("  FAILED: Paragraph Count")

if __name__ == "__main__":
    test_section_parse()
