#!/usr/bin/env python3
"""
Show all available matches for testing
"""

from match_registrar import PractiscoreRegistrar

def show_all_matches():
    """Show all available matches with their status"""
    try:
        registrar = PractiscoreRegistrar()
        
        print("🔍 Getting all available matches...")
        matches = registrar.get_available_matches()
        
        print(f"\nFound {len(matches)} total matches:")
        print("=" * 80)
        
        for i, match in enumerate(matches, 1):
            match_title = match.get('title', 'Unknown Title')
            match_url = match.get('url', 'No URL')
            
            print(f"{i:2d}. {match_title}")
            print(f"    URL: {match_url}")
            
            # Check if it's a registerable match
            if 'register' in match_url:
                print("    🎯 REGISTRABLE MATCH")
                
                # Check if it contains our keywords
                title_lower = match_title.lower()
                if 'run & gun' in title_lower:
                    print("    🔫 RUN & GUN MATCH")
                elif 'practice with purpose' in title_lower:
                    print("    🎯 PRACTICE WITH PURPOSE MATCH")
                elif 'nsps' in title_lower:
                    print("    🏆 NSPS MATCH")
            else:
                print("    ℹ️  Information only (no registration)")
                
            print()  # blank line
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("📋 Available Matches Overview")
    print("=" * 80)
    show_all_matches()