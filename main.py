import os
from typing import TypedDict,Annotated
import operator
import psycopg
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage, # it is generally used for the typing
    BaseMessage, # it is the parent class for all the messages
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain_groq import ChatGroq
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv
load_dotenv()


