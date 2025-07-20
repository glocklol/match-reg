#!/usr/bin/env python3
"""
Test registration for Practice with Purpose match on 07/24/25
"""

import os
from match_registrar import PractiscoreRegistrar
import time

def test_practice_purpose_registration():
    """Test registration for specific Practice with Purpose match on 07/24/25"""
    try:
        registrar = PractiscoreRegistrar()
        
        print("🔍 Looking for Practice with Purpose 07/24/25 match...")
        matches = registrar.get_available_matches()
        
        # Look specifically for the 07/24/25 Practice with Purpose match
        target_match = None
        for match in matches:
            match_title = match.get('title', '').lower()
            if ('practice with purpose' in match_title and 
                '07/24/25' in match_title and 
                'register' in match.get('url', '')):
                target_match = match
                print(f"✅ Found target match: {match.get('title')}")
                break
        
        if not target_match:
            print("❌ Could not find Practice with Purpose 07/24/25 match with registration URL")
            print("Available matches:")
            for match in matches:
                if 'register' in match.get('url', ''):
                    print(f"  - {match.get('title')}")
            return False
        
        match_title = target_match.get('title', 'Unknown')
        match_url = target_match.get('url', '')
        
        print(f"\n🎯 Testing registration for: {match_title}")
        print(f"   URL: {match_url}")
        
        # Check current registration status
        print("\n1️⃣ Checking registration status...")
        status = registrar.check_registration_status(match_url, match_title)
        print(f"   Status: {status}")
        
        if status == "already_registered":
            print("   ✅ Already registered for this match!")
            return True
        elif status == "paid_match":
            print("   💳 This is a paid match - registration requires manual intervention")
            return False
        elif status == "open":
            print("   🟢 Registration is open!")
            
            # Test registration with provided details (passed as parameters for security)
            print("   🚀 Attempting test registration...")
            success = registrar.register_for_match(
                match_url,
                first_name="Adam",
                last_name="Golko", 
                email="a@asg.io",
                power_factor="minor"
            )
            
            if success:
                print("   ✅ Registration successful!")
                return True
            else:
                print("   ❌ Registration failed - check logs for details")
                return False
                
        elif status == "not_open":
            print("   ⏳ Registration not yet open")
            return False
        elif status == "full":
            print("   🔴 Match is full")
            return False
        else:
            print(f"   ❓ Unknown status: {status}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Practice with Purpose 07/24/25 registration...")
    print("=" * 70)
    success = test_practice_purpose_registration()
    
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test encountered issues - see output above")