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
        
        # Setup Chrome options for headless browsing
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--remote-debugging-port=9222')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        self.chrome_options.binary_location = '/snap/bin/chromium'
        
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
        
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            driver.get(self.club_url)
            time.sleep(3)  # Wait for page to load
            
            # Look for match elements
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            matches = []
            
            # Find match containers (this will need to be adjusted based on actual HTML structure)
            match_elements = soup.find_all(['div', 'a'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['match', 'event', 'competition']
            ))
            
            for element in match_elements:
                if self.target_match.lower() in element.get_text().lower():
                    match_data = {
                        'title': element.get_text().strip(),
                        'url': element.get('href', ''),
                        'element': str(element)
                    }
                    matches.append(match_data)
            
            logger.info(f"Found {len(matches)} matching events")
            return matches
            
        except Exception as e:
            logger.error(f"Error fetching matches: {e}")
            return []
        finally:
            driver.quit()
    
    def login(self, driver) -> bool:
        """Login to PractiScore"""
        logger.info("Logging in to PractiScore...")
        
        try:
            driver.get(self.login_url)
            time.sleep(2)
            
            # Find and fill login form
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # Submit form
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(3)
            
            # Check if login was successful
            if "login" not in driver.current_url.lower():
                logger.info("Login successful")
                return True
            else:
                logger.error("Login failed")
                return False
                
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
    
    def register_for_match(self, match_url: str) -> bool:
        """Attempt to register for a match"""
        logger.info(f"Attempting to register for match: {match_url}")
        
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            if not self.login(driver):
                return False
            
            full_url = match_url if match_url.startswith('http') else f"{self.base_url}{match_url}"
            driver.get(full_url)
            time.sleep(3)
            
            # Look for registration button
            register_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]"))
            )
            register_button.click()
            
            time.sleep(3)
            
            # Fill out registration form (this will need customization based on actual form)
            # Common fields might include:
            # - Division
            # - Class
            # - Special requirements
            
            # Submit registration
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            submit_button.click()
            
            time.sleep(3)
            
            # Check for success message
            page_source = driver.page_source.lower()
            if "registered" in page_source or "confirmation" in page_source:
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