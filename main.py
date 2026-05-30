from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph.workflow import build_graph
from memory.postgres import get_checkpointer
import uuid # to make thread id

#load environments
load_dotenv()

#Building app
graph=build_graph()
checkpointer=get_checkpointer()
app=graph.compile(checkpointer=checkpointer)

#Generate thread id
def generate_thread_id():
    return str(uuid.uuid4())

#Get App
def get_app():
    """ Return compiled Langgraph app."""
    return app

#CLI Runner
def run():
    thread_id=generate_thread_id()
    user_input=input("\nEnter travel request:")
    config={"configurable":{
        "thread_id":thread_id
    }}
    result=app.invoke({
        "messages":[HumanMessage(content=user_input)],
        "user_query":user_input,
        "flight_results":[],
        "hotel_results":[],
        "itinerary":"",
        "final_response":"",
        "llm_calls":0
    },
    config=config)


if __name__=="__main__":
    run()