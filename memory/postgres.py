import os
import psycopg
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

#environment loding
load_dotenv()

#data base url
DATABASE_URL=os.getenv("DATABASE_URL")

#postgres checkpointer
def get_checkpointer():
    """Create PostSQL checkpointer for Langgraph Persistence."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL missing in .env file")
    try:
        conn=psycopg.connect(DATABASE_URL,autocommit=True)
        checkpointer=(PostgresSaver(conn=conn))
        checkpointer.setup()
        return checkpointer
    except Exception as e:
        raise e