from langchain_core.messages import AIMessage
from models.state import TravelState
from tools.tavily_tool import tavily_search


#hotel agent

def hotel_agent(state:TravelState):
    """Featch hotel information for the travel request."""
    user_query=state["user_query"]
    search_query=(f"Best hotels accommodation price,location for {user_query}")
    try:
        hotel_results=(tavily_search.invoke({"query":search_query}))
        #handle tool errors
        if(hotel_results and isinstance(hotel_results,list) and "error" in hotel_results[0]):
            error_msg=(hotel_results[0]["error"])
            return {"hotel_results":[],
                    "messages":[
                        AIMessage(
                            content=f"Hotel search failed:{error_msg}"
                        )
                    ]}
        return {
            "hotel_results":hotel_results,
            "messages":[AIMessage(
                content="Successfully retrieved hotel information."
            )]
        }
    except Exception as e:
        return{
            "hotel_results":[],
            "messages":[AIMessage(
                content="Unable to retrieve hotel data."
            )]
        }