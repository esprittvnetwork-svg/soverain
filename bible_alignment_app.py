# ======================= Module 0: Setup, Styling, Navigation =======================

import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Soverain: Spiritual Intelligence",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Compass Bar
selected_profile = st.session_state.get("selected_profile", "Me")
profile_data = st.session_state.get(f"profile_{selected_profile}", {})
goal_text = profile_data.get("goal", "—")
last_score = profile_data.get("last_score", "—")
verse_today = "“Walk in the Spirit, and you shall not fulfill the lust of the flesh.” — Galatians 5:16"

st.markdown(f"""
<div style="background:#0f172a; padding:12px 24px; border-bottom:1px solid #334155;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
    <div style="flex:1; min-width:200px; font-size:0.95rem; color:#f1f5f9;">
      📖 <em>{verse_today}</em>
    </div>
    <div style="flex:1; min-width:200px; text-align:center; font-size:0.9rem; color:#f1f5f9;">
      👤 <strong>{selected_profile}</strong> · Goal: <em>{goal_text}</em> · Last Score: <strong>{last_score}</strong>
    </div>
    <div style="flex:1; min-width:200px; text-align:right;">
      <div style="font-size:0.9rem; color:#f1f5f9;"><em>Soverain: Reflect. Align. Grow in Christ.</em></div>
      <div style="background:#334155; height:8px; border-radius:4px; margin-top:4px;">
        <div style="width:70%; background:#3b82f6; height:8px; border-radius:4px;"></div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Profile Selector (Functional Input)
with st.sidebar:
    st.markdown("### 👤 Active Profile")
    profile_options = ["Me", "Team", "Mentor", "Board"]
    selected_profile = st.selectbox("Choose Profile", profile_options, index=profile_options.index(st.session_state.get("selected_profile", "Me")))
    st.session_state["selected_profile"] = selected_profile

st.markdown("> _“Write the vision; make it plain…” — Habakkuk 2:2_")

# Initialize profile data if missing
profile_key = f"profile_{selected_profile}"
if profile_key not in st.session_state:
    st.session_state[profile_key] = {
        "scenarios": [],
        "assessments": [],
        "reflections": [],
        "goal": "—",
        "last_score": "—"
    }

# Update Compass Bar values
profile_data = st.session_state[profile_key]
goal_text = profile_data.get("goal", "—")
last_score = profile_data.get("last_score", "—")

with st.sidebar:
    st.markdown("### ✍️ Profile Setup")
    new_goal = st.text_input("Spiritual Goal", value=profile_data.get("goal", ""), placeholder="e.g. Walk in love daily")
    new_name = st.text_input("Profile Name", value=selected_profile, placeholder="e.g. Ava, Team, Mentor")

    if st.button("💾 Save Profile Info"):
        st.session_state["selected_profile"] = new_name.strip() or selected_profile
        profile_key = f"profile_{st.session_state['selected_profile']}"
        if profile_key not in st.session_state:
            st.session_state[profile_key] = {
                "scenarios": [],
                "assessments": [],
                "reflections": [],
                "goal": new_goal.strip(),
                "last_score": "—"
            }
        else:
            st.session_state[profile_key]["goal"] = new_goal.strip()
        st.success("Profile updated.")

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    st.markdown("""
    - [📊 Profile Dashboard](#profile-dashboard)
    - [📖 Scripture Catalog](#scripture-catalog)
    - [✍️ Add Custom Scenario](#custom-scenario)
    - [⚡ Instant Calculator](#instant-calculator)
    - [🧭 Life Assessment](#life-assessment)
    - [📈 Progress Viewer](#spiritual-progress)
    - [✝️ Greatest Commands](#greatest-commands)
    - [🌟 Closing Reflection](#closing-reflection)
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ℹ️ About Soverain")
    st.markdown("""
    *Soverain* helps you reflect on your decisions through the lens of Scripture.  
    Use the catalog, add your own scenarios, or try the instant calculator.  
    Your scores are based on Christlikeness, Heart, and Faithfulness—three pillars of godly living.
    """)

# Optional onboarding trigger (for Module 10)
if "onboarded" not in st.session_state:
    st.session_state["onboarded"] = False

# Full Night Sky Theme
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f172a !important;
    color: #f1f5f9 !important;
}

[data-testid="stHeader"] {
    background-color: #0f172a !important;
}

[data-testid="stSidebar"] {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
}

h1, h2, h3, h4, h5, h6, .stMarkdown, .stTextInput, .stSlider, .stSelectbox, .stButton {
    color: #f1f5f9 !important;
}

[data-testid="stVerticalBlock"] {
    background-color: #0f172a !important;
}

[data-testid="stMarkdownContainer"] {
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)
# ======================= Module 1: Core Logic & Visual Components =======================

st.markdown('<a name="core-logic"></a>', unsafe_allow_html=True)

scale = True  # Set to False for 0–10 scale

def G_from_CHF(C, H, F):
    return round((C * H * F) ** (1/3), 3)

def A_from_G(G):
    return round((G - 0.5) * 2, 3)

def score_from_A(A):
    return max(0, min(10, round((A + 1) * 5)))

def label_from_score(score):
    if score >= 7: return "✅ Aligned (God)"
    elif score >= 3: return "🟣 Mixed"
    else: return "⛔ Not God"

def pct(x):
    return int(round(x * 100))

def donut_html(score, label="Score", scale_label="0–100"):
    return f"""
    <div class="donut">
      <svg viewBox="0 0 36 36">
        <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 1 0 0.00001 0" />
        <path class="circle" stroke-dasharray="{score}, 100" d="M18 2.0845 a 15.9155 15.9155 0 1 0 0.00001 0" />
        <text x="18" y="20.35" class="score-text" style="font-size: 10px; font-weight: bold;">{score}</text>
      </svg>
      <div class="donut-label">{label}</div>
      <div class="donut-scale">{scale_label}</div>
    </div>
    """

def chip_html(label):
    color = "#10b981" if "Aligned" in label else "#f59e0b" if "Mixed" in label else "#ef4444"
    return f"""
    <div style="display:inline-block; background:{color}; color:white; padding:4px 12px; border-radius:20px; font-size:0.85rem;">
      {label}
    </div>
    """

def bar_html(value, label="Progress", color="#3b82f6"):
    return f"""
    <div style="margin-top:8px;">
      <div style="font-size:0.85rem; color:#f1f5f9;">{label}</div>
      <div style="background:#334155; height:8px; border-radius:4px;">
        <div style="width:{pct(value)}%; background:{color}; height:8px; border-radius:4px;"></div>
      </div>
    </div>
    """

def preview_card(G, title="Score", scale=True):
    A = A_from_G(G)
    score = score_from_A(A)
    label = label_from_score(score)
    score_display = score * 10 if scale else score
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cL, cR = st.columns([1, 1.2])
    with cL:
        st.markdown(donut_html(score_display, title, "0–100" if scale else "0–10"), unsafe_allow_html=True)
        st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Direction and intensity of alignment. Positive values reflect Christlike movement.")
        st.write(f"**G (God Alignment Score):** `{G:.3f}` — Measures how closely this moment reflects God’s character.")
    with cR:
        st.markdown(f'{chip_html(label)}', unsafe_allow_html=True)
        st.markdown(bar_html(G, "G Alignment"), unsafe_allow_html=True)
        st.markdown(bar_html(score_display / 100, "Score", "#10b981" if "Aligned" in label else "#f59e0b" if "Mixed" in label else "#ef4444"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================= Module 2: Scripture Catalog & Scenario Builder =======================

st.markdown('<a name="scripture-catalog"></a>', unsafe_allow_html=True)
st.header("📖 Scripture Catalog")
st.caption("Explore biblical moments and reflect on their spiritual alignment. Adjust sliders to preview scores.")

SCRIPTURE_CATALOG = [
    ("Genesis", "22:9–12", "Abraham", "Offer Isaac in obedience", 0.95, 0.95, 0.95, "Genesis 22:9–12"),
    ("Exodus", "3:4", "Moses", "Respond to God's call at the burning bush", 0.90, 0.90, 0.90, "Exodus 3:4"),
    ("Matthew", "5:1–12", "Jesus", "Teach the Beatitudes", 1.00, 1.00, 1.00, "Matthew 5:1–12"),
    ("Luke", "15:20", "Father", "Forgive the prodigal son", 0.95, 0.95, 0.95, "Luke 15:20"),
    ("John", "13:5", "Jesus", "Wash the disciples’ feet", 1.00, 1.00, 1.00, "John 13:5"),
    ("Acts", "2:42–47", "Early Church", "Live in unity and generosity", 0.95, 0.95, 0.95, "Acts 2:42–47"),
]

selected = st.selectbox("Choose a Scripture moment", SCRIPTURE_CATALOG, format_func=lambda x: f"{x[0]} {x[1]} — {x[2]}: {x[3]}")
book, verse, figure, situation, default_C, default_H, default_F, ref = selected

st.markdown("### ✍️ Rate the Spiritual Alignment")
C = st.slider("Christlikeness (C)", 0.0, 1.0, default_C, 0.01)
H = st.slider("Heart (H)", 0.0, 1.0, default_H, 0.01)
F = st.slider("Faithfulness (F)", 0.0, 1.0, default_F, 0.01)

G = G_from_CHF(C, H, F)
A = A_from_G(G)
preview_card(G, title=f"{book} {verse}")

st.markdown("### 🔍 Spiritual Alignment Summary")
st.write(f"**G (God Alignment Score):** `{G:.3f}` — Reflects how closely this moment aligns with God’s character.")
st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Indicates the direction and intensity of alignment.")

profile_name = st.session_state.get("selected_profile", "Me")
if st.button("💾 Save This Scenario"):
    scenario = {
        "Book": book,
        "Verse": verse,
        "Figure": figure,
        "Situation": situation,
        "C": C,
        "H": H,
        "F": F,
        "G": G,
        "Score": score_from_A(A),
        "Label": label_from_score(score_from_A(A)),
        "Ref": ref,
        "Saved": datetime.today().strftime("%Y-%m-%d")
    }
    key = f"profile_{profile_name}"
    if key in st.session_state:
        st.session_state[key]["scenarios"].append(scenario)
        st.success(f"Saved to profile '{profile_name}'")
    else:
        st.warning("Profile not found. Please create a profile first.")

# ======================= Module 3: Custom Scenario Entry =======================

st.markdown('<a name="custom-scenario"></a>', unsafe_allow_html=True)
st.header("✍️ Add a Custom Scripture Scenario")
st.caption("Reflect on a moment from Scripture—or your own life—and assess its spiritual alignment.")

with st.form("custom_scenario_form"):
    book = st.text_input("Book", value="", placeholder="e.g. Romans")
    verse = st.text_input("Chapter:Verse", value="", placeholder="e.g. 12:1–2")
    figure = st.text_input("Figure or person", value="", placeholder="e.g. Paul, Me, My team")
    situation = st.text_area("Situation or decision", height=80, placeholder="e.g. Urging transformation and renewal")
    C = st.slider("Christlikeness (C)", 0.0, 1.0, 0.85, 0.01)
    H = st.slider("Heart (H)", 0.0, 1.0, 0.85, 0.01)
    F = st.slider("Faithfulness (F)", 0.0, 1.0, 0.85, 0.01)
    submitted = st.form_submit_button("💾 Save Scenario")

if submitted and book.strip() and verse.strip():
    G = G_from_CHF(C, H, F)
    A = A_from_G(G)
    profile_name = st.session_state.get("selected_profile", "Me")
    scenario = {
        "Book": book.strip(),
        "Verse": verse.strip(),
        "Figure": figure.strip(),
        "Situation": situation.strip(),
        "C": C,
        "H": H,
        "F": F,
        "G": G,
        "Score": score_from_A(A),
        "Label": label_from_score(score_from_A(A)),
        "Ref": f"{book.strip()} {verse.strip()}",
        "Saved": datetime.today().strftime("%Y-%m-%d")
    }
    key = f"profile_{profile_name}"
    if key in st.session_state:
        st.session_state[key]["scenarios"].append(scenario)
        st.success(f"Custom scenario saved to profile '{profile_name}'")
        preview_card(G, title=f"{book.strip()} {verse.strip()}")
        st.markdown("### 🔍 Spiritual Alignment Summary")
        st.write(f"**G (God Alignment Score):** `{G:.3f}` — Reflects how closely this moment aligns with God’s character.")
        st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Indicates the direction and intensity of alignment.")
    else:
        st.warning("Profile not found. Please create a profile first.")

# ======================= Module 4: Instant Score Calculator & Saved Scenarios =======================

st.markdown('<a name="instant-calculator"></a>', unsafe_allow_html=True)
st.header("⚡ Instant Score Calculator")
st.caption("Thinking about a decision? Use this tool to reflect on how closely it aligns with God’s character. Move each slider based on your sense of the moment’s spiritual integrity:")

st.markdown("""
- **Christlikeness (C)**: Does this decision reflect the humility, love, and truth of Jesus?  
  _Would Christ make this choice in your place?_
- **Heart (H)**: Is your motive pure, generous, and surrendered?  
  _Are you acting from love, or from fear, pride, or self-interest?_
- **Faithfulness (F)**: Does this action honor God’s Word and your spiritual commitments?  
  _Are you walking in obedience, even when it’s costly?_
""")

# Live sliders with unique keys
C = st.slider("Christlikeness (C)", 0.0, 1.0, 0.85, 0.01, key="instant_C_slider")
H = st.slider("Heart (H)", 0.0, 1.0, 0.85, 0.01, key="instant_H_slider")
F = st.slider("Faithfulness (F)", 0.0, 1.0, 0.85, 0.01, key="instant_F_slider")

# Score logic
G = G_from_CHF(C, H, F)
A = A_from_G(G)
score = score_from_A(A)
label = label_from_score(score)
score_display = score * 10

# Enhanced score preview
st.markdown("### 🔍 Spiritual Alignment Summary")
st.write(f"**G (God Alignment Score):** `{G:.3f}` — Reflects how closely this decision aligns with God’s character. A score near 1.00 suggests strong spiritual integrity.")
st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Indicates the direction and intensity of alignment. Positive values show movement toward Christlike living; negative values suggest drift or misalignment.")
preview_card(G, title="Instant Score")

# Divider
st.markdown("---")
st.markdown('<a name="saved-scenarios"></a>', unsafe_allow_html=True)
st.header("📂 Saved Scenarios")
st.caption("Review your saved reflections and spiritual scores.")

profile_name = st.session_state.get("selected_profile", "Me")
key = f"profile_{profile_name}"
if key in st.session_state and st.session_state[key]["scenarios"]:
    for i, scenario in enumerate(reversed(st.session_state[key]["scenarios"])):
        with st.expander(f"{scenario['Book']} {scenario['Verse']} — {scenario['Figure']}: {scenario['Situation']}"):
            st.write(f"**Saved:** {scenario['Saved']}")
            st.write(f"**C:** `{scenario['C']}` · **H:** `{scenario['H']}` · **F:** `{scenario['F']}`")
            st.write(f"**G (God Alignment Score):** `{scenario['G']}` — Measures how closely this moment reflects God’s character.")
            st.write(f"**Score:** `{scenario['Score']}` — Overall spiritual integrity based on Christlikeness, Heart, and Faithfulness.")
            st.markdown(f"{chip_html(scenario['Label'])}", unsafe_allow_html=True)
            st.markdown(bar_html(scenario['G'], "G Alignment"), unsafe_allow_html=True)
            st.markdown(bar_html(scenario['Score'] / 10, "Score", "#10b981" if "Aligned" in scenario['Label'] else "#f59e0b" if "Mixed" in scenario['Label'] else "#ef4444"), unsafe_allow_html=True)
else:
    st.info("No scenarios saved yet. Use the Scripture Catalog or Custom Scenario to begin.")

# ======================= Module 5: Life Assessment & Growth Tracker =======================

st.markdown('<a name="life-assessment"></a>', unsafe_allow_html=True)
st.header("🧭 Life Assessment & Growth Tracker")
st.caption("Reflect on your own choices and spiritual habits. Use the sliders to assess alignment with God.")

st.markdown("""
- **Christlikeness (C)**: Are your recent decisions marked by humility, love, and truth?  
- **Heart (H)**: Are you acting from a place of surrender, generosity, and spiritual clarity?  
- **Faithfulness (F)**: Are you walking in obedience to God’s Word and your calling?
""")

with st.form("life_assessment_form"):
    C = st.slider("Christlikeness (C)", 0.0, 1.0, 0.85, 0.01)
    H = st.slider("Heart (H)", 0.0, 1.0, 0.85, 0.01)
    F = st.slider("Faithfulness (F)", 0.0, 1.0, 0.85, 0.01)
    submitted = st.form_submit_button("💾 Save Life Assessment")

if submitted:
    G = G_from_CHF(C, H, F)
    A = A_from_G(G)
    profile_name = st.session_state.get("selected_profile", "Me")
    assessment = {
        "Type": "Life Assessment",
        "C": C,
        "H": H,
        "F": F,
        "G": G,
        "Score": score_from_A(A),
        "Label": label_from_score(score_from_A(A)),
        "Saved": datetime.today().strftime("%Y-%m-%d")
    }
    key = f"profile_{profile_name}"
    if key in st.session_state:
        st.session_state[key]["assessments"].append(assessment)
        st.success(f"Life assessment saved to profile '{profile_name}'")
        preview_card(G, title="Life Assessment")
        st.markdown("### 🔍 Spiritual Alignment Summary")
        st.write(f"**G (God Alignment Score):** `{G:.3f}` — Reflects how closely your choices align with God’s character.")
        st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Indicates the direction and intensity of your spiritual alignment.")
    else:
        st.warning("Profile not found. Please create a profile first.")

# ======================= Module 6: Progress Viewer & Greatest Commands =======================

st.markdown('<a name="progress-viewer"></a>', unsafe_allow_html=True)
st.header("📈 Progress Viewer")
st.caption("Review your saved life assessments and reflect on your spiritual growth over time.")

profile_name = st.session_state.get("selected_profile", "Me")
key = f"profile_{profile_name}"
if key in st.session_state and st.session_state[key]["assessments"]:
    for i, assessment in enumerate(reversed(st.session_state[key]["assessments"])):
        with st.expander(f"🧭 Life Assessment — {assessment['Saved']}"):
            st.write(f"**C:** `{assessment['C']}` · **H:** `{assessment['H']}` · **F:** `{assessment['F']}`")
            st.write(f"**G (God Alignment Score):** `{assessment['G']}` — Measures how closely your choices reflect God’s character.")
            st.write(f"**Score:** `{assessment['Score']}` — Overall spiritual integrity.")
            st.markdown(f"{chip_html(assessment['Label'])}", unsafe_allow_html=True)
            st.markdown(bar_html(assessment['G'], "G Alignment"), unsafe_allow_html=True)
            st.markdown(bar_html(assessment['Score'] / 10, "Score", "#10b981" if "Aligned" in assessment['Label'] else "#f59e0b" if "Mixed" in assessment['Label'] else "#ef4444"), unsafe_allow_html=True)
else:
    st.info("No life assessments saved yet. Use the Life Assessment tool to begin.")

# Divider
st.markdown("---")
st.markdown('<a name="greatest-commands"></a>', unsafe_allow_html=True)
st.header("💖 Greatest Commands Reflection")
st.caption("How are you loving God and loving your neighbor in this season?")

with st.form("greatest_commands_form"):
    love_god = st.slider("Love of God", 0.0, 1.0, 0.85, 0.01)
    love_neighbor = st.slider("Love of Neighbor", 0.0, 1.0, 0.85, 0.01)
    submitted = st.form_submit_button("💾 Save Reflection")

if submitted:
    G = G_from_CHF(love_god, love_neighbor, 1.0)
    A = A_from_G(G)
    reflection = {
        "Type": "Greatest Commands",
        "LoveGod": love_god,
        "LoveNeighbor": love_neighbor,
        "G": G,
        "Score": score_from_A(A),
        "Label": label_from_score(score_from_A(A)),
        "Saved": datetime.today().strftime("%Y-%m-%d")
    }
    if key in st.session_state:
        st.session_state[key]["assessments"].append(reflection)
        st.success("Reflection saved.")
        preview_card(G, title="Greatest Commands")
        st.markdown("### 🔍 Spiritual Alignment Summary")
        st.write(f"**G (God Alignment Score):** `{G:.3f}` — Reflects how fully you’re living out love for God and neighbor.")
        st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Indicates the direction and intensity of your spiritual alignment.")
    else:
        st.warning("Profile not found. Please create a profile first.")

# ======================= Module 7: Closing Reflection & Footer =======================

st.markdown('<a name="closing-reflection"></a>', unsafe_allow_html=True)
st.header("🌟 Closing Reflection")
st.caption("Pause and reflect on what you've seen, felt, and discerned.")

st.markdown("""
> _“Search me, O God, and know my heart; test me and know my anxious thoughts.  
> Point out anything in me that offends you, and lead me along the path of everlasting life.”_  
> — Psalm 139:23–24
""")

st.markdown("You’ve explored Scripture, reflected on your choices, and measured spiritual alignment. Let this be a moment of clarity—not just calculation. May your journey continue in love, truth, and transformation.")

st.markdown("---")
st.markdown('<a name="footer"></a>', unsafe_allow_html=True)
st.caption("🖤 Soverain · Spiritual Intelligence Platform")
st.caption("Version 1.0 · Built with prayer, precision, and purpose")

# ======================= Module 8: Profile Dashboard =======================

st.markdown('<a name="profile-dashboard"></a>', unsafe_allow_html=True)
st.header("🧑 Profile Dashboard")
st.caption("View your spiritual journey at a glance.")

# Active profile and key
profile_name = st.session_state.get("selected_profile", "Me")
profile_key = f"profile_{profile_name}"
profile_data = st.session_state.get(profile_key, {
    "scenarios": [],
    "assessments": [],
    "reflections": [],
    "goal": "—",
    "last_score": "—"
})

# Extract data
scenarios = profile_data.get("scenarios", [])
assessments = profile_data.get("assessments", [])
reflections = profile_data.get("reflections", [])

# Summary stats
total_scenarios = len(scenarios)
total_assessments = len(assessments)
total_reflections = len(reflections)

all_scores = [s["Score"] for s in scenarios + assessments if "Score" in s]
avg_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else "—"

all_G = [s["G"] for s in scenarios + assessments if "G" in s]
avg_G = round(sum(all_G) / len(all_G), 3) if all_G else "—"

all_A = [A_from_G(s["G"]) for s in scenarios + assessments if "G" in s]
avg_A = round(sum(all_A) / len(all_A), 3) if all_A else "—"

# Display summary
st.markdown(f"### 👤 Profile: `{profile_name}`")
st.write(f"**Spiritual Goal:** `{profile_data.get('goal', '—')}`")
st.write(f"**Last Score:** `{profile_data.get('last_score', '—')}`")
st.write(f"**Saved Scenarios:** `{total_scenarios}`")
st.write(f"**Life Assessments:** `{total_assessments}`")
st.write(f"**Reflections:** `{total_reflections}`")
st.write(f"**Average Score:** `{avg_score}`")
st.write(f"**Average G (God Alignment):** `{avg_G}`")
st.write(f"**Average A (Spiritual Vector):** `{avg_A}`")

# Visual preview
if isinstance(avg_G, float):
    preview_card(avg_G, title="Profile Alignment")

# Quick links
st.markdown("### 🔗 Quick Navigation")
st.markdown("""
- [📖 Scripture Catalog](#scripture-catalog)  
- [✍️ Add Custom Scenario](#custom-scenario)  
- [⚡ Instant Calculator](#instant-calculator)  
- [🧭 Life Assessment](#life-assessment)  
- [📈 Progress Viewer](#progress-viewer)  
- [✝️ Greatest Commands](#greatest-commands)  
- [🌟 Closing Reflection](#closing-reflection)
""", unsafe_allow_html=True)

# Optional: Recent reflections
if reflections:
    st.markdown("### 📝 Recent Reflections")
    for r in reversed(reflections[-3:]):
        st.markdown(f"- *{r['Saved']}*: {r['Text'][:80]}{'...' if len(r['Text']) > 80 else ''}")

# ======================= Module 9: Journaling & Reflection =======================

st.markdown('<a name="journaling-reflection"></a>', unsafe_allow_html=True)
st.header("📝 Journaling & Reflection")
st.caption("Capture spiritual insights, moments of clarity, or personal prayers.")

with st.form("journal_entry_form"):
    entry_text = st.text_area("Write your reflection", height=160, placeholder="What is God showing you today?")
    tags = st.text_input("Tags (optional)", placeholder="e.g. obedience, forgiveness, Psalm 23")
    link_to = st.selectbox("Link to:", ["None", "Last Scenario", "Last Assessment"])
    submitted = st.form_submit_button("💾 Save Reflection")

if submitted and entry_text.strip():
    profile_name = st.session_state.get("selected_profile", "Me")
    profile_key = f"profile_{profile_name}"
    linked_score = None
    linked_G = None

    # Link to last scenario or assessment if selected
    if link_to == "Last Scenario" and st.session_state[profile_key]["scenarios"]:
        last = st.session_state[profile_key]["scenarios"][-1]
        linked_score = last["Score"]
        linked_G = last["G"]
    elif link_to == "Last Assessment" and st.session_state[profile_key]["assessments"]:
        last = st.session_state[profile_key]["assessments"][-1]
        linked_score = last["Score"]
        linked_G = last["G"]

    reflection = {
        "Text": entry_text.strip(),
        "Tags": tags.strip(),
        "LinkedTo": link_to,
        "Score": linked_score,
        "G": linked_G,
        "Saved": datetime.today().strftime("%Y-%m-%d")
    }

    st.session_state[profile_key]["reflections"].append(reflection)
    st.success("Reflection saved.")

    # Optional preview
    if linked_G is not None:
        preview_card(linked_G, title="Linked Alignment")
        st.markdown("### 🔍 Spiritual Alignment Summary")
        st.write(f"**G (God Alignment Score):** `{linked_G:.3f}` — Reflects the alignment of the linked moment.")
        st.write(f"**A (Spiritual Vector):** `{A_from_G(linked_G):.3f}` — Direction and intensity of spiritual alignment.")

# ======================= Module 10: Guided Onboarding Flow =======================

st.markdown('<a name="guided-onboarding"></a>', unsafe_allow_html=True)

# 🌅 Welcome message at the top
st.header("🌅 Welcome to Soverain")
st.markdown("""
> _“The unfolding of your words gives light; it gives understanding to the simple.”_  
> — Psalm 119:130

*Soverain* is a spiritual intelligence platform that helps you reflect on decisions, Scripture, and life through the lens of Christlikeness, Heart, and Faithfulness.

Your spiritual alignment is measured using:
- **C (Christlikeness)**: Does this reflect the humility, love, and truth of Jesus?
- **H (Heart)**: Is your motive pure, generous, and surrendered?
- **F (Faithfulness)**: Does this honor God’s Word and your spiritual commitments?

These form your **G (God Alignment Score)** and **A (Spiritual Vector)**—a snapshot of how closely your choices align with God’s character.
""")

# Onboarding logic
if not st.session_state.get("onboarded", False):
    st.markdown("### ✍️ Let’s Try It Together")
    st.markdown("Rate a recent decision or moment:")

    C = st.slider("Christlikeness (C)", 0.0, 1.0, 0.85, 0.01)
    H = st.slider("Heart (H)", 0.0, 1.0, 0.85, 0.01)
    F = st.slider("Faithfulness (F)", 0.0, 1.0, 0.85, 0.01)

    G = G_from_CHF(C, H, F)
    A = A_from_G(G)
    score = score_from_A(A)

    preview_card(G, title="Your First Score")
    st.markdown("### 🔍 Spiritual Alignment Summary")
    st.write(f"**G (God Alignment Score):** `{G:.3f}` — Reflects how closely this moment aligns with God’s character.")
    st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Direction and intensity of alignment.")

    if st.button("✅ Finish Onboarding"):
        st.session_state["onboarded"] = True
        st.success("Welcome aboard! You’re now ready to explore Soverain.")
        st.rerun()

else:
    st.markdown("✅ You’ve completed onboarding. Use the navigation sidebar to explore Scripture, add scenarios, or reflect on your life journey.")

# ======================= Module 11: Scripture Expansion & Catalog Editor =======================

st.markdown('<a name="scripture-editor"></a>', unsafe_allow_html=True)
st.header("📖 Scripture Catalog Editor")
st.caption("View, edit, or expand the biblical moments used in spiritual reflection.")

# Initialize catalog if missing
if "scripture_catalog" not in st.session_state:
    st.session_state["scripture_catalog"] = [
        ("Genesis", "22:9–12", "Abraham", "Offer Isaac in obedience", 0.95, 0.95, 0.95, "Genesis 22:9–12"),
        ("Exodus", "3:4", "Moses", "Respond to God's call at the burning bush", 0.90, 0.90, 0.90, "Exodus 3:4"),
        ("Matthew", "5:1–12", "Jesus", "Teach the Beatitudes", 1.00, 1.00, 1.00, "Matthew 5:1–12"),
        ("Luke", "15:20", "Father", "Forgive the prodigal son", 0.95, 0.95, 0.95, "Luke 15:20"),
        ("John", "13:5", "Jesus", "Wash the disciples’ feet", 1.00, 1.00, 1.00, "John 13:5"),
        ("Acts", "2:42–47", "Early Church", "Live in unity and generosity", 0.95, 0.95, 0.95, "Acts 2:42–47"),
    ]

# Display current catalog
st.markdown("### 📂 Current Entries")
for i, entry in enumerate(st.session_state["scripture_catalog"]):
    book, verse, figure, situation, C, H, F, ref = entry
    st.markdown(f"- **{book} {verse}** — {figure}: *{situation}* (C: `{C}`, H: `{H}`, F: `{F}`)")

# Add new entry
st.markdown("---")
st.markdown("### ➕ Add New Scripture Entry")

with st.form("add_scripture_form"):
    book = st.text_input("Book", placeholder="e.g. Romans")
    verse = st.text_input("Chapter:Verse", placeholder="e.g. 12:1–2")
    figure = st.text_input("Figure or person", placeholder="e.g. Paul")
    situation = st.text_area("Situation or decision", height=80, placeholder="e.g. Urging transformation and renewal")
    C = st.slider("Christlikeness (C)", 0.0, 1.0, 0.85, 0.01)
    H = st.slider("Heart (H)", 0.0, 1.0, 0.85, 0.01)
    F = st.slider("Faithfulness (F)", 0.0, 1.0, 0.85, 0.01)
    submitted = st.form_submit_button("💾 Add to Catalog")

if submitted and book.strip() and verse.strip():
    new_entry = (book.strip(), verse.strip(), figure.strip(), situation.strip(), C, H, F, f"{book.strip()} {verse.strip()}")
    st.session_state["scripture_catalog"].append(new_entry)
    st.success(f"Added {book.strip()} {verse.strip()} to Scripture Catalog.")

# ======================= Module 12: Discipleship Pathways =======================

st.markdown('<a name="discipleship-pathways"></a>', unsafe_allow_html=True)
st.header("🧭 Discipleship Pathways")
st.caption("Choose a spiritual growth track and reflect on curated Scripture moments.")

# Define pathways
PATHWAYS = {
    "Obedience": [
        ("Genesis", "22:9–12", "Abraham", "Offer Isaac in obedience", 0.95, 0.95, 0.95),
        ("Matthew", "4:19", "Jesus", "Call the disciples to follow", 0.90, 0.90, 0.90),
    ],
    "Love": [
        ("Luke", "15:20", "Father", "Forgive the prodigal son", 0.95, 0.95, 0.95),
        ("John", "13:5", "Jesus", "Wash the disciples’ feet", 1.00, 1.00, 1.00),
    ],
    "Wisdom": [
        ("Proverbs", "3:5–6", "Solomon", "Trust in the Lord", 0.90, 0.90, 0.90),
        ("James", "1:5", "James", "Ask God for wisdom", 0.90, 0.90, 0.90),
    ]
}

# Select pathway
selected_pathway = st.selectbox("Choose a pathway", list(PATHWAYS.keys()))
entries = PATHWAYS[selected_pathway]

# Display entries
for i, (book, verse, figure, situation, C_default, H_default, F_default) in enumerate(entries):
    with st.expander(f"{book} {verse} — {figure}: {situation}"):
        C = st.slider(f"Christlikeness (C) — {verse}", 0.0, 1.0, C_default, 0.01, key=f"C_{i}")
        H = st.slider(f"Heart (H) — {verse}", 0.0, 1.0, H_default, 0.01, key=f"H_{i}")
        F = st.slider(f"Faithfulness (F) — {verse}", 0.0, 1.0, F_default, 0.01, key=f"F_{i}")
        G = G_from_CHF(C, H, F)
        A = A_from_G(G)
        score = score_from_A(A)
        preview_card(G, title=f"{book} {verse}")
        st.markdown("### 🔍 Spiritual Alignment Summary")
        st.write(f"**G (God Alignment Score):** `{G:.3f}` — Reflects how closely this moment aligns with God’s character.")
        st.write(f"**A (Spiritual Vector):** `{A:.3f}` — Direction and intensity of alignment.")

        if st.button(f"💾 Save Reflection — {verse}"):
            profile_name = st.session_state.get("selected_profile", "Me")
            key = f"profile_{profile_name}"
            reflection = {
                "Type": "Pathway Reflection",
                "Pathway": selected_pathway,
                "Book": book,
                "Verse": verse,
                "Figure": figure,
                "Situation": situation,
                "C": C,
                "H": H,
                "F": F,
                "G": G,
                "Score": score,
                "Label": label_from_score(score),
                "Saved": datetime.today().strftime("%Y-%m-%d")
            }
            st.session_state[key]["reflections"].append(reflection)
            st.success(f"Reflection saved to profile '{profile_name}'")

# ======================= Module 13: Spiritual Scoreboard =======================

import pandas as pd

st.markdown('<a name="spiritual-scoreboard"></a>', unsafe_allow_html=True)
st.header("📊 Spiritual Scoreboard")
st.caption("Visualize your spiritual alignment over time.")

# Active profile
profile_name = st.session_state.get("selected_profile", "Me")
profile_key = f"profile_{profile_name}"
profile_data = st.session_state.get(profile_key, {
    "scenarios": [],
    "assessments": [],
    "reflections": []
})

# Combine all scored entries
entries = []
for s in profile_data.get("scenarios", []):
    entries.append({
        "Date": s["Saved"],
        "Type": "Scenario",
        "Label": s["Label"],
        "Score": s["Score"],
        "G": s["G"]
    })
for a in profile_data.get("assessments", []):
    entries.append({
        "Date": a["Saved"],
        "Type": "Assessment",
        "Label": a["Label"],
        "Score": a["Score"],
        "G": a["G"]
    })
for r in profile_data.get("reflections", []):
    if "Score" in r and "G" in r:
        entries.append({
            "Date": r["Saved"],
            "Type": r.get("Type", "Reflection"),
            "Label": r.get("Label", ""),
            "Score": r["Score"],
            "G": r["G"]
        })

# Build DataFrame
if entries:
    df = pd.DataFrame(entries)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    # Line chart
    st.markdown("### 📈 Score Over Time")
    st.line_chart(df.set_index("Date")["Score"])

    # Breakdown by type
    st.markdown("### 🧭 Score Breakdown by Type")
    avg_by_type = df.groupby("Type")["Score"].mean().round(2)
    st.bar_chart(avg_by_type)

    # Alignment preview
    avg_G = round(df["G"].mean(), 3)
    preview_card(avg_G, title="Average Alignment")

    st.markdown("### 🔍 Spiritual Alignment Summary")
    st.write(f"**Average G (God Alignment Score):** `{avg_G}` — Reflects overall spiritual integrity across entries.")
    st.write(f"**Average A (Spiritual Vector):** `{A_from_G(avg_G):.3f}` — Direction and intensity of alignment.")

else:
    st.info("No scored entries yet. Use the Scripture Catalog, Life Assessment, or Journaling modules to begin.")

# ======================= Module 14: Spiritual Nudges & Notifications =======================

from datetime import datetime, timedelta

st.markdown('<a name="spiritual-nudges"></a>', unsafe_allow_html=True)
st.header("🔔 Spiritual Nudges")
st.caption("Gentle prompts to help you reflect, realign, and grow.")

# Active profile
profile_name = st.session_state.get("selected_profile", "Me")
profile_key = f"profile_{profile_name}"
profile_data = st.session_state.get(profile_key, {
    "scenarios": [],
    "assessments": [],
    "reflections": []
})

# Get last activity date
all_dates = []
for s in profile_data["scenarios"]:
    all_dates.append(s["Saved"])
for a in profile_data["assessments"]:
    all_dates.append(a["Saved"])
for r in profile_data["reflections"]:
    all_dates.append(r["Saved"])

if all_dates:
    last_date = max(pd.to_datetime(all_dates))
    days_since = (datetime.today() - last_date).days
else:
    last_date = None
    days_since = None

# Get recent scores
recent_scores = [e["Score"] for e in profile_data["scenarios"] + profile_data["assessments"] if "Score" in e]
avg_score = round(sum(recent_scores[-5:]) / len(recent_scores[-5:]), 2) if recent_scores[-5:] else None

# Nudges
st.markdown("### 🧭 Your Spiritual Rhythm")

if days_since is not None and days_since >= 5:
    st.warning(f"It’s been {days_since} days since your last reflection. Consider revisiting a Scripture or journaling a moment of clarity.")
elif days_since is not None and days_since >= 2:
    st.info(f"{days_since} days since your last entry. A moment of quiet could bring fresh insight.")

if avg_score is not None and avg_score < 6:
    st.warning(f"Your recent average score is `{avg_score}`. You may be navigating a spiritually mixed season. Consider revisiting the **Obedience** or **Love** pathway.")
elif avg_score is not None and avg_score >= 8:
    st.success(f"Your recent average score is `{avg_score}`. You’re walking in strong alignment—consider journaling what’s sustaining you.")

# Scripture nudge
st.markdown("### 📖 Suggested Scripture")
st.markdown("> _“Let us examine our ways and test them, and let us return to the Lord.”_ — Lamentations 3:40")

# Action buttons
st.markdown("### ✍️ What would you like to do next?")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📖 Open Scripture Catalog"):
        st.markdown('<a href="#scripture-catalog">Jumping to Scripture Catalog...</a>', unsafe_allow_html=True)
with col2:
    if st.button("📝 Start a Journal Entry"):
        st.markdown('<a href="#journaling-reflection">Jumping to Journaling...</a>', unsafe_allow_html=True)
with col3:
    if st.button("🧭 Revisit a Pathway"):
        st.markdown('<a href="#discipleship-pathways">Jumping to Pathways...</a>', unsafe_allow_html=True)

# ======================= Module 15: Spiritual Tags & Search =======================

st.markdown('<a name="spiritual-search"></a>', unsafe_allow_html=True)
st.header("🔍 Spiritual Tags & Search")
st.caption("Explore your spiritual journey by theme, Scripture, or score.")

# Active profile
profile_name = st.session_state.get("selected_profile", "Me")
profile_key = f"profile_{profile_name}"
profile_data = st.session_state.get(profile_key, {
    "scenarios": [],
    "assessments": [],
    "reflections": []
})

# Combine all entries
entries = []
for s in profile_data["scenarios"]:
    entries.append({**s, "Type": "Scenario"})
for a in profile_data["assessments"]:
    entries.append({**a, "Type": "Assessment"})
for r in profile_data["reflections"]:
    entries.append({**r, "Type": r.get("Type", "Reflection")})

# Search inputs
st.markdown("### 🔎 Filter Your Journey")
search_text = st.text_input("Search by keyword, book, figure, or tag", placeholder="e.g. forgiveness, Luke, obedience")
min_score = st.slider("Minimum Score", 0, 10, 0)
sort_order = st.selectbox("Sort by", ["Newest", "Oldest", "Highest Score", "Lowest Score"])

# Filter logic
filtered = []
for e in entries:
    match_text = f"{e.get('Book','')} {e.get('Verse','')} {e.get('Figure','')} {e.get('Situation','')} {e.get('Tags','')} {e.get('Text','')}".lower()
    if search_text.lower() in match_text and e.get("Score", 0) >= min_score:
        filtered.append(e)

# Sort logic
if sort_order == "Newest":
    filtered = sorted(filtered, key=lambda x: x.get("Saved", ""), reverse=True)
elif sort_order == "Oldest":
    filtered = sorted(filtered, key=lambda x: x.get("Saved", ""))
elif sort_order == "Highest Score":
    filtered = sorted(filtered, key=lambda x: x.get("Score", 0), reverse=True)
elif sort_order == "Lowest Score":
    filtered = sorted(filtered, key=lambda x: x.get("Score", 0))

# Display results
if filtered:
    st.markdown(f"### 📂 {len(filtered)} Matching Entries")
    for i, e in enumerate(filtered):
        with st.expander(f"{e.get('Book','')} {e.get('Verse','')} — {e.get('Figure','')} ({e['Type']})"):
            st.write(f"**Saved:** {e.get('Saved','—')}")
            st.write(f"**Tags:** {e.get('Tags','—')}")
            st.write(f"**Score:** `{e.get('Score','—')}` · **G:** `{e.get('G','—')}` · **Label:** {e.get('Label','—')}")
            if "Text" in e:
                st.markdown(f"**Reflection:** {e['Text']}")
            preview_card(e["G"], title=f"{e.get('Book','')} {e.get('Verse','')}")
else:
    st.info("No matching entries found. Try adjusting your filters or search terms.")

# ======================= Module 16: Spiritual Export & Legacy Builder =======================

st.markdown('<a name="legacy-builder"></a>', unsafe_allow_html=True)
st.header("📜 Spiritual Legacy Builder")
st.caption("Curate your spiritual journey into a testimony of growth, insight, and alignment.")

# Active profile
profile_name = st.session_state.get("selected_profile", "Me")
profile_key = f"profile_{profile_name}"
profile_data = st.session_state.get(profile_key, {
    "scenarios": [],
    "assessments": [],
    "reflections": []
})

# Filter options
st.markdown("### 🔎 Select Entries to Include")
entry_types = st.multiselect("Include types", ["Scenario", "Assessment", "Reflection", "Pathway Reflection"], default=["Scenario", "Assessment", "Reflection"])
start_date = st.date_input("Start date", value=datetime.today() - timedelta(days=90))
end_date = st.date_input("End date", value=datetime.today())

# Compile entries
entries = []
for s in profile_data["scenarios"]:
    if "Scenario" in entry_types and pd.to_datetime(s["Saved"]).date() >= start_date and pd.to_datetime(s["Saved"]).date() <= end_date:
        entries.append({**s, "Type": "Scenario"})
for a in profile_data["assessments"]:
    if "Assessment" in entry_types and pd.to_datetime(a["Saved"]).date() >= start_date and pd.to_datetime(a["Saved"]).date() <= end_date:
        entries.append({**a, "Type": "Assessment"})
for r in profile_data["reflections"]:
    if r.get("Type", "Reflection") in entry_types and pd.to_datetime(r["Saved"]).date() >= start_date and pd.to_datetime(r["Saved"]).date() <= end_date:
        entries.append({**r, "Type": r.get("Type", "Reflection")})

# Display legacy preview
if entries:
    st.markdown(f"### 📖 Legacy Preview ({len(entries)} entries)")
    for i, e in enumerate(sorted(entries, key=lambda x: x["Saved"], reverse=True)):
        with st.expander(f"{e.get('Saved','—')} — {e['Type']}"):
            st.write(f"**Book:** {e.get('Book','—')} · **Verse:** {e.get('Verse','—')} · **Figure:** {e.get('Figure','—')}")
            st.write(f"**Situation:** {e.get('Situation','—')}")
            st.write(f"**Tags:** {e.get('Tags','—')}")
            st.write(f"**Score:** `{e.get('Score','—')}` · **G:** `{e.get('G','—')}` · **Label:** {e.get('Label','—')}")
            if "Text" in e:
                st.markdown(f"**Reflection:** {e['Text']}")
            preview_card(e["G"], title=f"{e.get('Book','')} {e.get('Verse','')}")
else:
    st.info("No entries found for the selected filters. Try adjusting the date range or types.")
