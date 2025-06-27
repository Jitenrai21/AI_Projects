from fastapi import FastAPI, Request, Header, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

# In-memory session store
chat_sessions = {}

# Custom app-level API key
PROGRAM_API_KEY = os.getenv("PROGRAM_API_KEY")

# Available personas
persona_options = {
    "Isaac Newton": "Mathematician and physicist",
    "Marie Curie": "Pioneering scientist in radioactivity",
    "William Shakespeare": "English playwright and poet",
    "Adam Smith": "Father of modern economics",
    "Alan Turing": "Father of computer science"
}

# FastAPI app
app = FastAPI()

# JSON request schema
class ChatRequest(BaseModel):
    session_id: str  # The session ID now comes in the request body
    persona: str
    message: str

@app.post("/chat")
async def chat(req: Request, data: ChatRequest, authorization: str = Header(None)):
    session_id = data.session_id  # Get session ID from the request body
    
    # 1. Validate API key
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
    
    token = authorization.split(" ")[1]
    if token != PROGRAM_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized API key.")
    
    # 2. Validate persona
    if data.persona not in persona_options:
        raise HTTPException(status_code=400, detail="Invalid persona.")
    
    # 3. Handle session state (chat history and persona)
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "persona": data.persona,
            "chat_history": [],
            "gemini_chat_session": model.start_chat(history=[])
        }
    
    # Update persona if changed
    if chat_sessions[session_id]["persona"] != data.persona:
        chat_sessions[session_id]["persona"] = data.persona
        chat_sessions[session_id]["chat_history"] = []  # Reset chat history
        chat_sessions[session_id]["gemini_chat_session"] = model.start_chat(history=[])

    print(f"Session ID: {session_id}")
    print(f"Chat History: {chat_sessions[session_id]['chat_history']}")
    print(f"Persona: {chat_sessions[session_id]['persona']}")
    
    # 4. Build the prompt
    with open('prompt_template.txt', 'r') as file:
        prompt_template = file.read().strip()

    # Format the prompt with persona details
    persona_instruction = prompt_template.format(
        persona_name=data.persona,
        persona_description=persona_options[data.persona]
    )
    prompt = persona_instruction + "\n\nUser: " + data.message
    
    try:
        # Maintain chat history
        response = chat_sessions[session_id]["gemini_chat_session"].send_message(prompt)
        chat_sessions[session_id]["chat_history"].append(("User", data.message))
        chat_sessions[session_id]["chat_history"].append((data.persona, response.text))
        
        return JSONResponse(content={"response": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# uvicorn main:app --reload
