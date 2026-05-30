# streamlit_app.py
import os
import json
import uuid
from datetime import datetime

import streamlit as st
from langchain_core.messages import (
    HumanMessage
)

from main import get_app


# ==========================================================
# APP CONFIG
# ==========================================================
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)


# ==========================================================
# CONSTANTS
# ==========================================================
CHAT_HISTORY_FILE = (
    "travel_chats.json"
)

app = get_app()


# ==========================================================
# CHAT PERSISTENCE
# ==========================================================
def load_chats():

    if not os.path.exists(
        CHAT_HISTORY_FILE
    ):
        return []

    try:

        with open(
            CHAT_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:
        return []


def save_chats(chats):

    with open(
        CHAT_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chats,
            f,
            indent=4
        )


# ==========================================================
# SESSION STATE
# ==========================================================
if "thread_id" not in (
    st.session_state
):
    st.session_state[
        "thread_id"
    ] = str(uuid.uuid4())


if "chat_title" not in (
    st.session_state
):
    st.session_state[
        "chat_title"
    ] = "New Travel Chat"


if "final_response" not in (
    st.session_state
):
    st.session_state[
        "final_response"
    ] = ""


if "chat_history" not in (
    st.session_state
):
    st.session_state[
        "chat_history"
    ] = load_chats()


if "active_chat" not in (
    st.session_state
):
    st.session_state[
        "active_chat"
    ] = None


# ==========================================================
# CREATE NEW CHAT
# ==========================================================
def create_new_chat():

    st.session_state[
        "thread_id"
    ] = str(uuid.uuid4())

    st.session_state[
        "chat_title"
    ] = "New Travel Chat"

    st.session_state[
        "final_response"
    ] = ""

    st.session_state[
        "active_chat"
    ] = None


# ==========================================================
# SAVE CHAT
# ==========================================================
def persist_chat(
    query,
    response
):

    chats = load_chats()

    existing_index = None

    for idx, chat in enumerate(
        chats
    ):

        if (
            chat["thread_id"]
            ==
            st.session_state[
                "thread_id"
            ]
        ):
            existing_index = idx
            break

    chat_data = {

        "thread_id":
        st.session_state[
            "thread_id"
        ],

        "title":
        st.session_state[
            "chat_title"
        ],

        "query":
        query,

        "response":
        response,

        "updated_at":
        datetime.now()
        .strftime(
            "%Y-%m-%d %H:%M"
        )
    }

    if (
        existing_index
        is not None
    ):

        chats[
            existing_index
        ] = chat_data

    else:

        chats.insert(
            0,
            chat_data
        )

    save_chats(chats)

    st.session_state[
        "chat_history"
    ] = chats


# ==========================================================
# LOAD CHAT
# ==========================================================
def load_chat(chat):

    st.session_state[
        "thread_id"
    ] = chat[
        "thread_id"
    ]

    st.session_state[
        "chat_title"
    ] = chat[
        "title"
    ]

    st.session_state[
        "final_response"
    ] = chat[
        "response"
    ]

    st.session_state[
        "active_chat"
    ] = chat[
        "thread_id"
    ]

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #080d14;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #090e18 !important;
    border-right: 1px solid #162338;
}

.sidebar-title {
    color: #e0edf8;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
}

.chat-item {
    background: #0e1a2b;
    border: 1px solid #1a2e44;
    border-radius: 12px;
    padding: 0.8rem;
    margin-bottom: 0.5rem;
}

.chat-meta {
    color: #7aa8cc;
    font-size: 0.72rem;
}

.hero-wrapper {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    height: 280px;
    margin-bottom: 2rem;
}

.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.35);
}

.hero-content {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
    text-align: center;
    padding: 2rem;
}

