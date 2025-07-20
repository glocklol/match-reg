#!/usr/bin/env python3
"""
Test registration status checking with duplicate prevention
"""

from match_registrar import PractiscoreRegistrar

def test_registration_checking():
    """Test complete registration status checking"""
    try:
        registrar = PractiscoreRegistrar()
        
        print("🔍 Getting available matches...")
        matches = registrar.get_available_matches()
        
        # Filter to only registration matches
        registration_matches = [m for m in matches if 'register' in m.get('url', '')]
        
        print(f"Found {len(registration_matches)} registration matches\n")
        
        # Test first match to see current registration status
        if registration_matches:
            test_match = registration_matches[0]
            match_title = test_match.get('title', 'Unknown')
            match_url = test_match.get('url', '')
            
            print(f"🎯 Testing registration check for: {match_title}")
            print(f"   URL: {match_url}\n")
            
            # Check if already registered
            print("1️⃣ Checking if already registered...")
            already_registered = registrar.check_if_already_registered(match_url)
            print(f"   Already registered: {already_registered}")
            
            # Check overall status
            print("\n2️⃣ Checking overall registration status...")
            status = registrar.check_registration_status(match_url)
            print(f"   Registration status: {status}")
            
            # Interpret status
            if status == "already_registered":
                print("   🟢 SAFE: Already registered - will not attempt duplicate registration")
            elif status == "open":
                print("   🟡 CAUTION: Registration open - would attempt to register")
            elif status == "not_open":
                print("   🔵 INFO: Registration not yet open")
            elif status == "full":
                print("   🔴 FULL: Match roster is full")
            else:
                print(f"   ❓ UNKNOWN: Unexpected status: {status}")
                
            # Show current registrations across all matches
            print("\n3️⃣ Checking all current registrations...")
            registered_matches = registrar.check_current_registrations()
            
            if registered_matches:
                print(f"   Currently registered for {len(registered_matches)} match(es)")
            else:
                print("   Not registered for any matches")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing registration status with duplicate prevention...")
    print("=" * 60)
    test_registration_checking()