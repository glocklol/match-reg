#!/usr/bin/env python3
"""
Test registration status checking
"""

from match_registrar import PractiscoreRegistrar

def test_registration_status():
    """Test checking registration status for found matches"""
    try:
        registrar = PractiscoreRegistrar()
        
        print("🔍 Getting available matches...")
        matches = registrar.get_available_matches()
        
        print(f"Found {len(matches)} matches, testing registration status...\n")
        
        for match in matches:
            if 'register' in match.get('url', ''):
                match_title = match.get('title', 'Unknown')
                match_url = match.get('url', '')
                
                print(f"🎯 Testing: {match_title}")
                print(f"   URL: {match_url}")
                
                status = registrar.check_registration_status(match_url)
                print(f"   Status: {status}")
                
                if status == "open":
                    print("   🟢 Registration is OPEN!")
                elif status == "not_open":
                    print("   🟡 Registration not yet open")
                elif status == "full":
                    print("   🔴 Match is full")
                else:
                    print(f"   ❓ Unknown status: {status}")
                    
                print()  # blank line
                
                # Only test first few to avoid being blocked
                break
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing registration status checking...")
    print("=" * 50)
    test_registration_status()