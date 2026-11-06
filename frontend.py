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
   st.session_state['message_history'].append({'role':'ai','content':user_input})
   response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]},config=CONFIG)

   with st.chat_message("ai"):
        st.text(response["messages"][-1].content)


      
