#!/usr/bin/env python3
"""
Minimal test app to isolate the save button issue
"""

import streamlit as st
from db_manager import DatabaseManager

def test_save_functionality():
    st.title("Test Save Functionality")
    
    # Initialize database
    try:
        db = DatabaseManager()
        st.success("Database initialized successfully")
    except Exception as e:
        st.error(f"Database error: {e}")
        return
    
    # Simple form
    with st.form("test_form"):
        site_url = st.text_input("Site URL", value="https://test.com")
        feed_url = st.text_input("Feed URL", value="https://test.com/rss.xml")
        feed_name = st.text_input("Feed Name", value="Test Feed")
        website_name = st.text_input("Website Name", value="Test Site")
        
        submitted = st.form_submit_button("Save Feed")
        
        if submitted:
            try:
                st.write("Attempting to save...")
                st.write(f"Site URL: {site_url}")
                st.write(f"Feed URL: {feed_url}")
                st.write(f"Feed Name: {feed_name}")
                st.write(f"Website Name: {website_name}")
                
                feed_id = db.save_feed(
                    site_url=site_url,
                    feed_url=feed_url,
                    user_given_name=feed_name,
                    website_nickname=website_name,
                    is_synthetic=False
                )
                
                st.success(f"Feed saved successfully with ID: {feed_id}")
                
            except Exception as e:
                st.error(f"Save error: {e}")
                import traceback
                st.error(f"Full traceback: {traceback.format_exc()}")
    
    # Show existing feeds
    st.subheader("Existing Feeds")
    try:
        feeds = db.get_all_feeds()
        st.write(f"Total feeds: {len(feeds)}")
        for feed in feeds:
            st.write(f"- {feed['user_given_name']}: {feed['feed_url']}")
    except Exception as e:
        st.error(f"Error retrieving feeds: {e}")

if __name__ == "__main__":
    test_save_functionality()