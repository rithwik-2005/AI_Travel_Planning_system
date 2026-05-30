from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_groq import ChatGroq
from models.state import TravelState
import os
from dotenv import load_dotenv

load_dotenv()

#llm is defining
#llm=ChatGroq(model="llama-3.3-70b-versatile")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
#itinerary agent
def itinerary_agent(state:TravelState):
    """generate an intelligent travel itinerary using flight+hotels."""
    user_query=state["user_query"]
    #flights 
    flights=state.get("flight_results",[])
    #hotels
    hotels=state.get("hotel_results",[])
    try:
        prompt = f""" 
        You are a professional AI travel planner. 
        Your task:
        Generate a complete travel itinerary. 
        User Request: 
        {user_query} 
        Flight Information: 
        {flights} 
        Hotel Information: 
        {hotels} Instructions: 
        1. Use available flight and hotel information. 
        2. Recommend practical travel plans. 
        3. Consider budget if mentioned. 
        4. Keep itinerary realistic. 
        5. Avoid hallucinating unavailable details. 
        6. Structure the itinerary day-by-day. 
        Output format: 
        Trip Summary 
        Recommended Flights 
        Recommended Hotels  
        Day-by-Day Plan 
        Estimated Budget 
        """
        response=llm.invoke([
            SystemMessage(
                content=
                "You are an expert travel planning AI."
            ),
            HumanMessage(content=prompt)
        ])
        return{
            "itinerary":response.content,
            "messages":[AIMessage(content="Successfully generated travel itinerary.")],
            "llm_calls":state.get("llm_calls",0)+1
        }
    except Exception as e:
        return{
            "itinerary":"Unable to generate itinerary.",
            "messages":[
                AIMessage(content="failed to generate travel itinerary")
            ]
        }