import struct
import io
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.record import RecordParser, HwpRecord

def create_mock_header(tag, level, size):
    """
    Creates a 4-byte header value.
    """
    val = (tag & 0x3FF) | ((level & 0x3FF) << 10) | ((size & 0xFFF) << 20)
    return struct.pack('<I', val)

def test_single_record():
    print("Test 1: Single Record")
    # Tag=10, Level=0, Size=5
    header = create_mock_header(10, 0, 5)
    content = b'HELLO'
    stream = io.BytesIO(header + content)
    
    parser = RecordParser(stream)
    records = list(parser.parse_records())
    
    if len(records) == 1:
        r = records[0]
        print(f"  Parsed: Tag={r.tag_id}, Level={r.level}, Size={r.size}")
        if r.tag_id == 10 and r.size == 5 and r.content == b'HELLO':
            print("  SUCCESS")
        else:
            print("  FAILED: Content mismatch")
    else:
        print("  FAILED: Record count incorrect")

def test_extended_record():
    print("Test 2: Extended Record")
    # Tag=20, Level=1, Size=4095 (0xFFF) -> Followed by real size (e.g., 4100)
    header = create_mock_header(20, 1, 0xFFF)
    real_size = 4100
    size_header = struct.pack('<I', real_size)
    content = b'A' * real_size
    
    stream = io.BytesIO(header + size_header + content)
    parser = RecordParser(stream)
    records = list(parser.parse_records())
    
    if len(records) == 1:
        r = records[0]
        print(f"  Parsed: Tag={r.tag_id}, Size={r.size}")
        if r.tag_id == 20 and r.size == real_size and len(r.content) == real_size:
            print("  SUCCESS")
        else:
            print("  FAILED: Size mismatch")
    else:
        print("  FAILED: Record count incorrect")

if __name__ == "__main__":
    test_single_record()
    test_extended_record()
