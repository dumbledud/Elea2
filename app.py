import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime, date, timedelta

# --- App Configuration --------------------------------------------------
st.set_page_config(page_title="Daily Jesus Check-In", page_icon="✝️")

# --- Data Storage Setup -------------------------------------------------
DATA_FILE = "gratitude_entries.csv"

def load_entries():
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=["timestamp", "entry", "verse_ref", "verse_text"]) \
          .to_csv(DATA_FILE, index=False)
    df = pd.read_csv(DATA_FILE)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

def save_entry(entry_row):
    df = load_entries()
    new_df = pd.DataFrame([entry_row])
    df = pd.concat([df, new_df], ignore_index=True)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(DATA_FILE, index=False)

# --- Bible Verses -------------------------------------------------------
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
    ],
}

# --- Bordle Word List (first 200) ---------------------------------------
WORDLE_WORDS = [
    # 1–100
    "JESUS","FAITH","GRACE","MERCY","PEACE","TRUTH","LIGHT","GLORY","POWER","BLOOD",
    "BREAD","ANGEL","DEVIL","CROSS","ALPHA","BABEL","SHEEP","BIRDS","HEART","SOULS",
    "WORDS","NAMES","TRIBE","ELDER","THREE","SEVEN","EIGHT","FIRST","WATER","SMITE",
    "SPEAK","WRITE","SHALT","WHICH","THEIR","THESE","THOSE","THERE","WHERE","OTHER",
    "WHILE","AFTER","WOULD","COULD","MIGHT","UNDER","AGAIN","ABOUT","SHALL","DAVID",
    "MOSES","JAMES","PETER","ISAAC","NAOMI","JUDAS","SARAH","HAGAR","RAHAB","ABIDE",
    "REIGN","TRUST","SONGS","PSALM","REVEL","ABRAM","TRIAL","DEATH","LIVES","EARTH",
    "FLESH","TIMES","STOOD","MOUNT","EGYPT","RIVER","SWORD","MONEY","SPOKE","WROTE",
    "LOVES","SIGNS","SINCE","SAINT","THINE","SHINE","BLESS","HONOR","GREAT","HORSE",
    "KINGS","CROWN","CLOUD","STONE","SLEPT","GODLY","FLOUR","BRIDE","ALIVE","CHOSE",
    # 101–200
    "ELIAS","JONAH","MICAH","HOSEA","NAHUM","ABNER","TAMAR","SIMON","NABAL","JUDAH",
    "LAZAR","QUAKE","SALVA","SAVED","CLEAN","HELPS","GUIDE","FIELD","VINES","GRAIN",
    "FRUIT","SEEDS","SHEOL","ABYSS","SHOES","WELLS","WHEAT","YEAST","OLIVE","BRASS",
    "ALTAR","TEMPLE","GATES","WALLS","PEARL","CEDAR","OCEAN","SMOKE","FLAME","FIRES",
    "FLOOD","TOWER","TENTS","DOVES","SNAKE","TORCH","SPICE","FEAST","BEGIN","SPOIL",
    "HASTE","TREAD","SHIFT","SHARE","GIVES","TAKEN","TOUCH","HEARD","CALMS","BIBLE",
    "VERSE","QUOTE","FOUND","FINAL","GLOOM","LOYAL","HUMOR","HAPPY","GROWS","DWELL",
    "WALKS","LEAPS","CARRY","BOUND","SERVE","PRAIS","FENCE","VALLE","TABLE","GUEST",
    "CHEST","SPEAR","BARNS","CHOIR","PIPES","FOCUS","FOODS","MEATS","BANNS","SALTS",
    "SANDS","CROWS","OWLS","LIONS","FOOLS","WINES","KNEEL","RAISE","HYMNS","MARCH",
]

# --- Sidebar Navigation -----------------------------------------------
page = st.sidebar.radio(
    "📖 Navigate",
    ("Check-In", "Daily Verse", "Bible Wordle", "Verse Jumble", "History", "Achievements", "About")
)

# --- Page: Check-In ----------------------------------------------------
if page == "Check-In":
    st.title("🙏 Daily Jesus Check-In")
    st.header("Reflect & Give Thanks")
    theme = st.selectbox("Theme", list(BIBLE_VERSES.keys()))
    verse_ref, verse_text = random.choice(BIBLE_VERSES[theme])
    st.markdown(f"> **{verse_ref}** — _{verse_text}_")
    st.write("---")

    gratitude = st.text_area("What are you grateful for today?", height=150)
    if st.button("Submit 🙏"):
        text = gratitude.strip()
        if text:
            now = datetime.now()
            save_entry({
                "timestamp": now,
                "entry": text,
                "verse_ref": verse_ref,
                "verse_text": verse_text
            })
            st.success("🎉 Your gratitude has been recorded!")
            st.balloons()
        else:
            st.error("Please share something you're grateful for.")

