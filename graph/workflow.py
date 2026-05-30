from langgraph.graph import StateGraph,START,END
from models.state import TravelState
from agents.final_agent import final_agent
from agents.itinerary_agent import itinerary_agent
from agents.hotel_agent import hotel_agent
from agents.flight_agent import flight_agent


#Building of the graph
def build_graph():
    graph=StateGraph(TravelState)
    #adding the nodes
    graph.add_node("flight_agent",flight_agent)
    graph.add_node("hotel_agent",hotel_agent)
    graph.add_node("itinerary_agent",itinerary_agent)
    graph.add_node("final_agent",final_agent)
    
    #parallel execution
    graph.add_edge(START,"flight_agent")
    graph.add_edge(START,"hotel_agent")

    #merge result
    graph.add_edge("flight_agent","itinerary_agent")
    graph.add_edge("hotel_agent","itinerary_agent")

    #final response
    graph.add_edge("itinerary_agent","final_agent")
    graph.add_edge("final_agent",END)
    
    return graph
