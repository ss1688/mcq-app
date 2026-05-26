import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="My Premium LMS", page_icon="🚀", layout="wide")

# ==========================================
# 🎨 MASTER COLOR THEMES
# ==========================================
THEMES = {
    "Midnight Dark (Premium)": {
        "bg_gradient": "radial-gradient(circle at top left, #1a1a2e, #16213e)",
        "text_main": "#e0e0e0",
        "primary": "#0f3460",
        "highlight": "#e94560",
        "box_bg": "#0f3460",
        "box_border": "#e94560",
        "success_bg": "rgba(40, 167, 69, 0.2)",
        "success_text": "#28a745",
        "success_border": "#28a745",
        "error_bg": "rgba(220, 53, 69, 0.2)",
        "error_text": "#ff4b5c",
        "error_border": "#ff4b5c",
        "neutral_bg": "rgba(255, 255, 255, 0.05)",
        "neutral_text": "#a0a0a0",
        "neutral_border": "#444444"
    },
    "Vibrant Light": {
        "bg_gradient": "radial-gradient(circle at top left, #f0f7ff, #ffffff)",
        "text_main": "#111111",
        "primary": "#4361ee",
        "highlight": "#f72585",
        "box_bg": "#ffffff",
        "box_border": "#4361ee",
        "success_bg": "#d4edda",
        "success_text": "#155724",
        "success_border": "#28a745",
        "error_bg": "#f8d7da",
        "error_text": "#721c24",
        "error_border": "#dc3545",
        "neutral_bg": "#f8f9fa",
        "neutral_text": "#6c757d",
        "neutral_border": "#dee2e6"
    },
    "Hacker Green": {
        "bg_gradient": "linear-gradient(135deg, #000000, #0a0a0a)",
        "text_main": "#00ff00",
        "primary": "#003300",
        "highlight": "#00ff00",
        "box_bg": "#050505",
        "box_border": "#00ff00",
        "success_bg": "#002200",
        "success_text": "#00ff00",
        "success_border": "#00ff00",
        "error_bg": "#220000",
        "error_text": "#ff0000",
        "error_border": "#ff0000",
        "neutral_bg": "#111111",
        "neutral_text": "#008800",
        "neutral_border": "#004400"
    }
}

# --- SIDEBAR & SETTINGS ---
with st.sidebar:
    st.header("⚙️ App Settings")
    selected_theme_name = st.selectbox("🎨 Choose Theme", list(THEMES.keys()))
    t = THEMES[selected_theme_name] 
    font_size = st.slider("🔠 Text Size", min_value=0.8, max_value=1.5, value=1.0, step=0.1)
    st.divider()

