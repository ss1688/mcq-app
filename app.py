import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="My Study App", layout="centered")

# 2. Load Data from Google Sheets (Caches for 60 seconds)
@st.cache_data(ttl=60)
def load_data():
    # REPLACE THE LINK BELOW WITH YOUR GOOGLE SHEET LINK
    sheet_url = "https://docs.google.com/spreadsheets/d/1EfuQE3qvJSZzheX7HzCfy3ESLBB-ilkd-_zYqRB6UHY/edit?gid=0#gid=0"
    
    csv_export_url = sheet_url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_export_url)

def main():
    st.title("📚 My MCQ Practice")
    
    try:
        df = load_data()
        # Drop empty rows just in case your sheet has blank lines at the bottom
        df = df.dropna(subset=['Question']) 
    except Exception as e:
        st.error("Could not load the Google Sheet. Please check the link and sharing settings.")
        return

    # 3. Setup Session State (Memory)
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False

    # 4. Display the Quiz
    if st.session_state.current_q < len(df):
        row = df.iloc[st.session_state.current_q]
        
        # Progress and Context
        st.progress((st.session_state.current_q) / len(df))
        st.caption(f"**Subject:** {row['Subject Name']} | **Unit:** {row['Unit Name']}")
        st.write(f"**Question {st.session_state.current_q + 1} of {len(df)}**")
        
        # The Question
        st.subheader(row['Question'])
        
        # The Options
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        user_choice = st.radio("Select your answer:", options, index=None, key=f"q_{st.session_state.current_q}")
        
        # Action Buttons
        if st.button("Check Answer") and user_choice:
            st.session_state.show_explanation = True
            
        if st.session_state.show_explanation:
            # Clean up the correct answer letter (e.g., in case it has spaces)
            correct_letter = str(row['Correct Answer']).strip().upper()
            ans_map = {'A': row['Option A'], 'B': row['Option B'], 'C': row['Option C'], 'D': row['Option D']}
            
            # Get the actual text of the correct answer
            correct_text = ans_map.get(correct_letter, correct_letter)
            
            # Grade it
            if user_choice == correct_text:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer is {correct_letter}.")
                
            # Show Explanation
            st.info(f"**Explanation:** {row['Explanation']}")
            
            # Move to next
            if st.button("Next Question"):
                st.session_state.current_q += 1
                st.session_state.show_explanation = False
                st.rerun()
                
    else:
        st.success("🎉 You have completed all the questions!")
        if st.button("Restart"):
            st.session_state.current_q = 0
            st.session_state.show_explanation = False
            st.rerun()

if __name__ == "__main__":
    main()
