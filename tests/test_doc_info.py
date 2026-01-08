import struct
import io
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.doc_info import DocInfo
from hwplib.hwp5.core.defs import HwpTag

def create_mock_record(tag, content=b''):
    """
    Creates a record header + content.
    """
    size = len(content)
    # Tag(10) | Level(10) | Size(12)
    header_val = (tag & 0x3FF) | (0 << 10) | (size & 0xFFF) << 20
    return struct.pack('<I', header_val) + content

def test_doc_info_parse():
    print("Test: DocInfo Parsing")
    
    # Create stream with 1 FaceName, 1 CharShape, 1 ParaShape
    # Tag IDs: FaceName=0x13, CharShape=0x15, ParaShape=0x19
    data = b''
    data += create_mock_record(HwpTag.HWPTAG_FACE_NAME, b'FontData')
    data += create_mock_record(HwpTag.HWPTAG_CHAR_SHAPE, b'CharData')
    data += create_mock_record(HwpTag.HWPTAG_PARA_SHAPE, b'ParaData')
    
    stream = io.BytesIO(data)
    
    doc_info = DocInfo()
    doc_info.parse(stream)
    
    print(f"  FaceNames: {len(doc_info.face_names)}")
    print(f"  CharShapes: {len(doc_info.char_shapes)}")
    print(f"  ParaShapes: {len(doc_info.para_shapes)}")
    
    if len(doc_info.face_names) == 1 and len(doc_info.char_shapes) == 1 and len(doc_info.para_shapes) == 1:
        print("  SUCCESS")
    else:
        print("  FAILED")

if __name__ == "__main__":
    test_doc_info_parse()
