#!/usr/bin/env python3
"""
Test registration for Practice with Purpose match
"""

from match_registrar import PractiscoreRegistrar
import time

def test_practice_registration():
    """Test actual registration for Practice with Purpose match"""
    try:
        registrar = PractiscoreRegistrar()
        
        print("🔍 Getting available matches...")
        matches = registrar.get_available_matches()
        
        # Look for Practice with Purpose matches
        practice_matches = []
        for match in matches:
            match_title = match.get('title', '').lower()
            if 'practice with purpose' in match_title and 'register' in match.get('url', ''):
                practice_matches.append(match)
                print(f"Found Practice match: {match.get('title')}")
        
        if not practice_matches:
            print("❌ No Practice with Purpose matches found with registration URLs")
            return
        
        # Use the first Practice with Purpose match
        test_match = practice_matches[0]
        match_title = test_match.get('title', 'Unknown')
        match_url = test_match.get('url', '')
        
        print(f"\n🎯 Testing registration for: {match_title}")
        print(f"   URL: {match_url}")
        
        # Check current status
        print("\n1️⃣ Checking registration status...")
        status = registrar.check_registration_status(match_url)
        print(f"   Status: {status}")
        
        if status == "already_registered":
            print("   ✅ Already registered for this match!")
        elif status == "open":
            print("   🟢 Registration is open!")
            
            # Ask for confirmation before registering
            response = input("\n   Do you want to proceed with registration? (y/N): ").strip().lower()
            
            if response in ['y', 'yes']:
                print("   🚀 Attempting registration...")
                success = registrar.register_for_match(match_url)
                
                if success:
                    print("   ✅ Registration successful!")
                else:
                    print("   ❌ Registration failed - check logs for details")
            else:
                print("   ⏸️ Registration cancelled by user")
                
        elif status == "not_open":
            print("   ⏳ Registration not yet open")
        elif status == "full":
            print("   🔴 Match is full")
        else:
            print(f"   ❓ Unknown status: {status}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing Practice with Purpose registration...")
    print("=" * 60)
    test_practice_registration()