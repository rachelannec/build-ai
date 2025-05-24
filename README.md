# GameBot - Powered by RAWG & Gemini

GameBot is an interactive chatbot web application built with Streamlit that leverages the Gemini AI API for conversational intelligence and the RAWG Games Database API for real-time video game information. It provides users with game recommendations, details, and general gaming knowledge in a modern chat interface.

## Features

- **Conversational Chatbot**: Chat with an AI assistant about games, platforms, genres, and more.
- **RAWG Game Search**: Search for games using the RAWG API and get detailed information, including release dates, ratings, platforms, genres, and screenshots.
- **/game Command**: Use `/game [title]` in chat to fetch and display detailed information about a specific game.
- **Modern UI**: Clean, scrollable chat interface with the input bar fixed at the bottom.
- **Environment-based API Keys**: Securely load your Gemini and RAWG API keys from a `.env` file.

## Setup Instructions

1. **Clone the Repository**

```powershell
git clone <repo-url>
cd GEN-AI-PH-WORKSHOP-2-main
```

2. **Install Dependencies**

```powershell
pip install -r requirements.txt
```

3. **Configure API Keys**

Create a `.env` file in the project root with the following content:

```
RAWG_API_KEY=your_rawg_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

- Get your RAWG API key from [RAWG.io](https://rawg.io/apidocs)
- Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

4. **Run the App**

```powershell
streamlit run app.py
```

## Usage

- **Chat**: Type your questions or requests in the input bar at the bottom. The assistant can answer general gaming questions, recommend games, and more.
- **Game Search**: Use the sidebar to search for games by title. Click on a result to see more details.
- **/game Command**: In the chat, type `/game [title]` (e.g., `/game Elden Ring`) to fetch detailed info about a specific game.

## File Structure

- `app.py` - Main Streamlit application file.
- `requirements.txt` - Python dependencies.
- `utils.py` - Utility functions (if present).
- `.env` - Environment variables for API keys (not included in version control).
- `README.md` - This documentation.

## Customization

- **UI**: The chat interface uses custom CSS for a modern look. You can further adjust the style in `app.py`.
- **APIs**: You can extend the chatbot to support more commands or integrate additional APIs.

## License

This project is for educational and demonstration purposes.

---

**Powered by [Streamlit](https://streamlit.io/), [Gemini AI](https://aistudio.google.com/), and [RAWG Games Database](https://rawg.io/).**
