# Real-time Profile Search System

An AI-powered real-time profile search application that helps users find professional profiles across various platforms using advanced language models and web search capabilities.

## Set-up Guidelines

### Prerequisites
- Python 3.8+
- API Keys (details below)

### Setup & Run (5 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/teeshaa/real-time-profile-search.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ENVIRONMENT=development
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Test the API**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/profile/fetch" \
   -H "Content-Type: application/json" \
   -d '{"query": "Find Python developers in San Francisco"}'
   ```
6. **Run Streamlit Interface (UI)**
   ```bash
   streamlit run streamlit.py
   ```
   Than you will be able to access the web interface at http://localhost:8501

## 🔑 API Keys Required

| Service | Purpose | Get API Key |
|---------|---------|-------------|
| **Groq** | LLM processing (Llama models) | [console.groq.com](https://console.groq.com) |
| **Tavily** | Real-time web search | [tavily.com](https://tavily.com) |

## Technology Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework with automatic API documentation
- **Uvicorn** - ASGI server for production-ready deployment

### AI/ML Integration
- **LiteLLM** - Unified interface for multiple LLM providers
- **Groq (Llama 3.3 70B Versatile)** - Query analysis and content moderation
- **Groq (Llama 4 Maverick 17B)** - General and profile response generation
- **Tavily API** - Real-time web search across professional platforms

### Key Features
- **Content Moderation** - AI-powered safety filtering
- **Async Processing** - Non-blocking operations for better performance
- **Clean Architecture** - Separation of concerns with Router→Controller→Usecase→Service pattern


##  Application Workflow

1. **Query Reception** → User sends profile search request
2. **Content Moderation** → AI validates query safety using Groq Llama
3. **Query Analysis** → AI determines if web search is needed
4. **Web Search** → Tavily searches across LinkedIn, GitHub, StackOverflow
5. **Response Generation** → Maverick creates comprehensive profile response

