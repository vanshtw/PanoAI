from openai import OpenAI
import os
import streamlit as st

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

# Streamlit UI
st.set_page_config(page_title="VG Gen AI Chatbot", page_icon="🤖")
st.title("🤖 Vansh's Gen AI Bot via OpenAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful chatbot."}]

# Chat input box
user_input = st.text_input("You:", "")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=st.session_state.messages
    )

    bot_response = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display chat history
    for message in st.session_state.messages[1:]:
        role = "User" if message["role"] == "user" else "Bot"
        st.write(f"**{role}:** {message['content']}")

# Add a "Clear Chat" button
if st.button("Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful chatbot."}]
    st.rerun()


