#!/usr/bin/env python3
"""
Dry run test for Practice with Purpose match on 07/24/25 - checks form fields without registering
"""

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def test_practice_purpose_dry_run():
    """Test accessing the registration form without submitting"""
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.binary_location = '/snap/bin/chromium'
        
        driver = webdriver.Chrome(options=chrome_options)
        
        print("🔍 Testing access to Practice with Purpose 07/24/25 registration...")
        
        # Go directly to the registration URL
        registration_url = "https://practiscore.com/nsps-practice-with-purpose-07-24-25/register"
        driver.get(registration_url)
        time.sleep(3)
        
        print(f"✅ Successfully loaded registration page: {registration_url}")
        print(f"   Page title: {driver.title}")
        
        # Parse the page to look for form fields
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Check for login requirement
        if "login" in driver.current_url.lower() or "sign in" in soup.get_text().lower():
            print("🔐 Registration requires login - this is expected")
            
            # Try to find login form elements
            login_form = soup.find('form')
            if login_form:
                print("   Found login form with fields:")
                for input_field in login_form.find_all(['input', 'button']):
                    field_type = input_field.get('type', 'unknown')
                    field_name = input_field.get('name', 'unnamed')
                    if field_type not in ['hidden', 'csrf']:
                        print(f"     - {field_name}: {field_type}")
            
        # Check for registration form fields (may be after login)
        form_fields = soup.find_all(['input', 'select', 'textarea'])
        registration_fields = []
        
        for field in form_fields:
            field_name = field.get('name', '').lower()
            field_type = field.get('type', 'unknown')
            
            if any(keyword in field_name for keyword in ['first', 'last', 'name', 'email', 'power', 'division', 'class']):
                registration_fields.append({
                    'name': field.get('name', 'unnamed'),
                    'type': field_type,
                    'required': field.get('required') is not None
                })
        
        if registration_fields:
            print(f"\n📋 Found {len(registration_fields)} potential registration fields:")
            for field in registration_fields:
                required_text = " (required)" if field['required'] else ""
                print(f"   - {field['name']}: {field['type']}{required_text}")
        else:
            print("\n⚠️  No obvious registration fields found (may require login)")
        
        # Check for any indication this is the correct match
        page_text = soup.get_text().lower()
        match_indicators = []
        
        if "practice with purpose" in page_text:
            match_indicators.append("✅ Contains 'Practice with Purpose'")
        if "07/24" in page_text or "july 24" in page_text:
            match_indicators.append("✅ Contains July 24 date")
        if "nsps" in page_text:
            match_indicators.append("✅ Contains NSPS club reference")
            
        if match_indicators:
            print(f"\n🎯 Match verification:")
            for indicator in match_indicators:
                print(f"   {indicator}")
        else:
            print("\n❓ Could not verify this is the correct match page")
        
        # Check registration status indicators
        if any(term in page_text for term in ["registration closed", "full", "sold out"]):
            print("\n🔴 Registration appears to be closed or full")
        elif "register" in page_text:
            print("\n🟢 Registration appears to be available")
        else:
            print("\n❓ Registration status unclear")
            
        print(f"\n📊 Test Summary:")
        print(f"   - Successfully accessed registration URL: ✅")
        print(f"   - Form fields detected: {'✅' if registration_fields else '❓'}")
        print(f"   - Match verification: {'✅' if match_indicators else '❓'}")
        print(f"   - Ready for actual registration: {'✅' if registration_fields and match_indicators else '⚠️'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    print("🧪 Dry Run Test: Practice with Purpose 07/24/25")
    print("=" * 60)
    print("This test checks form access without submitting registration")
    print()
    
    success = test_practice_purpose_dry_run()
    
    if success:
        print("\n🎉 Dry run completed - ready for actual registration testing!")
    else:
        print("\n❌ Dry run encountered issues")