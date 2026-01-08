import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.distribute.distribute_crypto import MSVCRandom, generate_random_arrays

def test_msvc_rand():
    print("Testing MSVC Random...")
    # Known sequence for Seed=1
    # 1st call: (1 * 214013 + 2531011) >> 16 & 0x7FFF = 41
    rnd = MSVCRandom(1)
    val1 = rnd.rand()
    print(f"  Seed 1, Call 1: {val1} (Expected 41)")
    
    val2 = rnd.rand()
    print(f"  Seed 1, Call 2: {val2} (Expected 18467)")
    
    if val1 == 41 and val2 == 18467:
        print("  SUCCESS: MSVC rand matches C++ behavior.")
    else:
        print("  FAILED: Value mismatch.")

def test_random_array():
    print("Testing Random Array Generation...")
    seed = 12345
    arr = generate_random_arrays(seed)
    print(f"  Array length: {len(arr)} (Expected 256)")
    print(f"  First 10 bytes: {list(arr[:10])}")
    
    if len(arr) == 256:
        print("  SUCCESS: Array length correct.")
    else:
        print("  FAILED: Array length incorrect.")

if __name__ == "__main__":
    test_msvc_rand()
    test_random_array()
