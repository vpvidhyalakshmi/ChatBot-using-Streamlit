import streamlit as st
import random
import time
from streamlit_pills import pills

st.title("Simple Bot")

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, this chatbot is under development",
            "Sorry, I don't have information on that",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from the session history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Setting up pills
st.session_state.pills_index = None
suggested_prompt = None

st.session_state.suggestions_list = ["What is Streamlit?",
                    "How does this chat work?",
                    "Who is Adam Smith?",
                    "What is the most famous quotes by Adam Smith"]

st.session_state.icon = ["📚", "🤔", "👨","❓"]
# source: https://emojipedia.org/light-bulb

# Flag to determine if selectbox should be shown
show_selectbox = st.checkbox("Show prompt suggestions")

# Suggestions with a selection box
if show_selectbox:
    # Display suggestions as a pills
    suggested_prompt = pills(
            "Choose a question to get started or write your own below.",
            st.session_state.suggestions_list,
            st.session_state.icon,
            index = st.session_state.pills_index
        )
    
# Accept to user input
if prompt := st.chat_input("What is up?") or suggested_prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

