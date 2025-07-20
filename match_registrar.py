#!/usr/bin/env python3
"""
PractiScore USPSA Match Auto-Registration Tool
Automatically registers for NSPS Run & Gun matches at North Shore Practical Shooters
"""

import os
import time
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import pytz
from notifications import NotificationManager

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('match_registrar.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PractiscoreRegistrar:
    def __init__(self):
        self.base_url = "https://practiscore.com"
        self.club_url = f"{self.base_url}/clubs/north_shore_practical_shooters"
        self.login_url = f"{self.base_url}/login"
        
        self.username = os.getenv('PRACTISCORE_USERNAME')
        self.password = os.getenv('PRACTISCORE_PASSWORD')
        self.target_match = os.getenv('TARGET_MATCH_NAME', 'NSPS')  # Match both Run & Gun and Practice
        
        if not self.username or not self.password:
            raise ValueError("PractiScore credentials not found in environment variables")
        
        # Setup Chrome options for headless browsing with Cloudflare bypass
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless=new')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
        
        # Add experimental options to avoid detection
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Additional preferences to appear more like a real browser
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2
        }
        self.chrome_options.add_experimental_option("prefs", prefs)
        
        # Set binary location based on environment  
        chrome_binary_set = False
        chrome_paths = [
            '/snap/bin/chromium',
            '/usr/bin/google-chrome', 
            '/opt/hostedtoolcache/setup-chrome/chrome/stable/x64/chrome',
            '/usr/bin/chromium-browser',
            '/usr/bin/chrome'
        ]
        
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                self.chrome_options.binary_location = chrome_path
                logger.info(f"Using Chrome binary at: {chrome_path}")
                chrome_binary_set = True
                break
        
        if not chrome_binary_set:
            logger.warning("No Chrome binary found in expected locations")
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Initialize notification manager
        self.notifier = NotificationManager()
        
    def get_available_matches(self) -> List[Dict]:
        """Get all available matches from the club page"""
        logger.info("Fetching available matches from club page...")
        
        # Log Chrome binary location being used
        if hasattr(self.chrome_options, 'binary_location'):
            logger.info(f"Chrome binary location: {self.chrome_options.binary_location}")
        else:
            logger.info("Using default Chrome binary location")
        
        # Log Chrome arguments being used
        logger.info(f"Chrome arguments: {self.chrome_options.arguments}")
        
        try:
            # Set DISPLAY for headless mode if not set
            import os
            if 'DISPLAY' not in os.environ:
                os.environ['DISPLAY'] = ':99'
                logger.info("Set DISPLAY environment variable to :99")
            
            driver = webdriver.Chrome(options=self.chrome_options)
            
            # Execute script to remove webdriver property  
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return []
        
        try:
            logger.info(f"Navigating to club URL: {self.club_url}")
            
            # Try multiple times if Cloudflare blocks us
            for attempt in range(3):
                driver.get(self.club_url)
                time.sleep(5)  # Wait longer for page to load
                
                current_url = driver.current_url
                page_title = driver.title
                page_length = len(driver.page_source)
                
                logger.info(f"Attempt {attempt + 1}: URL: {current_url}, Title: {page_title}, Length: {page_length}")
                
                # Check if we're blocked by Cloudflare
                if "cloudflare" in page_title.lower() or page_length < 10000:
                    logger.warning(f"Attempt {attempt + 1}: Detected Cloudflare block, retrying...")
                    if attempt < 2:  # Don't sleep on last attempt
                        time.sleep(10)  # Wait longer between attempts
                    continue
                else:
                    logger.info("Successfully loaded PractiScore page")
                    break
            else:
                logger.error("Failed to bypass Cloudflare after 3 attempts")
                return []
            
            # Look for match elements
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            matches = []
            
            logger.info(f"Final page content length: {len(driver.page_source)} characters")
            
            # Find match containers (this will need to be adjusted based on actual HTML structure)
            match_elements = soup.find_all(['div', 'a'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['match', 'event', 'competition']
            ))
            
            logger.info(f"Found {len(match_elements)} potential match elements")
            
            for i, element in enumerate(match_elements):
                element_text = element.get_text().strip()
                logger.debug(f"Element {i}: {element_text[:100]}...")  # First 100 chars
                
                if self.target_match.lower() in element_text.lower():
                    match_data = {
                        'title': element_text,
                        'url': element.get('href', ''),
                        'element': str(element)
                    }
                    matches.append(match_data)
                    logger.info(f"Matched element: {element_text[:100]}...")
            
            logger.info(f"Found {len(matches)} matching events")
            return matches
            
        except Exception as e:
            logger.error(f"Error fetching matches: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
        finally:
            try:
                driver.quit()
                logger.info("Chrome driver closed")
            except:
                pass
    
    def login(self, driver) -> bool:
        """Login to PractiScore"""
        logger.info("Logging in to PractiScore...")
        
        try:
            driver.get(self.login_url)
            time.sleep(3)
            
            # Try multiple selectors for username field
            username_field = None
            for selector in [
                (By.NAME, "username"),
                (By.NAME, "email"),
                (By.ID, "username"),
                (By.ID, "email"),
                (By.XPATH, "//input[@type='email']"),
                (By.XPATH, "//input[contains(@placeholder, 'email')]"),
                (By.XPATH, "//input[contains(@placeholder, 'username')]")
            ]:
                try:
                    username_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    break
                except:
                    continue
            
            if not username_field:
                logger.error("Could not find username/email field")
                return False
            
            # Try multiple selectors for password field
            password_field = None
            for selector in [
                (By.NAME, "password"),
                (By.ID, "password"),
                (By.XPATH, "//input[@type='password']")
            ]:
                try:
                    password_field = driver.find_element(*selector)
                    break
                except:
                    continue
            
            if not password_field:
                logger.error("Could not find password field")
                return False
            
            # Clear and fill fields
            username_field.clear()
            username_field.send_keys(self.username)
            password_field.clear()
            password_field.send_keys(self.password)
            
            time.sleep(1)
            
            # Try multiple selectors for submit button
            submit_button = None
            for selector in [
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//input[@type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Sign In')]"),
                (By.XPATH, "//button[contains(text(), 'Log In')]"),
                (By.XPATH, "//button[contains(text(), 'Login')]")
            ]:
                try:
                    submit_button = driver.find_element(*selector)
                    break
                except:
                    continue
            
            if not submit_button:
                logger.error("Could not find submit button")
                return False
            
            submit_button.click()
            time.sleep(4)
            
            # Check if login was successful
            current_url = driver.current_url.lower()
            page_source = driver.page_source.lower()
            
            if ("login" not in current_url and "sign" not in current_url) or "dashboard" in current_url:
                logger.info("Login successful")
                return True
            elif "invalid" in page_source or "incorrect" in page_source:
                logger.error("Login failed - invalid credentials")
                return False
            else:
                logger.warning("Login status unclear, continuing...")
                return True  # Assume success if no clear failure indicators
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def check_if_already_registered(self, match_url: str) -> bool:
        """Check if user is already registered for a match"""
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            if not self.login(driver):
                logger.error("Failed to login while checking registration status")
                return False
            
            full_url = match_url if match_url.startswith('http') else f"{self.base_url}{match_url}"
            driver.get(full_url)
            time.sleep(3)
            
            page_source = driver.page_source.lower()
            
            # Check for indicators that user is already registered
            already_registered_indicators = [
                "already registered",
                "you are registered",
                "unregister",
                "withdraw",
                "cancel registration",
                f"{self.username.lower()}" in page_source  # Look for username in roster
            ]
            
            for indicator in already_registered_indicators:
                if indicator in page_source:
                    logger.info("User is already registered for this match")
                    return True
            
            return False
                
        except Exception as e:
            logger.error(f"Error checking if already registered: {e}")
            return False
        finally:
            driver.quit()

    def is_paid_match(self, match_title: str, match_url: str) -> bool:
        """Check if a match requires payment (classifiers, fees, etc.)"""
        title_lower = match_title.lower()
        
        # Keywords that indicate paid matches
        paid_indicators = [
            "classifier",
            "classifiers", 
            "uspsa classifier",
            "level ii",
            "level 2",
            "$",  # Dollar sign in title
            "fee",
            "cost",
            "sanctioned"
        ]
        
        for indicator in paid_indicators:
            if indicator in title_lower:
                logger.info(f"Detected paid match: {match_title} (contains '{indicator}')")
                return True
                
        return False

    def check_registration_status(self, match_url: str, match_title: str = "") -> str:
        """Check if registration is open for a match"""
        # Check if it's a paid match first
        if match_title and self.is_paid_match(match_title, match_url):
            return "paid_match"
            
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            if not self.login(driver):
                return "login_failed"
            
            # First check if already registered
            if self.check_if_already_registered(match_url):
                return "already_registered"
            
            full_url = match_url if match_url.startswith('http') else f"{self.base_url}{match_url}"
            driver.get(full_url)
            time.sleep(3)
            
            page_source = driver.page_source.lower()
            
            # Also check for payment indicators on the page
            if any(indicator in page_source for indicator in ["payment", "credit card", "paypal", "stripe", "fee:", "cost:", "$"]):
                logger.info("Detected payment requirements on registration page")
                return "paid_match"
            
            if "registration not open" in page_source:
                return "not_open"
            elif "register" in page_source and "button" in page_source:
                return "open"
            elif "full" in page_source or "roster full" in page_source:
                return "full"
            else:
                return "unknown"
                
        except Exception as e:
            logger.error(f"Error checking registration status: {e}")
            return "error"
        finally:
            driver.quit()
    
    def register_for_match(self, match_url: str, first_name: str = None, last_name: str = None, 
                          email: str = None, power_factor: str = None) -> bool:
        """Attempt to register for a match"""
        logger.info(f"Attempting to register for match: {match_url}")
        
        # Get registration details from environment variables for security
        reg_first_name = first_name or os.getenv('REGISTRATION_FIRST_NAME')
        reg_last_name = last_name or os.getenv('REGISTRATION_LAST_NAME') 
        reg_email = email or os.getenv('REGISTRATION_EMAIL')
        reg_power_factor = power_factor or os.getenv('REGISTRATION_POWER_FACTOR', 'minor')
        
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            if not self.login(driver):
                return False
            
            full_url = match_url if match_url.startswith('http') else f"{self.base_url}{match_url}"
            driver.get(full_url)
            time.sleep(3)
            
            # Look for registration button
            register_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')] | //a[contains(text(), 'Register')]"))
            )
            register_button.click()
            
            time.sleep(3)
            
            # Fill out registration form
            try:
                # Common form fields
                if reg_first_name:
                    first_name_field = driver.find_element(By.NAME, "first_name")
                    first_name_field.clear()
                    first_name_field.send_keys(reg_first_name)
                    logger.info("Filled first name field")
                    
                if reg_last_name:
                    last_name_field = driver.find_element(By.NAME, "last_name") 
                    last_name_field.clear()
                    last_name_field.send_keys(reg_last_name)
                    logger.info("Filled last name field")
                    
                if reg_email:
                    email_field = driver.find_element(By.NAME, "email")
                    email_field.clear()
                    email_field.send_keys(reg_email)
                    logger.info("Filled email field")
                
                # Power factor selection
                if reg_power_factor:
                    try:
                        power_factor_select = driver.find_element(By.NAME, "power_factor")
                        for option in power_factor_select.find_elements(By.TAG_NAME, "option"):
                            if reg_power_factor.lower() in option.text.lower():
                                option.click()
                                logger.info(f"Selected power factor: {reg_power_factor}")
                                break
                    except:
                        logger.warning("Could not find power factor field")
                
                time.sleep(2)
                
            except Exception as form_error:
                logger.warning(f"Form filling error (may be expected): {form_error}")
            
            # Submit registration
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
            )
            submit_button.click()
            
            time.sleep(3)
            
            # Check for success message
            page_source = driver.page_source.lower()
            if "registered" in page_source or "confirmation" in page_source or "success" in page_source:
                logger.info("Registration successful!")
                return True
            else:
                logger.error("Registration may have failed")
                return False
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False
        finally:
            driver.quit()
    
    def check_current_registrations(self):
        """Check and log all current registrations"""
        logger.info("Checking current registrations...")
        
        matches = self.get_available_matches()
        if not matches:
            logger.info("No matching events found")
            return []
        
        registered_matches = []
        for match in matches:
            if 'register' in match.get('url', ''):
                try:
                    if self.check_if_already_registered(match['url']):
                        registered_matches.append(match['title'])
                        logger.info(f"✅ Already registered: {match['title']}")
                except Exception as e:
                    logger.error(f"Error checking registration for {match['title']}: {e}")
        
        if registered_matches:
            logger.info(f"Currently registered for {len(registered_matches)} matches: {', '.join(registered_matches)}")
        else:
            logger.info("Not currently registered for any matches")
            
        return registered_matches
    
    def run_check(self):
        """Main function to check for and register for matches"""
        logger.info("Starting match registration check...")
        
        # First, check what we're already registered for
        self.check_current_registrations()
        
        matches = self.get_available_matches()
        if not matches:
            logger.info("No matching events found")
            return
        
        for match in matches:
            match_title = match.get('title', 'Unknown')
            match_url = match.get('url', '')
            
            logger.info(f"Checking match: {match_title}")
            
            status = self.check_registration_status(match_url, match_title)
            logger.info(f"Registration status: {status}")
            
            if status == "already_registered":
                logger.info("✅ Already registered for this match - skipping")
            elif status == "paid_match":
                logger.warning(f"💳 PAID MATCH DETECTED: {match_title}")
                logger.warning("   This match requires payment (likely has classifiers or fees)")
                logger.warning("   NOTIFICATION: Manual registration required")
                logger.warning(f"   URL: {self.base_url}{match_url}")
                self.notifier.notify_match_found(match_title, match_url, is_paid=True)
            elif status == "open":
                logger.info("🟢 FREE match registration is open - attempting to register")
                success = self.register_for_match(match_url)
                if success:
                    logger.info("Successfully registered!")
                    self.notifier.notify_registration_success(match_title, match_url)
                    break  # Only register for one match to avoid duplicates
                else:
                    # Still notify about the attempt
                    self.notifier.notify_match_found(match_title, match_url, is_paid=False)
            elif status == "not_open":
                logger.info("Registration not yet open")
            elif status == "full":
                logger.info("Match is full")
            else:
                logger.warning(f"Unknown status: {status}")

if __name__ == "__main__":
    registrar = PractiscoreRegistrar()
    registrar.run_check()