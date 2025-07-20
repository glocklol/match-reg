#!/usr/bin/env python3
"""
Test the full system with paid/free match handling
"""

from match_registrar import PractiscoreRegistrar

def test_full_system():
    """Test the complete system with current matches"""
    try:
        print("🧪 Testing Full System with Paid/Free Match Handling")
        print("=" * 70)
        
        registrar = PractiscoreRegistrar()
        
        # This will run the complete check process
        registrar.run_check()
        
        print("\n" + "=" * 70)
        print("🏁 System test complete!")
        print("Check the logs above to see how the system handled each match type.")
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_system()