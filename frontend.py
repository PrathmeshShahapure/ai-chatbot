import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage


if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

# prev messages
for message in st.session_state['message_history']:
   with st.chat_message(message['role']):
        st.text(message['content'])


user_input=st.chat_input('Type Here')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("human"):
        st.text(f"{user_input} ")

    thread_id='1'
    CONFIG={'configurable':{'thread_id':thread_id}}

    with st.chat_message("ai"):
        ai_message= st.write_stream( message_chuck.content for message_chuck,metadata in chatbot.stream({"messages": [HumanMessage(content=user_input)]},config=CONFIG,stream_mode="messages" ) )

    st.session_state['message_history'].append({'role':'ai','content':ai_message})


      