# 2. Dynamic Custom CSS (Includes Flexbox for Clean Icons)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
        background: {t['bg_gradient']};
    }}
    
    h1, h2, h3, h4, h5, h6, p, label, span, li, .stMarkdown {{
        color: {t['text_main']} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {t['highlight']} !important; 
        font-weight: 900 !important;
    }}

    .question-box {{
        padding: {30 * font_size}px;
        border-radius: 15px;
        border: 3px solid {t['box_border']};
        background-color: {t['box_bg']};
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }}
    .question-text {{
        font-size: {2.0 * font_size}rem !important; 
        line-height: 1.5;
        font-weight: 700;
        color: {t['text_main']} !important;
    }}

    /* FLEXBOX Answer Boxes: Pushes the text to the left and the icon to the right */
    .ans-box {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: {15 * font_size}px 25px;
        border-radius: 12px;
        font-size: {1.2 * font_size}rem;
        font-weight: 600;
        margin-bottom: 15px;
    }}
    .ans-correct {{
        background-color: {t['success_bg']};
        border: 2px solid {t['success_border']};
        color: {t['success_text']} !important;
        box-shadow: 0 0 15px {t['success_bg']};
    }}
    .ans-wrong {{
        background-color: {t['error_bg']};
        border: 2px solid {t['error_border']};
        color: {t['error_text']} !important;
        box-shadow: 0 0 15px {t['error_bg']};
    }}
    .ans-neutral {{
        background-color: {t['neutral_bg']};
        border: 2px solid {t['neutral_border']};
        color: {t['neutral_text']} !important;
    }}
    .icon-large {{
        font-size: {1.4 * font_size}rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. Load Data
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1EfuQE3qvJSZzheX7HzCfy3ESLBB-ilkd-_zYqRB6UHY/edit?gid=0#gid=0"
    if "/edit" in sheet_url:
        base_url = sheet_url.split("/edit")[0]
        csv_export_url = f"{base_url}/export?format=csv"
    else:
        csv_export_url = sheet_url
    return pd.read_csv(csv_export_url)

def get_rank(correct_count):
    if correct_count < 5: return "🌱 Novice"
    elif correct_count < 15: return "🔥 Rising Star"
    elif correct_count < 30: return "🧠 Scholar"
    else: return "👑 Master"

def main():
    try:
        df = load_data()
        df = df.dropna(subset=['Question'])
        for col in ['Course', 'Subject Name', 'Unit Name', 'S.No']:
            if col not in df.columns: df[col] = "Uncategorized"
            df[col] = df[col].fillna("Uncategorized")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Memory
    if 'user_answers' not in st.session_state: st.session_state.user_answers = {} 
    if 'current_index' not in st.session_state: st.session_state.current_index = 0

    # --- SIDEBAR NAV ---
    with st.sidebar:
        st.header("🗂️ Navigation")
        
        courses = df['Course'].unique()
        selected_course = st.selectbox("1. Course", courses)
        df_course = df[df['Course'] == selected_course]
        
        subjects = df_course['Subject Name'].unique()
        selected_subject = st.selectbox("2. Subject", subjects)
        df_subject = df_course[df_course['Subject Name'] == selected_subject]
        
        units = df_subject['Unit Name'].unique()
        selected_unit = st.selectbox("3. Unit", units)
        current_view_df = df_subject[df_subject['Unit Name'] == selected_unit]
        
        st.divider()
        st.subheader("🔢 Question Grid")
        grid_cols = st.columns(5)
        
        for i, (actual_df_index, row) in enumerate(current_view_df.iterrows()):
            col_idx = i % 5
            is_answered = actual_df_index in st.session_state.user_answers
            btn_label = "✅" if is_answered else f"{i+1}"
            
            with grid_cols[col_idx]:
                if st.button(btn_label, key=f"grid_{actual_df_index}", use_container_width=True):
                    st.session_state.current_index = actual_df_index
                    st.rerun()

    # --- MAIN SCREEN ---
    if st.session_state.current_index not in current_view_df.index:
        if not current_view_df.empty: st.session_state.current_index = current_view_df.index[0]
        else:
            st.warning("No questions found.")
            return

    row = df.loc[st.session_state.current_index]
    actual_idx = st.session_state.current_index
    
    # Extract Options
    options = {
        "A": str(row.get('Option A', '')).strip(),
        "B": str(row.get('Option B', '')).strip(),
        "C": str(row.get('Option C', '')).strip(),
        "D": str(row.get('Option D', '')).strip()
    }
    
    # Smart Correct Answer Logic
    raw_correct = str(row.get('Correct Answer', '')).strip()
    correct_letter = None
    clean_correct = raw_correct.upper().replace("OPTION", "").replace(")", "").replace(".", "").strip()
    
    if clean_correct in ["A", "B", "C", "D"]:
        correct_letter = clean_correct
    else:
        for letter, text in options.items():
            if text and raw_correct:
                if str(text).strip().lower() in raw_correct.lower() or raw_correct.lower() in str(text).strip().lower():
                    correct_letter = letter
                    break
    if not correct_letter:
        correct_letter = "UNKNOWN"
    
    # Dashboard Metrics
    total_answered = len(st.session_state.user_answers)
    total_correct = sum(1 for q_idx, ans_data in st.session_state.user_answers.items() if ans_data['is_correct'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Attempted", f"{total_answered}")
    col2.metric("Correct", f"{total_correct}")
    col3.metric("Rank", get_rank(total_correct))
    col4.metric("ID", f"S.No: {row['S.No']}")
    
    st.divider()

    # The Themed Question Box
    st.markdown(f"<div class='question-box'><div class='question-text'>{row['Question']}</div></div>", unsafe_allow_html=True)

    has_answered_this = actual_idx in st.session_state.user_answers
    user_choice = st.session_state.user_answers.get(actual_idx, {}).get('letter')

    # Options Grid
    opt_col1, opt_col2 = st.columns(2) 
    col_mapping = {"A": opt_col1, "B": opt_col2, "C": opt_col1, "D": opt_col2}
    
    for letter, text in options.items():
        with col_mapping[letter]:
            if not has_answered_this:
                # Standard buttons before answering
                if st.button(f"{letter}. {text}", use_container_width=True, key=f"opt_{actual_idx}_{letter}"):
                    is_correct = (letter == correct_letter)
                    st.session_state.user_answers[actual_idx] = {'letter': letter, 'is_correct': is_correct}
                    if is_correct: st.balloons()
                    st.rerun()
            else:
                # Minimalist UI Feedback (No bulky text, just colors and icons)
                if letter == correct_letter:
                    st.markdown(f"""
                        <div class='ans-box ans-correct'>
                            <span><b>{letter}.</b> {text}</span>
                            <span class='icon-large'>✅</span>
                        </div>
                    """, unsafe_allow_html=True)
                elif letter == user_choice and letter != correct_letter:
                    st.markdown(f"""
                        <div class='ans-box ans-wrong'>
                            <span><b>{letter}.</b> {text}</span>
                            <span class='icon-large'>❌</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class='ans-box ans-neutral'>
                            <span><b>{letter}.</b> {text}</span>
                            <span></span>
                        </div>
                    """, unsafe_allow_html=True)

    # Clean Review Section
    if has_answered_this:
        st.write("")
        with st.container(border=True):
            st.markdown(f"### 📖 Explanation")
            st.info(row.get('Explanation', 'No explanation provided.'))
            
            distractors = row.get('Distractors', '')
            if pd.notna(distractors) and str(distractors).strip() != "":
                st.divider()
                st.markdown(f"### 🚫 Why the others are wrong")
                st.error(distractors)
                
    st.write("")
    
    # Navigation
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    current_view_indices = current_view_df.index.tolist()
    current_position = current_view_indices.index(actual_idx)
    
    with nav_col1:
        if current_position > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_index = current_view_indices[current_position - 1]
                st.rerun()
                
    with nav_col3:
        if current_position < len(current_view_indices) - 1:
            if st.button("Next ➡️", use_container_width=True, type="primary"):
                st.session_state.current_index = current_view_indices[current_position + 1]
                st.rerun()

if __name__ == "__main__":
    main()
