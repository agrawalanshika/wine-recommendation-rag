import streamlit as st
from utils import search_wines
from openai import OpenAI
import os

# Title
st.title("Wine Recommendation System")

# 🎨 FIXED CSS (IMPORTANT)
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        rgba(0, 0, 0, 0.75),  
        rgba(0, 0, 0, 0.75)
    ),
    url("https://images8.alphacoders.com/365/365645.jpg");

    background-size: cover;
    background-position: center top 60px;
    background-repeat: no-repeat;
}

/* Text visibility */
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

/* Glassmorphism Card */
.card {
    padding: 15px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.08);  
    backdrop-filter: blur(10px);           
    -webkit-backdrop-filter: blur(10px);
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Button styling */
.stButton>button {
    border-radius: 10px;
    background: linear-gradient(45deg, #8B0000, #B22222);
    color: white;
    border: none;
    padding: 10px 20px;
}

</style>
""", unsafe_allow_html=True)

# Input
user_prompt = st.text_input("Enter your wine preference:")

# Button
if st.button("Get Recommendation"):

    if not user_prompt.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Finding the perfect wine... 🍷"):

            # 🔍 Search
            hits = search_wines(user_prompt)

            # Filter
            filtered_hits = [hit for hit in hits.points if hit.score > 0.7]

            # Sort
            filtered_hits = sorted(filtered_hits, key=lambda x: x.score, reverse=True)

            # Remove duplicates
            unique_notes = set()
            filtered_hits_unique = []

            for hit in filtered_hits:
                note = hit.payload.get("notes", "").strip().lower()

                if note not in unique_notes:
                    unique_notes.add(note)
                    filtered_hits_unique.append(hit)

            # Top 3
            filtered_hits = filtered_hits_unique[:3]

            # Fallback
            if not filtered_hits:
                filtered_hits = hits.points[:3]

            # Display
            st.subheader("🔍 Retrieved Wines")

            for hit in filtered_hits:
                wine = hit.payload
                st.markdown(f"""
                <div class="card">
                🍷 <b>Variety:</b> {wine.get('variety','Unknown')} <br>
                📝 <b>Notes:</b> {wine.get('notes','No description')} <br>
                🌍 <b>Region:</b> {wine.get('region','Unknown')} <br>
                ⭐ <b>Score:</b> {round(hit.score, 2)}
                </div>
                """, unsafe_allow_html=True)

            # 🤖 LLM
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY")
            )

            search_results = [
                {
                    "variety": hit.payload.get("variety"),
                    "notes": hit.payload.get("notes")[:200]
                }
                for hit in filtered_hits[:2]
            ]

            messages = [
                {
                    "role": "system",
                    "content": "You are a wine expert. Give a detailed, structured recommendation including wine type, flavor profile, and why it matches the user’s preference. Only use provided data."
                },
                {
                    "role": "system",
                    "content": f"Here are some relevant wines:\n{search_results}"
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

            response = client.chat.completions.create(
                model="deepseek/deepseek-r1",
                messages=messages,
                max_tokens=1200
            )

            # Final Output
            st.subheader("🍷 Final Recommendation")

            st.markdown(f"""
            <div class="card">
            {response.choices[0].message.content}
            </div>
            """, unsafe_allow_html=True)