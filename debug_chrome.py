#!/usr/bin/env python3
"""
Debug Chrome driver issues in GitHub Actions
"""

import os
import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_chrome():
    """Test Chrome driver setup"""
    logger.info("=== Chrome Driver Debug Test ===")
    
    # Check environment
    logger.info(f"Python version: {sys.version}")
    logger.info(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    
    # Check Chrome binary locations
    chrome_paths = [
        '/snap/bin/chromium',
        '/usr/bin/google-chrome', 
        '/opt/hostedtoolcache/setup-chrome/chrome/stable/x64/chrome',
        '/usr/bin/chromium-browser',
        '/usr/bin/chrome'
    ]
    
    for chrome_path in chrome_paths:
        exists = os.path.exists(chrome_path)
        logger.info(f"Chrome path {chrome_path}: {'EXISTS' if exists else 'NOT FOUND'}")
        if exists:
            try:
                # Try to get version
                import subprocess
                result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True, timeout=10)
                logger.info(f"  Version: {result.stdout.strip()}")
            except Exception as e:
                logger.info(f"  Error getting version: {e}")
    
    # Test Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Linux; x86_64) AppleWebKit/537.36')
    
    # Set binary location
    chrome_binary_set = False
    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            chrome_options.binary_location = chrome_path
            logger.info(f"Using Chrome binary: {chrome_path}")
            chrome_binary_set = True
            break
    
    if not chrome_binary_set:
        logger.error("No Chrome binary found!")
        return False
    
    # Test driver initialization
    logger.info("Attempting to initialize Chrome driver...")
    try:
        driver = webdriver.Chrome(options=chrome_options)
        logger.info("✅ Chrome driver initialized successfully!")
        
        # Test basic navigation
        logger.info("Testing navigation to Google...")
        driver.get("https://www.google.com")
        logger.info(f"Current URL: {driver.current_url}")
        logger.info(f"Page title: {driver.title}")
        logger.info(f"Page source length: {len(driver.page_source)}")
        
        # Test PractiScore navigation
        logger.info("Testing navigation to PractiScore...")
        driver.get("https://practiscore.com")
        logger.info(f"PractiScore URL: {driver.current_url}")
        logger.info(f"PractiScore title: {driver.title}")
        logger.info(f"PractiScore source length: {len(driver.page_source)}")
        
        driver.quit()
        logger.info("✅ Chrome driver test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Chrome driver failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = debug_chrome()
    sys.exit(0 if success else 1)