# --- Page: Daily Verse -------------------------------------------------
elif page == "Daily Verse":
    st.title("📜 Daily Bible Verse")
    category = st.selectbox("Choose category", list(BIBLE_VERSES.keys()))
    ref, text = random.choice(BIBLE_VERSES[category])
    st.subheader(ref)
    st.markdown(f"> _{text}_")
    st.info("Head back to Check-In to reflect on it!")

# --- Page: Bible Wordle ------------------------------------------------
elif page == "Bible Wordle":
    st.title("🟩 Bible Wordle 🟨")
    # Kids Mode toggle
    kids_mode = st.checkbox("👶 Kids Mode: Unlimited tries & free-form guesses")

    # Daily seed for target (or random on each reload if kids_mode)
    if kids_mode:
        random.seed(None)
    else:
        random.seed(int(date.today().strftime("%Y%m%d")))

    target = random.choice(WORDLE_WORDS)

    # Init session state
    if "guesses" not in st.session_state:
        st.session_state.guesses = []
        st.session_state.solved = False

    def evaluate(word):
        """Return Wordle feedback for any 5-letter word."""
        fb = []
        for i, ch in enumerate(word):
            if ch == target[i]:
                fb.append("🟩")
            elif ch in target:
                fb.append("🟨")
            else:
                fb.append("⬜")
        return "".join(fb)

    # Only enforce 6-guess limit if not kids_mode
    can_guess = (kids_mode or len(st.session_state.guesses) < 6) and not st.session_state.solved

    if can_guess:
        guess = st.text_input(
            "Enter your 5-letter guess:",
            max_chars=5,
            key="bordle_input"
        ).upper()

        if st.button("Guess"):
            if len(guess) != 5 or not guess.isalpha():
                st.error("Please enter exactly 5 letters.")
            else:
                fb = evaluate(guess)
                st.session_state.guesses.append((guess, fb))
                if guess == target:
                    st.session_state.solved = True

    # Show history of guesses
    for g, fb in st.session_state.guesses:
        st.write(f"{g}   {fb}")

    # Game end messages
    if st.session_state.solved:
        st.success(f"You got it! The word was **{target}**.")
        st.balloons()
    elif not kids_mode and len(st.session_state.guesses) >= 6:
        st.error(f"Out of guesses—word was **{target}**.")

    if st.button("Reset"):
        st.session_state.guesses = []
        st.session_state.solved = False

# --- Page: Verse Jumble ------------------------------------------------
elif page == "Verse Jumble":
    st.title("🔀 Verse Jumble 🔀")
    verse_ref, verse_text = random.choice(random.choice(list(BIBLE_VERSES.values())))
    words = verse_text.split()
    random.shuffle(words)
    st.markdown(f"**Scrambled:**  \n{' '.join(words)}")

    answer = st.text_area("Unscramble to the original verse:")
    if st.button("Check"):
        if answer.strip().lower() == verse_text.lower():
            st.success("🎉 Perfect!")
        else:
            st.error("Not quite—try again!")

# --- Page: History ------------------------------------------------------
elif page == "History":
    st.title("📚 Gratitude History")
    df = load_entries()
    if df.empty:
        st.warning("No entries yet. Record one on Check-In.")
    else:
        df = df.sort_values("timestamp", ascending=False)
        st.table(df[["timestamp", "entry", "verse_ref"]])

# --- Page: Achievements ------------------------------------------------
elif page == "Achievements":
    st.title("🏆 Achievements 🏆")
    df = load_entries()
    if df.empty:
        st.info("Make your first Check-In to earn badges!")
    else:
        dates = {d.date() for d in df["timestamp"]}
        streak = 0
        d = date.today()
        while d in dates:
            streak += 1
            d -= timedelta(days=1)

        st.subheader(f"Current Check-In Streak: {streak} days")
        if streak >= 30:
            st.markdown("**Gold Badge** 🏅")
        elif streak >= 7:
            st.markdown("**Silver Badge** 🥈")
        elif streak >= 3:
            st.markdown("**Bronze Badge** 🥉")
        else:
            st.markdown("_No badge yet—keep going!_")

# --- Page: About --------------------------------------------------------
else:
    st.title("ℹ️ About This App")
    st.markdown("""
    **Daily Jesus Check-In** now includes:
    - A Bible-themed Wordle with **Kids Mode**  
    - Free-form guesses & unlimited tries option  
    - A fun Verse Jumble puzzle  
    - Streak-based Achievements  

    Built with 💖 by Eleanor.
    """)
