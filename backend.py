from langgraph.graph import StateGraph,END,START
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

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


checkpointer=MemorySaver()

graph=StateGraph(ChatState)
graph.add_node('chatnode',chatnode)

graph.add_edge(START,'chatnode')
graph.add_edge('chatnode',END)

chatbot=graph.compile(checkpointer=checkpointer)
