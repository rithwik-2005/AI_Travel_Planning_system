import os
from typing import List,Dict,Any
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

#loading the environment variables
load_dotenv()
Tavily_api_key=os.getenv("TAVILY_API_KEY")

if not Tavily_api_key:
    raise ValueError(
        "Tavily_api_key missing"
        "from the environment variables."
    )

client=TavilyClient(
    api_key=Tavily_api_key
)

#tool defining
@tool
def tavily_search(query:str)->List[Dict[str,Any]]:
    """ Search the web using tavily for the information. """
    if not query.strip():
        return [{"error":"Query cannot be empty."}]
    try:
        response=client.search(
            query=query,
            max_results=5
        )
        results=[]
        for item in response.get("results",[]):
            content=item.get("content","").strip()
            if(len(content)>300):
                content=(content[:300].rsplit(" ",1)[0]+"...")
            results.append({ "title": item.get( "title", "Unknown" ), 
                            "url": item.get( "url", "" ), 
                            "snippet": content })
        return results
    except Exception as e:
        return [{
            "error":
            "Search failed."
        }]
    
            



