from langchain_core.messages import AIMessage
from models.state import TravelState
from tools.flight_tool import search_flight

#flight agent
def flight_agent(state:TravelState):
    """ Fetch flight inforamtion for the users travel query."""
    user_query=state['user_query']
    try:
        flight_results=(search_flight.invoke({"query":user_query}))
        if(flight_results and isinstance(flight_results,list) and "error" in flight_results[0]):
            error_msg=(flight_results[0]["error"])
            return {"flight_results":[],
                    "messages":[AIMessage(content=f"Flight search failed:{error_msg}")]}
        return {"flight_results":flight_results,
                "messages":[AIMessage(content="Successufully retrived flight information.")]}
    except Exception as e:
        return {"flight_results":[],
                "messages":[AIMessage(content="Unable to retrive flight data.")]}
