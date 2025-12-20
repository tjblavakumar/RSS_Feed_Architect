#!/usr/bin/env python3
"""
Test script to verify session state initialization
"""

def test_session_state_variables():
    """Test that all required session state variables are defined"""
    print("Testing Session State Variable Definitions")
    print("=" * 50)
    
    # List of all session state variables that should be initialized
    required_session_vars = [
        'force_rescan',
        'last_scanned_url', 
        'saved_feeds',
        'discovered_feeds',
        'current_url',
        'website_nickname',
        'show_nickname_error',
        'last_url_input'
    ]
    
    print("Required session state variables:")
    for var in required_session_vars:
        print(f"  ✓ {var}")
    
    print(f"\nTotal variables to initialize: {len(required_session_vars)}")
    
    # Check if the app.py file contains all initializations
    print("\nChecking app.py for session state initializations...")
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    missing_vars = []
    for var in required_session_vars:
        init_pattern = f"if '{var}' not in st.session_state:"
        if init_pattern not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing initializations for:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    else:
        print("✅ All session state variables are properly initialized!")
        return True

if __name__ == "__main__":
    success = test_session_state_variables()
    if success:
        print("\n🎉 Session state initialization test passed!")
    else:
        print("\n❌ Session state initialization test failed!")
        exit(1)