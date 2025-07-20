#!/usr/bin/env python3
"""
Test script for PractiScore scraper
"""

import os
from match_registrar import PractiscoreRegistrar

def test_basic_functionality():
    """Test basic scraper functionality"""
    try:
        print("🔍 Initializing PractiscoreRegistrar...")
        registrar = PractiscoreRegistrar()
        print("✅ Registrar initialized successfully!")
        
        print("\n🌐 Testing club page access...")
        matches = registrar.get_available_matches()
        print(f"✅ Found {len(matches)} potential matches")
        
        if matches:
            print("\n📋 Match details:")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match.get('title', 'Unknown Title')}")
                print(f"     URL: {match.get('url', 'No URL')}")
        else:
            print("ℹ️  No 'NSPS Run & Gun' matches found on the page")
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing PractiScore scraper functionality...")
    print("=" * 50)
    
    # Check environment variables
    if not os.getenv('PRACTISCORE_USERNAME') or not os.getenv('PRACTISCORE_PASSWORD'):
        print("⚠️  Warning: PractiScore credentials not found in environment!")
        print("   Make sure .env file exists with correct credentials")
    
    success = test_basic_functionality()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed!")
    else:
        print("💥 Some tests failed!")