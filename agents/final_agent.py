from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_groq import ChatGroq
from models.state import TravelState
import os
from dotenv import load_dotenv

load_dotenv()
#LLM
#llm=ChatGroq(model="lama-3.3-70b-versatile",)
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

#final agent
def final_agent(state:TravelState):
    """Generate polished final travel response."""
    itinerary=state.get("itinerary","")
    flights=state.get("flight_results",[])
    hotels=state.get("hotel_results",[])
    try:
        prompt = f""" 
        Create a polished travel response. 
        Travel Itinerary: 
        {itinerary} 
        Flight Information: 
        {flights} 
        Hotel Information: 
        {hotels} 
        
        Instructions: 
        1. Make response user-friendly. 
        2. Summarize trip clearly. 
        3. Keep recommendations practical. 
        4. Avoid inventing missing details. 
        5. Present in clean sections. 
        
        Output Format: 
        ✈️ Trip Overview 
        🛫 Flight Recommendations 
        🏨 Hotel Recommendations 
        🗓️ Travel Plan 
        💰 Budget Notes 
        ✅ Final Suggestions 
        """
        response=llm.invoke([
            SystemMessage(
                content="You are a helpful AI travel assistant creating polished travel plans."
            ),
            HumanMessage(content=prompt)
        ])
        return {
            "final_response":response.content,
            "messages":[
                AIMessage(
                    content=response.content
                )
            ],
            "llm_calls":state.get("llm_calls",0)+1
        }
    except Exception as e:
        return{
            "final_response":"Unable to generate final response.",
            "messages":[
                AIMessage(content="Failed to generate final travel response.")
            ]
        }
