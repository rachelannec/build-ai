import streamlit as st
# Important: set_page_config must be the first Streamlit command
st.set_page_config(page_title="GameBot - Powered by RAWG & Gemini", page_icon="🎮", layout="wide")

import google.generativeai as genai
import requests
import os
import json
from datetime import datetime
import warnings
from dotenv import load_dotenv
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()
RAWG_API_KEY = os.getenv("RAWG_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API if key is available
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Add custom CSS for gaming-themed chat interface
st.markdown("""
<style>
    /* Gaming-inspired theme */
    @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;700&display=swap');
    
    body {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    .app-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 2px solid #30cfd0;
        margin-bottom: 2rem;
        background: linear-gradient(to right, #121212, #1e3c72, #121212);
        border-radius: 8px;
    }
    
    .app-title {
        font-family: 'Chakra Petch', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #30cfd0, #c43ad6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0px 0px 10px rgba(48, 207, 208, 0.5);
    }
    
    .app-subtitle {
        font-family: 'Chakra Petch', sans-serif;
        font-size: 1.2rem;
        color: #B0B0B0;
    }
    
    /* Chat container styling */
    # .chat-container {
    #     margin: 0 auto;
    #     padding: 1rem;
    #     background-color: rgba(30, 30, 30, 0.7);
    #     border-radius: 8px;
    #     border: 1px solid #30cfd0;
    #     box-shadow: 0 0 15px rgba(48, 207, 208, 0.2);
    # }
    
    /* Game card styling */
    # .game-card {
    #     background-color: #1E1E1E;
    #     border-radius: 8px;
    #     padding: 15px;
    #     margin-bottom: 15px;
    #     border: 1px solid #333;
    # }
    
    # .game-card:hover {
    #     border-color: #30cfd0;
    #     box-shadow: 0 0 10px rgba(48, 207, 208, 0.3);
    # }
    
    # .game-title {
    #     color: #30cfd0;
    #     font-family: 'Chakra Petch', sans-serif;
    #     font-weight: 700;
    #     margin-bottom: 5px;
    # }
    
    /* Hide Streamlit branding */
    #MainMenu, footer {
        visibility: hidden;
    }
    
    /* Custom button styling */
    .stButton>button {
        background: linear-gradient(to right, #30cfd0, #5b21b6);
        color: white;
        border: none;
        font-family: 'Chakra Petch', sans-serif;
    }
    
    .stButton>button:hover {
        background: linear-gradient(to right, #5b21b6, #30cfd0);
    }
    
    /* Fixed chat container with proper scrolling */
    # .fixed-chat-container {
    #     display: flex;
    #     flex-direction: column;
    #     height: 70vh;
    #     background-color: rgba(30, 30, 30, 0.7);
    #     border-radius: 8px;
    #     border: 1px solid #30cfd0;
    #     box-shadow: 0 0 15px rgba(48, 207, 208, 0.2);
    #     position: relative;
    #     overflow: hidden;
    # }
    
    # .messages-container {
    #     flex: 1;
    #     overflow-y: auto;
    #     padding: 1rem;
    #     padding-bottom: 70px; /* Extra space to prevent messages being hidden behind input */
    #     max-height: calc(70vh - 70px);
    #     position: absolute;
    #     top: 0;
    #     left: 0;
    #     right: 0;
    #     bottom: 70px;
    # }
    
    # .input-container {
    #     position: absolute;
    #     bottom: 0;
    #     left: 0;
    #     right: 0;
    #     padding: 10px;
    #     background-color: rgba(30, 30, 30, 0.9);
    #     border-top: 1px solid #30cfd0;
    #     min-height: 60px;
    #     z-index: 10;
    # }
    
    # /* Adjust Streamlit's default styles */
    # .stChatInput {
    #     background-color: transparent !important;
    # }
    
    # /* Ensure chat messages appear above the container */
    # .stChatMessage {
    #     z-index: 5;
    # }
    
    /* Auto-scroll script */
    iframe[height="0"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# RAWG API Functions
def search_games(query, page_size=5):
    """Search for games on RAWG API"""
    if not RAWG_API_KEY:
        return {"error": "RAWG API Key not found"}
    
    try:
        url = f"https://api.rawg.io/api/games"
        params = {
            "key": RAWG_API_KEY,
            "search": query,
            "page_size": page_size
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_game_details(game_id):
    """Get detailed information about a specific game"""
    if not RAWG_API_KEY:
        return {"error": "RAWG API Key not found"}
    
    try:
        url = f"https://api.rawg.io/api/games/{game_id}"
        params = {"key": RAWG_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_game_screenshots(game_id, count=4):
    """Get screenshots for a specific game"""
    if not RAWG_API_KEY:
        return {"error": "RAWG API Key not found"}
    
    try:
        url = f"https://api.rawg.io/api/games/{game_id}/screenshots"
        params = {
            "key": RAWG_API_KEY,
            "page_size": count
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None

if 'last_search_results' not in st.session_state:
    st.session_state.last_search_results = None

# Configure Gemini model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.85,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# System prompt for gaming assistant
GAMING_PROMPT = """You are GameBot, a knowledgeable video game expert assistant.
You can provide information about games, gaming platforms, developers, game mechanics, 
reviews, gaming history, and recommendations.
When users ask about specific games, you can provide insights about gameplay, story, 
release dates, platforms, and similar games they might enjoy.
Be enthusiastic and friendly in your responses, and use gaming terminology appropriately.
If the user asks a question that might require looking up specific game details via the RAWG API,
suggest they use the /game command followed by the game title to search the database."""

# App Header
st.markdown('<div class="app-header">', unsafe_allow_html=True)
st.markdown('<p class="app-title">GameBot</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Your Ultimate Gaming Assistant</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main layout with columns
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### API Status")
    
    if not RAWG_API_KEY:
        st.warning("⚠️ RAWG API key not found in environment variables. Game search features will be limited.")
        rawg_api_key = st.text_input('Enter RAWG API key (optional):', type='password')
        if rawg_api_key:
            # Use the provided key temporarily
            RAWG_API_KEY = rawg_api_key
    else:
        st.success("✅ RAWG API key loaded")
    
    if not GEMINI_API_KEY:
        st.warning("⚠️ Gemini API key not found in environment variables. Chat features will be limited.")
    else:
        st.success("✅ Gemini API key loaded")
        
        # Initialize Gemini model if not already done
        if 'chat_session' not in st.session_state or st.session_state.chat_session is None:
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash",
                    generation_config=generation_config,
                )
                
                st.session_state.chat_session = model.start_chat(history=[])
                welcome_message = "Hello gamer! I'm GameBot, your gaming assistant. I can help with game recommendations, information about specific titles, platforms, and more. Try asking me about games or use /game followed by a title to search the RAWG database! 🎮"
                st.session_state.messages.append({"role": "assistant", "content": welcome_message})
                
            except Exception as e:
                st.error(f"Gemini API error: {e}", icon="🚨")
    
    # Game search box
    st.markdown("### Quick Game Search")
    game_search = st.text_input("Search for a game:", placeholder="e.g., The Witcher 3")
    if st.button("Search") and game_search:
        with st.spinner("Searching games..."):
            results = search_games(game_search)
            if "error" in results:
                st.error(f"Error searching games: {results['error']}")
            elif results.get("results"):
                st.session_state.last_search_results = results["results"]
                st.success(f"Found {len(results['results'])} games")
            else:
                st.warning("No games found")
    
    # Display search results
    if st.session_state.last_search_results:
        st.markdown("### Search Results")
        for game in st.session_state.last_search_results:
            with st.container():
                st.markdown(f"""<div class="game-card">
                    <p class="game-title">{game['name']}</p>
                    <p>Released: {game.get('released', 'Unknown')}</p>
                    <p>Rating: {game.get('rating', 'N/A')}/5</p>
                    </div>""", unsafe_allow_html=True)
                
                if st.button(f"Details: {game['name']}", key=f"btn_{game['id']}"):
                    game_details = get_game_details(game['id'])
                    screenshots = get_game_screenshots(game['id'])
                    
                    if "error" not in game_details:
                        # Create a nice summary of the game to add to chat
                        platforms = ", ".join([p['platform']['name'] for p in game_details.get('platforms', [])])
                        genres = ", ".join([g['name'] for g in game_details.get('genres', [])])
                        
                        game_info = f"""
                        ## {game_details['name']}
                        
                        ![Game Image]({game_details.get('background_image', '')})
                        
                        **Released:** {game_details.get('released', 'Unknown')}
                        **Rating:** {game_details.get('rating', 'N/A')}/5
                        **Platforms:** {platforms}
                        **Genres:** {genres}
                        
                        {game_details.get('description_raw', 'No description available.')}
                        
                        **Website:** [{game_details.get('website', 'N/A')}]({game_details.get('website', '#')})
                        """
                        
                        # Add message to chat
                        st.session_state.messages.append({"role": "assistant", "content": game_info})
    
    # Example prompts
    st.markdown("### Try asking about:")
    example_questions = [
        "What are the best RPGs of all time?",
        "Recommend games similar to Skyrim",
        "What's the history of the Final Fantasy series?",
        "Which games have the best storylines?",
        "/game Elden Ring"
    ]
    
    for q in example_questions:
        if st.button(q, key=f"prompt_{q}"):
            # Add to chat
            st.session_state.messages.append({"role": "user", "content": q})

with col1:
    # Add CSS for fixed chat container with bottom input
    st.markdown("""
    <style>
        /* Fixed chat container with proper scrolling */
        # .fixed-chat-container {
        #     display: flex;
        #     flex-direction: column;
        #     height: 70vh;
        #     background-color: rgba(30, 30, 30, 0.7);
        #     border-radius: 8px;
        #     border: 1px solid #30cfd0;
        #     box-shadow: 0 0 15px rgba(48, 207, 208, 0.2);
        #     position: relative;
        #     overflow: hidden;
        # }
        
        # .messages-container {
        #     flex: 1;
        #     overflow-y: auto;
        #     padding: 1rem;
        #     padding-bottom: 70px; /* Extra space to prevent messages being hidden behind input */
        #     max-height: calc(70vh - 70px);
        #     position: absolute;
        #     top: 0;
        #     left: 0;
        #     right: 0;
        #     bottom: 70px;
        # }
        
        # .input-container {
        #     position: absolute;
        #     bottom: 0;
        #     left: 0;
        #     right: 0;
        #     padding: 10px;
        #     background-color: rgba(30, 30, 30, 0.9);
        #     border-top: 1px solid #30cfd0;
        #     min-height: 60px;
        #     z-index: 10;
        # }
        
        # /* Adjust Streamlit's default styles */
        # .stChatInput {
        #     background-color: transparent !important;
        # }
        
        /* Ensure chat messages appear above the container */
        .stChatMessage {
            z-index: 5;
        }
        
        /* Auto-scroll script */
        iframe[height="0"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create container for the entire chat interface
    chat_container = st.container()
    
    # Use columns to structure the input at the bottom
    with chat_container:
        # Main chat interface
        st.markdown('<div class="fixed-chat-container">', unsafe_allow_html=True)
        
        # Create a container for scrollable messages
        with st.container():
            st.markdown('<div class="messages-container">', unsafe_allow_html=True)
            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Process special commands function definition
        def process_game_commands(user_message):
            """Process special game-related commands"""
            
            if user_message.startswith("/game "):
                game_query = user_message.replace("/game ", "").strip()
                results = search_games(game_query)
                
                if "error" in results:
                    return f"Couldn't search for games: {results['error']}"
                
                if not results.get("results"):
                    return f"No games found matching '{game_query}'. Try a different search term."
                
                # Get the top result
                top_game = results["results"][0]
                game_id = top_game["id"]
                
                # Get detailed info and screenshots
                game_details = get_game_details(game_id)
                screenshots = get_game_screenshots(game_id)
                
                if "error" in game_details:
                    return f"Found game but couldn't get details: {game_details['error']}"
                
                # Format the response
                platforms = ", ".join([p['platform']['name'] for p in game_details.get('platforms', [])])
                genres = ", ".join([g['name'] for g in game_details.get('genres', [])])
                
                response = f"""
                ## {game_details['name']}
                
                ![Game Image]({game_details.get('background_image', '')})
                
                **Released:** {game_details.get('released', 'Unknown')}
                **Rating:** {game_details.get('rating', 'N/A')}/5
                **Platforms:** {platforms}
                **Genres:** {genres}
                
                {game_details.get('description_raw', 'No description available.')}
                
                **Website:** [{game_details.get('website', 'N/A')}]({game_details.get('website', '#')})
                """
                
                return response
            
            return None
        
        # Chat input - positioned at the bottom
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        if user_message := st.chat_input("Ask about games or use /game [title] to search..."):
            if not GEMINI_API_KEY:
                st.info("Please add your Gemini API key to the .env file.")
            else:
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": user_message})
                with st.chat_message("user"):
                    st.markdown(user_message)
                
                # Check for special commands
                command_response = process_game_commands(user_message)
                
                if command_response:
                    # It's a special command, display the response
                    with st.chat_message("assistant"):
                        st.markdown(command_response)
                    st.session_state.messages.append({"role": "assistant", "content": command_response})
                elif st.session_state.chat_session:
                    # Regular chat message, send to Gemini
                    with st.spinner("Thinking..."):
                        try:
                            response = st.session_state.chat_session.send_message(user_message)
                            with st.chat_message("assistant"):
                                st.markdown(response.text)
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        except Exception as e:
                            st.error(f"Error getting response: {e}")
                            st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I encountered an error: {e}"})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
