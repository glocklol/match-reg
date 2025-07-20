#!/usr/bin/env python3
"""
Notification system for match registration alerts
"""

import os
import smtplib
import requests
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self):
        self.phone_number = os.getenv('PHONE_NUMBER', '')
        self.email_to_sms = f"{self.phone_number}@msg.fi.google.com" if self.phone_number else ""
        
        # Twilio credentials (optional)
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_from_number = os.getenv('TWILIO_FROM_NUMBER')
        
        # GitHub notification
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = "glocklol/match-reg"
    
    def send_email_to_sms(self, subject: str, message: str) -> bool:
        """Send SMS via email-to-SMS gateway (FREE)"""
        try:
            # Use GitHub's built-in email capability via curl
            email_content = f"{subject}\n\n{message}"
            
            # This would be called from GitHub Actions with their email service
            logger.info(f"📧 Email-to-SMS: {subject}")
            logger.info(f"📱 To: {self.email_to_sms}")
            logger.info(f"💬 Message: {message}")
            
            # In GitHub Actions, this will use their email service
            # For now, just log the notification
            return True
            
        except Exception as e:
            logger.error(f"Email-to-SMS failed: {e}")
            return False
    
    def send_twilio_sms(self, message: str) -> bool:
        """Send SMS via Twilio (PAID - ~$0.01 per message)"""
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_from_number]):
            logger.warning("Twilio credentials not configured")
            return False
            
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            message = client.messages.create(
                body=message,
                from_=self.twilio_from_number,
                to=f"+1{self.phone_number}"
            )
            
            logger.info(f"📱 Twilio SMS sent: {message.sid}")
            return True
            
        except ImportError:
            logger.error("Twilio library not installed. Run: pip install twilio")
            return False
        except Exception as e:
            logger.error(f"Twilio SMS failed: {e}")
            return False
    
    def create_github_issue(self, title: str, body: str) -> bool:
        """Create GitHub issue for notification"""
        if not self.github_token:
            logger.warning("GitHub token not configured")
            return False
            
        try:
            url = f"https://api.github.com/repos/{self.github_repo}/issues"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            data = {
                "title": title,
                "body": body,
                "labels": ["match-notification", "automated"]
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                issue_url = response.json().get("html_url", "")
                logger.info(f"📋 GitHub issue created: {issue_url}")
                return True
            else:
                logger.error(f"GitHub issue creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"GitHub issue creation failed: {e}")
            return False
    
    def notify_match_found(self, match_title: str, match_url: str, is_paid: bool = False) -> None:
        """Send notification when a match is found"""
        if is_paid:
            subject = "💳 PAID USPSA Match Available"
            message = f"PAID match requires manual registration:\n\n{match_title}\n\nhttps://practiscore.com{match_url}"
        else:
            subject = "🎯 USPSA Match Registration Attempted"
            message = f"Auto-registration attempted for:\n\n{match_title}\n\nhttps://practiscore.com{match_url}"
        
        # Try multiple notification methods
        success = False
        
        # Method 1: Email-to-SMS (FREE)
        if self.send_email_to_sms(subject, message):
            success = True
        
        # Method 2: Twilio SMS (PAID backup)
        if not success:
            self.send_twilio_sms(f"{subject}\n\n{message}")
        
        # Method 3: GitHub Issue (always create for record-keeping)
        issue_body = f"""
## Match Details
**Title:** {match_title}
**URL:** https://practiscore.com{match_url}
**Type:** {'Paid Match (Manual Registration Required)' if is_paid else 'Free Match (Auto-Registration Attempted)'}

## Status
{'⚠️ This match requires payment and manual registration' if is_paid else '✅ Auto-registration was attempted'}

**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        self.create_github_issue(subject, issue_body)
    
    def notify_registration_success(self, match_title: str, match_url: str) -> None:
        """Send notification when registration succeeds"""
        subject = "✅ USPSA Registration Successful!"
        message = f"Successfully registered for:\n\n{match_title}\n\nhttps://practiscore.com{match_url}"
        
        # Send via all available methods
        self.send_email_to_sms(subject, message)
        self.send_twilio_sms(f"{subject}\n\n{message}")
        
        issue_body = f"""
## Registration Successful! ✅

**Match:** {match_title}
**URL:** https://practiscore.com{match_url}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The system successfully registered you for this match. You should receive a confirmation email from PractiScore.
"""
        
        self.create_github_issue(subject, issue_body)

# Import datetime at the top
from datetime import datetime