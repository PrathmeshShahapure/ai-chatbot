from langgraph.graph import StateGraph,END,START
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

load_dotenv()

model = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.7
)

class ChatState(TypedDict):
  messages:Annotated[list[BaseMessage],add_messages]

def chatnode(state:ChatState):
  response=model.invoke(state['messages'])
  return {'messages':[response]}

conn=sqlite3.connect('chatbot.db',check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatState)
graph.add_node('chatnode',chatnode)

graph.add_edge(START,'chatnode')
graph.add_edge('chatnode',END)

chatbot=graph.compile(checkpointer=checkpointer)

def retrive_all_threads():
  all_threads=set()
  for checkpoint in checkpointer.list(None):
    all_threads.add(checkpoint.config['configurable']['thread_id'])
  return list(all_threads)
