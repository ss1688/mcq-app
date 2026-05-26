import streamlit as st
import pandas as pd

# 1. Page Configuration (Must be the first command)
st.set_page_config(page_title="My Study App", page_icon="📱", layout="centered")

# Custom CSS for a better UI
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    div[data-testid="stRadio"] > div {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    .question-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Bulletproof Data Loading
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1EfuQE3qvJSZzheX7HzCfy3ESLBB-ilkd-_zYqRB6UHY/edit?gid=0#gid=0"
    
    # This splits the URL exactly at "/edit" and drops everything after it
    if "/edit" in sheet_url:
        base_url = sheet_url.split("/edit")[0]
        csv_export_url = f"{base_url}/export?format=csv"
    else:
        csv_export_url = sheet_url
        
    return pd.read_csv(csv_export_url)

def main():
    st.title("📚 My Practice App")
    st.divider()
    
    try:
        df = load_data()
        df = df.dropna(subset=['Question']) 
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Check if your Google Sheet is set to 'Anyone with the link can view'.")
        return

    # 3. Setup Memory
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False

    # 4. Display the Quiz
    if st.session_state.current_q < len(df):
        row = df.iloc[st.session_state.current_q]
        
        # Progress Bar
        st.progress((st.session_state.current_q) / len(df))
        st.caption(f"**Subject:** {row['Subject Name']} | **Unit:** {row['Unit Name']}")
        st.markdown(f"**Question {st.session_state.current_q + 1} of {len(df)}**")
        
        # The Question (Styled)
        st.markdown(f"<div class='question-box'><h3>{row['Question']}</h3></div>", unsafe_allow_html=True)
        
        # The Options
        options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
        user_choice = st.radio("Select your answer:", options, index=None, key=f"q_{st.session_state.current_q}")
        
        st.write("") # Spacer
        
        # Action Buttons
        if st.button("Check Answer", type="primary") and user_choice:
            st.session_state.show_explanation = True
            
        if st.session_state.show_explanation:
            correct_letter = str(row['Correct Answer']).strip().upper()
            ans_map = {'A': str(row['Option A']), 'B': str(row['Option B']), 'C': str(row['Option C']), 'D': str(row['Option D'])}
            correct_text = ans_map.get(correct_letter, correct_letter)
            
            if user_choice == correct_text:
                st.success("✅ **Correct!**")
            else:
                st.error(f"❌ **Incorrect.** The correct answer is **{correct_letter}**: {correct_text}")
                
            st.info(f"**Explanation:**\n\n{row['Explanation']}")
            
            if st.button("Next Question"):
                st.session_state.current_q += 1
                st.session_state.show_explanation = False
                st.rerun()
                
    else:
        st.balloons()
        st.success("🎉 You have completed all the questions!")
        if st.button("Restart Quiz"):
            st.session_state.current_q = 0
            st.session_state.show_explanation = False
            st.rerun()

if __name__ == "__main__":
    main()
