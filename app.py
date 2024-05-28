import streamlit as st
from main import datachat as dc

chat_object= dc()


st.title(":blue[ Chat with your Data]")

col1, col2, col3 = st.columns(3)
with col2:
    st.image("")

with col3:
    st.subheader("powered by GenAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == 'user':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if message["role"] == 'assistant':
        with st.chat_message(message["role"]):
            st.dataframe(message["content"],hide_index=True)


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response, x_a, y_a  = chat_object.data_ops(prompt)
    print(' Axis ', x_a, y_a)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        #st.markdown(response)
        st.dataframe(response,hide_index=True)
        cols = []
import streamlit as st
from main import datachat as dc


chat_object= dc()

#conn=st.button('connect')
#if conn:
#    chat_object.vectorize()

st.title(":blue[Talk to UR Database]")

col1, col2, col3 = st.columns(3)
with col2:
    st.image("")

with col3:
    st.subheader("Driven by GenAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == 'user':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if message["role"] == 'assistant':
        with st.chat_message(message["role"]):
            st.dataframe(message["content"],hide_index=True)


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response, x_a, y_a  = chat_object.data_ops(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        #st.markdown(response)
        st.dataframe(response,hide_index=True)
        cols = []
                                    
