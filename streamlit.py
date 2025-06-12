API_URL = "http://localhost:8000/api/v1/profile/fetch"

import json
from urllib.parse import urlparse
import requests
import streamlit as st

st.set_page_config(
    page_title="Real-time Profile Search Chat",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0f1419; }
    .main-title { text-align: center; color: #ffffff; font-size: 2.5rem; margin-bottom: 10px; }
    .subtitle { text-align: center; color: #8b949e; margin-bottom: 30px; }
    .loading-container { display: flex; align-items: center; justify-content: center; padding: 20px; color: #8b949e; font-size: 16px; }
    .spinner { border: 3px solid #30363d; border-top: 3px solid #58a6ff; border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; margin-right: 12px; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .typing-indicator { color: #8b949e; font-style: italic; }
    .stChatMessage { margin-bottom: 1rem; }
    .stChatInput > div > div > textarea { background-color: #21262d !important; border: 1px solid #30363d !important; color: #f0f6fc !important; }
    div[data-testid="column"] { background: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin: 8px 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🔍 Profile Search Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Find professionals and discover their profiles in real-time</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

def show_loading():
    return st.markdown("""
    <div class="loading-container">
        <div class="spinner"></div>
        <span>Generating...</span>
    </div>
    """, unsafe_allow_html=True)

def get_platform_info(url):
    if "linkedin.com" in url: return "LinkedIn", "💼"
    elif "github.com" in url: return "GitHub", "🐙"
    elif "stackoverflow.com" in url: return "Stack Overflow", "📚"
    elif "medium.com" in url: return "Medium", "📝"
    elif "twitter.com" in url: return "Twitter", "🐦"
    else: return "Other", "🔗"

def display_links(urls):
    if not urls:
        return
    
    st.markdown("**🔗 Relevant Profile Links:**")
    cols = st.columns(1 if len(urls) == 1 else 2 if len(urls) == 2 else 3)
    
    for i, url_data in enumerate(urls):
        url = url_data.get('url', '')
        title = url_data.get('title', 'Untitled')
        platform, emoji = get_platform_info(url)
        
        try:
            domain = urlparse(url).netloc
            domain_display = domain.replace('www.', '') if domain.startswith('www.') else domain
        except:
            domain_display = "External Link"
        
        with cols[i % len(cols)]:
            with st.container():
                st.markdown(f"**{emoji} {platform}**")
                st.markdown(f"**{title}**")
                st.markdown(f"🌐 [{domain_display}]({url})")
                st.markdown("---")

def parse_streaming_response(response_text):
    lines = response_text.strip().split('\n')
    data_chunks = []
    urls = []
    
    for line in lines:
        if not line.strip():
            continue
        try:
            json_obj = json.loads(line)
            if json_obj.get("type") == "data":
                data_content = json_obj.get("data", "")
                if data_content != "[DONE]":
                    data_chunks.append(data_content)
            elif json_obj.get("type") == "urls":
                urls = json_obj.get("data", [])
        except json.JSONDecodeError:
            continue
    
    return ''.join(data_chunks), urls

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "urls" in message and message["urls"]:
            display_links(message["urls"])

if prompt := st.chat_input("Search for people..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        loading_placeholder = show_loading()
        
        try:
            response = requests.post(
                API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps({"query": prompt}),
                stream=True
            )
            response.raise_for_status()
            
            accumulated_text = ""
            full_response = ""
            current_urls = []
            response_started = False
            
            for chunk in response.iter_lines(decode_unicode=True):
                if not chunk:
                    continue
                accumulated_text += chunk + "\n"
                
                try:
                    parsed_response, urls = parse_streaming_response(accumulated_text)
                    if parsed_response != full_response:
                        full_response = parsed_response
                        if full_response.strip():
                            response_started = True
                    if urls and not current_urls:
                        current_urls = urls
                except Exception:
                    continue
            
            loading_placeholder.empty()
            message_placeholder = st.empty()
            links_placeholder = st.empty()
            
            if response_started and full_response.strip():
                message_placeholder.markdown(full_response)
            else:
                message_placeholder.markdown("No response received from the server.")
            
            if current_urls:
                with links_placeholder.container():
                    display_links(current_urls)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response if response_started else "No response received from the server.",
                "urls": current_urls
            })
            
        except requests.exceptions.RequestException as e:
            loading_placeholder.empty()
            error_msg = f"❌ Error connecting to API: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "urls": []
            })
            
        except Exception as e:
            loading_placeholder.empty()
            error_msg = f"❌ An unexpected error occurred: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "urls": []
            })
