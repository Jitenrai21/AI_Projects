from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Set up Streamlit page
st.set_page_config(page_title='Character-based Chatbot', layout='centered')
st.header('Character-based Chatbot')

# Persona options
persona_options = {
    "Isaac Newton": "Mathematician and physicist",
    "Marie Curie": "Pioneering scientist in radioactivity",
    "William Shakespeare": "English playwright and poet",
    "Adam Smith": "Father of modern economics",
    "Alan Turing": "Father of computer science"
}

# Initialize session state variables
if 'persona' not in st.session_state:
    st.session_state['persona'] = "Isaac Newton"  # default

if 'last_persona' not in st.session_state:
    st.session_state['last_persona'] = st.session_state['persona']

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'gemini_chat_session' not in st.session_state:
    st.session_state['gemini_chat_session'] = model.start_chat(history=[])

# Step 1: Choose a Persona
selected_persona = st.selectbox("Choose a character to chat with:", list(persona_options.keys()))

# Handle persona switching: reset if changed
if selected_persona != st.session_state['last_persona']:
    st.session_state['persona'] = selected_persona
    st.session_state['last_persona'] = selected_persona
    st.session_state['chat_history'] = []
    st.session_state['gemini_chat_session'] = model.start_chat(history=[])
    st.success(f"Switched to {selected_persona}. Starting a new conversation.")

# Function to generate response
def get_gemini_response(user_message):
    try:
        persona_instruction = (
            f"You are {st.session_state['persona']}, a {persona_options[st.session_state['persona']]}. "
            f"Please respond in their style and voice, as if you are them."
        )
        full_prompt = persona_instruction + "\n\nUser: " + user_message

        response = st.session_state['gemini_chat_session'].send_message(full_prompt, stream=True)
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

if not st.session_state['chat_history']:
    st.markdown(f"*Start your conversation with {st.session_state['persona']}!*")

# Input + Submit using a form
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input('Enter your message:', key='user_message_input')
    submit_button = st.form_submit_button('Ask')

# Handle input
if submit_button and user_input.strip():
    st.session_state['chat_history'].append(('You', user_input.strip()))
    with st.spinner("Thinking..."):
        response_chunks = get_gemini_response(user_input.strip())
        if response_chunks:
            full_response = ""
            response_placeholder = st.empty()
            for chunk in response_chunks:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            st.session_state['chat_history'].append(('Bot', full_response))

    st.rerun()

# Display chat history
st.subheader('Chat History:')
for role, text in reversed(st.session_state['chat_history']):
    if role == 'You':
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**{st.session_state['persona']}:** {text}")
