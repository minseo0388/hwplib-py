import struct
import io
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.core.file_header import HwpFileHeader

def test_valid_header():
    print("Test 1: Valid Header")
    # Signature (32 bytes)
    sig = b"HWP Document File" + b"\x00" * (32 - len(b"HWP Document File"))
    
    # Version 5.0.3.0 -> 0x05000300 (Little Endian?)
    # MM nn PP rr -> 5.0.3.0
    # Val = (5<<24) | (0<<16) | (3<<8) | 0
    ver_val = (5<<24) | (0<<16) | (3<<8) | 0
    # Actually code uses shift like this:
    # rr = val >> 0
    # pp = val >> 8
    # nn = val >> 16
    # mm = val >> 24
    # So constructing int is (MM<<24)...
    # struct pack '<I' puts LSB first.
    # 0x05000300 -> 00 03 00 05
    ver_bytes = struct.pack('<I', ver_val)
    
    # Flags: Compressed(1) + Encrypted(2) = 3
    flags_val = 3
    flags_bytes = struct.pack('<I', flags_val)
    
    # Padding to 256
    padding = b"\x00" * (256 - 32 - 4 - 4)
    
    data = sig + ver_bytes + flags_bytes + padding
    
    header = HwpFileHeader()
    header.parse(data)
    
    print(f"  Parsed Version: {header.version_str}")
    print(f"  Flags: Compressed={header.is_compressed}, Encrypted={header.is_encrypted}")
    
    if header.version_mm == 5 and header.is_compressed and header.is_encrypted:
        print("  SUCCESS")
    else:
        print("  FAILED")

if __name__ == "__main__":
    test_valid_header()
