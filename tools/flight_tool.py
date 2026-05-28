import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from typing import List,Dict,Any

#load environment variables
load_dotenv()

#apikey
API_KEY=os.getenv("AVIATIONSTACK_API_KEY")

#Base URL
base_url="https://api.aviationstack.com/v1/flights"

#tool creation using decorator
@tool
def search_flight(query:str)->List[Dict[str,Any]]:
    """ Search for the flight information using AviationStack API 
    based on the query by the user which is in Natural language travel request."""
    if not API_KEY:
        raise ValueError("AVIATIONSTACK_API_KEY not found in the environment variables.")
    params={
        "access_key":API_KEY,
        "limit":5
    }
    try:
        response=requests.get(
            base_url,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        data=response.json()
        flights=[]
        for flight in data.get("data",[])[:5]:
            flights.append({
                "airline":flight.get("airline",{}).get("name","UnKnown"),
                "departure_airport":flight.get("departure",{}).get("airport","UnKnown"),
                "arrival_airport":flight.get("arrival",{}).get("airport","UnKnown"),
                "flight_status":flight.get("flight_status","UnKnown")
            })
        return flights
    
    except requests.exceptions.Timeout:
        return [{"error":"Flight API timed out."}]
    
    except requests.exceptions.RequestException as e:
        return [{"error":"Unable to fetch flights."}]