import streamlit as st
from backend import chatbot,retrive_all_threads
from langchain_core.messages import HumanMessage
import uuid

# utility Functions
def generate_thread_id():
    thread_id=uuid.uuid4()
    return str(thread_id)

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_convo(thread_id):
    state=chatbot.get_state(
        config={'configurable':{'thread_id':thread_id}}
                          )
    return state.values.get('messages', [])


# session setup
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=retrive_all_threads()

add_thread(st.session_state['thread_id'])

# sidebar
st.sidebar.title("LangGraph Chatbot ")

if st.sidebar.button("New Chat "):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(thread_id):
        st.session_state['thread_id']=thread_id
        messages=load_convo(thread_id)

        temp_msg=[]
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else :
                role='ai'
            temp_msg.append({'role':role,'content':message.content})
        st.session_state['message_history']=temp_msg


# prev messages
for message in st.session_state['message_history']:
   with st.chat_message(message['role']):
        st.text(message['content'])


user_input=st.chat_input('Type Here')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("human"):
        st.text(f"{user_input} ")

    CONFIG={'configurable':{'thread_id':st.session_state['thread_id']}}

    with st.chat_message("ai"):
        ai_message= st.write_stream( message_chuck.content for message_chuck,metadata in chatbot.stream({"messages": [HumanMessage(content=user_input)]},config=CONFIG,stream_mode="messages" ) )

    st.session_state['message_history'].append({'role':'ai','content':ai_message})


      
