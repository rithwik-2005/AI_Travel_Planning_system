import operator
from typing import TypedDict,Annotated,List,Dict,Any
from langchain_core.messages import AnyMessage


#state
class TravelState(TypedDict):
    """Shared state across all travel agent."""
    messages:Annotated[List[AnyMessage],operator.add] #conversational history
    user_query:str  #user request
    flight_results:List[Dict[str,Any]] #structured flight data
    hotel_results:List[Dict[str,Any]]  #structured hotel data
    itinerary:str  # final detailed plan for the journey
    final_response:str #final response
    llm_calls:int  # no of llm call's

