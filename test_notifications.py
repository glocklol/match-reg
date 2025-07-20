#!/usr/bin/env python3
"""
Test notification system
"""

from notifications import NotificationManager

def test_notifications():
    """Test notification functionality"""
    try:
        notifier = NotificationManager()
        
        print("🧪 Testing Notification System")
        print("=" * 50)
        
        # Test paid match notification
        print("1️⃣ Testing PAID match notification...")
        notifier.notify_match_found(
            "NSPS Run & Gun - with USPSA Classifiers 07/21/25",
            "/nsps-run-gun-with-uspsa-classifiers-07-21-25/register",
            is_paid=True
        )
        
        print("\n2️⃣ Testing FREE match notification...")
        notifier.notify_match_found(
            "NSPS Run & Gun 07/28/25", 
            "/nsps-run-gun-07-28-25/register",
            is_paid=False
        )
        
        print("\n3️⃣ Testing registration success notification...")
        notifier.notify_registration_success(
            "NSPS Practice with Purpose 07/24/25",
            "/nsps-practice-with-purpose-07-24-25/register"
        )
        
        print("\n✅ Notification tests complete!")
        print("Check the logs above to see notification attempts.")
        
    except Exception as e:
        print(f"❌ Notification test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_notifications()