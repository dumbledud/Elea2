import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# --- Configuration --------------------------------------------------
st.set_page_config(
    page_title="Daily Jesus Check-In",
    page_icon="✝️",
    layout="wide"
)

BIBLE_VERSES = {
    "gratitude": [
        ("1 Thessalonians 5:18", "Give thanks in all circumstances; for this is the will of God in Christ Jesus for you."),
        ("Psalm 107:1", "Oh give thanks to the LORD, for he is good, for his steadfast love endures forever!"),
    ],
    "strength": [
        ("Philippians 4:13", "I can do all things through him who strengthens me."),
        ("Isaiah 40:31", "But they who wait for the LORD shall renew their strength; they shall mount up with wings like eagles; they shall run and not be weary; they shall walk and not faint."),
    ],
    "peace": [
        ("John 14:27", "Peace I leave with you; my peace I give to you. Not as the world gives do I give to you."),
        ("Philippians 4:6-7", "Do not be anxious about anything, but in everything by prayer and supplication with thanksgiving let your requests be made known to God."),
    ]
}

DATA_FILE = "gratitude_entries.csv"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["timestamp", "entry", "verse_ref", "verse_text"]).to_csv(DATA_FILE, index=False)

# --- Sidebar Menu ----------------------------------------------------
menu = st.sidebar.radio(
    "📖 Navigate",
    ("Check-In", "Daily Verse", "History", "About")
)

# --- Pages -----------------------------------------------------------
if menu == "Check-In":
    st.title("🙏 Daily Jesus Check-In")
    st.header("Reflect & Give Thanks")
    st.write("Choose a theme to guide your reflection and receive a fitting Bible verse.")

    theme = st.selectbox("Select a theme", list(BIBLE_VERSES.keys()))
    verse_ref, verse_text = random.choice(BIBLE_VERSES[theme])
    st.markdown(f"> **{verse_ref}** — _{verse_text}_")

    st.text_area("What are you grateful for today?", key="gratitude_input", height=150)

    if st.button("Submit 😊"):
        entry = st.session_state.gratitude_input.strip()
        if entry:
            timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
            new_row = {"timestamp": timestamp, "entry": entry, "verse_ref": verse_ref, "verse_text": verse_text}
            df = pd.read_csv(DATA_FILE)
            df = df.append(new_row, ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("🎉 Your gratitude has been recorded!")
            st.balloons()
            st.progress(100)
        else:
            st.error("Please share something you're grateful for.")

elif menu == "Daily Verse":
    st.title("📜 Daily Bible Verse")
    category = st.selectbox("Choose category", list(BIBLE_VERSES.keys()))
    verse_ref, verse_text = random.choice(BIBLE_VERSES[category])
    st.markdown(f"## {verse_ref}")
    st.markdown(f"> _{verse_text}_")
    st.write("---")
    st.info("Let this verse guide your day! You can go to Check-In to reflect.")

elif menu == "History":
    st.title("📚 Gratitude History")
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        st.warning("No entries yet. Head to Check-In to add your first gratitude.")
    else:
        st.dataframe(df.sort_values(by="timestamp", ascending=False), use_container_width=True)

elif menu == "About":
    st.title("ℹ️ About This App")
    st.markdown("""
    **Daily Jesus Check-In** helps you:
    - Reflect on God's goodness daily  
    - Record gratitude entries  
    - Receive relevant Bible verses  
    - Review your entries over time  

    Built with Streamlit by Chris Comiskey.  
    """)
