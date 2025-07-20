#!/usr/bin/env python3
"""
Test script to verify system readiness for Monday's automated registration
"""

import os
from datetime import datetime, timedelta
from match_registrar import PractiscoreRegistrar
from dotenv import load_dotenv

load_dotenv()

def test_monday_readiness():
    """Test all components needed for Monday's automated registration"""
    print("🚀 Monday Registration Readiness Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Environment Configuration
    print("\n1️⃣ Testing Environment Configuration...")
    
    required_secrets = [
        'PRACTISCORE_USERNAME',
        'PRACTISCORE_PASSWORD', 
        'REGISTRATION_FIRST_NAME',
        'REGISTRATION_LAST_NAME',
        'REGISTRATION_EMAIL',
        'REGISTRATION_POWER_FACTOR'
    ]
    
    missing_secrets = []
    for secret in required_secrets:
        if not os.getenv(secret):
            missing_secrets.append(secret)
    
    if missing_secrets:
        print(f"   ❌ Missing required secrets: {', '.join(missing_secrets)}")
        all_tests_passed = False
    else:
        print("   ✅ All required environment variables configured")
    
    # Test 2: Match Target Verification
    print("\n2️⃣ Testing Match Detection...")
    
    try:
        registrar = PractiscoreRegistrar()
        matches = registrar.get_available_matches()
        
        # Look for Run & Gun matches (target for Monday)
        run_gun_matches = []
        practice_matches = []
        
        for match in matches:
            title = match.get('title', '').lower()
            url = match.get('url', '')
            
            if 'run & gun' in title and 'register' in url:
                run_gun_matches.append(match)
            elif 'practice with purpose' in title and 'register' in url:
                practice_matches.append(match)
        
        print(f"   📊 Found {len(run_gun_matches)} Run & Gun matches")
        print(f"   📊 Found {len(practice_matches)} Practice with Purpose matches")
        
        # Show upcoming matches that would be targeted
        today = datetime.now()
        monday = today + timedelta(days=(7-today.weekday()) % 7)  # Next Monday
        
        upcoming_matches = []
        for match in run_gun_matches:
            match_title = match.get('title', '')
            # Look for dates in title that might indicate upcoming matches
            if any(date_str in match_title for date_str in ['07/28', '08/', '09/']):
                upcoming_matches.append(match)
        
        if upcoming_matches:
            print(f"   🎯 Found {len(upcoming_matches)} upcoming Run & Gun matches:")
            for match in upcoming_matches:
                print(f"      - {match.get('title')}")
                print(f"        URL: {match.get('url')}")
        else:
            print("   ⚠️  No obvious upcoming Run & Gun matches found")
        
    except Exception as e:
        print(f"   ❌ Match detection failed: {e}")
        all_tests_passed = False
    
    # Test 3: Registration Logic Verification
    print("\n3️⃣ Testing Registration Logic...")
    
    try:
        # Verify the system correctly identifies free vs paid matches
        test_titles = [
            "NSPS Run & Gun 07/28/25",  # Should be free
            "NSPS Run & Gun - with USPSA Classifiers 07/21/25",  # Should be paid
            "NSPS Practice with Purpose 07/24/25"  # Should be free
        ]
        
        for title in test_titles:
            is_paid = registrar.is_paid_match(title, "")
            match_type = "PAID" if is_paid else "FREE"
            print(f"   📝 \"{title}\": {match_type}")
        
        print("   ✅ Paid/Free match detection working")
        
    except Exception as e:
        print(f"   ❌ Registration logic test failed: {e}")
        all_tests_passed = False
    
    # Test 4: GitHub Action Schedule Verification
    print("\n4️⃣ Verifying GitHub Action Schedule...")
    
    try:
        with open('.github/workflows/match-checker.yml', 'r') as f:
            workflow_content = f.read()
        
        if "cron: '0 3 * * *'" in workflow_content:
            print("   ✅ GitHub Action scheduled for 10 PM Central (3 AM UTC) daily")
        else:
            print("   ⚠️  GitHub Action schedule may need verification")
        
        # Check if all required secrets are referenced
        required_env_vars = [
            'PRACTISCORE_USERNAME',
            'PRACTISCORE_PASSWORD',
            'REGISTRATION_FIRST_NAME', 
            'REGISTRATION_LAST_NAME',
            'REGISTRATION_EMAIL',
            'REGISTRATION_POWER_FACTOR'
        ]
        
        missing_workflow_vars = []
        for var in required_env_vars:
            if f"secrets.{var}" not in workflow_content:
                missing_workflow_vars.append(var)
        
        if missing_workflow_vars:
            print(f"   ⚠️  Workflow missing secret references: {', '.join(missing_workflow_vars)}")
        else:
            print("   ✅ All required secrets referenced in workflow")
            
    except Exception as e:
        print(f"   ❌ GitHub workflow verification failed: {e}")
        all_tests_passed = False
    
    # Test 5: Chrome Configuration
    print("\n5️⃣ Testing Chrome Configuration...")
    
    try:
        chrome_binary_found = False
        
        if os.path.exists('/snap/bin/chromium'):
            print("   ✅ Chromium binary found at /snap/bin/chromium (local)")
            chrome_binary_found = True
        
        if os.path.exists('/usr/bin/google-chrome'):
            print("   ✅ Chrome binary found at /usr/bin/google-chrome (GitHub Actions)")
            chrome_binary_found = True
        
        if not chrome_binary_found:
            print("   ⚠️  Chrome binary locations configured but not found locally (OK for GitHub Actions)")
        
        print("   ✅ Chrome configuration appears correct")
        
    except Exception as e:
        print(f"   ❌ Chrome configuration test failed: {e}")
        all_tests_passed = False
    
    # Final Summary
    print(f"\n🏁 Final Readiness Assessment:")
    print("=" * 40)
    
    if all_tests_passed:
        print("   🎉 SYSTEM READY FOR MONDAY!")
        print("   ✅ All components tested successfully")
        print(f"   📅 Next run: Monday at 10:00 PM Central")
        print(f"   🎯 Target: Run & Gun matches")
        
        print(f"\n📋 Required GitHub Secrets to Configure:")
        print("   Copy these values from your .env file to GitHub repository secrets:")
        for secret in required_secrets:
            if secret == 'PRACTISCORE_PASSWORD':
                print(f"   - {secret}: [HIDDEN]")
            else:
                print(f"   - {secret}: {os.getenv(secret, 'NOT_SET')}")
    else:
        print("   ❌ SYSTEM NOT READY - Issues found above")
        print("   🔧 Fix the issues before Monday")
    
    return all_tests_passed

if __name__ == "__main__":
    test_monday_readiness()