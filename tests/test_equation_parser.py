import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from hwplib.hwp5.equation.equation_parser import EqParser

def test_parse(script, expected_contain=None):
    print(f"Parsing: [{script}]")
    try:
        parser = EqParser(script)
        ast = parser.parse()
        regen = ast.to_script()
        print(f"  -> Regenerated: [{regen}]")
        
        if expected_contain and expected_contain not in regen:
            print(f"  FAILED: Expected to contain '{expected_contain}'")
        else:
            print("  SUCCESS")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    # Test 1: Simple addition
    test_parse("a + b", "a + b")
    
    # Test 2: Fraction
    test_parse("a OVER b", "a OVER b")
    
    # Test 3: Superscript
    test_parse("x^2", "x^{2}")
    
    # Test 4: Complex grouping
    test_parse("{a + b} OVER {2a}", "a + b OVER 2a")
    
    # Test 5: Root
    test_parse("SQRT {x^2 + 1}", "SQRT {x^{2} + 1}")
    
    # Test 6: Decoration
    test_parse("vec {v}", "vec {v}")