.hero-badge {
    background: rgba(58,123,213,0.2);
    border: 1px solid rgba(58,123,213,0.4);
    color: #7ab8f5;
    border-radius: 999px;
    padding: 0.4rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.hero-title {
    color: white;
    font-size: 2.8rem;
    font-weight: 700;
}

.hero-sub {
    color: #9ab6d4;
    font-size: 1rem;
    max-width: 600px;
}

.stTextArea textarea {
    background: #0e1623 !important;
    border: 1px solid #1e2e44 !important;
    border-radius: 16px !important;
    color: #e0edf8 !important;
}

.stTextArea textarea::placeholder {
    color: #4a6a85 !important;
}

div[data-testid="stButton"] > button {
    border-radius: 14px !important;
    border: none !important;
    background: linear-gradient(
        135deg,
        #1a6bbf,
        #0d4a8a
    ) !important;
    color: white !important;
    font-weight: 700 !important;
}

.final-card {
    background: linear-gradient(
        160deg,
        #0c1a2e,
        #0a1520
    );
    border: 1px solid #1e3a5c;
    border-left: 5px solid #3a7bd5;
    border-radius: 18px;
    padding: 2rem;
    color: #dcecff;
    line-height: 1.8;
    margin-top: 1rem;
}

.metric-box {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
}

.metric-value {
    font-size: 1.8rem;
    color: #4ea8f0;
    font-weight: 700;
}

.metric-label {
    color: #7aa8cc;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================
with st.sidebar:

    st.markdown(
        """
        <div class='sidebar-title'>
        🌍 AI Travel Planner
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):
        create_new_chat()
        st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div class='sidebar-title'>
        💬 Travel Chats
        </div>
        """,
        unsafe_allow_html=True
    )

    chats = (
        st.session_state[
            "chat_history"
        ]
    )

    if not chats:
        st.caption(
            "No chats yet"
        )

    for idx, chat in enumerate(
        chats
    ):

        title = chat.get(
            "title",
            "Travel Chat"
        )

        updated = chat.get(
            "updated_at",
            ""
        )

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:
            if st.button(
                f"💬 {title}",
                key=
                f"chat_{idx}",
                use_container_width=True
            ):
                load_chat(chat)
                st.rerun()

        with col2:
            if st.button(
                "🗑️",
                key=
                f"delete_{idx}"
            ):

                chats.pop(idx)

                save_chats(
                    chats
                )

                st.session_state[
                    "chat_history"
                ] = chats

                st.rerun()

        st.caption(updated)

    st.markdown("---")

    st.markdown(
        """
        ### Powered By
        - 🔗 LangGraph
        - 🧠 Groq LLaMA 3.3
        - 🐘 PostgreSQL
        - 🔍 Tavily
        - ✈️ AviationStack
        """
    )


# ==========================================================
# HERO
# ==========================================================
st.markdown("""
<div class="hero-wrapper">
    <img class="hero-bg"
    src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1600&q=80">

    <div class="hero-content">

        <div class="hero-badge">
        ✦ Multi-Agent Travel Planner
        </div>

        <div class="hero-title">
        ✈️ AI Travel Booking System
        </div>

        <div class="hero-sub">
        Plan flights, hotels and
        itineraries with an
        intelligent multi-agent
        AI system.
        </div>

    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# DESTINATIONS
# ==========================================================
DESTINATIONS = [
    ("🇯🇵 Tokyo",
     "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),

    ("🇫🇷 Paris",
     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),

    ("🇹🇭 Bangkok",
     "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),

    ("🇦🇪 Dubai",
     "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

cols = st.columns(4)

for col, (
    city,
    image_url
) in zip(
    cols,
    DESTINATIONS
):

    with col:

        st.markdown(
            f"""
            <div style="
                border-radius:16px;
                overflow:hidden;
                position:relative;
                height:120px;
            ">
                <img
                src="{image_url}"
                style="
                    width:100%;
                    height:100%;
                    object-fit:cover;
                    filter:brightness(0.6);
                ">

                <div style="
                    position:absolute;
                    bottom:12px;
                    left:0;
                    right:0;
                    text-align:center;
                    color:white;
                    font-weight:700;
                ">
                {city}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# USER INPUT
# ==========================================================
st.markdown(
    "### 🗺️ Describe Your Trip"
)

QUICK_TRIPS = [
    "7-day Japan trip under ₹2L",
    "Dubai luxury weekend",
    "Paris honeymoon trip",
    "Bali backpacking 10 days"
]

quick_fill = ""

qcols = st.columns(
    len(QUICK_TRIPS)
)

for col, trip in zip(
    qcols,
    QUICK_TRIPS
):
    with col:
        if st.button(
            trip,
            key=f"trip_{trip}"
        ):
            quick_fill = trip


user_query = st.text_area(
    label="Travel request",
    value=quick_fill,
    placeholder="Plan a luxury 7-day Japan trip under ₹2 lakhs...",
    height=120,
    label_visibility="collapsed"
)


generate = st.button(
    "🚀 Generate Travel Plan",
    use_container_width=True
)


# ==========================================================
# AGENT META
# ==========================================================
AGENT_META = {

    "flight_agent": (
        "✈️",
        "Flight Agent"
    ),

    "hotel_agent": (
        "🏨",
        "Hotel Agent"
    ),

    "itinerary_agent": (
        "🗓️",
        "Itinerary Agent"
    ),

    "final_agent": (
        "🧠",
        "Final Agent"
    )
}


# ==========================================================
# GENERATE
# ==========================================================
if generate:

    if not (
        user_query.strip()
    ):
        st.warning(
            "Please describe "
            "your trip."
        )

    else:

        # ------------------
        # Chat title
        # ------------------
        if (
            st.session_state[
                "chat_title"
            ]
            ==
            "New Travel Chat"
        ):

            title = (
                user_query[:40]
            )

            if (
                len(user_query)
                > 40
            ):
                title += "..."

            st.session_state[
                "chat_title"
            ] = title

        # ------------------
        # Config
        # ------------------
        config = {
            "configurable": {
                "thread_id":
                st.session_state[
                    "thread_id"
                ]
            }
        }

        collected = {

            "flight_results":
                "",

            "hotel_results":
                "",

            "itinerary":
                "",

            "final_response":
                "",

            "llm_calls":
                0
        }

        st.markdown("---")

        st.markdown(
            """
            ## 🤖 Agent Pipeline
            """
        )

        # ------------------
        # Stream graph
        # ------------------
        try:

            for chunk in app.stream(
                {
                    "messages": [
                        HumanMessage(
                            content=
                            user_query
                        )
                    ],

                    "user_query":
                        user_query,

                    "flight_results":
                        [],

                    "hotel_results":
                        [],

                    "itinerary":
                        "",

                    "final_response":
                        "",

                    "llm_calls":
                        0
                },

                config=config,

                stream_mode=
                "updates"
            ):

                for (
                    node_name,
                    state_update
                ) in chunk.items():

                    icon, label = (
                        AGENT_META
                        .get(
                            node_name,
                            (
                                "⚙️",
                                node_name
                            )
                        )
                    )

                    with st.status(
                        f"{icon} "
                        f"{label}",
                        expanded=True
                    ):

                        # ------------------
                        # Flight Agent
                        # ------------------
                        if (
                            node_name
                            ==
                            "flight_agent"
                        ):

                            flights = (
                                state_update
                                .get(
                                    "flight_results",
                                    []
                                )
                            )

                            collected[
                                "flight_results"
                            ] = (
                                flights
                            )

                            if flights:

                                for flight in (
                                    flights
                                ):

                                    st.markdown(
                                        f"""
**Airline**
{flight.get(
'airline',
'Unknown'
)}

**Departure**
{flight.get(
'departure_airport',
'Unknown'
)}

**Arrival**
{flight.get(
'arrival_airport',
'Unknown'
)}

**Status**
{flight.get(
'flight_status',
'Unknown'
)}
"""
                                    )

                            else:
                                st.info(
                                    "No flights found."
                                )

                        # ------------------
                        # Hotel Agent
                        # ------------------
                        elif (
                            node_name
                            ==
                            "hotel_agent"
                        ):

                            hotels = (
                                state_update
                                .get(
                                    "hotel_results",
                                    []
                                )
                            )

                            collected[
                                "hotel_results"
                            ] = hotels

                            if hotels:

                                for hotel in hotels:

                                    st.markdown(
                                        f"""
### {
hotel.get(
'title',
'Unknown'
)}

{hotel.get(
'snippet',
''
)}

🔗 {
hotel.get(
'url',
''
)}
"""
                                    )

                            else:
                                st.info(
                                    "No hotels found."
                                )

                        # ------------------
                        # Itinerary Agent
                        # ------------------
                        elif (
                            node_name
                            ==
                            "itinerary_agent"
                        ):

                            itinerary = (
                                state_update
                                .get(
                                    "itinerary",
                                    ""
                                )
                            )

                            collected[
                                "itinerary"
                            ] = (
                                itinerary
                            )

                            st.markdown(
                                itinerary
                            )

                        # ------------------
                        # Final Agent
                        # ------------------
                        elif (
                            node_name
                            ==
                            "final_agent"
                        ):

                            final = (
                                state_update
                                .get(
                                    "final_response",
                                    ""
                                )
                            )

                            collected[
                                "final_response"
                            ] = (
                                final
                            )

                            st.success(
                                "Travel plan generated!"
                            )

                            st.markdown(
                                final
                            )

                        collected[
                            "llm_calls"
                        ] = (
                            state_update
                            .get(
                                "llm_calls",
                                collected[
                                    "llm_calls"
                                ]
                            )
                        )

        except Exception as e:

            st.error(
                f"Something "
                f"went wrong: "
                f"{e}"
            )

        # ------------------
        # Save final response
        # ------------------
        st.session_state[
            "final_response"
        ] = (
            collected[
                "final_response"
            ]
        )

        persist_chat(
            user_query,
            collected[
                "final_response"
            ]
        )

        # ------------------
        # Metrics
        # ------------------
        st.markdown("---")

        m1, m2, m3 = (
            st.columns(3)
        )

        with m1:
            st.markdown(
                """
<div class='metric-box'>
<div class='metric-value'>
4
</div>
<div class='metric-label'>
Agents Run
</div>
</div>
""",
                unsafe_allow_html=True
            )

        with m2:
            st.markdown(
                f"""
<div class='metric-box'>
<div class='metric-value'>
{
collected[
'llm_calls'
]
}
</div>
<div class='metric-label'>
LLM Calls
</div>
</div>
""",
                unsafe_allow_html=True
            )

        with m3:
            st.markdown(
                """
<div class='metric-box'>
<div class='metric-value'>
✅
</div>
<div class='metric-label'>
Completed
</div>
</div>
""",
                unsafe_allow_html=True
            )


# ==========================================================
# SHOW EXISTING CHAT
# ==========================================================
if (
    st.session_state[
        "final_response"
    ]
    and not generate
):

    st.markdown("---")

    st.markdown(
        """
        ## 🧠 Saved Travel Plan
        """
    )

    st.markdown(
        f"""
        <div class='final-card'>
        {
        st.session_state[
            "final_response"
        ]
        }
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# DOWNLOAD + SAVE
# ==========================================================
if (
    st.session_state[
        "final_response"
    ]
):

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    filename = (
        f"travel_plan_"
        f"{timestamp}.md"
    )

    save_dir = (
        "travel_plans"
    )

    os.makedirs(
        save_dir,
        exist_ok=True
    )

    file_content = f"""
# Travel Plan

## Chat
{st.session_state['chat_title']}

## Generated
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Final Travel Plan

{st.session_state['final_response']}
"""

    # Save markdown file
    with open(
        os.path.join(
            save_dir,
            filename
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            file_content
        )

    st.markdown("---")

    col1, col2 = (
        st.columns(
            [1, 3]
        )
    )

    with col1:

        st.download_button(
            label=
            "⬇ Download Plan",

            data=
            file_content,

            file_name=
            filename,

            mime=
            "text/markdown",

            use_container_width=
            True
        )

    with col2:

        st.success(
            f"Auto-saved → "
            f"{save_dir}/"
            f"{filename}"
        )


# ==========================================================
# FOOTER
# ==========================================================
st.markdown("---")

st.caption(
    "✈️ AI Travel Planner "
    "• Powered by "
    "LangGraph + Groq "
    "• Multi-Agent System"
)


