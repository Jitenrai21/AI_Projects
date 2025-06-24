from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize the Gemini model and chat history
model = genai.GenerativeModel('gemini-1.5-flash')

# Set up Streamlit page
st.set_page_config(page_title='Gemini API-based chatbot', layout='centered')
st.header('Gemini API-based chatbot')

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize a key for the text input to allow clearing it
if 'current_input' not in st.session_state:
    st.session_state['current_input'] = ""

def get_gemini_response(question):
    try:
        if 'gemini_chat_session' not in st.session_state:
            st.session_state['gemini_chat_session'] = model.start_chat(history=[]) # model.start_chat() -> (Gemini’s chat session object)

        response = st.session_state['gemini_chat_session'].send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Display chat history
st.subheader('Chat History:')
# Using markdown for better formatting of chat messages
for role, text in st.session_state['chat_history']:
    if role == 'You':
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Bot:** {text}")

# Input field and submit button
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input('Enter your message:', key='user_message_input',
                                value=st.session_state['current_input'])
with col2:
    # Add a bit of space for alignment if needed
    st.write("") # Placeholder for vertical alignment
    submit_button = st.button('Ask', key='ask_button')

# Handle input submission
if submit_button and user_input:
    # Clear the input field immediately
    st.session_state['current_input'] = ""
    st.session_state['chat_history'].append(('You', user_input))

    with st.spinner("Thinking..."):
        response_chunks = get_gemini_response(user_input)
        if response_chunks:
            full_response = ""
            # Display response as it streams
            st.subheader('Response:')
            response_placeholder = st.empty() # Placeholder to update streamed response
            for chunk in response_chunks:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌") # Add a blinking cursor effect
            response_placeholder.markdown(full_response) # Final display without cursor

            st.session_state['chat_history'].append(('Bot', full_response))
            # Rerun to update chat history display
            st.rerun()

elif user_input and st.session_state['current_input'] != user_input:
    st.session_state['current_input'] = user_input