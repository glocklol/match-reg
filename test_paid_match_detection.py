#!/usr/bin/env python3
"""
Test paid match detection
"""

from match_registrar import PractiscoreRegistrar

def test_paid_match_detection():
    """Test detection of paid matches (classifiers, etc.)"""
    try:
        registrar = PractiscoreRegistrar()
        
        print("🔍 Testing paid match detection...")
        
        # Test cases
        test_matches = [
            ("NSPS Run & Gun - with USPSA Classifiers 07/21/25", "/test-url", True),
            ("NSPS Run & Gun 07/28/25", "/test-url", False),
            ("NSPS Practice with Purpose 07/24/25", "/test-url", False),
            ("USPSA Level II Classifier Match", "/test-url", True),
            ("Special Match - $25 Fee", "/test-url", True),
            ("Sanctioned USPSA Match", "/test-url", True),
        ]
        
        print("\nTesting match titles:")
        print("-" * 60)
        
        for title, url, expected_paid in test_matches:
            is_paid = registrar.is_paid_match(title, url)
            status = "✅ CORRECT" if is_paid == expected_paid else "❌ WRONG"
            paid_str = "PAID" if is_paid else "FREE"
            expected_str = "PAID" if expected_paid else "FREE"
            
            print(f"{status} {title}")
            print(f"      Detected: {paid_str} | Expected: {expected_str}")
            print()
            
        print("\nTesting actual matches from club page...")
        print("-" * 60)
        
        matches = registrar.get_available_matches()
        registration_matches = [m for m in matches if 'register' in m.get('url', '')]
        
        for match in registration_matches:
            title = match.get('title', 'Unknown')
            url = match.get('url', '')
            
            is_paid = registrar.is_paid_match(title, url)
            status_icon = "💳" if is_paid else "🆓"
            
            print(f"{status_icon} {title}")
            print(f"      URL: {url}")
            print(f"      Status: {'PAID (notification only)' if is_paid else 'FREE (auto-register possible)'}")
            print()
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing Paid Match Detection")
    print("=" * 60)
    test_paid_match_detection()