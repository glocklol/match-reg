#!/usr/bin/env python3
"""
Test actual registration process with the July 21 match
"""

from match_registrar import PractiscoreRegistrar

def test_july_21_registration():
    """Test registration for the July 21 Run & Gun match"""
    try:
        registrar = PractiscoreRegistrar()
        
        # Target the July 21 match
        match_url = "/nsps-run-gun-with-uspsa-classifiers-07-21-25/register"
        match_title = "NSPS Run & Gun - with USPSA Classifiers 07/21/25"
        
        print(f"🎯 Testing registration for: {match_title}")
        print(f"   URL: {match_url}")
        
        # Check current status first
        print("\n1️⃣ Checking if already registered...")
        already_registered = registrar.check_if_already_registered(match_url)
        print(f"   Already registered: {already_registered}")
        
        if already_registered:
            print("   ✅ Already registered - skipping registration attempt")
            return
        
        # Check overall registration status
        print("\n2️⃣ Checking registration status...")
        status = registrar.check_registration_status(match_url)
        print(f"   Registration status: {status}")
        
        if status == "open":
            print("   🟢 Registration is open!")
            
            # Ask for confirmation
            response = input("\n   🚨 WARNING: This will actually register you for the match!")
            response += input("      Do you want to proceed? Type 'YES' to confirm: ").strip()
            
            if response == "YES":
                print("   🚀 Proceeding with actual registration...")
                
                success = registrar.register_for_match(match_url)
                
                if success:
                    print("   ✅ Registration successful!")
                    print("   📧 You should receive a confirmation email")
                else:
                    print("   ❌ Registration failed - check logs")
                    
                # Check status again to confirm
                print("\n3️⃣ Verifying registration...")
                new_status = registrar.check_registration_status(match_url)
                print(f"   New status: {new_status}")
                
            else:
                print("   ⏸️ Registration cancelled")
                
        elif status == "already_registered":
            print("   ✅ Already registered!")
        elif status == "not_open":
            print("   ⏳ Registration not yet open")
        elif status == "full":
            print("   🔴 Match is full")
        else:
            print(f"   ❓ Unknown status: {status}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing Actual Registration Process")
    print("=" * 60)
    print("⚠️  This will attempt REAL registration if you confirm!")
    print("=" * 60)
    test_july_21_registration()